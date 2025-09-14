import streamlit as st
import sqlite3
import hashlib
import os
from datetime import datetime
import uuid
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="EchoPrep",
    page_icon="🎤",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Import custom modules
from utils.database import init_database, verify_user, create_user

def main():
    """Main application entry point"""
    
    # Initialize database
    try:
        # Ensure data directory exists
        os.makedirs("./data", exist_ok=True)
        init_database()
    except Exception as e:
        st.error(f"Database initialization error: {e}")
        st.stop()
    
    # Clean, modern CSS styling inspired by the example
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    /* Reset and base styles */
    .stApp {
        background: #f8fafc;
        font-family: 'Inter', sans-serif;
        color: #0f172a;
    }
    
    /* Ensure all inputs have proper text color */
    input[type="text"], input[type="password"], textarea, select {
        color: #1f2937 !important;
        background: #ffffff !important;
    }
    
    /* Hide Streamlit branding and elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* Main container */
    .main-container {
        max-width: 1200px;
        margin: 0 auto;
        padding: 2rem;
        background: #ffffff;
        border-radius: 16px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        margin-top: 2rem;
    }
    
    /* Hero section */
    .hero-section {
        text-align: center;
        padding: 3rem 2rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 16px;
        margin-bottom: 3rem;
        color: white;
    }
    
    .main-title {
        font-size: 3.5rem;
        font-weight: 800;
        margin-bottom: 1rem;
        line-height: 1.1;
        color: white;
    }
    
    .subtitle {
        font-size: 1.25rem;
        opacity: 0.9;
        font-weight: 400;
        line-height: 1.6;
        max-width: 600px;
        margin: 0 auto;
    }
    
    /* Feature cards */
    .features-section {
        margin: 3rem 0;
    }
    
    .section-title {
        font-size: 2rem;
        font-weight: 700;
        color: #1e293b;
        margin-bottom: 2rem;
        text-align: center;
    }
    
    .feature-card {
        background: #ffffff;
        border-radius: 12px;
        padding: 2rem;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        border: 1px solid #e2e8f0;
        transition: all 0.3s ease;
        height: 100%;
        text-align: center;
    }
    
    .feature-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15);
        border-color: #667eea;
    }
    
    .feature-icon {
        font-size: 3rem;
        margin-bottom: 1.5rem;
        display: block;
    }
    
    .feature-title {
        font-size: 1.25rem;
        font-weight: 600;
        color: #1e293b;
        margin-bottom: 1rem;
        line-height: 1.3;
    }
    
    .feature-description {
        color: #64748b;
        line-height: 1.6;
        font-size: 0.95rem;
    }
    
    
    /* Dashboard styles */
    .dashboard-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 16px;
        padding: 2.5rem;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
    }
    
    .dashboard-title {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        color: white;
    }
    
    .welcome-text {
        font-size: 1.1rem;
        opacity: 0.9;
        font-weight: 400;
    }
    
    /* Stats grid */
    .stats-container {
        margin: 2rem 0;
    }
    
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1.5rem;
        margin-top: 1rem;
    }
    
    .stat-card {
        background: #ffffff;
        padding: 2rem;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        border: 1px solid #e2e8f0;
        transition: all 0.3s ease;
    }
    
    .stat-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    }
    
    .stat-number {
        font-size: 2.5rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
    }
    
    .stat-label {
        color: #64748b;
        font-size: 0.9rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    /* Interview cards */
    .interview-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
    }
    
    .interview-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        border-color: #667eea;
    }
    
    .interview-title {
        font-size: 1.125rem;
        font-weight: 600;
        color: #1e293b;
        margin-bottom: 0.75rem;
    }
    
    .interview-detail {
        color: #64748b;
        font-size: 0.875rem;
        margin-bottom: 0.25rem;
    }
    
    .interview-status {
        font-weight: 500;
        font-size: 0.875rem;
        margin: 0.75rem 0;
    }
    
    .interview-date {
        color: #94a3b8;
        font-size: 0.75rem;
    }
    
    /* Form inputs */
    .stTextInput > div > div > input {
        border-radius: 8px !important;
        border: 1px solid #d1d5db !important;
        padding: 0.875rem 1rem !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
        background: #ffffff !important;
        color: #1f2937 !important;
        font-family: 'Inter', sans-serif !important;
        box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05) !important;
        outline: none !important;
        height: auto !important;
        line-height: 1.5 !important;
        -webkit-text-fill-color: #1f2937 !important;
        -webkit-background-clip: text !important;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: #9ca3af !important;
        opacity: 1 !important;
        -webkit-text-fill-color: #9ca3af !important;
    }
    
    .stTextInput > div > div > input:hover {
        border-color: #9ca3af !important;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1) !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #3b82f6 !important;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1) !important;
        outline: none !important;
        color: #1f2937 !important;
        -webkit-text-fill-color: #1f2937 !important;
    }
    
    /* Force text visibility on all input types */
    .stTextInput input,
    .stTextInput input[type="text"],
    .stTextInput input[type="password"] {
        color: #1f2937 !important;
        background-color: #ffffff !important;
        -webkit-text-fill-color: #1f2937 !important;
        opacity: 1 !important;
    }
    
    /* Override Streamlit's default input container styling */
    div[data-testid="stTextInputRootElement"] {
        background: transparent !important;
    }
    
    div[data-testid="stTextInputRootElement"] > div {
        background: #ffffff !important;
        border-radius: 8px !important;
    }
    
    div[data-testid="stTextInputRootElement"] > div > div {
        background: #ffffff !important;
    }
    
    /* Target all Streamlit input classes specifically */
    .st-ay.st-ag.st-ce input,
    .st-d2.st-b5.st-b7 input,
    input.st-ay.st-d2 {
        color: #1f2937 !important;
        background: #ffffff !important;
        border: 1px solid #d1d5db !important;
        border-radius: 8px !important;
        padding: 0.875rem 1rem !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 1rem !important;
        -webkit-text-fill-color: #1f2937 !important;
    }
    
    /* Override specific Streamlit color classes */
    .st-cz {
        background-color: #ffffff !important;
    }
    
    .st-cv, .st-cw, .st-cx, .st-cy {
        border-color: #d1d5db !important;
    }
    
    /* Force white background on input containers */
    .st-ag.st-cf.st-d1.st-bg.st-cp.st-bp.st-cu.st-br.st-bs.st-bt.st-bu.st-c1.st-cz {
        background-color: #ffffff !important;
    }
    
    /* Ultra-specific override for the exact classes in the DOM */
    input.st-ay.st-d2.st-b5.st-b7.st-b6.st-b8.st-b9.st-bb.st-ba.st-bc.st-bi.st-cf.st-d3.st-d4.st-d5.st-d6.st-d7.st-d8.st-d9.st-da.st-bp.st-cu.st-db.st-dc.st-bt.st-bu.st-c1.st-dd.st-de {
        color: #1f2937 !important;
        background: #ffffff !important;
        -webkit-text-fill-color: #1f2937 !important;
        border: 1px solid #d1d5db !important;
    }
    
    /* Maximum specificity override - this should work */
    div[data-testid="stTextInputRootElement"] div[data-baseweb="base-input"] input {
        background-color: #ffffff !important;
        color: #1f2937 !important;
        border: 1px solid #d1d5db !important;
        border-radius: 8px !important;
        padding: 0.875rem 1rem !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 1rem !important;
        -webkit-text-fill-color: #1f2937 !important;
        -webkit-background-clip: border-box !important;
    }
    
    /* Force override with highest specificity */
    body div[data-testid="stTextInputRootElement"] div[data-baseweb="base-input"] input[type="text"],
    body div[data-testid="stTextInputRootElement"] div[data-baseweb="base-input"] input[type="password"] {
        background: white !important;
        color: black !important;
        -webkit-text-fill-color: black !important;
        border: 2px solid #3b82f6 !important;
        border-radius: 8px !important;
        padding: 12px 16px !important;
        font-size: 16px !important;
        font-family: 'Inter', sans-serif !important;
    }
    
    /* Password visibility toggle button (eye icon) */
    div[data-testid="stTextInputRootElement"] button[aria-label*="password"],
    div[data-testid="stTextInputRootElement"] button[title*="password"] {
        background: transparent !important;
        border: none !important;
        color: #6b7280 !important;
        padding: 8px !important;
        margin: 0 !important;
        cursor: pointer !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        border-radius: 4px !important;
        transition: all 0.2s ease !important;
        position: absolute !important;
        right: 8px !important;
        top: 50% !important;
        transform: translateY(-50%) !important;
        z-index: 10 !important;
        width: 32px !important;
        height: 32px !important;
    }
    
    div[data-testid="stTextInputRootElement"] button[aria-label*="password"]:hover,
    div[data-testid="stTextInputRootElement"] button[title*="password"]:hover {
        background: #f3f4f6 !important;
        color: #374151 !important;
    }
    
    /* Eye icon SVG styling */
    div[data-testid="stTextInputRootElement"] button svg {
        width: 16px !important;
        height: 16px !important;
        fill: currentColor !important;
        opacity: 1 !important;
        display: block !important;
    }
    
    /* Ensure password input container has relative positioning */
    div[data-testid="stTextInputRootElement"] div[data-baseweb="base-input"] {
        position: relative !important;
        background: white !important;
        border-radius: 8px !important;
        border: 2px solid #3b82f6 !important;
    }
    
    /* Adjust password input padding to make room for the button */
    div[data-testid="stTextInputRootElement"] input[type="password"] {
        padding-right: 45px !important;
    }
    
    /* Additional targeting for button visibility */
    button[data-baseweb="button"],
    button.st-ag.st-b0.st-ba.st-bc.st-b9.st-bb {
        opacity: 1 !important;
        visibility: visible !important;
        display: flex !important;
        background: transparent !important;
        border: none !important;
        color: #6b7280 !important;
        cursor: pointer !important;
    }
    
    /* Input container styling */
    .stTextInput > div {
        background: transparent !important;
    }
    
    .stTextInput > div > div {
        background: #ffffff !important;
        border-radius: 8px !important;
    }
    
    /* Password input specific styling */
    .stTextInput > div > div > input[type="password"] {
        color: #1f2937 !important;
        background: #ffffff !important;
        font-family: 'Inter', sans-serif !important;
    }
    
    /* Input labels */
    .stTextInput > label {
        color: #374151 !important;
        font-weight: 500 !important;
        font-size: 0.875rem !important;
        margin-bottom: 0.5rem !important;
        font-family: 'Inter', sans-serif !important;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.75rem 1.5rem !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
        width: 100% !important;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1) !important;
        font-family: 'Inter', sans-serif !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3) !important;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
        background: #f1f5f9;
        padding: 0.5rem;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        display: flex;
        justify-content: center;
        align-items: center;
        max-width: 400px;
        margin: 0 auto 2rem auto;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent !important;
        border-radius: 8px !important;
        color: #64748b !important;
        font-weight: 500 !important;
        padding: 1rem 2rem !important;
        font-family: 'Inter', sans-serif !important;
        border: none !important;
        transition: all 0.3s ease !important;
        flex: 1 !important;
        text-align: center !important;
        font-size: 0.95rem !important;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(255, 255, 255, 0.5) !important;
        color: #3b82f6 !important;
    }
    
    .stTabs [aria-selected="true"] {
        background: #ffffff !important;
        color: #3b82f6 !important;
        box-shadow: 0 2px 8px rgba(59, 130, 246, 0.15) !important;
        font-weight: 600 !important;
    }
    
    /* Section headers */
    .section-header {
        font-size: 1.5rem;
        font-weight: 600;
        color: #1e293b;
        margin: 2rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #e2e8f0;
    }
    
    /* Empty state */
    .empty-state {
        text-align: center;
        padding: 3rem 2rem;
        background: #f8fafc;
        border-radius: 12px;
        border: 2px dashed #cbd5e1;
    }
    
    .empty-state-icon {
        font-size: 4rem;
        margin-bottom: 1rem;
        opacity: 0.6;
    }
    
    .empty-state-title {
        font-size: 1.25rem;
        font-weight: 600;
        color: #1e293b;
        margin-bottom: 0.5rem;
    }
    
    .empty-state-description {
        color: #64748b;
        font-size: 1rem;
    }
    
    /* Auth section */
    .auth-container {
        max-width: 600px;
        margin: 0 auto;
        padding: 0 1rem;
    }
    
    .auth-section {
        max-width: 400px;
        margin: 2rem auto;
        padding: 2rem;
        background: #ffffff;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        border: 1px solid #e2e8f0;
    }
    
    .auth-title {
        font-size: 1.75rem;
        font-weight: 700;
        color: #1e293b;
        text-align: center;
        margin-bottom: 1.5rem;
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 6px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f5f9;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #cbd5e1;
        border-radius: 6px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #94a3b8;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Check if user is authenticated
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    
    if not st.session_state.authenticated:
        show_login_page()
    else:
        show_dashboard()

def show_login_page():
    """Display modern login/registration page"""
    
    # Hero section with clean design
    st.markdown("""
    <div class="hero-section">
        <h1 class="main-title">🎤 EchoPrep</h1>
        <p class="subtitle">AI-powered mock interview coach that helps you practice with confidence</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Feature cards using pure Streamlit
    st.markdown('<div class="section-header">✨ Key Features</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🎯</div>
            <h3 class="feature-title">Personalized Interviews</h3>
            <p style="font-family: 'Inter', sans-serif; color: #6b7280; line-height: 1.6; margin: 0; font-size: 0.95rem;">Create tailored mock interviews based on your role and experience level with AI-powered question generation.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🎙️</div>
            <h3 class="feature-title">Voice Interaction</h3>
            <p style="font-family: 'Inter', sans-serif; color: #6b7280; line-height: 1.6; margin: 0; font-size: 0.95rem;">Practice with real-time speech-to-text and text-to-speech for an authentic interview experience.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📊</div>
            <h3 class="feature-title">AI Feedback</h3>
            <p style="font-family: 'Inter', sans-serif; color: #6b7280; line-height: 1.6; margin: 0; font-size: 0.95rem;">Get detailed performance analysis and constructive feedback to improve your interview skills.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Authentication section
    st.markdown('<div style="margin: 48px 0 32px 0;"><hr style="border: none; height: 1px; background: #e5e7eb; margin: 0;"></div>', unsafe_allow_html=True)
    
    # Create centered container for tabs
    st.markdown('<div class="auth-container">', unsafe_allow_html=True)
    tab1, tab2 = st.tabs(["🔑 Sign In", "👤 Create Account"])
    st.markdown('</div>', unsafe_allow_html=True)
    
    with tab1:
        st.markdown('<h2 style="font-family: \'Inter\', sans-serif; color: #1a1a1a; text-align: center; margin: 24px 0; font-weight: 600;">Welcome Back</h2>', unsafe_allow_html=True)
        
        # Center the login form
        login_col1, login_col2, login_col3 = st.columns([1, 2, 1])
        
        with login_col2:
            username = st.text_input("Username", key="login_username", placeholder="Enter your username")
            password = st.text_input("Password", type="password", key="login_password", placeholder="Enter your password")
            
            if st.button("Sign In", type="primary", use_container_width=True):
                if username and password:
                    user_id = verify_user(username, password)
                    if user_id:
                        st.session_state.authenticated = True
                        st.session_state.user_id = user_id
                        st.session_state.username = username
                        st.success("✅ Welcome back! Redirecting...")
                        st.rerun()
                    else:
                        st.error("❌ Invalid credentials. Please try again.")
                else:
                    st.error("⚠️ Please fill in all fields")
    
    with tab2:
        st.markdown('<h2 style="font-family: \'Inter\', sans-serif; color: #1a1a1a; text-align: center; margin: 24px 0; font-weight: 600;">Create Your Account</h2>', unsafe_allow_html=True)
        
        # Center the registration form
        reg_col1, reg_col2, reg_col3 = st.columns([1, 2, 1])
        
        with reg_col2:
            new_username = st.text_input("Username", key="reg_username", placeholder="Choose a username")
            new_password = st.text_input("Password", type="password", key="reg_password", placeholder="Create a password")
            confirm_password = st.text_input("Confirm Password", type="password", key="reg_confirm", placeholder="Confirm your password")
            
            if st.button("Create Account", type="primary", use_container_width=True):
                if new_username and new_password and confirm_password:
                    if new_password == confirm_password:
                        if len(new_password) >= 6:
                            if create_user(new_username, new_password):
                                st.success("🎉 Account created successfully! Please sign in with your credentials.")
                                st.balloons()
                            else:
                                st.error("❌ Username already exists. Please choose a different username.")
                        else:
                            st.error("⚠️ Password must be at least 6 characters long")
                    else:
                        st.error("❌ Passwords do not match")
                else:
                    st.error("⚠️ Please fill in all fields")

def show_dashboard():
    """Display modern user dashboard"""
    
    # Header section
    st.markdown("""
    <div class="dashboard-header">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <h1 class="dashboard-title">Welcome back, {username}! 👋</h1>
                <p class="welcome-text">Ready to practice and improve your interview skills?</p>
            </div>
        </div>
    </div>
    """.format(username=st.session_state.username), unsafe_allow_html=True)
    
    # Quick stats
    from utils.database import get_user_stats
    stats = get_user_stats(st.session_state.user_id)
    
    st.markdown("""
        <div class="stats-grid">
            <div class="stat-card">
                <h3 style="color: #3b82f6; font-size: 2rem; margin: 0; font-family: 'Inter', sans-serif; font-weight: 700;">{total}</h3>
                <p style="color: #6b7280; margin: 8px 0 0 0; font-family: 'Inter', sans-serif; font-size: 0.875rem; font-weight: 500;">Total Interviews</p>
            </div>
            <div class="stat-card">
                <h3 style="color: #10b981; font-size: 2rem; margin: 0; font-family: 'Inter', sans-serif; font-weight: 700;">{completed}</h3>
                <p style="color: #6b7280; margin: 8px 0 0 0; font-family: 'Inter', sans-serif; font-size: 0.875rem; font-weight: 500;">Completed</p>
            </div>
            <div class="stat-card">
                <h3 style="color: #f59e0b; font-size: 2rem; margin: 0; font-family: 'Inter', sans-serif; font-weight: 700;">{rate}%</h3>
                <p style="color: #6b7280; margin: 8px 0 0 0; font-family: 'Inter', sans-serif; font-size: 0.875rem; font-weight: 500;">Success Rate</p>
            </div>
        </div>
    """.format(
        total=stats['total'],
        completed=stats['completed'],
        rate=f"{stats['success_rate']:.1f}"
    ), unsafe_allow_html=True)
    
    # Main content area
    col1, col2 = st.columns([2.5, 1.5])
    
    with col1:
        st.markdown('<div class="section-header">📚 Your Interview History</div>', unsafe_allow_html=True)
        
        # Get user's interview mocks from database
        from utils.database import get_user_interviews
        interviews = get_user_interviews(st.session_state.user_id)
        
        if interviews:
            for interview in interviews:
                status_color = "#10b981" if interview['completed'] else "#f59e0b"
                status_text = "✅ Completed" if interview['completed'] else "⏳ In Progress"
                
                st.markdown(f"""
                <div class="interview-card">
                    <div style="display: flex; justify-content: space-between; align-items: start;">
                        <div style="flex-grow: 1;">
                            <h3 style="color: #1a1a1a; margin: 0 0 12px 0; font-size: 1.125rem; font-family: 'Inter', sans-serif; font-weight: 600; line-height: 1.3;">
                                🎯 {interview.get('job_role', 'Unknown Role')} - {interview.get('experience_level', 'Unknown Level')}
                            </h3>
                            <p style="color: #6b7280; margin: 4px 0; font-family: 'Inter', sans-serif; font-size: 0.875rem;"><span style="font-weight: 500;">Type:</span> {interview.get('interview_type', 'Unknown Type')}</p>
                            <p style="color: #6b7280; margin: 4px 0; font-family: 'Inter', sans-serif; font-size: 0.875rem;"><span style="font-weight: 500;">Skills:</span> {interview.get('skills', 'N/A')}</p>
                            <p style="color: {status_color}; margin: 12px 0 8px 0; font-weight: 500; font-family: 'Inter', sans-serif; font-size: 0.875rem;">{status_text}</p>
                            <p style="color: #9ca3af; margin: 0; font-size: 0.75rem; font-family: 'Inter', sans-serif;">Created: {interview.get('created_at', 'Unknown Date')}</p>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Action buttons
                col_a, col_b, col_c, col_d = st.columns([1, 1, 1, 2])
                
                with col_a:
                    if not interview.get('completed', False):
                        if st.button("▶️ Start", key=f"start_{interview.get('id', '')}", help="Start Interview"):
                            st.session_state.current_interview_id = interview.get('id')
                            st.switch_page("pages/interview.py")
                
                with col_b:
                    if interview.get('completed', False):
                        if st.button("📊 Report", key=f"report_{interview.get('id', '')}", help="View Report"):
                            st.session_state.current_interview_id = interview.get('id')
                            st.switch_page("pages/report.py")
                
                st.markdown("<div style='margin: 16px 0;'></div>", unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="text-align: center; padding: 48px 24px; background: #f9fafb; border-radius: 12px; border: 1px solid #e5e7eb;">
                <div style="font-size: 3rem; margin-bottom: 16px;">🎯</div>
                <h3 style="font-family: 'Inter', sans-serif; color: #1a1a1a; font-weight: 600; margin-bottom: 8px;">Ready to start your interview journey?</h3>
                <p style="font-family: 'Inter', sans-serif; color: #6b7280; margin: 0;">Create your first mock interview and begin practicing!</p>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="section-header">🚀 Quick Actions</div>', unsafe_allow_html=True)
        
        if st.button("🆕 Create New Interview", type="primary", use_container_width=True):
            st.switch_page("pages/setup.py")
        
        st.markdown("<div style='margin: 16px 0;'></div>", unsafe_allow_html=True)
        
        if st.button("🔄 Refresh Dashboard", use_container_width=True):
            st.rerun()
        
        st.markdown("<div style='margin: 16px 0;'></div>", unsafe_allow_html=True)
        
        if st.button("🚪 Sign Out", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
