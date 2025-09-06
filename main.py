import stre# Page configuration
st.set_page_config(
    page_title="EchoPrep",
      st.markdown('<div class="main-header">🎤 EchoPrep</div>', unsafe_allow_html=True)
        with col1:
        st.markdown('<div class="main-header">🎤 EchoPrep Dashboard</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="sub-header">Welcome back, {st.session_state.username}!</div>', unsafe_allow_html=True)markdown('<div class="sub-header">Voice-Driven Mock Interview Coach</div>', unsafe_allow_html=True)page_icon="🎤",
    layout="wide",
    initial_sidebar_state="collapsed"
)s st
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
    page_title="EchoPrep AI",
    page_icon="🎤",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Import custom modules
from utils.database import init_database, verify_user, create_user
from utils.auth import check_authentication_status

def main():
    """Main application entry point"""
    
    # Initialize database
    init_database()
    
    # Custom CSS for better styling
    st.markdown("""
    <style>
    .main-header {
        text-align: center;
        color: #1f77b4;
        font-size: 3rem;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    
    .sub-header {
        text-align: center;
        color: #666;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    
    .feature-box {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
        border-left: 5px solid #1f77b4;
    }
    
    .login-container {
        max-width: 400px;
        margin: 0 auto;
        padding: 20px;
        background-color: #f9f9f9;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
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
    """Display login/registration page"""
    
    st.markdown('<div class="main-header">🎤 EchoPrep AI</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Voice-Driven Mock Interview Coach</div>', unsafe_allow_html=True)
    
    # Features overview
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-box">
            <h3>🎯 Personalized Interviews</h3>
            <p>AI-powered conversational setup to create tailored mock interviews based on your role and experience.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-box">
            <h3>🎙️ Voice Interaction</h3>
            <p>Real-time speech-to-text and text-to-speech for authentic interview experience.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-box">
            <h3>📊 AI Feedback</h3>
            <p>Detailed performance analysis and constructive feedback to improve your interview skills.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Login/Register forms
    st.markdown("---")
    
    tab1, tab2 = st.tabs(["Login", "Register"])
    
    with tab1:
        with st.container():
            st.markdown('<div class="login-container">', unsafe_allow_html=True)
            st.subheader("Login to Your Account")
            
            username = st.text_input("Username", key="login_username")
            password = st.text_input("Password", type="password", key="login_password")
            
            if st.button("Login", type="primary", use_container_width=True):
                if username and password:
                    user_id = verify_user(username, password)
                    if user_id:
                        st.session_state.authenticated = True
                        st.session_state.user_id = user_id
                        st.session_state.username = username
                        st.success("Login successful!")
                        st.rerun()
                    else:
                        st.error("Invalid username or password")
                else:
                    st.error("Please enter both username and password")
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    with tab2:
        with st.container():
            st.markdown('<div class="login-container">', unsafe_allow_html=True)
            st.subheader("Create New Account")
            
            new_username = st.text_input("Choose Username", key="reg_username")
            new_password = st.text_input("Choose Password", type="password", key="reg_password")
            confirm_password = st.text_input("Confirm Password", type="password", key="reg_confirm")
            
            if st.button("Create Account", type="primary", use_container_width=True):
                if new_username and new_password and confirm_password:
                    if new_password == confirm_password:
                        if len(new_password) >= 6:
                            if create_user(new_username, new_password):
                                st.success("Account created successfully! Please login with your credentials.")
                            else:
                                st.error("Username already exists. Please choose a different username.")
                        else:
                            st.error("Password must be at least 6 characters long")
                    else:
                        st.error("Passwords do not match")
                else:
                    st.error("Please fill in all fields")
            
            st.markdown('</div>', unsafe_allow_html=True)

def show_dashboard():
    """Display user dashboard"""
    
    # Header with logout
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown('<div class="main-header">🎤 EchoPrep AI Dashboard</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="sub-header">Welcome back, {st.session_state.username}!</div>', unsafe_allow_html=True)
    
    with col2:
        if st.button("Logout", type="secondary"):
            st.session_state.authenticated = False
            st.session_state.user_id = None
            st.session_state.username = None
            st.rerun()
    
    st.markdown("---")
    
    # Dashboard content
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Your Interview Mocks")
        
        # Get user's interview mocks from database
        from utils.database import get_user_interviews
        interviews = get_user_interviews(st.session_state.user_id)
        
        if interviews:
            for interview in interviews:
                with st.expander(f"🎯 {interview['job_role']} - {interview['experience_level']} ({interview['created_at']})"):
                    col_a, col_b, col_c = st.columns([2, 1, 1])
                    
                    with col_a:
                        st.write(f"**Type:** {interview['interview_type']}")
                        st.write(f"**Skills:** {interview['skills']}")
                        if interview['completed']:
                            st.write("**Status:** ✅ Completed")
                        else:
                            st.write("**Status:** ⏳ Not Started")
                    
                    with col_b:
                        if not interview['completed']:
                            if st.button("Start Interview", key=f"start_{interview['id']}"):
                                st.session_state.current_interview_id = interview['id']
                                st.switch_page("pages/interview.py")
                    
                    with col_c:
                        if interview['completed']:
                            if st.button("View Report", key=f"report_{interview['id']}"):
                                st.session_state.current_interview_id = interview['id']
                                st.switch_page("pages/report.py")
        else:
            st.info("No interview mocks found. Create your first mock interview!")
    
    with col2:
        st.subheader("Quick Actions")
        
        if st.button("🆕 Create New Mock Interview", type="primary", use_container_width=True):
            st.switch_page("pages/setup.py")
        
        st.markdown("---")
        
        # Stats
        from utils.database import get_user_stats
        stats = get_user_stats(st.session_state.user_id)
        
        st.metric("Total Interviews", stats['total'])
        st.metric("Completed", stats['completed'])
        st.metric("Success Rate", f"{stats['success_rate']:.1f}%")

if __name__ == "__main__":
    main()
