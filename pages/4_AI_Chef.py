import streamlit as st
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

    # Fetch Gemini API key from main app page selection (session state)
    api_key = st.session_state.get("gemini_api_key", "")
    
    # Mode badge
    if api_key:
        st.markdown("<span class=\"badge badge-score\">LIVE MODE (Gemini API Active)</span>", unsafe_allow_html=True)
    else:
        st.markdown("<span class=\"badge badge-difficulty\">SIMULATION MODE (No API Key)</span>", unsafe_allow_html=True)
        st.caption("To activate live AI responses, enter your Gemini API key in the 'Advanced Settings' expander on the main dashboard home page.")

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
                api_key=api_key,
                master_df=master_df,
                ing_df=ing_df,
                nut_df=nut_df,
                steps_df=steps_df
            )
            
            # Display assistant message
            with st.chat_message("assistant"):
                st.markdown(response_text)
            st.session_state["chat_history"].append({"role": "assistant", "content": response_text})
            
            # Trigger page rerun to refresh button keys/inputs
            st.rerun()
else:
    st.warning("Please verify your data folder structure is complete.")
