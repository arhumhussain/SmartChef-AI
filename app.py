import streamlit as st
import os
import pandas as pd
from src.data.loader import load_all_data, get_recipe_details
from src.utils.styles import inject_premium_css

# Set up page configurations - MUST BE FIRST
st.set_page_config(
    page_title="SmartChef-AI - Smart Recipe Discovery",
    page_icon="🍳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Force light theme and inject base styles BEFORE anything else
st.markdown("""
    <style>
        .stApp {
            background-color: #F8F9FA !important;
        }
        .main > div {
            background-color: #F8F9FA !important;
        }
        p, div, span, li, label, .stMarkdown {
            color: #2D3436 !important;
        }
        section[data-testid="stSidebar"] {
            background-color: #FFFFFF !important;
        }
    </style>
""", unsafe_allow_html=True)

# Inject premium theme styling
inject_premium_css()

# Load all data on startup (cached)
@st.cache_data
def load_data():
    try:
        return load_all_data()
    except Exception as e:
        st.error(f"Error loading datasets: {e}")
        return None, None, None, None

master_df, ing_df, nut_df, steps_df = load_data()
data_loaded = master_df is not None

# Main Dashboard Layout
st.markdown("<h1 class='hero-title'>Welcome to SmartChef-AI 🍳</h1>", unsafe_allow_html=True)
st.markdown("<p class='hero-subtitle'>Discover recipes you can cook right now, customize menus to meet your nutritional goals, and consult your personal AI Chef.</p>", unsafe_allow_html=True)

if data_loaded:
    # Stats row
    num_recipes = len(master_df)
    num_cuisines = master_df['cuisine'].nunique()
    num_ingredients = len(ing_df.columns) - 1
    
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
            <p>Don't let ingredients go to waste. Input what you have in your pantry and our matching system will find recipes, score their matching level, and suggest them.</p>
            <p style="font-weight: 500; color: #FF6B35;">Try out "Recipe Finder" in the sidebar menu!</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="glass-card">
            <h3>📅 Customized Meal Planner</h3>
            <p>Generate diet-specific daily or weekly menus matching your caloric limits and protein needs.</p>
            <p style="font-weight: 500; color: #FF6B35;">Try out "Meal Planner" in the sidebar menu!</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="glass-card">
            <h3>🥗 Target-Nutrition Filters</h3>
            <p>Filter suggestions by weight loss, muscle gain, low-carb, or low-fat goals.</p>
            <p style="font-weight: 500; color: #2EC4B6;">Supports customizable diet targets!</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="glass-card">
            <h3>💬 Conversational AI Chef</h3>
            <p>Chat directly with your private AI Chef bot for quick ingredient replacements and cooking tips.</p>
            <p style="font-weight: 500; color: #2EC4B6;">Try out "AI Chef" in the sidebar menu!</p>
        </div>
        """, unsafe_allow_html=True)

    # Top-Rated Featured Recipes Section
    st.markdown("<h3>⭐ Featured Top-Rated Recipes</h3>", unsafe_allow_html=True)
    
    top_recipes = master_df.sort_values(by=['rating', 'review_count'], ascending=[False, False]).head(3)
    
    feat_cols = st.columns(3)
    for i, (_, row) in enumerate(top_recipes.iterrows()):
        with feat_cols[i]:
            st.markdown(f"""
            <div class="glass-card" style="height: 100%;">
                <h4 style="margin-top: 0; color: #2D3436;">{row['recipe_name']}</h4>
                <div>
                    <span class="badge badge-cuisine">{row['cuisine']}</span>
                    <span class="badge badge-difficulty">{row['difficulty']}</span>
                    <span class="badge badge-score">★ {row['rating']:.1f}</span>
                </div>
                <p style="font-size: 0.9rem; color: #636E72; margin: 1rem 0;">
                    <b>Total Time:</b> {row['total_time_minutes']} minutes <br>
                    <b>Prep/Cook:</b> {row['prep_time_minutes']}m / {row['cook_time_minutes']}m <br>
                    <b>Serving Cost:</b> ${row['estimated_cost_usd']:.2f} USD
                </p>
            </div>
            """, unsafe_allow_html=True)

else:
    st.warning("Please verify your dataset folder structure is complete.")

st.markdown("""
<div class="chef-footer">
    SmartChef-AI App • Built with Streamlit, Pandas, and Gemini API • 2026
</div>
""", unsafe_allow_html=True)