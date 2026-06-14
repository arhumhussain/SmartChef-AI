import pandas as pd

def get_dietary_allowed_recipe_ids(nut_df, goal):
    """
    Filters recipe names based on a selected dietary goal using percentile-based thresholds.
    
    Args:
        nut_df (pd.DataFrame): The nutrition dataframe with columns: 
                               ['recipe_name', 'calories', 'protein_g', 'carbohydrates_g', 'fat_g']
        goal (str): Selected dietary goal. One of: 
                    'Weight Loss', 'Muscle Gain', 'High Protein', 'Low Fat', 'Low Carb', 'Normal'
                    
    Returns:
        set: A set of recipe_names that satisfy the dietary constraints.
    """
    if not goal or goal == 'Normal':
        return set(nut_df['recipe_name'].tolist())
        
    # Calculate dynamic thresholds using percentiles
    if goal == 'Weight Loss':
        cal_threshold = nut_df['calories'].quantile(0.30)
        fat_threshold = nut_df['fat_g'].quantile(0.35)
        filtered_df = nut_df[(nut_df['calories'] <= cal_threshold) & (nut_df['fat_g'] <= fat_threshold)]
        
    elif goal in ['Muscle Gain', 'High Protein']:
        protein_threshold = nut_df['protein_g'].quantile(0.70)
        filtered_df = nut_df[nut_df['protein_g'] >= protein_threshold]
        
    elif goal == 'Low Fat':
        fat_threshold = nut_df['fat_g'].quantile(0.25)
        filtered_df = nut_df[nut_df['fat_g'] <= fat_threshold]
        
    elif goal == 'Low Carb':
        carb_threshold = nut_df['carbohydrates_g'].quantile(0.25)
        filtered_df = nut_df[nut_df['carbohydrates_g'] <= carb_threshold]
        
    else:
        # Fallback if unknown goal
        return set(nut_df['recipe_name'].tolist())
        
    return set(filtered_df['recipe_name'].tolist())
