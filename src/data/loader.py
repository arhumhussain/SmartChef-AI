import pandas as pd
import os

def find_csv_files(data_path="datasets"):
    """
    Find CSV files in the datasets folder and return a dictionary
    mapping file types to actual filenames.
    """
    if not os.path.exists(data_path):
        # Try alternate folder names
        for alt_folder in ['Datasets', 'dataset', 'Dataset', 'data']:
            if os.path.exists(alt_folder):
                data_path = alt_folder
                break
        else:
            raise FileNotFoundError(f"❌ No 'datasets' or similar folder found in {os.getcwd()}")
    
    all_files = os.listdir(data_path)
    csv_files = [f for f in all_files if f.endswith('.csv')]
    
    print(f"📁 Found {len(csv_files)} CSV files in '{data_path}':")
    for f in csv_files:
        print(f"   - {f}")
    
    # Map files based on keywords in filename
    file_map = {}
    for csv_file in csv_files:
        lower_name = csv_file.lower()
        
        # Master file: contains 'master' or is 'recipes_master'
        if 'master' in lower_name:
            file_map['master'] = csv_file
        
        # Ingredient file: contains 'ingredient' or 'ingrediect' (typo)
        elif 'ingredient' in lower_name or 'ingrediect' in lower_name:
            file_map['ingredient'] = csv_file
        
        # Nutrition file: contains 'nutrition'
        elif 'nutrition' in lower_name:
            file_map['nutrition'] = csv_file
        
        # Steps file: contains 'steps' or 'step'
        elif 'steps' in lower_name or 'step' in lower_name:
            file_map['steps'] = csv_file
    
    return file_map, data_path


def load_all_data():
    """
    Load all required datasets for the SmartChef-AI application.
    Automatically detects file names in the 'datasets' folder (handles typos).
    """
    data_path = "datasets"
    
    try:
        # Find actual file names
        file_map, data_path = find_csv_files(data_path)
        
        # Check if we found all required files
        required = ['master', 'ingredient', 'nutrition', 'steps']
        missing = [r for r in required if r not in file_map]
        
        if missing:
            # Show helpful error message
            files_found = os.listdir(data_path) if os.path.exists(data_path) else []
            raise FileNotFoundError(f"""
❌ Could not find all required CSV files.

Missing file types: {missing}
Found file types: {list(file_map.keys())}

Files in '{data_path}' folder:
{chr(10).join(f'  - {f}' for f in files_found)}

Expected files containing these keywords:
  - 'master' → for recipes master data
  - 'ingredient' or 'ingrediect' → for ingredient matrix
  - 'nutrition' → for nutrition data
  - 'steps' or 'step' → for cooking steps
            """)
        
        # Load each file
        print(f"\n📂 Loading data from '{data_path}/'...")
        
        # Load master recipe data
        master_path = os.path.join(data_path, file_map['master'])
        print(f"   ✅ Loading master: {file_map['master']}")
        master_df = pd.read_csv(master_path)
        
        # Load ingredient matrix
        ing_path = os.path.join(data_path, file_map['ingredient'])
        print(f"   ✅ Loading ingredients: {file_map['ingredient']}")
        ing_df = pd.read_csv(ing_path)
        
        # Load nutrition data
        nut_path = os.path.join(data_path, file_map['nutrition'])
        print(f"   ✅ Loading nutrition: {file_map['nutrition']}")
        nut_df = pd.read_csv(nut_path)
        
        # Load recipe steps
        steps_path = os.path.join(data_path, file_map['steps'])
        print(f"   ✅ Loading steps: {file_map['steps']}")
        steps_df = pd.read_csv(steps_path)
        
        # Basic data cleaning for master_df
        numeric_cols_master = {
            'estimated_cost_usd': 0,
            'total_time_minutes': 0,
            'prep_time_minutes': 0,
            'cook_time_minutes': 0,
            'rating': 0,
            'review_count': 0,
            'servings': 1,
            'calories_per_serving': 0
        }
        for col, default in numeric_cols_master.items():
            if col in master_df.columns:
                master_df[col] = pd.to_numeric(master_df[col], errors='coerce').fillna(default)
        
        # Basic data cleaning for nutrition data
        numeric_cols_nutrition = ['calories', 'protein_g', 'carbohydrates_g', 'fat_g', 
                                  'fiber_g', 'sugar_g', 'sodium_mg']
        for col in numeric_cols_nutrition:
            if col in nut_df.columns:
                nut_df[col] = pd.to_numeric(nut_df[col], errors='coerce').fillna(0)
        
        print(f"\n✅ Data loaded successfully!")
        print(f"   📊 {len(master_df)} recipes")
        print(f"   🥘 {len(ing_df.columns) - 1} ingredient types")
        print(f"   📈 {len(nut_df)} nutrition records")
        print(f"   📝 {len(steps_df)} cooking steps")
        print(f"   🍽️  Sample recipes: {', '.join(master_df['recipe_name'].head(3).tolist())}")
        
        return master_df, ing_df, nut_df, steps_df
        
    except Exception as e:
        print(f"\n❌ Error loading data: {e}")
        raise


def get_recipe_details(recipe_identifier, master_df, ing_df, nut_df, steps_df):
    """
    Get detailed information for a specific recipe.
    
    Parameters:
    - recipe_identifier: recipe_id or recipe_name to look up
    - master_df: Master recipes dataframe
    - ing_df: Ingredients dataframe
    - nut_df: Nutrition dataframe
    - steps_df: Cooking steps dataframe
    
    Returns:
    - dict with keys 'metadata', 'ingredients', 'nutrition', 'steps' or None if not found
    """
    try:
        # Try lookup by recipe_id first, then by recipe_name
        recipe_info = master_df[master_df['recipe_id'] == recipe_identifier]
        if recipe_info.empty:
            recipe_info = master_df[master_df['recipe_name'] == recipe_identifier]
        if recipe_info.empty:
            print(f"⚠️ Recipe '{recipe_identifier}' not found in master database")
            return None
        
        recipe_info = recipe_info.iloc[0]
        recipe_name = recipe_info['recipe_name']
        print(f"🔍 Loading details for: {recipe_name}")
        
        # Build metadata dict
        metadata = {
            'recipe_name': recipe_name,
            'recipe_id': recipe_info.get('recipe_id', 'N/A'),
            'cuisine': recipe_info.get('cuisine', 'N/A'),
            'category': recipe_info.get('category', 'N/A'),
            'cooking_method': recipe_info.get('cooking_method', 'N/A'),
            'difficulty': recipe_info.get('difficulty', 'N/A'),
            'prep_time_minutes': int(recipe_info.get('prep_time_minutes', 0)),
            'cook_time_minutes': int(recipe_info.get('cook_time_minutes', 0)),
            'total_time_minutes': int(recipe_info.get('total_time_minutes', 0)),
            'servings': int(recipe_info.get('servings', 1)),
            'spice_level': recipe_info.get('spice_level', 'N/A'),
            'meal_type': recipe_info.get('meal_type', 'N/A'),
            'is_vegetarian': bool(recipe_info.get('is_vegetarian', False)),
            'is_vegan': bool(recipe_info.get('is_vegan', False)),
            'is_gluten_free': bool(recipe_info.get('is_gluten_free', False)),
            'is_halal': bool(recipe_info.get('is_halal', False)),
            'rating': float(recipe_info.get('rating', 0)),
            'review_count': int(recipe_info.get('review_count', 0)),
            'calories_per_serving': int(recipe_info.get('calories_per_serving', 0)),
            'estimated_cost_usd': float(recipe_info.get('estimated_cost_usd', 0)),
        }
        
        # Get ingredients (list of ingredient name strings where value > 0)
        ingredients_data = ing_df[ing_df['recipe_name'] == recipe_name]
        ingredients_list = []
        if not ingredients_data.empty:
            ingredient_row = ingredients_data.iloc[0]
            ingredient_cols = [col for col in ing_df.columns if col != 'recipe_name']
            for col in ingredient_cols:
                val = ingredient_row[col]
                if pd.notna(val) and val > 0:
                    ingredients_list.append(col)
            print(f"   ✅ Found {len(ingredients_list)} ingredients")
        else:
            print(f"   ⚠️ No ingredients found")
        
        # Get nutrition info
        nutrition_data = nut_df[nut_df['recipe_name'] == recipe_name]
        if not nutrition_data.empty:
            nutrition_info = nutrition_data.iloc[0].to_dict()
            nutrition_info = {k: v for k, v in nutrition_info.items() 
                            if pd.notna(v) and k != 'recipe_name'}
            print(f"   ✅ Found nutrition data")
        else:
            nutrition_info = {}
            print(f"   ⚠️ No nutrition data found")
        
        # Get cooking steps
        steps_data = steps_df[steps_df['recipe_name'] == recipe_name].sort_values('step_number')
        if not steps_data.empty:
            steps_list = steps_data[['step_number', 'step_description', 
                                     'estimated_time_minutes']].to_dict('records')
            print(f"   ✅ Found {len(steps_list)} cooking steps")
        else:
            steps_list = []
            print(f"   ⚠️ No cooking steps found")
        
        # Return structured dict matching what the pages expect
        return {
            'metadata': metadata,
            'ingredients': ingredients_list,
            'nutrition': nutrition_info,
            'steps': steps_list
        }
        
    except Exception as e:
        print(f"❌ Error getting recipe details for '{recipe_identifier}': {e}")
        return None