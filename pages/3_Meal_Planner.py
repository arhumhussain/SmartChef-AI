import streamlit as st
import pandas as pd
import numpy as np
from src.data.loader import load_all_data, get_recipe_details
from src.recommender.diet_filter import get_dietary_allowed_recipe_ids
from src.utils.styles import inject_premium_css

# Page Configuration
st.set_page_config(
    page_title="Meal Planner - SmartChef-AI",
    page_icon="📅",
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


def generate_plan(days, target_calories, diet_type, selected_cuisines, master_df, nut_df):
    """
    Generates a daily or weekly meal plan (Breakfast, Lunch, Dinner) matching diet type, 
    cuisines, and calorie constraints.
    """
    # 1. Filter candidates by diet type
    allowed_ids = get_dietary_allowed_recipe_ids(nut_df, diet_type)
    candidates = master_df[master_df['recipe_id'].isin(allowed_ids)].copy()
    
    # 2. Filter candidates by cuisine if specified
    if selected_cuisines and "All" not in selected_cuisines:
        candidates = candidates[candidates['cuisine'].isin(selected_cuisines)]
        
    # Merge nutrition for calculation
    candidates = pd.merge(candidates, nut_df[['recipe_id', 'calories', 'protein_g', 'fat_g', 'carbohydrates_g']], on='recipe_id', how='left')
    
    plan = {}
    
    # Target breakdowns
    # Breakfast = ~25% of calories
    # Lunch = ~40% of calories
    # Dinner = ~35% of calories
    b_target = target_calories * 0.25
    l_target = target_calories * 0.40
    d_target = target_calories * 0.35
    
    for day in range(1, days + 1):
        day_plan = {}
        
        # 1. Breakfast
        b_candidates = candidates[candidates['meal_type'] == 'Breakfast']
        if not b_candidates.empty:
            # Sort by absolute distance to calorie target and select randomly from top 10
            b_candidates['dist'] = (b_candidates['calories'] - b_target).abs()
            best_b = b_candidates.sort_values('dist').head(10).sample(1).iloc[0]
            day_plan['Breakfast'] = best_b.to_dict()
        else:
            # Fallback
            day_plan['Breakfast'] = candidates.sample(1).iloc[0].to_dict()
            
        # 2. Lunch
        l_candidates = candidates[candidates['meal_type'] == 'Lunch']
        if not l_candidates.empty:
            l_candidates['dist'] = (l_candidates['calories'] - l_target).abs()
            best_l = l_candidates.sort_values('dist').head(10).sample(1).iloc[0]
            day_plan['Lunch'] = best_l.to_dict()
        else:
            day_plan['Lunch'] = candidates.sample(1).iloc[0].to_dict()
            
        # 3. Dinner
        d_candidates = candidates[candidates['meal_type'] == 'Dinner']
        if not d_candidates.empty:
            d_candidates['dist'] = (d_candidates['calories'] - d_target).abs()
            best_d = d_candidates.sort_values('dist').head(10).sample(1).iloc[0]
            day_plan['Dinner'] = best_d.to_dict()
        else:
            day_plan['Dinner'] = candidates.sample(1).iloc[0].to_dict()
            
        plan[f"Day {day}"] = day_plan
        
    return plan


if data_loaded:
    st.markdown("<h1 style='margin-bottom: 0px;'>📅 Meal Planner</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #64748b; font-size: 1.1rem;'>Generate custom menu plans matching your caloric targets and nutrition splits.</p>", unsafe_allow_html=True)

    # Inputs layout
    col_set1, col_set2 = st.columns(2)
    
    with col_set1:
        plan_duration = st.selectbox("Plan Duration", ["1 Day (Daily)", "7 Days (Weekly)"])
        target_cals = st.slider("Daily Target Calories (kcal)", min_value=1200, max_value=4000, value=2000, step=100)
        
    with col_set2:
        plan_diet = st.selectbox(
            "Target Diet Goal:",
            ["Normal", "Weight Loss", "Muscle Gain", "Low Fat", "Low Carb"],
            key="planner_diet"
        )
        
        all_cuisines = ["All"] + sorted(master_df['cuisine'].unique().tolist())
        plan_cuisines = st.multiselect("Preferred Cuisines", all_cuisines, default=["All"])

    st.write("---")
    
    # Session State holding meal plan
    if st.button("🍳 Generate Meal Plan"):
        duration_days = 1 if "1 Day" in plan_duration else 7
        
        with st.spinner("Compiling delicious schedules..."):
            meal_plan = generate_plan(duration_days, target_cals, plan_diet, plan_cuisines, master_df, nut_df)
            st.session_state['current_meal_plan'] = meal_plan
            st.session_state['current_meal_plan_days'] = duration_days
            
    # Display current meal plan if it exists
    if 'current_meal_plan' in st.session_state:
        plan = st.session_state['current_meal_plan']
        days_count = st.session_state['current_meal_plan_days']
        
        # Tabs for days if weekly, else just show single day
        if days_count > 1:
            tabs = st.tabs([f"Day {d}" for d in range(1, 8)])
        else:
            tabs = [st.container()]
            
        shopping_ingredients = set()
        
        for d_idx in range(days_count):
            day_name = f"Day {d_idx + 1}"
            day_meals = plan[day_name]
            
            # Aggregate stats for the day
            day_calories = sum([m['calories'] for m in day_meals.values()])
            day_protein = sum([m['protein_g'] for m in day_meals.values()])
            day_fat = sum([m['fat_g'] for m in day_meals.values()])
            day_carbs = sum([m['carbohydrates_g'] for m in day_meals.values()])
            
            with tabs[d_idx]:
                st.write(f"### 📋 Menu for {day_name}")
                
                # Daily total stats
                st.markdown(f"""
                <div style="display: flex; gap: 1rem; margin-bottom: 1.5rem; text-align: center;">
                    <div style="flex: 1; background: rgba(255, 255, 255, 0.03); border-radius: 8px; padding: 0.8rem;">
                        <span style="font-size: 1.3rem; font-weight: 800; color: #ff7e5f;">{day_calories:.0f}</span><br>
                        <span style="font-size: 0.75rem; color: #94a3b8;">Total kcal</span>
                    </div>
                    <div style="flex: 1; background: rgba(255, 255, 255, 0.03); border-radius: 8px; padding: 0.8rem;">
                        <span style="font-size: 1.3rem; font-weight: 800; color: #6366f1;">{day_protein:.1f}g</span><br>
                        <span style="font-size: 0.75rem; color: #94a3b8;">Total Protein</span>
                    </div>
                    <div style="flex: 1; background: rgba(255, 255, 255, 0.03); border-radius: 8px; padding: 0.8rem;">
                        <span style="font-size: 1.3rem; font-weight: 800; color: #ec4899;">{day_fat:.1f}g</span><br>
                        <span style="font-size: 0.75rem; color: #94a3b8;">Total Fat</span>
                    </div>
                    <div style="flex: 1; background: rgba(255, 255, 255, 0.03); border-radius: 8px; padding: 0.8rem;">
                        <span style="font-size: 1.3rem; font-weight: 800; color: #eab308;">{day_carbs:.1f}g</span><br>
                        <span style="font-size: 0.75rem; color: #94a3b8;">Total Carbs</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Meals display
                for slot in ['Breakfast', 'Lunch', 'Dinner']:
                    meal = day_meals[slot]
                    recipe_id = meal['recipe_id']
                    
                    # Fetch ingredients to accumulate for shopping list
                    details = get_recipe_details(recipe_id, master_df, ing_df, nut_df, steps_df)
                    if details:
                        shopping_ingredients.update(details['ingredients'])
                        
                    col_meal, col_go = st.columns([5, 1])
                    
                    with col_meal:
                        st.markdown(f"""
                        <div class="glass-card" style="padding: 1.2rem; margin-bottom: 0.8rem;">
                            <h4 style="margin: 0; font-size: 1.15rem; color: #a5b4fc;">{slot} - {meal['recipe_name']}</h4>
                            <p style="font-size: 0.85rem; color: #94a3b8; margin: 0.4rem 0 0 0;">
                                Cuisine: {meal['cuisine']} | Difficulty: {meal['difficulty']} | Time: {meal['total_time_minutes']} mins | Cost: ${meal['estimated_cost_usd']:.2f} USD | Calories: {meal['calories']:.0f} kcal
                            </p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                    with col_go:
                        st.write("")
                        st.write("")
                        if st.button("Details", key=f"details_{day_name}_{slot}_{recipe_id}"):
                            st.session_state['selected_recipe_id'] = recipe_id
                            st.success(f"Selected **{meal['recipe_name']}**! Navigate to '2 Recipe Details' tab.")

        # Unified Shopping List section
        st.write("---")
        st.write("### 🛒 Unified Shopping List")
        st.write("Here is the list of ingredients required to prepare the generated meal plan:")
        
        # Sort and render check list
        shopping_cols = st.columns(3)
        sorted_shop = sorted(list(shopping_ingredients))
        
        for index, item in enumerate(sorted_shop):
            col_target = shopping_cols[index % 3]
            with col_target:
                st.checkbox(item.title(), key=f"shop_list_{item}")
                
else:
    st.warning("Please verify your data folder structure is complete.")
