import streamlit as st

def inject_premium_css():
    """
    Injects custom CSS to style the Streamlit app with a high-fidelity glassmorphic dark theme,
    custom fonts, vibrant gradients, and micro-animations.
    """
    css_content = """
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=Playfair+Display:ital,wght@0,400..900;1,400..900&display=swap" rel="stylesheet">
    
    <style>
    /* Main Background & Text Styles */
    .stApp {
        background: radial-gradient(circle at top right, #1a1c2e 0%, #0d0e15 100%);
        color: #e2e8f0;
        font-family: 'Outfit', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Header Customization */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Outfit', sans-serif;
        font-weight: 700;
        letter-spacing: -0.02em;
        background: linear-gradient(135deg, #ffffff 30%, #a5b4fc 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    /* Hero Title styling */
    .hero-title {
        font-family: 'Playfair Display', serif;
        font-size: 3.5rem;
        font-weight: 800;
        line-height: 1.2;
        margin-bottom: 0.5rem;
        background: linear-gradient(135deg, #ff9f43 0%, #ff5252 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .hero-subtitle {
        font-size: 1.25rem;
        color: #94a3b8;
        font-weight: 300;
        margin-bottom: 2rem;
    }
    
    /* Glassmorphism Cards */
    .glass-card {
        background: rgba(30, 41, 59, 0.45);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.2);
    }
    
    .glass-card:hover {
        transform: translateY(-5px);
        border-color: rgba(165, 180, 252, 0.3);
        box-shadow: 0 10px 30px rgba(99, 102, 241, 0.15);
    }
    
    /* Stats grid */
    .stat-container {
        display: flex;
        justify-content: space-between;
        gap: 1rem;
        margin-bottom: 2rem;
    }
    
    .stat-box {
        flex: 1;
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        padding: 1.2rem;
        text-align: center;
        transition: all 0.2s ease;
    }
    
    .stat-box:hover {
        background: rgba(255, 255, 255, 0.06);
    }
    
    .stat-val {
        font-size: 2.2rem;
        font-weight: 800;
        background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
    }
    
    .stat-lbl {
        font-size: 0.85rem;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    /* Custom Badges */
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
        background-color: rgba(99, 102, 241, 0.2);
        color: #a5b4fc;
        border: 1px solid rgba(99, 102, 241, 0.4);
    }
    
    .badge-difficulty {
        background-color: rgba(234, 179, 8, 0.2);
        color: #fef08a;
        border: 1px solid rgba(234, 179, 8, 0.4);
    }
    
    .badge-score {
        background-color: rgba(34, 197, 94, 0.2);
        color: #86efac;
        border: 1px solid rgba(34, 197, 94, 0.4);
        font-weight: 800;
    }
    
    .badge-diet {
        background-color: rgba(236, 72, 153, 0.2);
        color: #fbcfe8;
        border: 1px solid rgba(236, 72, 153, 0.4);
    }
    
    /* Interactive custom selector buttons */
    .stButton > button {
        background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%) !important;
        color: white !important;
        font-weight: 600 !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.5rem 1.5rem !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3) !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(99, 102, 241, 0.45) !important;
    }
    
    /* Sidebar Container styling - Glassmorphism */
    section[data-testid="stSidebar"] {
        background-color: rgba(13, 15, 23, 0.75) !important;
        backdrop-filter: blur(20px) !important;
        -webkit-backdrop-filter: blur(20px) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.06) !important;
    }
    
    /* Sidebar Navigation Container */
    [data-testid="stSidebarNav"] {
        padding-top: 1.5rem !important;
    }
    
    /* Premium Sidebar Header Title with Ambient Glow */
    [data-testid="stSidebarNav"]::before {
        content: "SmartChef-AI 🍳" !important;
        display: block !important;
        padding: 1.5rem 1.8rem 1.2rem 1.8rem !important;
        font-family: 'Playfair Display', serif !important;
        font-size: 1.7rem !important;
        font-weight: 800 !important;
        background: linear-gradient(135deg, #ff9f43 0%, #ff5252 50%, #f72585 100%) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        border-bottom: 1px solid rgba(255, 255, 255, 0.06) !important;
        margin-bottom: 1.5rem !important;
        letter-spacing: -0.02em !important;
        text-shadow: 0 0 40px rgba(255, 82, 82, 0.2) !important;
    }
    
    /* Sidebar Navigation List Items - Styled as floating cards */
    div[data-testid="stSidebarNavLi"] {
        margin: 0.5rem 0.9rem !important;
        border-radius: 12px !important;
        border: 1px solid rgba(255, 255, 255, 0.02) !important;
        background-color: rgba(255, 255, 255, 0.01) !important;
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1) !important;
        overflow: visible !important; /* Allow glowing shadows to spread */
    }
    
    div[data-testid="stSidebarNavLi"]:hover {
        background-color: rgba(255, 255, 255, 0.03) !important;
        border-color: rgba(99, 102, 241, 0.2) !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1) !important;
    }
    
    /* Sidebar Navigation Link - Default State */
    a[data-testid="stSidebarNavLink"] {
        padding: 0.8rem 1.1rem !important;
        border-radius: 12px !important;
        border: 1px solid transparent !important;
        color: #94a3b8 !important;
        font-family: 'Outfit', sans-serif !important;
        font-size: 0.95rem !important;
        font-weight: 500 !important;
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1) !important;
        display: flex !important;
        align-items: center !important;
        text-decoration: none !important;
        background-color: transparent !important;
    }
    
    a[data-testid="stSidebarNavLink"] span {
        color: inherit !important;
        transition: all 0.3s ease !important;
    }
    
    /* Page Icon Styling & Micro-Animations */
    a[data-testid="stSidebarNavLink"] [data-testid="stSidebarNavLinkIcon"] {
        font-size: 1.15rem !important;
        margin-right: 0.8rem !important;
        transition: transform 0.35s cubic-bezier(0.175, 0.885, 0.32, 1.275), filter 0.3s ease !important;
    }
    
    /* Hover Link State */
    a[data-testid="stSidebarNavLink"]:hover {
        color: #ffffff !important;
        transform: translateX(4px) !important;
    }
    
    a[data-testid="stSidebarNavLink"]:hover [data-testid="stSidebarNavLinkIcon"] {
        transform: scale(1.2) rotate(5deg) !important;
    }
    
    /* Navigation Link - Active / Selected State */
    a[data-testid="stSidebarNavLink"][aria-current="page"] {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.16) 0%, rgba(168, 85, 247, 0.16) 100%) !important;
        border: 1px solid rgba(99, 102, 241, 0.3) !important;
        color: #ffffff !important;
        font-weight: 600 !important;
        box-shadow: 0 4px 20px rgba(99, 102, 241, 0.12), inset 0 0 15px rgba(99, 102, 241, 0.08) !important;
        position: relative !important;
    }
    
    a[data-testid="stSidebarNavLink"][aria-current="page"] span {
        font-weight: 600 !important;
        text-shadow: 0 0 12px rgba(165, 180, 252, 0.4) !important;
    }
    
    a[data-testid="stSidebarNavLink"][aria-current="page"] [data-testid="stSidebarNavLinkIcon"] {
        transform: scale(1.15) !important;
        filter: drop-shadow(0 0 6px rgba(99, 102, 241, 0.6)) !important;
    }
    
    /* Active Link - Left Capsule Accent Indicator */
    a[data-testid="stSidebarNavLink"][aria-current="page"]::before {
        content: "" !important;
        position: absolute !important;
        left: 0 !important;
        top: 25% !important;
        height: 50% !important;
        width: 4px !important;
        background: linear-gradient(to bottom, #6366f1, #a855f7) !important;
        border-radius: 0 4px 4px 0 !important;
    }
    
    /* Style collapsed control button for consistency */
    button[data-testid="collapsedSidebarControl"] {
        background-color: rgba(13, 15, 23, 0.8) !important;
        backdrop-filter: blur(10px) !important;
        border: 1px solid rgba(255, 255, 255, 0.06) !important;
        border-radius: 0 8px 8px 0 !important;
        color: #e2e8f0 !important;
        transition: all 0.2s ease !important;
    }
    
    button[data-testid="collapsedSidebarControl"]:hover {
        color: #6366f1 !important;
        border-color: rgba(99, 102, 241, 0.3) !important;
    }


    
    /* Footer elements */
    .chef-footer {
        text-align: center;
        padding: 2rem 0;
        margin-top: 4rem;
        border-top: 1px solid rgba(255, 255, 255, 0.05);
        color: #64748b;
        font-size: 0.85rem;
    }
    </style>
    """
    st.markdown(css_content, unsafe_allow_html=True)
