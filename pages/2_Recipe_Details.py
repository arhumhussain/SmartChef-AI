import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from src.data.loader import load_all_data, get_recipe_details
from src.utils.styles import inject_premium_css

# Page Configuration
st.set_page_config(
    page_title="Recipe Details - SmartChef-AI",
    page_icon="🍳",
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
    st.markdown("<h1 style='margin-bottom: 0px;'>🍳 Recipe Details</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #64748b; font-size: 1.1rem;'>Inspect nutritional facts, ingredients, and step-by-step cooking timelines.</p>", unsafe_allow_html=True)

    # 1. Select Recipe
    # Check if a recipe was set from the search results (name or id)
    saved_recipe_name = st.session_state.get('selected_recipe_name')
    saved_recipe_id = st.session_state.get('selected_recipe_id')
    
    # Generate list of dropdown items mapping 'Recipe Name (Cuisine)' -> recipe_id
    recipe_options = master_df.sort_values('recipe_name')
    options_dict = {}
    default_idx = 0
    
    for idx, row in enumerate(recipe_options.itertuples()):
        label = f"{row.recipe_name} ({row.cuisine}) - {row.recipe_id}"
        options_dict[label] = row.recipe_id
        if saved_recipe_name and row.recipe_name == saved_recipe_name:
            default_idx = idx
        elif saved_recipe_id and row.recipe_id == saved_recipe_id:
            default_idx = idx

    selected_label = st.selectbox(
        "Choose a recipe to inspect:",
        options=list(options_dict.keys()),
        index=default_idx
    )
    
    selected_recipe_id = options_dict[selected_label]
    
    # 2. Get details
    details = get_recipe_details(selected_recipe_id, master_df, ing_df, nut_df, steps_df)
    
    if details:
        meta = details['metadata']
        ingredients = details['ingredients']
        nutrition = details['nutrition']
        steps = details['steps']
        
        st.write("---")
        st.subheader(f"📖 {meta['recipe_name']}")
        
        # Details Columns
        col_left, col_right = st.columns([1, 1])
        
        with col_left:
            st.markdown(f"""
            <div class="glass-card">
                <h4>General Information</h4>
                <p style="font-size: 0.95rem; color: #2D3436; line-height: 1.6;">
                    <b>Cuisine:</b> {meta['cuisine']} <br>
                    <b>Category:</b> {meta['category']} <br>
                    <b>Cooking Method:</b> {meta['cooking_method']} <br>
                    <b>Difficulty:</b> {meta['difficulty']} <br>
                    <b>Servings:</b> {meta['servings']} servings <br>
                    <b>Estimated Cost:</b> ${meta['estimated_cost_usd']:.2f} USD <br>
                    <b>Rating:</b> ★ {meta['rating']:.1f} ({meta['review_count']:,} reviews)
                </p>
                <div style="margin-top: 1rem;">
                    <span class="badge badge-diet">{'Halal' if meta['is_halal'] else 'Non-Halal'}</span>
                    <span class="badge badge-cuisine">{'Vegetarian' if meta['is_vegetarian'] else 'Non-Vegetarian'}</span>
                    <span class="badge badge-difficulty">{'Vegan' if meta['is_vegan'] else 'Non-Vegan'}</span>
                    <span class="badge badge-score">{'Gluten-Free' if meta['is_gluten_free'] else 'Has Gluten'}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Ingredients List
            st.write("### 🛒 Ingredients Checklist")
            st.write("Check off the ingredients you have ready:")
            
            # Render check boxes for ingredients
            for ing in ingredients:
                st.checkbox(ing.title(), value=True, key=f"check_ing_{selected_recipe_id}_{ing}")
                
        with col_right:
            # Nutrition Graph Section
            st.write("### 📊 Nutritional Breakdown (Per Serving)")
            
            # Donut chart
            labels = ['Protein (g)', 'Fat (g)', 'Carbohydrates (g)']
            values = [nutrition.get('protein_g', 0), nutrition.get('fat_g', 0), nutrition.get('carbohydrates_g', 0)]
            
            fig = go.Figure(data=[go.Pie(
                labels=labels, 
                values=values, 
                hole=.4,
                marker=dict(colors=['#6366f1', '#ec4899', '#eab308']),
                textinfo='label+percent'
            )])
            
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#2D3436', family='Outfit'),
                showlegend=False,
                margin=dict(t=10, b=10, l=10, r=10),
                height=250
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Nutrition Stats row
            st.markdown(f"""
            <div style="display: flex; justify-content: space-between; text-align: center; margin-bottom: 1.5rem;">
                <div style="flex: 1;">
                    <span style="font-size: 1.5rem; font-weight: 800; color: #ff7e5f;">{nutrition.get('calories', 0)}</span><br>
                    <span style="font-size: 0.8rem; color: #636E72;">Calories</span>
                </div>
                <div style="flex: 1;">
                    <span style="font-size: 1.5rem; font-weight: 800; color: #6366f1;">{nutrition.get('protein_g', 0)}g</span><br>
                    <span style="font-size: 0.8rem; color: #636E72;">Protein</span>
                </div>
                <div style="flex: 1;">
                    <span style="font-size: 1.5rem; font-weight: 800; color: #ec4899;">{nutrition.get('fat_g', 0)}g</span><br>
                    <span style="font-size: 0.8rem; color: #636E72;">Fat</span>
                </div>
                <div style="flex: 1;">
                    <span style="font-size: 1.5rem; font-weight: 800; color: #eab308;">{nutrition.get('carbohydrates_g', 0)}g</span><br>
                    <span style="font-size: 0.8rem; color: #636E72;">Carbs</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Cooking steps checklist
            st.write("### 👩‍🍳 Cooking Instructions")
            
            if not steps:
                st.info("No cooking instructions available for this recipe.")
            else:
                completed_steps = 0
                total_steps = len(steps)
                
                # Render steps
                for step in steps:
                    checked = st.checkbox(
                        f"Step {step['step_number']} ({step['estimated_time_minutes']}m): {step['step_description']}",
                        key=f"step_check_{selected_recipe_id}_{step['step_number']}"
                    )
                    if checked:
                        completed_steps += 1
                        
                # Progress bar
                progress_pct = int((completed_steps / total_steps) * 100) if total_steps > 0 else 0
                st.write(f"**Preparation Progress: {progress_pct}%**")
                st.progress(progress_pct / 100.0)
                
                if progress_pct == 100:
                    st.balloons()
                    st.success("🎉 You've completed all the steps! Enjoy your meal!")

else:
    st.warning("Please verify your data folder structure is complete.")
