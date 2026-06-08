import pandas as pd
import numpy as np

def get_ingredient_match_df(ing_df, user_ingredients):
    """
    Computes ingredient matching scores for all recipes using vectorized pandas operations.
    
    Args:
        ing_df (pd.DataFrame): Ingredients dataframe (first col recipe_id, second col recipe_name, rest are binary).
        user_ingredients (list): List of ingredient strings entered by the user.
        
    Returns:
        pd.DataFrame: Dataframe with columns: ['recipe_id', 'match_score', 'match_count', 'total_ingredients']
    """
    # Exclude recipe_id and recipe_name columns to get pure ingredient flags
    ingredient_cols = list(ing_df.columns[2:])
    
    # Calculate total count of ingredients in each recipe
    total_ingredients = ing_df[ingredient_cols].sum(axis=1)
    
    # Handle case where user didn't enter any ingredients
    if not user_ingredients:
        result_df = pd.DataFrame({
            'recipe_id': ing_df['recipe_id'],
            'match_score': 0.0,
            'match_count': 0,
            'total_ingredients': total_ingredients
        })
        return result_df
        
    # Get only user ingredients that exist as columns in ing_df
    valid_user_ings = [ing for ing in user_ingredients if ing in ing_df.columns]
    
    if not valid_user_ings:
        # User entered ingredients, but none matched valid database ingredients
        result_df = pd.DataFrame({
            'recipe_id': ing_df['recipe_id'],
            'match_score': 0.0,
            'match_count': 0,
            'total_ingredients': total_ingredients
        })
        return result_df
        
    # Sum up matches across columns corresponding to valid user ingredients
    match_count = ing_df[valid_user_ings].sum(axis=1)
    
    # Score = match_count / total_ingredients
    # Avoid division by zero in case a recipe has 0 ingredients (shouldn't happen, but safe code is better)
    match_score = match_count / np.where(total_ingredients > 0, total_ingredients, 1)
    
    result_df = pd.DataFrame({
        'recipe_id': ing_df['recipe_id'],
        'match_score': match_score,
        'match_count': match_count,
        'total_ingredients': total_ingredients
    })
    
    return result_df
