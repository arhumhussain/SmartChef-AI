import os
import google.generativeai as genai
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


def generate_chef_response(user_query, api_key, master_df, ing_df, nut_df, steps_df):
    """
    Generates a culinary response using Gemini API with RAG context, 
    or falls back to a simulated chef response if no key is provided.
    
    Args:
        user_query (str): The user's message/question.
        api_key (str): The Gemini API key (can be None or empty).
        master_df, ing_df, nut_df, steps_df: DataFrames for RAG retrieval.
        
    Returns:
        tuple: (response_text, is_simulated)
    """
    # 1. Retrieve RAG context
    context_recipes = retrieve_recipes_for_query(user_query, master_df, ing_df, nut_df, steps_df, top_k=2)
    
    # 2. Format the prompt with context
    prompt = format_rag_prompt(user_query, context_recipes)
    
    # 3. Check for API key
    if not api_key:
        api_key = get_gemini_api_key()
        
    if not api_key:
        # Fallback to Simulated Mode
        return generate_simulated_chef_response(user_query, context_recipes), True
        
    try:
        # Configure Gemini
        genai.configure(api_key=api_key)
        
        # Initialize Gemini 1.5 Flash (or 2.5 Flash if available, let's use 1.5 Flash as standard safe choice)
        model = genai.GenerativeModel(
            model_name='gemini-1.5-flash',
            system_instruction=CHEF_SYSTEM_PROMPT
        )
        
        response = model.generate_content(prompt)
        return response.text, False
        
    except Exception as e:
        # Handle errors gracefully by falling back to simulation
        error_msg = f"*(API Connection Error: {str(e)})*\n\n"
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
