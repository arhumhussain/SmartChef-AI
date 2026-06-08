import streamlit as st
import pandas as pd
from src.data.loader import load_all_data
from src.recommender.recommend import get_recommendations
from src.utils.styles import inject_premium_css

# Page Configuration
st.set_page_config(
    page_title="Recipe Finder - SmartChef-AI",
    page_icon="🔍",
    layout="wide"
)

# Inject styling
inject_premium_css()

# Load Data
try:
    master_df, ing_df, nut_df, steps_df = load_all_data()
    data_loaded = True
except Exception as e:
    st.error(f"Error loading datasets: {e}")
    data_loaded = False

if data_loaded:
    st.markdown("<h1 style='margin-bottom: 0px;'>🔍 Recipe Finder</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #64748b; font-size: 1.1rem;'>Find recipes based on what ingredients you have in your kitchen.</p>", unsafe_allow_html=True)

    # Main search area layout
    col_input, col_diet = st.columns([2, 1])
    
    # Valid ingredient options from database columns
    valid_ings = list(ing_df.columns[2:]) # 58 columns
    
    with col_input:
        st.write("##### Select Available Ingredients")
        # Multi-select list
        selected_dropdown_ings = st.multiselect(
            "Choose from list of supported ingredients:",
            options=valid_ings,
            help="Select one or multiple ingredients from the database."
        )
        
        # Free-text search fallback
        text_ings = st.text_input(
            "Or type custom/comma-separated ingredients:",
            placeholder="e.g. Chicken, onion, tomato",
            help="You can type any ingredient here. We will attempt to normalize and match it with the database."
        )

    with col_diet:
        st.write("##### Dietary & Nutrition Goal")
        dietary_goal = st.selectbox(
            "Select Diet Type:",
            options=["Normal", "Weight Loss", "Muscle Gain", "Low Fat", "Low Carb"],
            help="Applies statistical percentile filters on carbohydrates, protein, calories, and fats."
        )
        
    # Advanced Filters Expander on the main page
    with st.expander("⚙️ Advanced Recipe Filters", expanded=False):
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            cuisines = ["All"] + sorted(master_df['cuisine'].unique().tolist())
            sel_cuisine = st.selectbox("Cuisine Type", cuisines)
            
            difficulties = ["All", "Easy", "Medium", "Hard"]
            sel_diff = st.selectbox("Cooking Difficulty", difficulties)
            
            sel_rating = st.slider("Minimum Rating (Stars)", min_value=0.0, max_value=5.0, value=0.0, step=0.1)
            
        with col_f2:
            max_time_val = int(master_df['total_time_minutes'].max())
            sel_time = st.slider("Maximum Cook Time (mins)", min_value=10, max_value=max_time_val, value=max_time_val)
            
            max_cost_val = float(master_df['estimated_cost_usd'].max())
            sel_cost = st.slider("Maximum Estimated Cost (USD)", min_value=1.0, max_value=max_cost_val, value=max_cost_val, step=0.5)

    # Assemble ingredient search list
    all_raw_ingredients = ""
    if selected_dropdown_ings:
        all_raw_ingredients = ",".join(selected_dropdown_ings)
    if text_ings:
        if all_raw_ingredients:
            all_raw_ingredients += "," + text_ings
        else:
            all_raw_ingredients = text_ings

    # Trigger search
    st.write("---")
    
    if st.button("🚀 Find Recipes"):
        with st.spinner("Searching and ranking matching recipes..."):
            # Call recommender pipeline
            rec_results = get_recommendations(
                user_ingredients_raw=all_raw_ingredients,
                dietary_goal=dietary_goal,
                master_df=master_df,
                ing_df=ing_df,
                nut_df=nut_df,
                cuisine=sel_cuisine,
                difficulty=sel_diff,
                max_total_time=sel_time,
                max_cost=sel_cost,
                min_rating=sel_rating,
                top_n=20
            )
            
            if rec_results.empty:
                st.warning("⚠️ No recipes found matching your selected criteria. Try easing the time, cost, or ingredient filter settings.")
            else:
                st.write(f"### Found {len(rec_results)} Matching Recipes")
                
                # Render results in beautiful lists
                for idx, row in rec_results.iterrows():
                    recipe_id = row['recipe_id']
                    
                    # Match stats
                    pct = int(row['match_score'] * 100)
                    cnt = int(row['match_count'])
                    tot = int(row['total_ingredients'])
                    
                    col_card, col_btn = st.columns([5, 1])
                    
                    with col_card:
                        # Card details
                        st.markdown(f"""
                        <div class="glass-card" style="margin-bottom: 0.8rem; padding: 1.2rem;">
                            <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                                <h3 style="margin: 0; font-size: 1.35rem; font-weight: 700;">{row['recipe_name']}</h3>
                                <div>
                                    <span class="badge badge-score">{pct}% Match ({cnt}/{tot} items)</span>
                                </div>
                            </div>
                            <div style="margin-top: 0.6rem;">
                                <span class="badge badge-cuisine">{row['cuisine']}</span>
                                <span class="badge badge-difficulty">{row['difficulty']}</span>
                                <span class="badge badge-diet">Estimated Cost: ${row['estimated_cost_usd']:.2f} USD</span>
                            </div>
                            <p style="font-size: 0.9rem; color: #94a3b8; margin: 0.6rem 0 0 0;">
                                ⏱️ {row['total_time_minutes']} mins total | ⭐ {row['rating']:.1f} stars ({row['review_count']:,} reviews) | 🔥 {row['calories']} kcal
                            </p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                    with col_btn:
                        # Button to select recipe
                        st.write("") # spacing
                        st.write("")
                        if st.button("👁️ View Details", key=f"btn_{recipe_id}"):
                            st.session_state['selected_recipe_id'] = recipe_id
                            st.success(f"Selected **{row['recipe_name']}**! Go to '2 Recipe Details' page in the sidebar.")
else:
    st.warning("Please verify your data folder structure is complete.")
