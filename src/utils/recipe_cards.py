"""
Beautiful Recipe Cards Component
Renders recipe cards with gradient backgrounds, glassmorphism, animations, and favorites.
"""
import streamlit as st
import pandas as pd
import random
from datetime import datetime


def get_cuisine_emoji(cuisine):
    """Returns an emoji based on cuisine type"""
    cuisine_emojis = {
        'Italian': '🍝', 'Mexican': '🌮', 'Chinese': '🥡', 'Indian': '🍛',
        'Japanese': '🍣', 'Thai': '🍜', 'French': '🥖', 'Greek': '🥗',
        'Spanish': '🥘', 'American': '🍔', 'British': '🍽️', 'Korean': '🍲',
        'Vietnamese': '🍜', 'Moroccan': '🍲', 'Turkish': '🍢', 'Lebanese': '🥙',
        'Mediterranean': '🫒', 'Caribbean': '🥥', 'Brazilian': '🥩', 'German': '🥨',
        'Asian': '🍜', 'European': '🍽️', 'Middle Eastern': '🥙', 'African': '🍲'
    }
    return cuisine_emojis.get(cuisine, '🍳')

def get_difficulty_emoji(difficulty):
    """Returns emoji and color for difficulty"""
    difficulty_map = {
        'Easy': ('🟢', '#22c55e'),
        'Medium': ('🟡', '#eab308'),
        'Hard': ('🔴', '#ef4444'),
    }
    return difficulty_map.get(difficulty, ('⚪', '#6366f1'))


def generate_gradient_colors(seed_string):
    """Generate consistent gradient colors based on input string"""
    random.seed(hash(seed_string) % (10 ** 8))
    colors = [
        ('#667eea', '#764ba2'),  # Purple to pink
        ('#f093fb', '#f5576c'),  # Pink to red
        ('#4facfe', '#00f2fe'),  # Blue to cyan
        ('#43e97b', '#38f9d7'),  # Green to mint
        ('#fa709a', '#fee140'),  # Pink to yellow
        ('#30cfd0', '#330867'),  # Cyan to dark purple
        ('#a8edea', '#fed6e3'),  # Mint to light pink
        ('#ff9a56', '#ff6a88'),  # Orange to pink
        ('#2e2e78', '#662d8c'),  # Dark blue to purple
        ('#667eea', '#764ba2'),  # Purple again
    ]
    return random.choice(colors)


def init_favorites_session():
    """Initialize favorites list in session state"""
    if 'favorites' not in st.session_state:
        st.session_state.favorites = set()


def render_recipe_card(recipe_data):
    """Render a single beautiful recipe card"""
    init_favorites_session()
    
    recipe_id = recipe_data.get('recipe_id', '')
    recipe_name = recipe_data.get('recipe_name', 'Untitled')
    cuisine = recipe_data.get('cuisine', 'Mixed')
    difficulty = recipe_data.get('difficulty', 'Medium')
    rating = recipe_data.get('rating', 0)
    time_mins = recipe_data.get('total_time_minutes', 0)
    cost_usd = recipe_data.get('estimated_cost_usd', 0)
    match_score = recipe_data.get('match_score', 0) if 'match_score' in recipe_data else None
    
    color1, color2 = generate_gradient_colors(recipe_name)
    difficulty_emoji, difficulty_color = get_difficulty_emoji(difficulty)
    cuisine_emoji = get_cuisine_emoji(cuisine)
    is_favorited = recipe_id in st.session_state.favorites
    
    card_html = f"""
    <div class="recipe-card-modern" data-recipe-id="{recipe_id}">
        <div class="card-gradient" style="background: linear-gradient(135deg, {color1} 0%, {color2} 100%);"></div>
        <div class="card-content-wrapper">
            <div class="recipe-name-badge">{recipe_name[:30]}</div>
            <div class="recipe-meta-grid">
                <div class="meta-cell"><span class="meta-icon">⭐</span><span class="meta-val">{rating:.1f}</span></div>
                <div class="meta-cell"><span class="meta-icon">⏱️</span><span class="meta-val">{time_mins}m</span></div>
                <div class="meta-cell"><span class="meta-icon">💰</span><span class="meta-val">${cost_usd:.0f}</span></div>
            </div>
            <div class="badges-group">
                <span class="cuisine-badge">{cuisine_emoji} {cuisine}</span>
                <span class="difficulty-badge" style="color:{difficulty_color};">{difficulty_emoji} {difficulty}</span>
            </div>
            {f'<div class="match-badge">{int(match_score*100)}% Match</div>' if match_score else ''}
        </div>
    </div>
    """
    
    return card_html


def render_recipe_grid(recipes_df, columns=3):
    """Render recipes in responsive grid"""
    if recipes_df.empty:
        st.info("😢 No recipes found. Try adjusting your filters!")
        return
    
    st.markdown("<div class='recipe-grid-container'>", unsafe_allow_html=True)
    cols = st.columns(columns)
    
    for idx, (_, recipe) in enumerate(recipes_df.iterrows()):
        col_idx = idx % columns
        with cols[col_idx]:
            card_html = render_recipe_card(recipe.to_dict())
            st.markdown(card_html, unsafe_allow_html=True)
            
            recipe_id = recipe['recipe_id']
            if st.button(f"View →", key=f"view_{recipe_id}", use_container_width=True):
                st.session_state['selected_recipe'] = recipe_id
                st.rerun()
    
    st.markdown("</div>", unsafe_allow_html=True)


def render_favorites_sidebar():
    """Render favorites in sidebar"""
    init_favorites_session()
    
    with st.sidebar:
        st.markdown("<h3>❤️ Favorites</h3>", unsafe_allow_html=True)
        
        if st.session_state.favorites:
            st.markdown(f"**{len(st.session_state.favorites)} saved**")
            
            for fav_id in list(st.session_state.favorites)[:5]:
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.caption(fav_id)
                with col2:
                    if st.button("✕", key=f"rm_{fav_id}"):
                        st.session_state.favorites.discard(fav_id)
                        st.rerun()
        else:
            st.caption("No favorites yet")