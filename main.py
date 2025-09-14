import streamlit as st
from datetime import datetime
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
    """Main application entry point for EchoPrep AI interview platform"""
    
    # Initialize database
    try:
        init_database()
    except Exception as e:
        st.error(f"Database initialization failed: {e}")
        return
    
    # Enhanced CSS with fixed overlapping and positioning
    st.markdown("""
    <style>
    /* Import fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Reset and base styling */
    * {
        box-sizing: border-box !important;
    }
    
    .stApp {
        background-color: #F5EFE6 !important;
        min-height: 100vh !important;
    }
    
    .main .block-container {
        background-color: #F5EFE6 !important;
        padding: 2rem 1rem !important;
        max-width: 1200px !important;
        margin: 0 auto !important;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* Remove all default margins and padding */
    .element-container {
        margin: 0 !important;
        padding: 0 !important;
    }
    
    .stMarkdown {
        margin: 0 !important;
        padding: 0 !important;
    }
    
    /* Typography */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif !important;
        color: #2c3e50 !important;
        font-weight: 600 !important;
        margin: 0 !important;
        padding: 0 !important;
    }
    
    p, div, span, label {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
        color: #34495e !important;
        margin: 0 !important;
        padding: 0 !important;
    }
    
    /* Centered content container */
    .centered-content {
        max-width: 800px !important;
        margin: 0 auto !important;
        padding: 0 !important;
    }
    
    /* Hero section styling */
    .hero-section {
        background-color: #CBDCEB !important;
        border: 2px solid #6D94C5 !important;
        border-radius: 16px !important;
        padding: 2rem !important;
        margin: 0 auto 2rem auto !important;
        text-align: center !important;
        box-shadow: 0 4px 20px rgba(109, 148, 197, 0.2) !important;
        width: 100% !important;
        max-width: 700px !important;
    }
    
    .hero-title {
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif !important;
        font-size: 2.8rem !important;
        font-weight: 700 !important;
        color: #2c3e50 !important;
        margin-bottom: 1rem !important;
    }
    
    .hero-subtitle {
        font-family: 'Inter', sans-serif !important;
        font-size: 1.1rem !important;
        color: #34495e !important;
        line-height: 1.5 !important;
        margin: 0 !important;
    }
    
    /* FIXED TAB SYSTEM - No overlapping */
    .stTabs {
        margin: 2rem auto 0 auto !important;
        max-width: 500px !important;
        width: 100% !important;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 0 !important;
        background-color: #E8DFCA !important;
        padding: 0.5rem !important;
        border-radius: 12px !important;
        border: 2px solid #6D94C5 !important;
        margin: 0 auto 0 auto !important;
        display: flex !important;
        justify-content: center !important;
        box-shadow: 0 2px 10px rgba(109, 148, 197, 0.15) !important;
        width: 100% !important;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: transparent !important;
        border-radius: 8px !important;
        color: #2c3e50 !important;
        font-weight: 600 !important;
        padding: 0.75rem 1.5rem !important;
        font-family: 'Inter', sans-serif !important;
        border: none !important;
        transition: all 0.2s ease !important;
        flex: 1 !important;
        text-align: center !important;
        font-size: 0.95rem !important;
        margin: 0 0.25rem !important;
        min-height: 40px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background-color: #CBDCEB !important;
        color: #2c3e50 !important;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #6D94C5 !important;
        color: #ffffff !important;
        box-shadow: 0 2px 8px rgba(109, 148, 197, 0.3) !important;
        font-weight: 700 !important;
    }
    
    /* FIXED TAB PANEL - No overlapping, proper spacing */
    .stTabs [data-baseweb="tab-panel"] {
        padding: 0 !important;
        margin: 1.5rem auto 0 auto !important;
        background: transparent !important;
        border: none !important;
        width: 100% !important;
        max-width: 500px !important;
    }
    
    /* Form container - Fixed positioning */
    .auth-form-container {
        background-color: #ffffff !important;
        border: 2px solid #6D94C5 !important;
        border-radius: 16px !important;
        padding: 2rem !important;
        margin: 0 auto !important;
        box-shadow: 0 8px 30px rgba(109, 148, 197, 0.2) !important;
        width: 100% !important;
        max-width: 500px !important;
        position: relative !important;
        z-index: 1 !important;
    }
    
    /* Form title */
    .auth-title {
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif !important;
        font-size: 1.8rem !important;
        font-weight: 600 !important;
        color: #2c3e50 !important;
        text-align: center !important;
        margin-bottom: 2rem !important;
        padding: 0 !important;
    }
    
    /* FIXED INPUT STYLING - No overlapping */
    .stTextInput {
        margin-bottom: 1.5rem !important;
        position: relative !important;
    }
    
    .stTextInput > div {
        position: relative !important;
        margin: 0 !important;
        padding: 0 !important;
    }
    
    .stTextInput > div > div {
        position: relative !important;
        margin: 0 !important;
        padding: 0 !important;
    }
    
    .stTextInput > div > div > input {
        background-color: #ffffff !important;
        color: #2c3e50 !important;
        border: 2px solid #6D94C5 !important;
        border-radius: 10px !important;
        padding: 1rem 1rem !important;
        padding-right: 3rem !important;
        font-size: 1rem !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 500 !important;
        width: 100% !important;
        height: 50px !important;
        box-sizing: border-box !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 2px 6px rgba(109, 148, 197, 0.1) !important;
        position: relative !important;
        z-index: 1 !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #5a7ba8 !important;
        box-shadow: 0 0 0 0.2rem rgba(109, 148, 197, 0.25) !important;
        outline: none !important;
        background-color: #fafafa !important;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: #6c757d !important;
        opacity: 0.7 !important;
        font-weight: 400 !important;
    }
    
    /* Input labels */
    .stTextInput > label {
        font-family: 'Inter', sans-serif !important;
        color: #2c3e50 !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        margin-bottom: 0.5rem !important;
        display: block !important;
        padding: 0 !important;
    }
    
    /* FIXED PASSWORD TOGGLE - Proper positioning */
    div[data-testid="stTextInputRootElement"] {
        position: relative !important;
    }
    
    div[data-testid="stTextInputRootElement"] button {
        position: absolute !important;
        right: 0.75rem !important;
        top: 50% !important;
        transform: translateY(-50%) !important;
        background-color: #6D94C5 !important;
        border: none !important;
        color: #ffffff !important;
        padding: 0.4rem !important;
        cursor: pointer !important;
        z-index: 10 !important;
        width: 2rem !important;
        height: 2rem !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        border-radius: 6px !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 1px 4px rgba(109, 148, 197, 0.3) !important;
        font-size: 0.8rem !important;
    }
    
    div[data-testid="stTextInputRootElement"] button:hover {
        background-color: #5a7ba8 !important;
        transform: translateY(-50%) scale(1.05) !important;
    }
    
    /* Show/Hide password button states */
    div[data-testid="stTextInputRootElement"] button[title*="Hide"] {
        background-color: #e74c3c !important;
    }
    
    div[data-testid="stTextInputRootElement"] button[title*="Hide"]:hover {
        background-color: #c0392b !important;
    }
    
    /* FIXED BUTTON STYLING - No overlapping */
    .stButton {
        margin-top: 2rem !important;
        margin-bottom: 0 !important;
        width: 100% !important;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #6D94C5 0%, #5a7ba8 100%) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 1rem 2rem !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        font-family: 'Inter', sans-serif !important;
        width: 100% !important;
        height: 50px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 12px rgba(109, 148, 197, 0.3) !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
        cursor: pointer !important;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #5a7ba8 0%, #4a6690 100%) !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 6px 18px rgba(109, 148, 197, 0.4) !important;
    }
    
    /* Form submit button */
    div[data-testid="stForm"] .stButton > button {
        background: linear-gradient(135deg, #6D94C5 0%, #5a7ba8 100%) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 1rem 2rem !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        font-family: 'Inter', sans-serif !important;
        width: 100% !important;
        height: 50px !important;
        margin-top: 2rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 12px rgba(109, 148, 197, 0.3) !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
    }
    
    div[data-testid="stForm"] .stButton > button:hover {
        background: linear-gradient(135deg, #5a7ba8 0%, #4a6690 100%) !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 6px 18px rgba(109, 148, 197, 0.4) !important;
    }
    
    /* Form containers - Remove default styling */
    .stForm {
        background: transparent !important;
        border: none !important;
        padding: 0 !important;
        margin: 0 !important;
    }
    
    div[data-testid="stForm"] {
        background: transparent !important;
        border: none !important;
        padding: 0 !important;
        margin: 0 !important;
    }
    
    /* Success/Error messages */
    .stSuccess, .stError, .stWarning, .stInfo {
        font-family: 'Inter', sans-serif !important;
        border-radius: 10px !important;
        margin: 1rem auto !important;
        max-width: 500px !important;
        font-weight: 600 !important;
        text-align: center !important;
    }
    
    /* Feature cards */
    .features-section {
        margin: 4rem auto 2rem auto !important;
        max-width: 900px !important;
    }
    
    .features-title {
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif !important;
        font-size: 2.2rem !important;
        font-weight: 700 !important;
        color: #2c3e50 !important;
        text-align: center !important;
        margin-bottom: 2.5rem !important;
    }
    
    .feature-card {
        background-color: #ffffff !important;
        border: 2px solid #6D94C5 !important;
        border-radius: 12px !important;
        padding: 1.8rem 1.5rem !important;
        text-align: center !important;
        height: 100% !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 16px rgba(109, 148, 197, 0.15) !important;
        margin-bottom: 1rem !important;
    }
    
    .feature-card:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 8px 25px rgba(109, 148, 197, 0.25) !important;
        border-color: #5a7ba8 !important;
    }
    
    .feature-icon {
        font-size: 2.5rem !important;
        margin-bottom: 1rem !important;
        display: block !important;
    }
    
    .feature-title {
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif !important;
        font-size: 1.2rem !important;
        font-weight: 700 !important;
        color: #2c3e50 !important;
        margin-bottom: 0.8rem !important;
    }
    
    .feature-description {
        font-family: 'Inter', sans-serif !important;
        color: #34495e !important;
        line-height: 1.5 !important;
        font-size: 0.95rem !important;
        font-weight: 400 !important;
    }
    
    /* Dashboard styling */
    .dashboard-header {
        background-color: #CBDCEB !important;
        border: 2px solid #6D94C5 !important;
        border-radius: 16px !important;
        padding: 2rem !important;
        margin: 0 auto 2rem auto !important;
        text-align: center !important;
        max-width: 700px !important;
        box-shadow: 0 6px 25px rgba(109, 148, 197, 0.2) !important;
    }
    
    .dashboard-title {
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif !important;
        font-size: 2.2rem !important;
        font-weight: 700 !important;
        color: #2c3e50 !important;
        margin-bottom: 0.5rem !important;
    }
    
    .dashboard-subtitle {
        font-family: 'Inter', sans-serif !important;
        font-size: 1rem !important;
        color: #34495e !important;
        font-weight: 500 !important;
    }
    
    /* Column spacing */
    .stColumn {
        padding: 0 0.5rem !important;
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .main .block-container {
            padding: 1rem 0.5rem !important;
        }
        
        .hero-section {
            max-width: 95% !important;
            padding: 1.5rem !important;
            margin: 0 auto 1.5rem auto !important;
        }
        
        .hero-title {
            font-size: 2.2rem !important;
        }
        
        .auth-form-container {
            padding: 1.5rem !important;
            max-width: 95% !important;
        }
        
        .stTabs {
            max-width: 95% !important;
        }
        
        .stTabs [data-baseweb="tab-panel"] {
            max-width: 95% !important;
        }
        
        .feature-card {
            margin: 0 0 1rem 0 !important;
        }
        
        .dashboard-title {
            font-size: 1.8rem !important;
        }
        
        .stTextInput > div > div > input {
            font-size: 16px !important; /* Prevent zoom on iOS */
        }
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Check if user is logged in
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    
    if st.session_state.logged_in:
        show_dashboard()
    else:
        show_login_page()

def show_login_page():
    """Display the EchoPrep login page with fixed positioning"""
    
    # Wrap content in centered container
    st.markdown('<div class="centered-content">', unsafe_allow_html=True)
    
    # Hero section
    st.markdown("""
    <div class="hero-section">
        <h1 class="hero-title">🎤 EchoPrep</h1>
        <p class="hero-subtitle">Master your interviews with AI-powered practice sessions. Get real-time feedback, improve your skills, and land your dream job with confidence.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Authentication tabs
    tab1, tab2 = st.tabs(["🔑 Sign In", "👤 Create Account"])
    
    with tab1:
        st.markdown("""
        <div class="auth-form-container">
            <h2 class="auth-title">Welcome Back</h2>
        </div>
        """, unsafe_allow_html=True)
        
        # Move form outside the container to avoid nesting issues
        with st.form("signin_form", clear_on_submit=False):
            username = st.text_input(
                "Username", 
                placeholder="Enter your username",
                key="signin_username",
                help="Your EchoPrep username"
            )
            password = st.text_input(
                "Password", 
                type="password", 
                placeholder="Enter your password",
                key="signin_password",
                help="Your account password"
            )
            
            submit_signin = st.form_submit_button("Sign In", use_container_width=True)
            
            if submit_signin:
                if username and password:
                    user_data = verify_user(username, password)
                    if user_data:
                        st.session_state.logged_in = True
                        st.session_state.user_id = user_data['id']
                        st.session_state.username = user_data['username']
                        st.success("✅ Login successful!")
                        st.rerun()
                    else:
                        st.error("❌ Invalid username or password")
                else:
                    st.warning("⚠️ Please fill in all fields")
    
    with tab2:
        st.markdown("""
        <div class="auth-form-container">
            <h2 class="auth-title">Create Your Account</h2>
        </div>
        """, unsafe_allow_html=True)
        
        # Move form outside the container to avoid nesting issues
        with st.form("signup_form", clear_on_submit=False):
            new_username = st.text_input(
                "Username", 
                placeholder="Choose a unique username",
                key="signup_username",
                help="3+ characters, letters and numbers only"
            )
            new_email = st.text_input(
                "Email", 
                placeholder="your.email@example.com",
                key="signup_email",
                help="Valid email address"
            )
            new_password = st.text_input(
                "Password", 
                type="password", 
                placeholder="Create a secure password",
                key="signup_password",
                help="Minimum 6 characters"
            )
            confirm_password = st.text_input(
                "Confirm Password", 
                type="password", 
                placeholder="Confirm your password",
                key="confirm_password",
                help="Re-enter your password"
            )
            
            submit_signup = st.form_submit_button("Create Account", use_container_width=True)
            
            if submit_signup:
                if new_username and new_email and new_password and confirm_password:
                    if new_password != confirm_password:
                        st.error("❌ Passwords do not match")
                    elif len(new_password) < 6:
                        st.error("❌ Password must be at least 6 characters long")
                    elif len(new_username) < 3:
                        st.error("❌ Username must be at least 3 characters long")
                    else:
                        success, message = create_user(new_username, new_email, new_password)
                        if success:
                            st.success("✅ Account created successfully! Please sign in.")
                            st.balloons()
                        else:
                            st.error(f"❌ {message}")
                else:
                    st.warning("⚠️ Please fill in all fields")
    
    # Features section
    st.markdown("""
    <div class="features-section">
        <h2 class="features-title">Why Choose EchoPrep?</h2>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1], gap="medium")
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🤖</div>
            <h3 class="feature-title">AI-Powered Feedback</h3>
            <p class="feature-description">Get intelligent, personalized feedback on your answers, communication style, and overall performance.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🎯</div>
            <h3 class="feature-title">Realistic Practice</h3>
            <p class="feature-description">Practice with industry-specific questions tailored to your role and experience level.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📈</div>
            <h3 class="feature-title">Track Progress</h3>
            <p class="feature-description">Monitor your improvement over time with detailed analytics and performance insights.</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def show_dashboard():
    """Display EchoPrep dashboard for authenticated users"""
    
    # Wrap content in centered container
    st.markdown('<div class="centered-content">', unsafe_allow_html=True)
    
    # Dashboard header
    st.markdown(f"""
    <div class="dashboard-header">
        <h1 class="dashboard-title">Welcome back, {st.session_state.username}! 👋</h1>
        <p class="dashboard-subtitle">Ready to practice and improve your interview skills?</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick actions section
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1], gap="medium")
    
    with col1:
        if st.button("🆕 New Interview", use_container_width=True, type="primary"):
            st.switch_page("pages/setup.py")
    
    with col2:
        if st.button("📊 View Reports", use_container_width=True):
            st.switch_page("pages/reports.py")
    
    with col3:
        if st.button("🔄 Refresh", use_container_width=True):
            st.rerun()
    
    with col4:
        if st.button("🚪 Sign Out", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
