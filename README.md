# SmartChef-AI 🍳

SmartChef-AI is a high-fidelity, data-driven web application for smart recipe discovery, nutrition-aware meal planning, and interactive cooking assistance. It features a fully customized, premium dark glassmorphic dashboard styled using professional-grade modern typography and dynamic UI micro-animations.


## 🚀 Key Features

### 1. 🔍 Recipe Finder (Ingredient-Based Discovery)
- Enter the ingredients available in your kitchen (e.g., *Chicken, Onion, Garlic*).
- An optimized, rule-based vectorized matching system calculates matching levels against the recipes database.
- Scores candidates by `match_count / total_ingredients` to prioritize dishes that maximize pantry utilization and minimize waste.

### 2. 🥗 Dynamic Dietary Goals & Target-Nutrition Filters
- Filter recipes matching specific fitness and dietary regimes:
  - **Weight Loss:** Lowers threshold for calories and fats (bottom 30% and 35% percentiles).
  - **Muscle Gain / High Protein:** Filters for high-protein recipes (top 30% percentile).
  - **Low Fat:** Filters for low-fat candidates (bottom 25% percentile).
  - **Low Carb:** Filters for low-carb candidates (bottom 25% percentile).
- Automatically calculates dynamic cutoffs based on the entire recipe dataset.

### 3. 📅 Customized Meal Planner
- Build day-by-day or weekly diet schedules based on your caloric and protein goals.
- Provides real-time interactive summaries of aggregated macronutrients.
- Exports a consolidated, printable grocery shopping checklist of required ingredients.

### 4. 💬 Conversational AI Chef (RAG-Enabled)
- Engage in conversation with a private culinary AI Chef.
- Powered by the **Gemini API** using a kitchen-specialized system instruction prompt.
- Utilizes **Retrieval-Augmented Generation (RAG)**: translates user questions into keyword queries, retrieves the top relevant recipes from your local CSV datasets, and feeds them to Gemini as grounding context.
- **Simulated Fallback Mode:** Works completely offline or without an API key using standard substitution heuristics, knife skill tutorials, and custom recipe guidelines.

---

## 📂 Repository Structure

```filepath
SmartChef-AI/
│
├── app.py                      # Main App Entrypoint & Global Analytics Dashboard
├── requirements.txt            # Python Dependencies
├── .gitignore                  # Git Ignore Settings
│
├── datasets/                   # Raw & Cleaned Culinary Datasets (CSV format)
│   ├── recipes_master.csv      # Recipe metadata (times, ratings, costs, difficulty)
│   ├── Recipe_ingrediect.csv   # Binary ingredient matrix per recipe
│   ├── Recipe_nutrition.csv    # Macronutrient details (calories, protein, carbs, fats)
│   └── Recipe_steps.csv        # Ordered cooking instructions and prep times
│
├── pages/                      # Multi-Page Streamlit Routes
│   ├── 1_Recipe_Finder.py      # Pantry-to-Recipe Matcher interface
│   ├── 2_Recipe_Details.py     # High-fidelity single recipe detail viewer
│   ├── 3_Meal_Planner.py       # Macro-oriented schedule calendar & shopping list builder
│   └── 4_AI_Chef.py            # Conversational Chatbot UI
│
└── src/                        # Core Application Backend Modules
    ├── data/
    │   ├── loader.py           # Cached dataset alignment, mapping, and parser functions
    │   └── preprocess.py       # Helper scripts for preprocessing raw CSV content
    ├── recommender/
    │   ├── diet_filter.py      # Percentile-based nutritional query filters
    │   └── ingredient_match.py # Vectorized ingredient score computation engine
    ├── chatbot/
    │   ├── chef_bot.py         # Gemini API driver and simulated chatbot engine
    │   ├── prompts.py          # Chatbot persona system prompts
    │   └── rag.py              # Local TF-IDF style keyword recipe context retriever
    └── utils/
        └── styles.py           # Injected Premium CSS styles & components layout
```

---

## 🛠️ Installation & Setup

1. **Clone the Repository:**
   ```bash
   git clone <repository-url>
   cd SmartChef-AI
   ```

2. **Create and Activate a Virtual Environment:**
   ```bash
   python -m venv venv
   # On Windows:
   .\venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Variables:**
   Create a `.env` file in the root directory to store your Gemini API key (optional):
   ```env
   GEMINI_API_KEY=your_gemini_api_key_here
   ```
   *Note: If no API key is detected, the app automatically switches to Simulated Fallback Mode for the AI Chef page.*

5. **Run the Streamlit Application:**
   ```bash
   streamlit run app.py
   ```

---

## 👥 Contributors Development Workflow

- **Dataset Alignment:** The datasets are joined dynamically at runtime. Modify [src/data/loader.py](file:///c:/Users/arhum/Desktop/SmartChef-AI/src/data/loader.py) to configure base merges or preprocess operations.
- **Custom UI Layouts:** To adjust the color scheme, hover animations, typography, or cards, edit the injected styles in [src/utils/styles.py](file:///c:/Users/arhum/Desktop/SmartChef-AI/src/utils/styles.py).
- **Recommendation Rules:** Tuning nutritional thresholds or modifying the ingredient matching weights should be handled inside [src/recommender/diet_filter.py](file:///c:/Users/arhum/Desktop/SmartChef-AI/src/recommender/diet_filter.py) and [src/recommender/ingredient_match.py](file:///c:/Users/arhum/Desktop/SmartChef-AI/src/recommender/ingredient_match.py).
