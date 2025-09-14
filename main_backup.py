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
    init_database()
    
    # Modern CSS styling
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Source+Sans+Pro:wght@400;600;700&display=swap');
    
    .stApp {
        background: linear-gradient(135deg, #273F4F 0%, #FE7743 100%);
        font-family: 'Inter', sans-serif;
    }
    
    .main-container {
        background: rgba(239, 238, 234, 0.95);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 40px;
        margin: 20px;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
    }
    
    .hero-section {
        text-align: center;
        margin-bottom: 50px;
    }
    
    .main-title {
        font-family: 'Inter', sans-serif;
        font-size: 3.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #273F4F, #FE7743);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 10px;
    }
    
    .subtitle {
        font-family: 'Source Sans Pro', sans-serif;
        font-size: 1.3rem;
        color: #273F4F;
        font-weight: 400;
        margin-bottom: 40px;
    }
    
    .feature-card {
        background: #EFEEEA;
        border-radius: 15px;
        padding: 30px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(254, 119, 67, 0.2);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
    }
    
    .feature-icon {
        font-size: 3rem;
        display: block;
        margin-bottom: 20px;
    }
    
    .feature-title {
        font-family: 'Inter', sans-serif;
        color: #000000;
        font-size: 1.5rem;
        margin-bottom: 15px;
        font-weight: 600;
    }
    
    .dashboard-header {
        margin: 40px 0;
        text-align: center;
    }
    
    .dashboard-title {
        font-family: 'Inter', sans-serif;
        color: #273F4F;
        font-size: 2.5rem;
        font-weight: 800;
        margin: 0;
        background: linear-gradient(135deg, #273F4F, #FE7743);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .welcome-text {
        font-family: 'Source Sans Pro', sans-serif;
        color: #273F4F;
        font-size: 1.2rem;
        margin: 10px 0 0 0;
    }
    
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 20px;
        margin: 40px 0;
    }
    
    .stat-card {
        background: #EFEEEA;
        padding: 30px;
        border-radius: 20px;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.08);
        border: 1px solid #FE7743;
        transition: all 0.3s ease;
    }
    
    .stat-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 40px rgba(254,119,67,0.15);
    }
    
    .interview-card {
        background: #EFEEEA;
        border: 1px solid #FE7743;
        border-radius: 20px;
        padding: 30px;
        margin: 20px 0;
        box-shadow: 0 10px 30px rgba(0,0,0,0.08);
        transition: all 0.3s ease;
    }
    
    .interview-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 15px 35px rgba(0,0,0,0.12);
    }
    
    
    .stTextInput > div > div > input {
        border-radius: 10px !important;
        border: 2px solid #FE7743 !important;
        padding: 12px 16px !important;
        font-size: 1rem !important;
        font-family: 'Source Sans Pro', sans-serif !important;
        transition: border-color 0.3s ease !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #273F4F !important;
        box-shadow: 0 0 0 3px rgba(39, 63, 79, 0.1) !important;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #273F4F, #FE7743) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 12px 24px !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        font-family: 'Inter', sans-serif !important;
        transition: all 0.3s ease !important;
        width: 100% !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 10px 25px rgba(254, 119, 67, 0.3) !important;
    }
    
    .dashboard-header {
        background: #EFEEEA;
        border-radius: 15px;
        padding: 30px;
        margin-bottom: 30px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(254, 119, 67, 0.2);
    }
    
    .dashboard-title {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 10px;
    }
    
    .welcome-text {
        color: #6c757d;
        font-size: 1.2rem;
    }
    
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
        gap: 20px;
        margin-top: 20px;
    }
    
    .stat-card {
        background: white;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(102, 126, 234, 0.1);
    }
    
    .interview-card {
        background: white;
        border-radius: 15px;
        padding: 25px;
        margin-bottom: 20px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(102, 126, 234, 0.1);
        transition: transform 0.3s ease;
    }
    
    .interview-card:hover {
        transform: translateY(-3px);
    }
    
    .action-button {
        background: linear-gradient(135deg, #667eea, #764ba2) !important;
        border: none !important;
        border-radius: 10px !important;
        color: white !important;
        font-weight: 600 !important;
        padding: 12px 24px !important;
        transition: all 0.3s ease !important;
    }
    
    .secondary-button {
        background: white !important;
        border: 2px solid #667eea !important;
        color: #667eea !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        padding: 12px 24px !important;
        transition: all 0.3s ease !important;
    }
    
    .secondary-button:hover {
        background: #667eea !important;
        color: white !important;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #647FBC, #91ADC8);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #647FBC;
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
    
    # Hero section
    st.markdown("""
    <div style="text-align: center; padding: 40px; background: rgba(250, 253, 214, 0.95); border-radius: 20px; margin: 20px;">
        <h1 style="font-family: 'Inter', sans-serif; font-size: 3.5rem; background: linear-gradient(135deg, #273F4F, #FE7743); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 10px;">🎤 EchoPrep</h1>
        <p style="font-family: 'Source Sans Pro', sans-serif; font-size: 1.3rem; color: #273F4F; margin-bottom: 40px;">Voice-Driven Mock Interview Coach</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Feature cards using pure Streamlit
    st.markdown("### ✨ Key Features")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="background: #AED6CF; padding: 30px; border-radius: 15px; text-align: center; margin: 10px 0;">
            <div style="font-size: 3rem; margin-bottom: 20px;">🎯</div>
            <h3 style="font-family: 'Inter', sans-serif; color: #000000; margin-bottom: 15px;">Personalized Interviews</h3>
            <p style="font-family: 'Source Sans Pro', sans-serif; color: #273F4F; line-height: 1.6;">AI-powered conversational setup to create tailored mock interviews based on your role and experience level.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: #AED6CF; padding: 30px; border-radius: 15px; text-align: center; margin: 10px 0;">
            <div style="font-size: 3rem; margin-bottom: 20px;">🎙️</div>
            <h3 style="font-family: 'Inter', sans-serif; color: #000000; margin-bottom: 15px;">Voice Interaction</h3>
            <p style="font-family: 'Source Sans Pro', sans-serif; color: #273F4F; line-height: 1.6;">Real-time speech-to-text and text-to-speech for an authentic interview experience.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="background: #AED6CF; padding: 30px; border-radius: 15px; text-align: center; margin: 10px 0;">
            <div style="font-size: 3rem; margin-bottom: 20px;">📊</div>
            <h3 style="font-family: 'Inter', sans-serif; color: #000000; margin-bottom: 15px;">AI Feedback</h3>
            <p style="font-family: 'Source Sans Pro', sans-serif; color: #273F4F; line-height: 1.6;">Detailed performance analysis and constructive feedback to improve your interview skills.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Authentication section
    st.markdown("---")
    tab1, tab2 = st.tabs(["🔑 Login", "👤 Register"])
    
    with tab1:
        st.markdown('<h2 style="font-family: \'Inter\', sans-serif; color: #273F4F; text-align: center; margin: 20px 0;">Welcome Back</h2>', unsafe_allow_html=True)
        
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
                        st.success("Welcome back! Redirecting to dashboard...")
                        st.rerun()
                    else:
                        st.error("Invalid credentials. Please try again.")
                else:
                    st.error("Please fill in all fields")
    
    with tab2:
        st.markdown('<h2 style="font-family: \'Inter\', sans-serif; color: #273F4F; text-align: center; margin: 20px 0;">Create Account</h2>', unsafe_allow_html=True)
        
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
                                st.success("Account created successfully! Please login with your credentials.")
                                st.balloons()
                            else:
                                st.error("Username already exists. Please choose a different username.")
                        else:
                            st.error("Password must be at least 6 characters long")
                    else:
                        st.error("Passwords do not match")
                else:
                    st.error("Please fill in all fields")

def show_dashboard():
    """Display modern aesthetic dashboard inspired by clean portfolio designs"""
    
    # Custom CSS for modern aesthetic design
    st.markdown("""
    <style>
    .dashboard-main {
        background: linear-gradient(135deg, #EFEEEA 0%, #FAFAFA 100%);
        min-height: 100vh;
        padding: 0;
        margin: 0;
    }
    
    .hero-section {
        background: linear-gradient(135deg, #273F4F 0%, #FE7743 100%);
        padding: 80px 40px;
        margin: -20px -20px 40px -20px;
        text-align: center;
        position: relative;
        overflow: hidden;
        border-radius: 0 0 30px 30px;
    }
    
    .hero-section::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: url('data:image/svg+xml,<svg width="60" height="60" viewBox="0 0 60 60" xmlns="http://www.w3.org/2000/svg"><g fill="none" fill-rule="evenodd"><g fill="%23ffffff" fill-opacity="0.05"><circle cx="30" cy="30" r="1"/></g></svg>');
        opacity: 0.3;
    }
    
    .hero-content {
        position: relative;
        z-index: 2;
    }
    
    .modern-dashboard-title {
        font-family: 'Inter', sans-serif;
        font-size: 3.5rem;
        font-weight: 700;
        color: white;
        margin-bottom: 20px;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
        line-height: 1.2;
    }
    
    .dashboard-subtitle {
        font-family: 'Source Sans Pro', sans-serif;
        font-size: 1.4rem;
        color: rgba(255,255,255,0.9);
        margin-bottom: 0;
        font-weight: 300;
    }
    
    .content-container {
        max-width: 1200px;
        margin: 0 auto;
        padding: 0 20px;
    }
    
    .section-title {
        font-family: 'Inter', sans-serif;
        font-size: 2rem;
        font-weight: 600;
        color: #273F4F;
        margin-bottom: 30px;
        text-align: center;
    }
    
    .modern-stats-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 30px;
        margin: 40px 0 60px 0;
    }
    
    .modern-stat-card {
        background: white;
        border-radius: 20px;
        padding: 40px 30px;
        text-align: center;
        box-shadow: 0 8px 32px rgba(0,0,0,0.08);
        border: 1px solid rgba(254,119,67,0.1);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .modern-stat-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #FE7743, #273F4F);
    }
    
    .modern-stat-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 20px 40px rgba(0,0,0,0.12);
    }
    
    .stat-number {
        font-family: 'Inter', sans-serif;
        font-size: 2.5rem;
        font-weight: 700;
        color: #273F4F;
        margin-bottom: 10px;
        display: block;
    }
    
    .stat-label {
        font-family: 'Source Sans Pro', sans-serif;
        font-size: 1rem;
        color: #666;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .modern-interviews-section {
        background: white;
        border-radius: 24px;
        padding: 40px;
        margin: 40px 0;
        box-shadow: 0 8px 32px rgba(0,0,0,0.06);
        border: 1px solid rgba(254,119,67,0.1);
    }
    
    .modern-interview-card {
        background: #FAFAFA;
        border-radius: 16px;
        padding: 30px;
        margin: 20px 0;
        border-left: 4px solid #FE7743;
        transition: all 0.3s ease;
        position: relative;
    }
    
    .modern-interview-card:hover {
        transform: translateX(8px);
        box-shadow: 0 8px 24px rgba(254,119,67,0.15);
    }
    
    .interview-title {
        font-family: 'Inter', sans-serif;
        font-size: 1.4rem;
        font-weight: 600;
        color: #273F4F;
        margin-bottom: 12px;
    }
    
    .interview-meta {
        font-family: 'Source Sans Pro', sans-serif;
        font-size: 0.95rem;
        color: #666;
        margin: 8px 0;
    }
    
    .interview-status {
        display: inline-block;
        padding: 6px 16px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        margin-top: 12px;
    }
    
    .status-completed {
        background: rgba(34, 197, 94, 0.1);
        color: #059669;
    }
    
    .status-pending {
        background: rgba(245, 158, 11, 0.1);
        color: #D97706;
    }
    
    .cta-section {
        text-align: center;
        padding: 60px 40px;
        background: linear-gradient(135deg, rgba(254,119,67,0.05), rgba(39,63,79,0.05));
        border-radius: 24px;
        margin: 40px 0;
    }
    
    .cta-title {
        font-family: 'Inter', sans-serif;
        font-size: 2.2rem;
        font-weight: 600;
        color: #273F4F;
        margin-bottom: 16px;
    }
    
    .cta-description {
        font-family: 'Source Sans Pro', sans-serif;
        font-size: 1.1rem;
        color: #666;
        margin-bottom: 30px;
        max-width: 600px;
        margin-left: auto;
        margin-right: auto;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Hero Section
    st.markdown("""
    <div class="hero-section">
        <div class="hero-content">
            <h1 class="modern-dashboard-title">Welcome Back!</h1>
            <p class="dashboard-subtitle">Ready to ace your next interview, {}?</p>
        </div>
    </div>
    """.format(st.session_state.username), unsafe_allow_html=True)
    
    # Main content container
    st.markdown('<div class="content-container">', unsafe_allow_html=True)
    
    # Quick stats with modern design
    from utils.database import get_user_stats
    stats = get_user_stats(st.session_state.user_id)
    
    st.markdown('<h2 class="section-title">Your Progress</h2>', unsafe_allow_html=True)
    
    st.markdown("""
        <div class="modern-stats-grid">
            <div class="modern-stat-card">
                <span class="stat-number">{total}</span>
                <span class="stat-label">Total Interviews</span>
            </div>
            <div class="modern-stat-card">
                <span class="stat-number">{completed}</span>
                <span class="stat-label">Completed</span>
            </div>
            <div class="modern-stat-card">
                <span class="stat-number">{rate}%</span>
                <span class="stat-label">Success Rate</span>
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
        st.markdown('<h2 style="color: #647FBC; margin: 30px 0 20px 0; font-family: \'Playfair Display\', serif;">📚 Your Interview History</h2>', unsafe_allow_html=True)
        
        # Get user's interview mocks from database
        from utils.database import get_user_interviews
        interviews = get_user_interviews(st.session_state.user_id)
        
        if interviews:
            for interview in interviews:
                status_color = "#FE7743" if interview['completed'] else "#273F4F"
                status_text = "✅ Completed" if interview['completed'] else "⏳ In Progress"
                
                st.markdown(f"""
                <div class="interview-card">
                    <div style="display: flex; justify-content: space-between; align-items: start;">
                        <div style="flex-grow: 1;">
                            <h3 style="color: #647FBC; margin: 0 0 10px 0; font-size: 1.3rem; font-family: 'Playfair Display', serif;">
                                🎯 {interview['job_role']} - {interview['experience_level']}
                            </h3>
                            <p style="color: #273F4F; margin: 5px 0; font-family: 'Source Sans Pro', sans-serif;"><strong>Type:</strong> {interview['interview_type']}</p>
                            <p style="color: #273F4F; margin: 5px 0; font-family: 'Source Sans Pro', sans-serif;"><strong>Skills:</strong> {interview['skills']}</p>
    # Interviews Section with modern design
    st.markdown("""
    <div class="modern-interviews-section">
        <h2 class="section-title">Your Interview Journey</h2>
    """, unsafe_allow_html=True)
    
    # Get user's interview mocks from database
    from utils.database import get_user_interviews
    interviews = get_user_interviews(st.session_state.user_id)
    
    if interviews:
        for interview in interviews:
            status_class = "status-completed" if interview['completed'] else "status-pending"
            status_text = "Completed" if interview['completed'] else "In Progress"
            
            st.markdown(f"""
            <div class="modern-interview-card">
                <div class="interview-title">Interview: {interview['job_role']} - {interview['experience_level']}</div>
                <div class="interview-meta"><strong>Type:</strong> {interview['interview_type']}</div>
                <div class="interview-meta"><strong>Skills:</strong> {interview['skills']}</div>
                <div class="interview-meta"><strong>Created:</strong> {interview['created_at']}</div>
                <span class="interview-status {status_class}">{status_text}</span>
            </div>
            """, unsafe_allow_html=True)
            
            # Action buttons
            col1, col2, col3 = st.columns([1, 1, 2])
            
            with col1:
                if not interview['completed']:
                    if st.button("Start", key=f"start_{interview['id']}", help="Start Interview"):
                        st.session_state.current_interview_id = interview['id']
                        st.switch_page("pages/interview.py")
            
            with col2:
                if interview['completed']:
                    if st.button("Report", key=f"report_{interview['id']}", help="View Report"):
                        st.session_state.current_interview_id = interview['id']
                        st.switch_page("pages/report.py")
    
    else:
        st.markdown("""
        <div class="cta-section">
            <h3 class="cta-title">Ready to start your interview journey?</h3>
            <p class="cta-description">Create your first mock interview and begin practicing with our AI-powered coach!</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)  # Close interviews section
    
    # Quick Actions Section
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Create New Interview", type="primary", use_container_width=True):
            st.switch_page("pages/setup.py")
    
    with col2:
        if st.button("Refresh Dashboard", use_container_width=True):
            st.rerun()
    
    with col3:
        if st.button("Logout", use_container_width=True):
            st.session_state.authenticated = False
            st.session_state.user_id = None
            st.session_state.username = None
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)  # Close content container

if __name__ == "__main__":
    main()
