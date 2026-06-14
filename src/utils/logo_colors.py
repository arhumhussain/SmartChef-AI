import streamlit as st

def render_premium_logo():
    """Render premium logo with Orange + Teal theme"""
    return """
    <div class="premium-logo" style="text-align: center; padding: 1rem 0;">
        <div class="logo-icon" style="font-size: 3rem; animation: float 3s ease-in-out infinite;">
            🍳
        </div>
        <div class="logo-text">
            <span style="font-size: 2rem; font-weight: 800; color: #FF6B35;">SMART</span>
            <span style="font-size: 2rem; font-weight: 800; color: #2EC4B6;">CHEF</span>
            <span style="font-size: 2rem; font-weight: 800; background: linear-gradient(135deg, #FF6B35, #2EC4B6); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">-AI</span>
        </div>
        <div class="logo-tagline" style="color: #636E72; font-size: 0.8rem; margin-top: 0.5rem;">
            Your Intelligent Kitchen Assistant
        </div>
    </div>
    """