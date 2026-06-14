import streamlit as st
import pandas as pd
from src.data.loader import load_all_data
from src.recommender.Knn_recommendation import recommend_recipes
from src.utils.styles import inject_premium_css

# Page Configuration
st.set_page_config(
    page_title="Recipe Finder - SmartChef-AI",
    page_icon="🔍",
    layout="wide"
)

# Inject styling
inject_premium_css()

# Load Data with caching
@st.cache_data
def load_data():
    """Cache data loading for better performance"""
    try:
        master_df, ing_df, nut_df, steps_df = load_all_data()
        return master_df, ing_df, nut_df, steps_df
    except Exception as e:
        st.error(f"Error loading datasets: {str(e)}")
        return None, None, None, None

# Initialize session state for results
if 'search_results' not in st.session_state:
    st.session_state.search_results = None
if 'last_search_ingredients' not in st.session_state:
    st.session_state.last_search_ingredients = ""

master_df, ing_df, nut_df, steps_df = load_data()
data_loaded = master_df is not None

if data_loaded:
    # Title
    st.markdown("<h1 style='margin-bottom: 0px; color: #2D3436;'>🔍 Recipe Finder</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #636E72; font-size: 1.1rem;'>Find recipes based on what ingredients you have in your kitchen.</p>", unsafe_allow_html=True)

    # Debug info in expander
    with st.expander("🔧 Database Information", expanded=False):
        st.write(f"✅ **Total Recipes:** {len(master_df)}")
        st.write(f"✅ **Cuisines Available:** {', '.join(sorted(master_df['cuisine'].unique()))}")
        st.write(f"✅ **Ingredient Types:** {len([col for col in ing_df.columns if col != 'recipe_name'])}")
        st.write(f"**Sample Ingredients:** {', '.join(sorted([col for col in ing_df.columns if col != 'recipe_name'])[:15])}...")

    # Main search area layout
    col_input, col_diet = st.columns([2, 1])
    
    # Get valid ingredient options from database columns
    valid_ings = sorted([col for col in ing_df.columns if col != 'recipe_name'])
    
    with col_input:
        st.markdown("<label style='color: #2D3436; font-weight: 500;'>Select Available Ingredients</label>", unsafe_allow_html=True)
        
        # Multi-select list
        selected_dropdown_ings = st.multiselect(
            "Choose from list of supported ingredients:",
            options=valid_ings,
            help="Select one or multiple ingredients from the database.",
            label_visibility="collapsed",
            key="ingredient_multiselect"
        )
        
        st.markdown("<label style='color: #2D3436; font-weight: 500; margin-top: 1rem;'>Or type custom/comma-separated ingredients:</label>", unsafe_allow_html=True)
        text_ings = st.text_input(
            "Type ingredients separated by commas",
            placeholder="e.g. chicken, onion, tomato, cumin, garlic",
            help="Type any ingredient here. We will match it with our database.",
            label_visibility="collapsed",
            key="ingredient_text_input"
        )

    with col_diet:
        st.markdown("<label style='color: #2D3436; font-weight: 500;'>Dietary & Nutrition Goal</label>", unsafe_allow_html=True)
        dietary_goal = st.selectbox(
            "Select Diet Type:",
            options=["Normal", "Weight Loss", "Muscle Gain", "Low Fat", "Low Carb"],
            help="Applies statistical percentile filters on nutrition values.",
            label_visibility="collapsed",
            key="dietary_goal_select"
        )
        
    # Advanced Filters Expander
    with st.expander("⚙️ Advanced Recipe Filters", expanded=False):
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            cuisines = ["All"] + sorted(master_df['cuisine'].dropna().unique().tolist())
            sel_cuisine = st.selectbox("Cuisine Type", cuisines, key="cuisine_select")
            
            difficulties = ["All"] + sorted(master_df['difficulty'].dropna().unique().tolist())
            sel_diff = st.selectbox("Cooking Difficulty", difficulties, key="difficulty_select")
            
            sel_rating = st.slider("Minimum Rating (Stars)", min_value=0.0, max_value=5.0, value=0.0, step=0.1, key="rating_slider")
            
        with col_f2:
            max_time_val = int(master_df['total_time_minutes'].max())
            sel_time = st.slider("Maximum Cook Time (mins)", 
                                min_value=10, 
                                max_value=max(max_time_val, 300), 
                                value=max(max_time_val, 300), 
                                key="time_slider")
            
            max_cost_val = float(master_df['estimated_cost_usd'].max())
            sel_cost = st.slider("Maximum Estimated Cost (USD)", 
                               min_value=1.0, 
                               max_value=max(max_cost_val, 20.0), 
                               value=max(max_cost_val, 20.0), 
                               step=0.5, 
                               key="cost_slider")

    # Assemble ingredient search list
    all_raw_ingredients = ""
    if selected_dropdown_ings:
        all_raw_ingredients = ",".join(selected_dropdown_ings)
    if text_ings:
        if all_raw_ingredients:
            all_raw_ingredients += "," + text_ings
        else:
            all_raw_ingredients = text_ings

    # Show selected ingredients
    if all_raw_ingredients:
        ingredient_list = [ing.strip() for ing in all_raw_ingredients.split(',') if ing.strip()]
        st.info(f"🔍 **Selected Ingredients ({len(ingredient_list)}):** {', '.join(ingredient_list)}")
    else:
        st.warning("👆 Please select or type at least one ingredient to begin your search!")
    
    # Search button
    st.write("---")
    col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
    with col_btn2:
        search_clicked = st.button("🚀 Find Recipes", use_container_width=True, key="find_recipes_button")
    
    if search_clicked:
        if not all_raw_ingredients:
            st.error("⚠️ Please select or type at least one ingredient to search for recipes.")
        else:
            with st.spinner("🔍 Searching and ranking matching recipes..."):
                # Call recommender pipeline
                ingredient_list = [
                    ing.strip().lower()
                    for ing in all_raw_ingredients.split(",")
                    if ing.strip()
                ]

                rec_results = recommend_recipes(
                    user_ingredients=ingredient_list,
                    master_df=master_df,
                    ing_df=ing_df,
                    nut_df=nut_df,
                    cuisine=sel_cuisine,
                    difficulty=sel_diff,
                    max_total_time=sel_time,
                    max_cost=sel_cost,
                    min_rating=sel_rating,
                    dietary_goal=dietary_goal,
                    top_n=10
                )
                
                # Store results in session state
                st.session_state.search_results = rec_results
                st.session_state.last_search_ingredients = all_raw_ingredients
                
                if rec_results.empty:
                    st.warning("⚠️ No recipes found matching your criteria. Try different ingredients or relax the filters.")
                else:
                    st.success(f"✨ Found {len(rec_results)} matching recipes!")
                    st.balloons()
    
    # Display results if they exist in session state
    if st.session_state.search_results is not None and not st.session_state.search_results.empty:
        rec_results = st.session_state.search_results
        
        st.markdown(f"### 🎯 Search Results")
        st.markdown(f"*Showing {len(rec_results)} recipes matching your ingredients*")
        st.write("---")
        
        # Render results
        for idx, (_, row) in enumerate(rec_results.iterrows()):
            recipe_name = row['recipe_name']
            recipe_id = row.get('recipe_id', f'RCP{idx:05d}')
            
            # Match stats
            pct = int(row.get('match_score', 0) * 100)
            cnt = int(row.get('match_count', 0))
            tot = int(row.get('total_ingredients', 0))
            
            # Calories
            if 'calories' in row and pd.notna(row['calories']) and row['calories'] > 0:
                calories_display = f"{int(row['calories'])} kcal"
            else:
                calories_display = f"{int(row.get('calories_per_serving', 0))} kcal/serving"
            
            # Create columns for card and button
            col_card, col_btn = st.columns([5, 1])
            
            with col_card:
                st.markdown(f"""
                <div class="glass-card" style="margin-bottom: 0.8rem; padding: 1.2rem;">
                    <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                        <h3 style="margin: 0; font-size: 1.35rem; font-weight: 700; color: #2D3436;">{recipe_name}</h3>
                        <div>
                            <span class="badge badge-score">🔥 {pct}% Match ({cnt}/{tot} items)</span>
                        </div>
                    </div>
                    <div style="margin-top: 0.6rem;">
                        <span class="badge badge-cuisine">🍽️ {row['cuisine']}</span>
                        <span class="badge badge-difficulty">📊 {row['difficulty']}</span>
                        <span class="badge badge-diet">💰 ${row['estimated_cost_usd']:.2f}</span>
                    </div>
                    <p style="font-size: 0.9rem; color: #636E72; margin: 0.6rem 0 0 0;">
                        ⏱️ {row['total_time_minutes']} mins | ⭐ {row['rating']:.1f} ({row['review_count']:,} reviews) | 🔥 {calories_display}
                    </p>
                </div>
                """, unsafe_allow_html=True)
                
            with col_btn:
                st.write("")
                if st.button("👁️ Details", key=f"btn_{idx}_{recipe_name.replace(' ', '_')}"):
                    st.session_state['selected_recipe_name'] = recipe_name
                    st.success(f"✅ Selected **{recipe_name}**! View details in the recipe page.")

else:
    st.error("❌ Data Loading Failed. Please check that all CSV files are in the 'datasets' folder.")