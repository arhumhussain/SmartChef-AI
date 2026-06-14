# SmartChef-AI 🍳

SmartChef-AI is a high-fidelity, data-driven web application for smart recipe discovery, nutrition-aware meal planning, and interactive cooking assistance. It features a fully customized, premium glassmorphic dashboard styled using professional-grade modern typography, vibrant colors, and dynamic UI micro-animations.

---

## 🚀 Key Features

### 1. 🔍 Recipe Finder (Ingredient-Based Discovery via KNN)
- Select from supported ingredients or type custom ones.
- Match score is calculated in the background using a **K-Nearest Neighbors (KNN)** model comparing the user's ingredient vector against all recipe ingredient profiles.
- Outputs matching level percentages (`🔥 X% Match`) and lists recipes that maximize pantry utilization and minimize waste.

### 2. 🥗 Dynamic Dietary Goals & Target-Nutrition Filters
- Filter recipes matching specific fitness and dietary regimes:
  - **Weight Loss:** Lowers threshold for calories and fats (bottom 50% percentile).
  - **Muscle Gain / High Protein:** Filters for high-protein recipes (top 60% percentile).
  - **Low Fat:** Filters for low-fat candidates (bottom 30% percentile).
  - **Low Carb:** Filters for low-carb candidates (bottom 30% percentile).
- Automatically calculates dynamic cutoffs based on the entire recipe dataset.

### 3. 📅 Customized Meal Planner
- Build day-by-day or weekly diet schedules based on your caloric and protein goals.
- Provides real-time interactive summaries of aggregated macronutrients.
- Exports a consolidated, printable grocery shopping checklist of required ingredients.

### 4. 💬 Conversational AI Chef (RAG-Enabled via Groq/Gemini)
- Engage in conversation with a private culinary AI Chef.
- Powered by either the **Groq API** (using `llama-3.3-70b-versatile`) or the **Gemini API** (using `gemini-1.5-flash`).
- Utilizes **Retrieval-Augmented Generation (RAG)**: translates user questions into keyword queries, retrieves the top relevant recipes from your local CSV datasets, and feeds them to the LLM as grounding context.
- **Simulated Fallback Mode:** Works completely offline or without an API key using standard substitution heuristics, knife skill tutorials, and custom recipe guidelines.

---

## 📂 Repository Structure

```filepath
SmartChef-AI/
│
├── app.py                      # Main App Entrypoint & Global Analytics Dashboard
├── requirements.txt            # Python Dependencies
├── .gitignore                  # Git Ignore Settings
├── .env                        # Local Environment Variables configuration
│
├── datasets/                   # Raw & Cleaned Culinary Datasets (CSV format)
│   ├── recipes_master.csv      # Recipe metadata (times, ratings, costs, difficulty)
│   ├── Recipe_ingrediect.csv   # Binary ingredient matrix per recipe
│   ├── Recipe_nutrition.csv    # Macronutrient details (calories, protein, carbs, fats)
│   └── Recipe_steps.csv        # Ordered cooking instructions and prep times
│
├── models/                     # Trained Recommender Artifacts
│   ├── Recipe_knn_model.pkl    # Serialized Scikit-Learn KNN Model
│   ├── ingredient_columns.pkl  # Vocabulary vector mapping of valid ingredients
│   └── recipe_names.pkl        # List of recipes aligned with model row indices
│
├── pages/                      # Multi-Page Streamlit Routes
│   ├── 1_Recipe_Finder.py      # Pantry-to-Recipe Matcher interface (KNN)
│   ├── 2_Recipe_Details.py     # High-fidelity single recipe detail viewer
│   ├── 3_Meal_Planner.py       # Macro-oriented schedule calendar & shopping list builder
│   └── 4_AI_Chef.py            # Conversational Chatbot UI
│
└── src/                        # Core Application Backend Modules
    ├── data/
    │   └── loader.py           # Cached dataset alignment, mapping, and parser functions
    ├── recommender/
    │   ├── diet_filter.py      # Percentile-based nutritional query filters
    │   └── Knn_recommendation.py# KNN-based recommendation algorithm and metadata matching
    ├── chatbot/
    │   ├── chef_bot.py         # Chatbot API driver (Groq/Gemini compatibility) and simulation
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
   python -m venv .venv
   # On Windows:
   .\.venv\Scripts\activate
   # On macOS/Linux:
   source .venv/bin/activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Variables:**
   Create a `.env` file in the root directory (already templates as `.env`):
   ```env
   GROQ_API_KEY=gsk_your_groq_api_key_here
   GEMINI_API_KEY=your_gemini_api_key_here
   ```
   *Note: If both keys are empty, the app automatically switches to Simulated Fallback Mode for the AI Chef page.*

5. **Run the Streamlit Application:**
   ```bash
   streamlit run app.py
   ```

---

## 👥 Contributors Development Workflow

- **Dataset Alignment:** The datasets are joined dynamically at runtime. Modify [src/data/loader.py](file:///e:/University/Uni%20Projects/PBLs/SmartChef-AI/SmartChef-AI/src/data/loader.py) to configure base merges or preprocess operations.
- **Custom UI Layouts:** To adjust the color scheme, hover animations, typography, or cards, edit the injected styles in [src/utils/styles.py](file:///e:/University/Uni%20Projects/PBLs/SmartChef-AI/SmartChef-AI/src/utils/styles.py).
- **KNN Recommendations:** Tuning the KNN model query parameters or modifying similarity thresholds should be handled inside [src/recommender/Knn_recommendation.py](file:///e:/University/Uni%20Projects/PBLs/SmartChef-AI/SmartChef-AI/src/recommender/Knn_recommendation.py).
- **Dietary Percentiles:** Adjust dietary goal cutoff percentiles inside [src/recommender/diet_filter.py](file:///e:/University/Uni%20Projects/PBLs/SmartChef-AI/SmartChef-AI/src/recommender/diet_filter.py).
