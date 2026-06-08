import re
from src.data.loader import get_recipe_details

def retrieve_recipes_for_query(query, master_df, ing_df, nut_df, steps_df, top_k=3):
    """
    Simple keyword-based RAG retriever to find top-k relevant recipes matching the user query.
    
    Args:
        query (str): The user search or chat query.
        master_df (pd.DataFrame): Master recipes metadata.
        ing_df (pd.DataFrame): Ingredients dataframe.
        nut_df (pd.DataFrame): Nutrition dataframe.
        steps_df (pd.DataFrame): Steps dataframe.
        top_k (int): Number of recipes to retrieve.
        
    Returns:
        list: List of detailed recipe dictionaries.
    """
    if not query:
        return []
        
    # Clean query into tokens
    clean_query = query.lower().strip()
    tokens = set(re.findall(r'\b\w+\b', clean_query))
    
    # Exclude common stopwords
    stopwords = {
        'how', 'to', 'make', 'cook', 'find', 'show', 'recipe', 'recipes', 'a', 'an', 'the',
        'what', 'can', 'i', 'do', 'with', 'for', 'about', 'some', 'any', 'my', 'your', 'me',
        'please', 'tell', 'help', 'is', 'are', 'in', 'of', 'on', 'at', 'by', 'with', 'and'
    }
    query_words = tokens - stopwords
    
    if not query_words:
        # Fallback to tokens if all words are stopwords
        query_words = tokens
        
    if not query_words:
        return []
        
    scores = []
    
    for idx, row in master_df.iterrows():
        recipe_id = row['recipe_id']
        recipe_name = str(row['recipe_name']).lower()
        cuisine = str(row['cuisine']).lower()
        category = str(row['category']).lower()
        
        # Calculate matching terms
        score = 0
        for word in query_words:
            # Check matches in metadata
            if word in recipe_name:
                score += 3  # Higher weight for name match
            if word in cuisine:
                score += 2
            if word in category:
                score += 1
                
        if score > 0:
            scores.append((recipe_id, score))
            
    # Sort by score descending
    scores.sort(key=lambda x: x[1], reverse=True)
    
    # Retrieve details for top-k recipe_ids
    results = []
    for recipe_id, _ in scores[:top_k]:
        details = get_recipe_details(recipe_id, master_df, ing_df, nut_df, steps_df)
        if details:
            results.append(details)
            
    return results
