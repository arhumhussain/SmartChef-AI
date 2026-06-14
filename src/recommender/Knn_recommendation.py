import joblib
import pandas as pd
import numpy as np

# Load artifacts once
# Use exact file name casing from models directory
knn_model = joblib.load("models/Recipe_knn_model.pkl")
ingredient_columns = joblib.load("models/ingredient_columns.pkl")
recipe_names = joblib.load("models/recipe_names.pkl")


def recommend_recipes(user_ingredients, master_df, ing_df, nut_df, 
                      cuisine="All", difficulty="All", max_total_time=None, 
                      max_cost=None, min_rating=0.0, dietary_goal="Normal", top_n=10):
    """
    Recommend recipes using KNN based on user ingredients, and apply metadata filters.
    """
    # 1. Filter master_df first by sidebar options to get the candidate pool
    filtered_df = master_df.copy()
    
    if cuisine and cuisine != "All":
        filtered_df = filtered_df[filtered_df['cuisine'] == cuisine]
        
    if difficulty and difficulty != "All":
        filtered_df = filtered_df[filtered_df['difficulty'] == difficulty]
        
    if max_total_time:
        filtered_df = filtered_df[filtered_df['total_time_minutes'] <= max_total_time]
        
    if max_cost:
        filtered_df = filtered_df[filtered_df['estimated_cost_usd'] <= max_cost]
        
    if min_rating and min_rating > 0:
        filtered_df = filtered_df[filtered_df['rating'] >= min_rating]

    # Drop duplicate recipe names to prevent cartesian product explosion during merges
    filtered_df = filtered_df.drop_duplicates(subset=['recipe_name'])

    # If candidate pool is empty, return early
    if filtered_df.empty:
        return pd.DataFrame()

    # 2. Build user ingredient vector
    user_vector = np.zeros(len(ingredient_columns))
    for ingredient in user_ingredients:
        ingredient = ingredient.strip().lower()
        if ingredient in ingredient_columns:
            idx = ingredient_columns.index(ingredient)
            user_vector[idx] = 1

    # 3. Query all neighbors from the KNN model
    # Pass user vector as a DataFrame with feature names matching the fitted model to avoid UserWarning
    user_df = pd.DataFrame([user_vector], columns=ingredient_columns)
    distances, indices = knn_model.kneighbors(
        user_df,
        n_neighbors=len(recipe_names)
    )

    # 4. Construct recommendations DataFrame sorted by similarity
    recommendations = []
    for idx, dist in zip(indices[0], distances[0]):
        recommendations.append({
            "recipe_name": recipe_names[idx],
            "match_score": round((1 - dist), 4)
        })
    rec_df = pd.DataFrame(recommendations)
    
    # Drop duplicates in rec_df to ensure a 1-to-1 merge on recipe_name
    rec_df = rec_df.drop_duplicates(subset=['recipe_name'])

    # 5. Merge to keep only the filtered candidates and retrieve their metadata
    rec_df = pd.merge(rec_df, filtered_df, on="recipe_name", how="inner")
    if rec_df.empty:
        return pd.DataFrame()

    # 6. Merge nutrition data
    if nut_df is not None and not nut_df.empty:
        try:
            nutrition_cols = ['recipe_name', 'calories', 'protein_g', 'fat_g', 'carbohydrates_g']
            available_cols = [col for col in nutrition_cols if col in nut_df.columns]
            nut_df_unique = nut_df[available_cols].drop_duplicates(subset=['recipe_name'])
            rec_df = pd.merge(rec_df, nut_df_unique, on='recipe_name', how='left')
            for col in ['calories', 'protein_g', 'fat_g', 'carbohydrates_g']:
                if col in rec_df.columns:
                    rec_df[col] = rec_df[col].fillna(0)
        except Exception as e:
            print(f"Warning: Could not merge nutrition data in KNN recommender: {e}")

    # 7. Apply dietary goal filters
    if dietary_goal and dietary_goal != "Normal":
        rec_df = apply_dietary_filter(rec_df, dietary_goal)
        if rec_df.empty:
            return pd.DataFrame()

    # 8. Compute match count and total ingredients for UI display
    match_counts = []
    total_ingredients_list = []
    user_ing_set = {ing.strip().lower() for ing in user_ingredients if ing.strip()}

    for _, row in rec_df.iterrows():
        r_name = row['recipe_name']
        recipe_rows = ing_df[ing_df['recipe_name'] == r_name]
        if recipe_rows.empty:
            match_counts.append(0)
            total_ingredients_list.append(0)
            continue
            
        recipe_row = recipe_rows.iloc[0]
        # Active ingredients in recipe (excluding identifier columns)
        recipe_ingredients = [col for col in ing_df.columns if col not in ['recipe_id', 'recipe_name'] and recipe_row[col] > 0]
        tot = len(recipe_ingredients)
        total_ingredients_list.append(tot)

        # Count ingredient matches (substring matching to match recommend.py logic)
        cnt = 0
        for user_ing in user_ing_set:
            for recipe_ing in recipe_ingredients:
                recipe_ing_lower = recipe_ing.lower()
                if user_ing == recipe_ing_lower or user_ing in recipe_ing_lower or recipe_ing_lower in user_ing:
                    cnt += 1
                    break
        match_counts.append(cnt)

    rec_df['match_count'] = match_counts
    rec_df['total_ingredients'] = total_ingredients_list

    # 9. Sort by match_score descending, and return top_n
    rec_df = rec_df.sort_values('match_score', ascending=False)
    return rec_df.head(top_n)


def apply_dietary_filter(df, dietary_goal):
    """Apply dietary goal filters based on nutritional percentiles."""
    if dietary_goal == "Weight Loss":
        if 'calories' in df.columns:
            threshold = df['calories'].quantile(0.5)
            df = df[df['calories'] <= threshold]
        if 'fat_g' in df.columns and len(df) > 0:
            threshold = df['fat_g'].quantile(0.5)
            df = df[df['fat_g'] <= threshold]
    elif dietary_goal == "Muscle Gain":
        if 'protein_g' in df.columns:
            threshold = df['protein_g'].quantile(0.4)
            df = df[df['protein_g'] >= threshold]
    elif dietary_goal == "Low Fat":
        if 'fat_g' in df.columns:
            threshold = df['fat_g'].quantile(0.3)
            df = df[df['fat_g'] <= threshold]
    elif dietary_goal == "Low Carb":
        if 'carbohydrates_g' in df.columns:
            threshold = df['carbohydrates_g'].quantile(0.3)
            df = df[df['carbohydrates_g'] <= threshold]
    return df
