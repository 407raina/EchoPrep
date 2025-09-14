import streamlit as st
import json
from utils.auth import get_current_user_id
from utils.ai_services import conversational_setup_assistant, generate_interview_questions
from utils.database import create_interview_mock, update_interview_questions

# Check authentication
if 'authenticated' not in st.session_state or not st.session_state.authenticated:
    st.error("Please login to access this page")
    if st.button("← Back to Login"):
        st.switch_page("main.py")
    st.stop()

# Configure page
st.set_page_config(
    page_title="EchoPrep - Setup Interview",
    page_icon="🎤",
    layout="wide"
)

# Modern clean CSS styling
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

.stApp {
    background: #FFFFFF;
    font-family: 'Inter', sans-serif;
    color: #1a1a1a;
}

.main-container {
    max-width: 800px;
    margin: 0 auto;
    padding: 2rem 1rem;
}

.header-section {
    text-align: center;
    margin-bottom: 3rem;
}

.page-title {
    font-size: 2.5rem;
    font-weight: 700;
    color: #1a1a1a;
    margin-bottom: 0.5rem;
    background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.page-subtitle {
    font-size: 1.1rem;
    color: #6b7280;
    font-weight: 400;
    line-height: 1.6;
}

.setup-card {
    background: #ffffff;
    border-radius: 16px;
    padding: 2rem;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    border: 1px solid #f3f4f6;
    margin-bottom: 2rem;
}

.progress-container {
    margin-bottom: 2rem;
}

.progress-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.75rem;
}

.step-indicator {
    font-size: 0.875rem;
    font-weight: 600;
    color: #3b82f6;
}

.progress-percentage {
    font-size: 0.875rem;
    color: #6b7280;
}

.progress-bar {
    width: 100%;
    height: 8px;
    background: #f3f4f6;
    border-radius: 4px;
    overflow: hidden;
}

.progress-fill {
    height: 100%;
    background: linear-gradient(90deg, #3b82f6, #1d4ed8);
    border-radius: 4px;
    transition: width 0.3s ease;
}

.conversation-container {
    min-height: 300px;
    margin-bottom: 2rem;
}

.message {
    margin-bottom: 1.5rem;
    padding: 1rem 1.25rem;
    border-radius: 12px;
    line-height: 1.6;
}

.assistant-message {
    background: #f8fafc;
    border-left: 4px solid #3b82f6;
    color: #374151;
}

.user-message {
    background: #eff6ff;
    border-left: 4px solid #60a5fa;
    color: #1e40af;
    margin-left: 2rem;
}

.input-section {
    margin-bottom: 1.5rem;
}

.action-buttons {
    display: flex;
    gap: 1rem;
    justify-content: center;
    margin-top: 2rem;
}

.completion-card {
    background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
    border: 1px solid #bae6fd;
    border-radius: 16px;
    padding: 2rem;
    text-align: center;
    margin: 2rem 0;
}

.completion-title {
    font-size: 1.5rem;
    font-weight: 700;
    color: #0f172a;
    margin-bottom: 0.5rem;
}

.completion-text {
    color: #64748b;
    margin-bottom: 2rem;
    line-height: 1.6;
}

/* Button styling */
div[data-testid="stButton"] > button {
    background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
    color: white;
    border: none;
    border-radius: 8px;
    padding: 0.75rem 1.5rem;
    font-weight: 600;
    font-size: 0.875rem;
    transition: all 0.2s ease;
    box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
}

div[data-testid="stButton"] > button:hover {
    background: linear-gradient(135deg, #2563eb 0%, #1e40af 100%);
    transform: translateY(-1px);
    box-shadow: 0 4px 8px -2px rgba(59, 130, 246, 0.5);
}

.back-button {
    background: #f9fafb !important;
    color: #374151 !important;
    border: 1px solid #d1d5db !important;
}

.back-button:hover {
    background: #f3f4f6 !important;
    border-color: #9ca3af !important;
}

/* Input styling */
div[data-testid="stTextInput"] > div > div > input,
div[data-testid="stTextArea"] > div > div > textarea,
div[data-testid="stSelectbox"] > div > div > select {
    border-radius: 8px;
    border: 1px solid #d1d5db;
    padding: 0.75rem;
    font-size: 0.875rem;
    transition: all 0.2s ease;
}

div[data-testid="stTextInput"] > div > div > input:focus,
div[data-testid="stTextArea"] > div > div > textarea:focus,
div[data-testid="stSelectbox"] > div > div > select:focus {
    border-color: #3b82f6;
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

/* Hide Streamlit branding */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

def main():
    """Main setup page function with clean UI"""
    
    # Initialize session state
    if 'setup_conversation' not in st.session_state:
        st.session_state.setup_conversation = []
        st.session_state.setup_step = 1
        st.session_state.interview_config = {}
    
    # Header
    st.markdown("""
    <div class="main-container">
        <div class="header-section">
            <h1 class="page-title">🎯 Interview Setup</h1>
            <p class="page-subtitle">Let's create your personalized mock interview experience with our AI assistant</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Back button
    col1, col2, col3 = st.columns([1, 6, 1])
    with col1:
        if st.button("← Back", key="back_btn", help="Return to Dashboard"):
            st.switch_page("main.py")
    
    # Progress indicator
    total_steps = 6
    progress = min(st.session_state.setup_step / total_steps, 1.0)
    
    st.markdown(f"""
    <div class="main-container">
        <div class="progress-container">
            <div class="progress-header">
                <span class="step-indicator">Step {st.session_state.setup_step} of {total_steps}</span>
                <span class="progress-percentage">{int(progress * 100)}% Complete</span>
            </div>
            <div class="progress-bar">
                <div class="progress-fill" style="width: {progress * 100}%"></div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Main setup card
    st.markdown('<div class="main-container"><div class="setup-card">', unsafe_allow_html=True)
    
    # Display conversation history
    if st.session_state.setup_conversation:
        st.markdown('<div class="conversation-container">', unsafe_allow_html=True)
        for message in st.session_state.setup_conversation:
            if message['role'] == 'assistant':
                st.markdown(f'<div class="message assistant-message">🤖 {message["content"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="message user-message">👤 {message["content"]}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Current step logic
    if st.session_state.setup_step == 1:
        if not st.session_state.setup_conversation:
            welcome_msg = """
            Welcome to EchoPrep! I'm your AI interview assistant, and I'm here to help you prepare for your upcoming interview.
            
            Let's start by understanding what role you're preparing for. What job position are you interviewing for?
            """
            st.session_state.setup_conversation.append({"role": "assistant", "content": welcome_msg})
            st.markdown(f'<div class="conversation-container"><div class="message assistant-message">🤖 {welcome_msg}</div></div>', unsafe_allow_html=True)
        
        st.markdown('<div class="input-section">', unsafe_allow_html=True)
        user_input = st.text_input("Your answer:", placeholder="e.g., Software Engineer, Data Scientist, Product Manager...", key="job_role_input")
        st.markdown('</div>', unsafe_allow_html=True)
        
        if st.button("Continue", key="step1_submit", type="primary") and user_input:
            st.session_state.setup_conversation.append({"role": "user", "content": user_input})
            st.session_state.interview_config['job_role'] = user_input
            st.session_state.setup_step = 2
            st.rerun()
    
    elif st.session_state.setup_step == 2:
        assistant_msg = f"""
        Great! You're preparing for a {st.session_state.interview_config['job_role']} position. 
        
        Now, what's your experience level in this field?
        """
        if len(st.session_state.setup_conversation) < 3:
            st.session_state.setup_conversation.append({"role": "assistant", "content": assistant_msg})
            st.markdown(f'<div class="conversation-container"><div class="message assistant-message">🤖 {assistant_msg}</div></div>', unsafe_allow_html=True)
        
        st.markdown('<div class="input-section">', unsafe_allow_html=True)
        experience_level = st.selectbox(
            "Select your experience level:",
            ["Entry Level (0-2 years)", "Mid Level (3-5 years)", "Senior Level (6-10 years)", "Lead/Principal (10+ years)"],
            key="experience_select"
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
        if st.button("Continue", key="step2_submit", type="primary"):
            st.session_state.setup_conversation.append({"role": "user", "content": experience_level})
            st.session_state.interview_config['experience_level'] = experience_level
            st.session_state.setup_step = 3
            st.rerun()
    
    elif st.session_state.setup_step == 3:
        assistant_msg = """
        Perfect! Now let's talk about the type of interview you'd like to practice. 
        
        What type of interview are you preparing for?
        """
        if len(st.session_state.setup_conversation) < 5:
            st.session_state.setup_conversation.append({"role": "assistant", "content": assistant_msg})
            st.markdown(f'<div class="conversation-container"><div class="message assistant-message">🤖 {assistant_msg}</div></div>', unsafe_allow_html=True)
        
        st.markdown('<div class="input-section">', unsafe_allow_html=True)
        interview_type = st.selectbox(
            "Choose interview type:",
            ["Technical Interview", "Behavioral Interview", "Case Study Interview", "Mixed (Technical + Behavioral)"],
            key="interview_type_select"
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
        if st.button("Next", key="step3_submit", type="primary"):
            st.session_state.setup_conversation.append({"role": "user", "content": interview_type})
            st.session_state.interview_config['interview_type'] = interview_type
            st.session_state.setup_step = 4
            st.rerun()
    
    elif st.session_state.setup_step == 4:
        assistant_msg = """
        Excellent choice! Now I need to understand your technical background better.
        
        What are the key skills or technologies you'd like to be questioned about?
        """
        if len(st.session_state.setup_conversation) < 7:
            st.session_state.setup_conversation.append({"role": "assistant", "content": assistant_msg})
            st.markdown(f'<div class="conversation-container"><div class="message assistant-message">🤖 {assistant_msg}</div></div>', unsafe_allow_html=True)
        
        st.markdown('<div class="input-section">', unsafe_allow_html=True)
        skills = st.text_area(
            "List your key skills/technologies:",
            placeholder="e.g., Python, React, Machine Learning, AWS, SQL, Leadership, Project Management...",
            height=100,
            key="skills_input"
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
        if st.button("Continue", key="step4_submit", type="primary") and skills:
            st.session_state.setup_conversation.append({"role": "user", "content": skills})
            st.session_state.interview_config['skills'] = skills
            st.session_state.setup_step = 5
            st.rerun()
    
    elif st.session_state.setup_step == 5:
        assistant_msg = """
        Great! One more thing - how long would you like your mock interview to be?
        
        This will help me structure the right number of questions for your practice session.
        """
        if len(st.session_state.setup_conversation) < 9:
            st.session_state.setup_conversation.append({"role": "assistant", "content": assistant_msg})
            st.markdown(f'<div class="conversation-container"><div class="message assistant-message">🤖 {assistant_msg}</div></div>', unsafe_allow_html=True)
        
        st.markdown('<div class="input-section">', unsafe_allow_html=True)
        duration = st.selectbox(
            "Interview duration:",
            ["15 minutes (5-7 questions)", "30 minutes (8-12 questions)", "45 minutes (13-18 questions)", "60 minutes (20+ questions)"],
            key="duration_select"
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
        if st.button("Finish Setup", key="step5_submit", type="primary"):
            st.session_state.setup_conversation.append({"role": "user", "content": duration})
            st.session_state.interview_config['duration'] = duration
            st.session_state.setup_step = 6
            st.rerun()
    
    elif st.session_state.setup_step == 6:
        # Final step - save and create interview
        st.markdown("""
        <div class="completion-card">
            <h2 class="completion-title">🎉 Setup Complete!</h2>
            <p class="completion-text">Your personalized mock interview has been created and is ready to start.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Save interview configuration
        try:
            interview_id = create_interview_mock(
                user_id=st.session_state.user_id,
                job_role=st.session_state.interview_config['job_role'],
                experience_level=st.session_state.interview_config['experience_level'],
                interview_type=st.session_state.interview_config['interview_type'],
                skills=st.session_state.interview_config['skills']
            )
            
            st.markdown('<div class="action-buttons">', unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("🚀 Start Interview Now", key="start_interview", type="primary"):
                    st.session_state.current_interview_id = interview_id
                    # Clear setup state
                    if 'setup_conversation' in st.session_state:
                        del st.session_state.setup_conversation
                    if 'setup_step' in st.session_state:
                        del st.session_state.setup_step
                    if 'interview_config' in st.session_state:
                        del st.session_state.interview_config
                    st.switch_page("pages/interview.py")
            
            with col2:
                if st.button("📊 Return to Dashboard", key="return_dashboard"):
                    # Clear setup state
                    if 'setup_conversation' in st.session_state:
                        del st.session_state.setup_conversation
                    if 'setup_step' in st.session_state:
                        del st.session_state.setup_step
                    if 'interview_config' in st.session_state:
                        del st.session_state.interview_config
                    st.switch_page("main.py")
            
            st.markdown('</div>', unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"Error creating interview: {str(e)}")
            if st.button("← Back to Dashboard", key="error_back"):
                st.switch_page("main.py")
    
    st.markdown('</div></div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
