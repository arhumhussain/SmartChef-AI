import streamlit as st
import os
import pandas as pd
from src.data.loader import load_all_data
from src.utils.styles import inject_premium_css

# Set up page configurations
st.set_page_config(
    page_title="SmartChef-AI - Smart Recipe Discovery",
    page_icon="🍳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject premium theme styling
inject_premium_css()

# Load all data on startup (cached)
try:
    master_df, ing_df, nut_df, steps_df = load_all_data()
    data_loaded = True
except Exception as e:
    st.error(f"Error loading datasets: {e}")
    data_loaded = False

# Main Dashboard Layout
st.markdown("<h1 class='hero-title'>Welcome to SmartChef-AI 🍳</h1>", unsafe_allow_html=True)
st.markdown("<p class='hero-subtitle'>Discover recipes you can cook right now, customize menus to meet your nutritional goals, and consult your personal AI Chef.</p>", unsafe_allow_html=True)

# Advanced Configurations Expander
with st.expander("🛠️ Advanced Settings & API Configurations", expanded=False):
    st.subheader("API Configuration")
    api_key_input = st.text_input(
        "Gemini API Key (Optional)",
        type="password",
        help="Enter your Gemini API key to activate the live AI Chef chatbot. If left empty, a simulated response system will be used.",
        value=st.session_state.get("gemini_api_key", os.getenv("GEMINI_API_KEY", ""))
    )
    st.session_state["gemini_api_key"] = api_key_input
    
    st.write("---")
    st.subheader("System Cache")
    if st.button("🔄 Clear App Cache", key="clear_cache_main"):
        st.cache_data.clear()
        st.cache_resource.clear()
        st.success("Cache cleared successfully!")
        st.rerun()

if data_loaded:
    # Stats row
    num_recipes = len(master_df)
    num_cuisines = master_df['cuisine'].nunique()
    num_ingredients = len(ing_df.columns) - 2 # excluding recipe_id and recipe_name
    
    st.markdown(f"""
    <div class="stat-container">
        <div class="stat-box">
            <div class="stat-val">{num_recipes:,}</div>
            <div class="stat-lbl">Total Recipes</div>
        </div>
        <div class="stat-box">
            <div class="stat-val">{num_cuisines}</div>
            <div class="stat-lbl">Unique Cuisines</div>
        </div>
        <div class="stat-box">
            <div class="stat-val">{num_ingredients}</div>
            <div class="stat-lbl">Supported Ingredients</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Hero features
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="glass-card">
            <h3>🔍 Discover by Ingredients</h3>
            <p>Don't let ingredients go to waste. Input what you have in your pantry (like Chicken, Onion, Garlic) and our rule-based matching system will find recipes, score their matching level, and suggest them.</p>
            <p style="font-weight: 500; color: #a5b4fc;">Try out "Recipe Finder" in the sidebar menu!</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="glass-card">
            <h3>📅 Customized Meal Planner</h3>
            <p>Generate diet-specific daily or weekly menus matching your caloric limits and protein needs. Get aggregate macro summaries and check off items for your weekly shopping list.</p>
            <p style="font-weight: 500; color: #a5b4fc;">Try out "Meal Planner" in the sidebar menu!</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="glass-card">
            <h3>🥗 Target-Nutrition Filters</h3>
            <p>Filter suggestions by weight loss, muscle gain, low-carb, or low-fat goals. The engine calculates dynamic percentile cutoffs to filter out matching recipe candidates.</p>
            <p style="font-weight: 500; color: #a5b4fc;">Supports customizable diet targets!</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="glass-card">
            <h3>💬 Conversational AI Chef</h3>
            <p>Chat directly with your private AI Chef bot for quick ingredient replacements, explaining kitchen terminology, or brainstorming what to prepare.</p>
            <p style="font-weight: 500; color: #a5b4fc;">Try out "AI Chef" in the sidebar menu!</p>
        </div>
        """, unsafe_allow_html=True)

    # Top-Rated Featured Recipes Section
    st.write("### ⭐ Featured Top-Rated Recipes")
    
    # Get top 3 recipes by rating
    top_recipes = master_df.sort_values(by=['rating', 'review_count'], ascending=[False, False]).head(3)
    
    feat_cols = st.columns(3)
    for i, (_, row) in enumerate(top_recipes.iterrows()):
        with feat_cols[i]:
            st.markdown(f"""
            <div class="glass-card" style="height: 100%;">
                <h4 style="margin-top: 0;">{row['recipe_name']}</h4>
                <div>
                    <span class="badge badge-cuisine">{row['cuisine']}</span>
                    <span class="badge badge-difficulty">{row['difficulty']}</span>
                    <span class="badge badge-score">★ {row['rating']:.1f}</span>
                </div>
                <p style="font-size: 0.9rem; color: #94a3b8; margin: 1rem 0;">
                    <b>Total Time:</b> {row['total_time_minutes']} minutes <br>
                    <b>Prep/Cook:</b> {row['prep_time_minutes']}m / {row['cook_time_minutes']}m <br>
                    <b>Serving Cost:</b> ${row['estimated_cost_usd']:.2f} USD
                </p>
            </div>
            """, unsafe_allow_html=True)

else:
    st.warning("Please verify your data folder structure is complete.")

st.markdown("""
<div class="chef-footer">
    SmartChef-AI App • Built with Streamlit, Pandas, and Gemini API • 2026
</div>
""", unsafe_allow_html=True)
