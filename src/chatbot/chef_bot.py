import os
import requests
from dotenv import load_dotenv
from src.chatbot.prompts import CHEF_SYSTEM_PROMPT, format_rag_prompt
from src.chatbot.rag import retrieve_recipes_for_query

# Load environment variables
load_dotenv()

def get_gemini_api_key():
    """
    Attempts to retrieve the Gemini API key from environment variables or streamlit secrets.
    """
    key = os.getenv("GEMINI_API_KEY")
    if not key:
        try:
            import streamlit as st
            key = st.secrets.get("GEMINI_API_KEY")
        except:
            pass
    return key


def generate_chef_response(user_query, api_key, master_df, ing_df, nut_df, steps_df, provider=None):
    """
    Generates a culinary response using Gemini or Groq API with RAG context, 
    or falls back to a simulated chef response if no key is provided.
    
    Args:
        user_query (str): The user's message/question.
        api_key (str): The API key (can be None or empty).
        master_df, ing_df, nut_df, steps_df: DataFrames for RAG retrieval.
        provider (str): The provider name ("Groq" or "Gemini"). Autodetected if None.
        
    Returns:
        tuple: (response_text, is_simulated)
    """
    # 1. Retrieve RAG context
    context_recipes = retrieve_recipes_for_query(user_query, master_df, ing_df, nut_df, steps_df, top_k=2)
    
    # 2. Format the prompt with context
    prompt = format_rag_prompt(user_query, context_recipes)
    
    # 3. Determine provider and key
    active_key = api_key
    active_provider = provider
    
    # Simple check to load streamlit if needed inside helper
    def get_st_secret(name):
        try:
            import streamlit as st
            return st.secrets.get(name)
        except:
            return None

    if not active_provider:
        groq_env_key = os.getenv("GROQ_API_KEY") or get_st_secret("GROQ_API_KEY")
        if (api_key and api_key.startswith("gsk_")) or (not api_key and groq_env_key):
            active_provider = "Groq"
            if not active_key:
                active_key = groq_env_key
        else:
            active_provider = "Gemini"
            if not active_key:
                active_key = os.getenv("GEMINI_API_KEY") or get_st_secret("GEMINI_API_KEY") or get_gemini_api_key()
    else:
        if not active_key:
            if active_provider == "Groq":
                active_key = os.getenv("GROQ_API_KEY") or get_st_secret("GROQ_API_KEY")
            else:
                active_key = os.getenv("GEMINI_API_KEY") or get_st_secret("GEMINI_API_KEY") or get_gemini_api_key()

    if not active_key:
        # Fallback to Simulated Mode
        return generate_simulated_chef_response(user_query, context_recipes), True

    if active_provider == "Groq":
        try:
            # Construct direct REST API endpoint for Groq Chat Completions
            url = "https://api.groq.com/openai/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {active_key}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": "llama-3.3-70b-versatile",
                "messages": [
                    {
                        "role": "system",
                        "content": CHEF_SYSTEM_PROMPT
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "temperature": 0.7
            }
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            response.raise_for_status()
            response_json = response.json()
            response_text = response_json['choices'][0]['message']['content']
            return response_text, False
        except requests.exceptions.HTTPError as e:
            # Extract detailed error message from response body
            error_details = ""
            if e.response is not None:
                try:
                    error_json = e.response.json()
                    error_details = error_json.get("error", {}).get("message", e.response.text)
                except:
                    error_details = e.response.text
            error_msg = f"*(Groq API Error: {error_details if error_details else str(e)})*\n\n"
            sim_response = generate_simulated_chef_response(user_query, context_recipes)
            return error_msg + sim_response, True
        except Exception as e:
            # Handle other errors gracefully by falling back to simulation
            error_msg = f"*(Groq API Connection Error: {str(e)})*\n\n"
            sim_response = generate_simulated_chef_response(user_query, context_recipes)
            return error_msg + sim_response, True
    else:
        # Gemini logic
        try:
            # Construct direct REST API endpoint for Gemini 1.5 Flash
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={active_key}"
            headers = {"Content-Type": "application/json"}
            
            # Build payload matching the Gemini API schema
            payload = {
                "contents": [
                    {
                        "role": "user",
                        "parts": [{"text": prompt}]
                    }
                ],
                "systemInstruction": {
                    "parts": [{"text": CHEF_SYSTEM_PROMPT}]
                }
            }
            
            # Make standard HTTP POST request (pure Python, bypasses gRPC)
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            response.raise_for_status()
            response_json = response.json()
            
            # Parse output
            try:
                response_text = response_json['candidates'][0]['content']['parts'][0]['text']
                return response_text, False
            except (KeyError, IndexError):
                raise Exception("Failed to parse response structure from Gemini API.")
            
        except Exception as e:
            # Handle errors gracefully by falling back to simulation
            error_msg = f"*(Gemini API Connection Error: {str(e)})*\n\n"
            sim_response = generate_simulated_chef_response(user_query, context_recipes)
            return error_msg + sim_response, True



def generate_simulated_chef_response(query, context_recipes):
    """
    Generates a high-quality simulated chef response based on query and retrieved recipes.
    """
    q_lower = query.lower()
    
    # Simple rule matching for common questions
    if "substitute" in q_lower or "replace" in q_lower:
        sub_suggestions = (
            "🍳 **Chef's Egg Substitution Guide:**\n"
            "- In baking: Use 1/4 cup unsweetened applesauce or mashed banana per egg.\n"
            "- In savory dishes: Use 1 tablespoon ground flaxseed mixed with 3 tablespoons water (let gel for 5 minutes).\n\n"
            "🥛 **Chef's Dairy Substitution Guide:**\n"
            "- Milk: Use almond milk, soy milk, or coconut milk.\n"
            "- Butter: Use coconut oil, olive oil, or vegan margarine."
        )
        return f"Greetings! As a chef, I get asked about substitutions all the time! Here is my professional recommendation:\n\n{sub_suggestions}"
        
    if "cut" in q_lower or "technique" in q_lower or "chop" in q_lower:
        return (
            "🔪 **Chef's Cutting Technique Guide:**\n"
            "1. **Julienne (Matchstick):** Cut food into thin strips, about 1/8 inch thick and 2 inches long.\n"
            "2. **Dice (Cubed):** Cut ingredients into uniform cubes. Small dice is 1/4 inch, medium is 1/2 inch.\n"
            "3. **Chiffonade:** Roll up leafy herbs (like basil or spinach) and slice thinly across the roll to create ribbons.\n\n"
            "Remember to always keep your fingers tucked in (use the 'claw' grip) and ensure your chef's knife is sharp for safety!"
        )

    # Context-based response
    if context_recipes:
        recipe = context_recipes[0]
        name = recipe['metadata']['recipe_name']
        cuisine = recipe['metadata']['cuisine']
        ingredients = recipe['ingredients']
        steps = recipe['steps']
        
        step_descriptions = "\n".join([f"{s['step_number']}. {s['step_description']}" for s in steps[:3]])
        
        response = (
            f"Hello! I see you are asking about recipe details or looking for suggestions. "
            f"Based on your database, I highly recommend checking out **{name}**, a delicious **{cuisine}** dish! \n\n"
            f"🥗 **Key Ingredients:** {', '.join(ingredients[:6])}...\n\n"
            f"👩‍🍳 **Initial Cooking Steps:**\n{step_descriptions}\n"
            f"*(Note: You can view full instructions on the **Recipe Details** page.)*\n\n"
            f"Is there a specific ingredient in this recipe you'd like to substitute, or would you like to know what pairings go well with it? Let me know!"
        )
        return response
        
    return (
        "Hello! I am your AI Chef Assistant. I can help you discover recipes, recommend ingredient substitutions, "
        "or explain cooking techniques.\n\n"
        "To get started, try asking me something like:\n"
        "- *'How can I substitute eggs in a recipe?'*\n"
        "- *'Show me details or explain how to cook Biryani.'*\n"
        "- *'What are some basic chopping techniques?'*"
    )
