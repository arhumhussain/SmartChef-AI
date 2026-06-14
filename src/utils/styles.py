import streamlit as st

def inject_premium_css():
    """
    Injects custom CSS with Orange + Teal Food-Tech theme
    Colors: Primary #FF6B35, Secondary #2EC4B6
    """
    css_content = """
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=Playfair+Display:ital,wght@0,400..900;1,400..900&display=swap" rel="stylesheet">
    
    <style>
    /* ========== BASE THEME ========== */
    .stApp {
        background-color: #F8F9FA !important;
        color: #2D3436 !important;
        font-family: 'Outfit', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }
    
    .main .block-container {
        background-color: #F8F9FA !important;
    }
    
    /* ========== TYPOGRAPHY ========== */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Outfit', sans-serif;
        font-weight: 700;
        letter-spacing: -0.02em;
        color: #2D3436;
    }
    
    p, li, span, div {
        color: #2D3436;
    }
    
    .hero-title {
        font-family: 'Playfair Display', serif;
        font-size: 3.5rem;
        font-weight: 800;
        line-height: 1.2;
        margin-bottom: 0.5rem;
        color: #2D3436;
        background: none;
        -webkit-text-fill-color: #2D3436;
    }
    
    .hero-subtitle {
        font-size: 1.25rem;
        color: #636E72;
        font-weight: 300;
        margin-bottom: 2rem;
    }
    
    /* ========== CARDS ========== */
    .glass-card, .recipe-card {
        background: #FFFFFF;
        backdrop-filter: none;
        border: 1px solid #E9ECEF;
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
    }
    
    .glass-card:hover, .recipe-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
        border-color: #FF6B35;
    }
    
    /* ========== STATS ========== */
    .stat-container {
        display: flex;
        justify-content: space-between;
        gap: 1rem;
        margin-bottom: 2rem;
        flex-wrap: wrap;
    }
    
    .stat-box {
        flex: 1;
        background: #FFFFFF;
        border: 1px solid #E9ECEF;
        border-radius: 12px;
        padding: 1.2rem;
        text-align: center;
        transition: all 0.2s ease;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.02);
    }
    
    .stat-box:hover {
        border-color: #FF6B35;
        box-shadow: 0 4px 12px rgba(255, 107, 53, 0.1);
    }
    
    .stat-val {
        font-size: 2.2rem;
        font-weight: 800;
        color: #FF6B35;
        margin-bottom: 0.2rem;
    }
    
    .stat-lbl {
        font-size: 0.85rem;
        color: #636E72;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    /* ========== BADGES ========== */
    .badge {
        display: inline-block;
        padding: 0.35em 0.65em;
        font-size: 0.75rem;
        font-weight: 600;
        line-height: 1;
        text-align: center;
        white-space: nowrap;
        vertical-align: baseline;
        border-radius: 50px;
        margin-right: 0.5rem;
        margin-bottom: 0.5rem;
    }
    
    .badge-cuisine {
        background-color: rgba(46, 196, 182, 0.1);
        color: #2EC4B6;
        border: 1px solid rgba(46, 196, 182, 0.2);
    }
    
    .badge-difficulty {
        background-color: rgba(255, 107, 53, 0.1);
        color: #FF6B35;
        border: 1px solid rgba(255, 107, 53, 0.2);
    }
    
    .badge-score {
        background-color: rgba(46, 196, 182, 0.1);
        color: #2EC4B6;
        border: 1px solid rgba(46, 196, 182, 0.2);
        font-weight: 800;
    }
    
    .badge-diet {
        background-color: rgba(255, 107, 53, 0.1);
        color: #FF6B35;
        border: 1px solid rgba(255, 107, 53, 0.2);
    }
    
    /* ========== BUTTONS ========== */
    .stButton > button {
        background: #FF6B35 !important;
        color: white !important;
        font-weight: 600 !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.5rem 1.5rem !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 2px 6px rgba(255, 107, 53, 0.3) !important;
    }
    
    .stButton > button:hover {
        background: #E85D2A !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 12px rgba(255, 107, 53, 0.4) !important;
    }
    
    /* ========== SIDEBAR ========== */
    section[data-testid="stSidebar"] {
        background-color: #FFFFFF !important;
        border-right: 1px solid #E9ECEF !important;
        box-shadow: 2px 0 8px rgba(0, 0, 0, 0.02) !important;
    }
    
    [data-testid="stSidebarNav"] {
        padding-top: 1.5rem !important;
    }
    
    [data-testid="stSidebarNav"]::before {
        content: "SmartChef-AI 🍳" !important;
        display: block !important;
        padding: 1.5rem 1.8rem 1.2rem 1.8rem !important;
        font-family: 'Outfit', sans-serif !important;
        font-size: 1.4rem !important;
        font-weight: 800 !important;
        color: #FF6B35 !important;
        border-bottom: 2px solid #FF6B35 !important;
        margin-bottom: 1.5rem !important;
        letter-spacing: -0.02em !important;
        white-space: nowrap !important;
    }
    
    div[data-testid="stSidebarNavLi"] {
        margin: 0.5rem 0.9rem !important;
        border-radius: 12px !important;
        transition: all 0.3s ease !important;
    }
    
    a[data-testid="stSidebarNavLink"] {
        padding: 0.8rem 1.1rem !important;
        border-radius: 12px !important;
        color: #636E72 !important;
        font-family: 'Outfit', sans-serif !important;
        font-size: 0.95rem !important;
        font-weight: 500 !important;
        transition: all 0.3s ease !important;
        text-transform: capitalize !important;
    }
    
    div[data-testid="stSidebarNavLi"]:hover {
        background-color: rgba(255, 107, 53, 0.05) !important;
    }
    
    a[data-testid="stSidebarNavLink"]:hover {
        color: #FF6B35 !important;
        transform: translateX(4px) !important;
    }
    
    a[data-testid="stSidebarNavLink"][aria-current="page"] {
        background: rgba(255, 107, 53, 0.1) !important;
        border-left: 3px solid #FF6B35 !important;
        color: #FF6B35 !important;
        font-weight: 600 !important;
    }
    
    /* CSS hack to rename "App" to "Home" in the sidebar navigation list */
    a[data-testid="stSidebarNavLink"][href="/"] span {
        display: none !important;
    }
    
    a[data-testid="stSidebarNavLink"][href="/"]::after {
        content: "Home" !important;
        color: inherit !important;
        font-family: 'Outfit', sans-serif !important;
        font-size: 0.95rem !important;
        font-weight: 500 !important;
    }
    
    a[data-testid="stSidebarNavLink"][href="/"][aria-current="page"]::after {
        font-weight: 600 !important;
    }
    
    /* ========== FIX FOR DROPDOWN TEXT COLORS ========== */
    
    /* Multiselect dropdown text */
    .stMultiSelect [data-baseweb="select"] span {
        color: #2D3436 !important;
    }
    
    /* Selected items in multiselect - corrected to match theme */
    .stMultiSelect [data-baseweb="tag"] span {
        color: #FF6B35 !important;
    }
    
    /* Popover/dropdown wrapper styling to prevent black background */
    div[data-baseweb="popover"] {
        background-color: #FFFFFF !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08) !important;
        border: 1px solid #E9ECEF !important;
        border-radius: 8px !important;
    }
    div[data-baseweb="popover"] ul {
        background-color: #FFFFFF !important;
        color: #2D3436 !important;
    }
    
    /* Dropdown options list */
    div[data-baseweb="popover"] div[role="listbox"] div[role="option"] {
        color: #2D3436 !important;
        background-color: #FFFFFF !important;
    }
    
    /* Dropdown option hover */
    div[data-baseweb="popover"] div[role="listbox"] div[role="option"]:hover {
        background-color: rgba(255, 107, 53, 0.1) !important;
        color: #FF6B35 !important;
    }
    
    /* Selectbox text */
    .stSelectbox [data-baseweb="select"] span {
        color: #2D3436 !important;
    }
    
    /* Dropdown arrows and icons */
    .stMultiSelect svg, .stSelectbox svg {
        fill: #FF6B35 !important;
        stroke: #FF6B35 !important;
    }
    
    /* Input text general */
    .stTextInput input, .stTextArea textarea {
        color: #2D3436 !important;
        background-color: #FFFFFF !important;
    }
    
    /* Placeholder text */
    .stTextInput input::placeholder, .stTextArea textarea::placeholder {
        color: #636E72 !important;
    }
    
    /* Number input */
    .stNumberInput input {
        color: #2D3436 !important;
    }
    
    /* Radio and checkbox labels */
    .stRadio label, .stCheckbox label {
        color: #2D3436 !important;
    }
    
    /* Selectbox dropdown options */
    div[data-baseweb="popover"] ul li {
        color: #2D3436 !important;
        background-color: #FFFFFF !important;
    }
    
    div[data-baseweb="popover"] ul li:hover {
        background-color: rgba(255, 107, 53, 0.1) !important;
        color: #FF6B35 !important;
    }
    
    /* Selected option in selectbox */
    div[data-baseweb="select"] [aria-selected="true"] {
        background-color: rgba(255, 107, 53, 0.1) !important;
        color: #FF6B35 !important;
    }
    
    /* ========== PROGRESS BAR ========== */
    .stProgress > div > div > div {
        background-color: #2EC4B6 !important;
    }
    
    /* ========== FOOTER ========== */
    .chef-footer {
        text-align: center;
        padding: 2rem 0;
        margin-top: 4rem;
        border-top: 1px solid #E9ECEF;
        color: #636E72;
        font-size: 0.85rem;
    }
    
    /* ========== RESPONSIVE ========== */
    @media (max-width: 768px) {
        .hero-title {
            font-size: 2rem !important;
        }
        
        .hero-subtitle {
            font-size: 1rem !important;
        }
        
        .stat-container {
            flex-direction: column !important;
            gap: 0.75rem !important;
        }
        
        section[data-testid="stSidebar"] {
            background-color: #FFFFFF !important;
        }
    }
    
    /* ========== ANIMATIONS ========== */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .recipe-card {
        animation: fadeInUp 0.5s ease-out;
    }
        /* ========== FIX EXPANDER (Orange Dot) ========== */
    
    /* Change expander arrow/caret color */
    .streamlit-expanderHeader svg {
        fill: #FF6B35 !important;
        stroke: #FF6B35 !important;
        color: #FF6B35 !important;
    }
    
    /* Change expander header text color */
    .streamlit-expanderHeader {
        color: #2D3436 !important;
        font-weight: 600 !important;
    }
    
    /* Change expander hover effect */
    .streamlit-expanderHeader:hover {
        color: #FF6B35 !important;
    }
    
    .streamlit-expanderHeader:hover svg {
        fill: #E85D2A !important;
        stroke: #E85D2A !important;
    }
    
    /* Change expander border color when open */
    .streamlit-expanderContent {
        border-left: 2px solid #FF6B35 !important;
    }
    
    /* ========== FIX SLIDER BAR COLOR ========== */
    
    /* Slider track (background) */
    .stSlider > div > div > div > div {
        background: #E9ECEF !important;
    }
    
    /* Slider filled portion */
    .stSlider > div > div > div > div > div {
        background: #FF6B35 !important;
    }
    
    /* Slider handle/thumb */
    .stSlider > div > div > div > div > div > div {
        background: #FF6B35 !important;
        border-color: #FFFFFF !important;
        border-width: 2px !important;
        box-shadow: 0 0 0 2px rgba(255, 107, 53, 0.2) !important;
    }
    
    /* Slider handle hover */
    .stSlider > div > div > div > div > div > div:hover {
        background: #E85D2A !important;
        transform: scale(1.2) !important;
    }
    
    /* Slider value numbers */
    .stSlider > div > div > div > div > div > div > div {
        color: #FF6B35 !important;
        font-weight: 600 !important;
    }
    
    /* ========== FIX SELECTBOX STYLES ========== */
    
    /* Selectbox container */
    .stSelectbox > div > div {
        background-color: #FFFFFF !important;
        border: 1px solid #E9ECEF !important;
        border-radius: 8px !important;
    }
    
    /* Selectbox label/text */
    .stSelectbox label {
        color: #2D3436 !important;
        font-weight: 500 !important;
    }
    
    /* Selectbox selected value */
    .stSelectbox [data-baseweb="select"] span {
        color: #2D3436 !important;
        font-weight: 500 !important;
    }
    
    /* Selectbox dropdown arrow */
    .stSelectbox svg {
        fill: #FF6B35 !important;
        stroke: #FF6B35 !important;
    }
    
    /* Selectbox focus border */
    .stSelectbox > div > div:focus-within {
        border-color: #FF6B35 !important;
        box-shadow: 0 0 0 2px rgba(255, 107, 53, 0.1) !important;
    }
    
    /* ========== FIX MULTISELECT STYLES ========== */
    
    /* Multiselect container */
    .stMultiSelect > div > div {
        background-color: #FFFFFF !important;
        border: 1px solid #E9ECEF !important;
        border-radius: 8px !important;
    }
    
    /* Multiselect label */
    .stMultiSelect label {
        color: #2D3436 !important;
        font-weight: 500 !important;
    }
    
    /* Multiselect selected items (tags) */
    .stMultiSelect [data-baseweb="tag"] {
        background-color: rgba(255, 107, 53, 0.1) !important;
        border: 1px solid rgba(255, 107, 53, 0.2) !important;
        border-radius: 6px !important;
    }
    
    /* Multiselect selected item text */
    .stMultiSelect [data-baseweb="tag"] span {
        color: #FF6B35 !important;
        font-weight: 500 !important;
    }
    
    /* Multiselect remove button (X) */
    .stMultiSelect [data-baseweb="tag"] svg {
        fill: #FF6B35 !important;
        stroke: #FF6B35 !important;
    }
    
    /* Multiselect remove button hover */
    .stMultiSelect [data-baseweb="tag"] svg:hover {
        fill: #E85D2A !important;
        stroke: #E85D2A !important;
    }
    
    /* Multiselect input text */
    .stMultiSelect input {
        color: #2D3436 !important;
    }
    
    /* Multiselect placeholder */
    .stMultiSelect input::placeholder {
        color: #636E72 !important;
    }
    
    /* Multiselect dropdown arrow */
    .stMultiSelect svg {
        fill: #FF6B35 !important;
        stroke: #FF6B35 !important;
    }
    
    /* Multiselect focus border */
    .stMultiSelect > div > div:focus-within {
        border-color: #FF6B35 !important;
        box-shadow: 0 0 0 2px rgba(255, 107, 53, 0.1) !important;
    }
    
    /* ========== FIX NUMBER INPUT ========== */
    
    /* Number input container */
    .stNumberInput > div > div {
        background-color: #FFFFFF !important;
        border: 1px solid #E9ECEF !important;
        border-radius: 8px !important;
    }
    
    /* Number input field */
    .stNumberInput input {
        color: #2D3436 !important;
        background-color: #FFFFFF !important;
    }
    
    /* Number input buttons (up/down) */
    .stNumberInput button {
        background-color: rgba(255, 107, 53, 0.1) !important;
        color: #FF6B35 !important;
        border: none !important;
    }
    
    .stNumberInput button:hover {
        background-color: rgba(255, 107, 53, 0.2) !important;
        color: #E85D2A !important;
    }
    
    /* Number input focus border */
    .stNumberInput > div > div:focus-within {
        border-color: #FF6B35 !important;
        box-shadow: 0 0 0 2px rgba(255, 107, 53, 0.1) !important;
    }
    
    /* ========== FIX TEXT INPUT ========== */
    
    /* Text input container */
    .stTextInput > div > div {
        background-color: #FFFFFF !important;
        border: 1px solid #E9ECEF !important;
        border-radius: 8px !important;
    }
    
    /* Text input field */
    .stTextInput input {
        color: #2D3436 !important;
        background-color: #FFFFFF !important;
    }
    
    /* Text input focus border */
    .stTextInput > div > div:focus-within {
        border-color: #FF6B35 !important;
        box-shadow: 0 0 0 2px rgba(255, 107, 53, 0.1) !important;
    }
    
    /* ========== FIX RADIO BUTTONS ========== */
    
    /* Radio button label */
    .stRadio label {
        color: #2D3436 !important;
    }
    
    /* Radio button selected circle */
    .stRadio [role="radiogroup"] [role="radio"][aria-checked="true"] {
        border-color: #FF6B35 !important;
    }
    
    .stRadio [role="radiogroup"] [role="radio"][aria-checked="true"] div {
        background-color: #FF6B35 !important;
    }
    
    /* Radio button hover */
    .stRadio [role="radiogroup"] [role="radio"]:hover {
        border-color: #E85D2A !important;
    }
    
    /* ========== FIX CHECKBOXES ========== */
    
    /* Checkbox label */
    .stCheckbox label {
        color: #2D3436 !important;
    }
    
    /* Checkbox selected */
    .stCheckbox [role="checkbox"][aria-checked="true"] {
        border-color: #FF6B35 !important;
        background-color: #FF6B35 !important;
    }
    
    /* Checkbox hover */
    .stCheckbox [role="checkbox"]:hover {
        border-color: #E85D2A !important;
    }
    
    /* ========== FIX DATE INPUT (if used) ========== */
    
    /* Date input container */
    .stDateInput > div > div {
        background-color: #FFFFFF !important;
        border: 1px solid #E9ECEF !important;
        border-radius: 8px !important;
    }
    
    .stDateInput input {
        color: #2D3436 !important;
    }
    </style>
    """
    st.markdown(css_content, unsafe_allow_html=True)