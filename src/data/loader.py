import pandas as pd
import numpy as np
import os

try:
    import streamlit as st
    cache_decorator = st.cache_data
except ImportError:
    # Dummy decorator fallback when running outside of Streamlit (e.g. in pytest)
    def cache_decorator(func):
        return func

@cache_decorator
def load_all_data():
    """
    Loads all project datasets, aligns them by recipe_id, and caches them in memory.
    
    Returns:
        tuple: (master_df, ing_df, nut_df, steps_df)
    """
    # Base path
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    master_path = os.path.join(base_dir, 'datasets', 'recipes_master.csv')
    ing_path = os.path.join(base_dir, 'datasets', 'Recipe_ingrediect.csv')
    nut_path = os.path.join(base_dir, 'datasets', 'Recipe_nutrition.csv')
    steps_path = os.path.join(base_dir, 'datasets', 'Recipe_steps.csv')

    # Load datasets
    master_df = pd.read_csv(master_path)
    ing_df = pd.read_csv(ing_path)
    nut_df = pd.read_csv(nut_path)
    steps_df = pd.read_csv(steps_path)

    # 1. Align ingredients and nutrition to recipe_id
    # Since the rows are aligned exactly with master_df
    ing_df.insert(0, 'recipe_id', master_df['recipe_id'])
    nut_df.insert(0, 'recipe_id', master_df['recipe_id'])

    # 2. Sequentially assign recipe_id to Recipe_steps.csv
    # We find indices of step_number == 1
    step_one_indices = steps_df.index[steps_df['step_number'] == 1].tolist()
    
    recipe_id_array = np.empty(len(steps_df), dtype=object)
    for i, start_idx in enumerate(step_one_indices):
        end_idx = step_one_indices[i+1] if i + 1 < len(step_one_indices) else len(steps_df)
        recipe_id_array[start_idx:end_idx] = master_df.loc[i, 'recipe_id']
        
    steps_df.insert(0, 'recipe_id', recipe_id_array)

    return master_df, ing_df, nut_df, steps_df


def get_recipe_details(recipe_id, master_df, ing_df, nut_df, steps_df):
    """
    Gets detailed information for a specific recipe_id.
    
    Args:
        recipe_id (str): The unique ID of the recipe.
        master_df (pd.DataFrame): Master recipes dataframe.
        ing_df (pd.DataFrame): Ingredients dataframe.
        nut_df (pd.DataFrame): Nutrition dataframe.
        steps_df (pd.DataFrame): Steps dataframe.
        
    Returns:
        dict: A dictionary containing recipe metadata, ingredients, nutrition, and steps.
    """
    master_row = master_df[master_df['recipe_id'] == recipe_id]
    if master_row.empty:
        return None
        
    master_info = master_row.iloc[0].to_dict()
    
    # Get active ingredients (where binary flag is 1)
    ing_row = ing_df[ing_df['recipe_id'] == recipe_id]
    ingredients = []
    if not ing_row.empty:
        # Columns after recipe_id and recipe_name
        for col in ing_df.columns[2:]:
            if ing_row.iloc[0][col] == 1:
                ingredients.append(col)
                
    # Get nutrition details
    nut_row = nut_df[nut_df['recipe_id'] == recipe_id]
    nutrition = {}
    if not nut_row.empty:
        # Columns after recipe_id and recipe_name
        for col in nut_df.columns[2:]:
            nutrition[col] = nut_row.iloc[0][col]
            
    # Get steps
    recipe_steps = steps_df[steps_df['recipe_id'] == recipe_id].sort_values('step_number')
    steps = recipe_steps[['step_number', 'step_description', 'estimated_time_minutes']].to_dict('records')
    
    return {
        'metadata': master_info,
        'ingredients': ingredients,
        'nutrition': nutrition,
        'steps': steps
    }
