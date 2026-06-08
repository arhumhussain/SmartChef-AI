import re

def normalize_ingredient(user_input, valid_ingredients):
    """
    Normalizes a user-input ingredient name to match one of the valid database ingredients.
    
    Args:
        user_input (str): The ingredient string entered by the user.
        valid_ingredients (list): List of valid ingredients in the database.
        
    Returns:
        str: The matched valid ingredient, or None if no match is found.
    """
    if not user_input:
        return None
        
    # Clean input: lowercase, remove special characters, strip whitespace
    clean_input = user_input.lower().strip()
    clean_input = re.sub(r'[^\w\s]', '', clean_input)
    
    # Singularize/pluralize simple helper
    clean_input = re.sub(r's$', '', clean_input) # simple de-pluralization (e.g. potatoes -> potatoe, carrots -> carrot)
    if clean_input.endswith('potatoe'):
        clean_input = 'potato'
    if clean_input.endswith('tomafoe') or clean_input.endswith('tomatoe'):
        clean_input = 'tomato'
    if clean_input.endswith('lentil'):
        clean_input = 'lentils' # map back to 'lentils (dal)'
        
    # Exact match check after cleaning
    for valid in valid_ingredients:
        v_clean = valid.lower().strip()
        # Direct equality check
        if clean_input == v_clean:
            return valid
            
    # Substring checks
    for valid in valid_ingredients:
        v_clean = valid.lower().strip()
        # Check if the valid ingredient is part of the user input (e.g. "chicken breast" -> "chicken")
        # Or if the user input is a substring of the valid ingredient (e.g. "dal" -> "lentils (dal)")
        if v_clean in clean_input or clean_input in v_clean:
            return valid
            
    return None


def parse_user_ingredients(user_input_str, valid_ingredients):
    """
    Parses a raw comma-separated string of user ingredients into a list of normalized valid ingredients.
    
    Args:
        user_input_str (str): Comma-separated string of ingredients (e.g. "Chicken, potatoes, garlic").
        valid_ingredients (list): List of valid ingredients in the database.
        
    Returns:
        list: List of unique matched valid ingredient strings.
    """
    if not user_input_str:
        return []
        
    # Split by comma or semicolon
    raw_ingredients = re.split(r'[,;]', user_input_str)
    
    matched_ingredients = set()
    for raw in raw_ingredients:
        raw = raw.strip()
        if not raw:
            continue
        matched = normalize_ingredient(raw, valid_ingredients)
        if matched:
            matched_ingredients.add(matched)
            
    return list(matched_ingredients)
