CHEF_SYSTEM_PROMPT = """
You are the "SmartChef AI Assistant", a friendly, world-class professional culinary chef and nutritionist. 
Your goal is to help users with:
1. Ingredient substitutions (e.g. replacing eggs, dairy, or gluten-containing ingredients).
2. Explaining cooking techniques (e.g. poaching, braising, folding batter).
3. Adapting recipes to fit specific dietary goals (low-carb, low-fat, high-protein, calorie-restricted).
4. Explaining recipes from the user's custom database and recommending pairings.

Guidelines:
- Keep your responses concise, friendly, and structured (use bolding, bullet points, or markdown tables where appropriate).
- If you base your recommendation on custom recipe context, mention the name of the recipe and detail why it matches their preferences.
- If you don't know the answer, politely offer your best culinary alternative.
- Maintain a helpful, inspiring, and professional chef persona.
"""

def format_rag_prompt(user_query, context_recipes):
    """
    Formats the user query and retrieved recipe context into a single prompt for the LLM.
    """
    recipes_context_str = ""
    if context_recipes:
        recipes_context_str = "\nHere are some relevant recipes from your database:\n"
        for i, recipe in enumerate(context_recipes):
            recipes_context_str += f"\n--- Recipe {i+1} ---\n"
            recipes_context_str += f"Name: {recipe.get('recipe_name')}\n"
            recipes_context_str += f"Cuisine: {recipe.get('cuisine')} | Category: {recipe.get('category')} | Difficulty: {recipe.get('difficulty')}\n"
            recipes_context_str += f"Time: {recipe.get('total_time_minutes')} mins | Rating: {recipe.get('rating')}/5.0\n"
            recipes_context_str += f"Ingredients: {', '.join(recipe.get('ingredients', []))}\n"
            
            nut = recipe.get('nutrition', {})
            recipes_context_str += f"Nutrition (per serving): {nut.get('calories', 'N/A')} kcal | Protein: {nut.get('protein_g', 'N/A')}g | Carbs: {nut.get('carbohydrates_g', 'N/A')}g | Fat: {nut.get('fat_g', 'N/A')}g\n"
            
            steps = recipe.get('steps', [])
            steps_str = ", ".join([f"Step {s['step_number']}: {s['step_description']}" for s in steps])
            recipes_context_str += f"Instructions: {steps_str}\n"
            recipes_context_str += "--------------------\n"
            
    prompt = f"""
{recipes_context_str}

User Question: {user_query}

Chef Response:
"""
    return prompt
