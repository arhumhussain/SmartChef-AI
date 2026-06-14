"""
Mobile Sidebar with Swipe Gestures
Provides responsive sidebar with touch-friendly interactions.
"""
import streamlit as st


def inject_mobile_sidebar_js():
    """
    Injects JavaScript for mobile sidebar with swipe gestures and animations.
    """
    js_code = """
    <script>
    // Mobile sidebar enhancement with swipe support
    (function() {
        let touchStartX = 0;
        let touchEndX = 0;
        let sidebarOpen = false;
        
        // Detect touch events
        document.addEventListener('touchstart', function(e) {
            touchStartX = e.changedTouches[0].screenX;
        }, false);
        
        document.addEventListener('touchend', function(e) {
            touchEndX = e.changedTouches[0].screenX;
            handleSwipe();
        }, false);
        
        function handleSwipe() {
            const swipeDistance = touchEndX - touchStartX;
            const sidebar = document.querySelector('section[data-testid="stSidebar"]');
            
            if (!sidebar) return;
            
            // Swipe right to open (from left edge)
            if (swipeDistance > 50 && touchStartX < 50) {
                sidebar.style.left = '0';
                sidebarOpen = true;
            }
            
            // Swipe left to close
            if (swipeDistance < -50 && sidebarOpen) {
                sidebar.style.left = '-280px';
                sidebarOpen = false;
            }
        }
        
        // Close sidebar when clicking main content on mobile
        document.addEventListener('click', function(e) {
            if (window.innerWidth > 768) return;
            
            const sidebar = document.querySelector('section[data-testid="stSidebar"]');
            const isClickOnSidebar = e.target.closest('section[data-testid="stSidebar"]');
            const isClickOnToggle = e.target.closest('[data-testid="stButton"]');
            
            if (!isClickOnSidebar && !isClickOnToggle && sidebarOpen) {
                sidebar.style.left = '-280px';
                sidebarOpen = false;
            }
        });
        
        // Hamburger menu button
        window.toggleMobileSidebar = function() {
            const sidebar = document.querySelector('section[data-testid="stSidebar"]');
            if (!sidebar) return;
            
            sidebarOpen = !sidebarOpen;
            sidebar.style.left = sidebarOpen ? '0' : '-280px';
        };
    })();
    </script>
    """
    
    st.markdown(js_code, unsafe_allow_html=True)


def render_mobile_menu_button():
    """
    Render a mobile hamburger menu button for small screens.
    """
    button_html = """
    <div style="display: none;" id="mobile-menu-btn">
        <button onclick="toggleMobileSidebar()" style="
            background: none;
            border: none;
            font-size: 1.5rem;
            cursor: pointer;
            padding: 0.5rem;
            color: #e2e8f0;
        ">
            ☰
        </button>
    </div>
    
    <style>
    @media (max-width: 768px) {
        #mobile-menu-btn {
            display: block !important;
            position: fixed;
            top: 1rem;
            left: 1rem;
            z-index: 99;
        }
    }
    </style>
    """
    
    st.markdown(button_html, unsafe_allow_html=True)