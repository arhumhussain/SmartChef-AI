import streamlit as st
import os
from src.data.loader import load_all_data
from src.chatbot.chef_bot import generate_chef_response
from src.utils.styles import inject_premium_css

# Page Configuration
st.set_page_config(
    page_title="AI Chef - SmartChef-AI",
    page_icon="💬",
    layout="wide"
)

# Inject CSS
inject_premium_css()

# Load Data
try:
    master_df, ing_df, nut_df, steps_df = load_all_data()
    data_loaded = True
except Exception as e:
    st.error(f"Error loading datasets: {e}")
    data_loaded = False

if data_loaded:
    st.markdown("<h1 style='margin-bottom: 0px;'>💬 AI Chef</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #64748b; font-size: 1.1rem;'>Consult your personal AI Chef for recipe adaptations, ingredient substitutions, and culinary advice.</p>", unsafe_allow_html=True)

    # Fetch API keys from session state or environment variables
    groq_key = st.session_state.get("groq_api_key", os.getenv("GROQ_API_KEY", ""))
    gemini_key = st.session_state.get("gemini_api_key", os.getenv("GEMINI_API_KEY", ""))
    
    active_key = groq_key if groq_key else gemini_key
    active_provider = "Groq" if groq_key else ("Gemini" if gemini_key else None)
    
    # Mode badge
    if active_provider == "Groq":
        st.markdown("<span class=\"badge badge-score\">LIVE MODE (Groq API Active)</span>", unsafe_allow_html=True)
    elif active_provider == "Gemini":
        st.markdown("<span class=\"badge badge-score\">LIVE MODE (Gemini API Active)</span>", unsafe_allow_html=True)
    else:
        st.markdown("<span class=\"badge badge-difficulty\">SIMULATION MODE (No API Key)</span>", unsafe_allow_html=True)
        st.caption("To activate live AI responses, enter your Groq or Gemini API key in the .env file or home page settings.")

    # Initialize chat history
    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = [
            {"role": "assistant", "content": "Greetings! I am Chef SmartChef. How can I help you in the kitchen today?"}
        ]

    # Quick Suggestion Chips
    st.write("")
    st.write("**Quick culinary questions to try:**")
    chip_cols = st.columns(3)
    
    suggestions = [
        "How can I substitute eggs?",
        "What are some knife cutting techniques?",
        "Recommend a low-carb recipe from the database."
    ]
    
    selected_suggestion = None
    for index, suggestion in enumerate(suggestions):
        col_tgt = chip_cols[index % 3]
        with col_tgt:
            if st.button(suggestion, key=f"chip_{index}"):
                selected_suggestion = suggestion

    st.write("---")

    # Display Chat History
    for msg in st.session_state["chat_history"]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Chat Input or Suggestion Trigger
    user_query = st.chat_input("Ask Chef SmartChef...")
    
    if selected_suggestion:
        user_query = selected_suggestion

    if user_query:
        # Display user message
        with st.chat_message("user"):
            st.markdown(user_query)
        st.session_state["chat_history"].append({"role": "user", "content": user_query})
        
        # Generate Chef Response
        with st.spinner("Chef is brainstorming..."):
            response_text, is_simulated = generate_chef_response(
                user_query=user_query,
                api_key=active_key,
                master_df=master_df,
                ing_df=ing_df,
                nut_df=nut_df,
                steps_df=steps_df,
                provider=active_provider
            )
            
            # Display assistant message
            with st.chat_message("assistant"):
                st.markdown(response_text)
            st.session_state["chat_history"].append({"role": "assistant", "content": response_text})
            
            # Trigger page rerun to refresh button keys/inputs
            st.rerun()
else:
    st.warning("Please verify your data folder structure is complete.")
