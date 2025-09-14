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

# Custom CSS
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Source+Sans+Pro:wght@400;600;700&display=swap');

.stApp {
    font-family: 'Inter', sans-serif;
    background: linear-gradient(135deg, #273F4F 0%, #FE7743 100%);
}

.setup-container {
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
    background: rgba(239, 238, 234, 0.95);
    border-radius: 20px;
    backdrop-filter: blur(10px);
}

.chat-message {
    padding: 15px;
    margin: 10px 0;
    border-radius: 10px;
    border-left: 4px solid #FE7743;
    font-family: 'Source Sans Pro', sans-serif;
}

.user-message {
    background-color: rgba(254, 119, 67, 0.1);
    margin-left: 50px;
    border-left-color: #273F4F;
}

.ai-message {
    background-color: rgba(239, 238, 234, 0.8);
    margin-right: 50px;
    border-left-color: #FE7743;
}

.info-box {
    background-color: #EFEEEA;
    border: 1px solid #FE7743;
    border-radius: 8px;
    padding: 15px;
    margin: 15px 0;
}

.success-box {
    background-color: rgba(254, 119, 67, 0.1);
    border: 1px solid #FE7743;
    border-radius: 8px;
    padding: 15px;
    margin: 15px 0;
}
</style>
""", unsafe_allow_html=True)

# Configure page
st.set_page_config(
    page_title="EchoPrep - Setup Interview",
    page_icon="🎤",
    layout="wide"
)

# Modern CSS styling
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@300;400;500;600;700;800&family=Crimson+Text:wght@400;600&display=swap');
    
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    .stApp {
        background: linear-gradient(135deg, #647FBC 0%, #91ADC8 100%);
        min-height: 100vh;
    }
    
    .main {
        font-family: 'Crimson Text', serif;
    }
    
    .setup-container {
        max-width: 1000px;
        margin: 0 auto;
        padding: 40px 20px;
    }
    
    .setup-header {
        text-align: center;
        margin-bottom: 50px;
    }
    
    .setup-title {
        font-family: 'Playfair Display', serif;
        color: white;
        font-size: 3rem;
        font-weight: 800;
        margin-bottom: 20px;
        text-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    .setup-subtitle {
        font-family: 'Crimson Text', serif;
        color: rgba(255,255,255,0.9);
        font-size: 1.3rem;
        font-weight: 400;
    }
    
    .chat-container {
        background: #FAFDD6;
        border-radius: 25px;
        padding: 40px;
        box-shadow: 0 20px 60px rgba(0,0,0,0.15);
        margin: 30px 0;
    }
    
    .assistant-message {
        background: linear-gradient(135deg, #647FBC, #91ADC8);
        color: white;
        padding: 20px 25px;
        border-radius: 20px 20px 20px 5px;
        margin: 15px 0;
        box-shadow: 0 8px 25px rgba(100, 127, 188, 0.3);
        font-family: 'Crimson Text', serif;
    }
    
    .user-response {
        background: #AED6CF;
        color: #647FBC;
        padding: 20px 25px;
        border-radius: 20px 20px 5px 20px;
        margin: 15px 0;
        border-left: 4px solid #647FBC;
        font-family: 'Crimson Text', serif;
    }
    
    .progress-bar {
        background: #AED6CF;
        height: 8px;
        border-radius: 10px;
        margin: 30px 0;
        overflow: hidden;
    }
    
    .progress-fill {
        background: linear-gradient(90deg, #647FBC, #91ADC8);
        height: 100%;
        border-radius: 10px;
        transition: width 0.5s ease;
    }
    
    .step-indicator {
        color: #647FBC;
        font-weight: 600;
        font-size: 1.1rem;
        margin-bottom: 10px;
        font-family: 'Playfair Display', serif;
    }
    
    .completion-card {
        background: linear-gradient(135deg, #91ADC8, #AED6CF);
        color: white;
        padding: 30px;
        border-radius: 20px;
        text-align: center;
        margin: 30px 0;
        box-shadow: 0 15px 40px rgba(145, 173, 200, 0.3);
    }
    
    [data-testid="stButton"] > button {
        background: linear-gradient(135deg, #647FBC, #91ADC8);
        color: white;
        border: none;
        border-radius: 15px;
        padding: 15px 30px;
        font-weight: 600;
        font-size: 1.1rem;
        font-family: 'Crimson Text', serif;
        transition: all 0.3s ease;
        box-shadow: 0 8px 25px rgba(100, 127, 188, 0.3);
    }
    
    [data-testid="stButton"] > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 35px rgba(100, 127, 188, 0.4);
    }
    
    [data-testid="stTextInput"] > div > div > input,
    [data-testid="stTextArea"] > div > div > textarea,
    [data-testid="stSelectbox"] > div > div > select {
        border-radius: 15px;
        border: 2px solid #AED6CF;
        padding: 15px;
        font-family: 'Crimson Text', serif;
        transition: all 0.3s ease;
    }
    
    [data-testid="stTextInput"] > div > div > input:focus,
    [data-testid="stTextArea"] > div > div > textarea:focus,
    [data-testid="stSelectbox"] > div > div > select:focus {
        border-color: #647FBC;
        box-shadow: 0 0 0 3px rgba(100, 127, 188, 0.1);
    }
    
    .back-button {
        background: rgba(255,255,255,0.2) !important;
        color: white !important;
        border: 2px solid rgba(255,255,255,0.3) !important;
        backdrop-filter: blur(10px);
    }
    
    .back-button:hover {
        background: rgba(255,255,255,0.3) !important;
        transform: translateY(-2px);
    }
    </style>
""", unsafe_allow_html=True)

def main():
    """Main setup page function with modern UI"""
    
    # Header
    st.markdown("""
    <div class="setup-container">
        <div class="setup-header">
            <h1 class="setup-title">🎯 Interview Setup</h1>
            <p class="setup-subtitle">Let's create your personalized mock interview experience</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Back button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("← Back to Dashboard", key="back_btn", help="Return to Dashboard"):
            st.switch_page("main.py")
    
    # Initialize session state for conversation
    if 'setup_conversation' not in st.session_state:
        st.session_state.setup_conversation = []
        st.session_state.setup_step = 1
        st.session_state.interview_config = {}
    
    # Progress indicator
    total_steps = 6
    progress = min(st.session_state.setup_step / total_steps, 1.0)
    
    st.markdown(f"""
    <div class="step-indicator">Step {st.session_state.setup_step} of {total_steps}</div>
    <div class="progress-bar">
        <div class="progress-fill" style="width: {progress * 100}%"></div>
    </div>
    """, unsafe_allow_html=True)
    
    # Chat container
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    # Display conversation history
    for message in st.session_state.setup_conversation:
        if message['role'] == 'assistant':
            st.markdown(f'<div class="assistant-message">🤖 {message["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="user-response">👤 {message["content"]}</div>', unsafe_allow_html=True)
    
    # Current step logic
    if st.session_state.setup_step == 1:
        if not st.session_state.setup_conversation:
            welcome_msg = """
            👋 Welcome to EchoPrep! I'm your AI interview assistant, and I'm here to help you prepare for your upcoming interview.
            
            Let's start by understanding what role you're preparing for. What job position are you interviewing for?
            """
            st.session_state.setup_conversation.append({"role": "assistant", "content": welcome_msg})
            st.markdown(f'<div class="assistant-message">🤖 {welcome_msg}</div>', unsafe_allow_html=True)
        
        user_input = st.text_input("Your answer:", placeholder="e.g., Software Engineer, Data Scientist, Product Manager...")
        if st.button("Submit", key="step1_submit") and user_input:
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
            st.markdown(f'<div class="assistant-message">🤖 {assistant_msg}</div>', unsafe_allow_html=True)
        
        experience_level = st.selectbox(
            "Select your experience level:",
            ["Entry Level (0-2 years)", "Mid Level (3-5 years)", "Senior Level (6-10 years)", "Lead/Principal (10+ years)"]
        )
        
        if st.button("Continue", key="step2_submit"):
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
            st.markdown(f'<div class="assistant-message">🤖 {assistant_msg}</div>', unsafe_allow_html=True)
        
        interview_type = st.selectbox(
            "Choose interview type:",
            ["Technical Interview", "Behavioral Interview", "Case Study Interview", "Mixed (Technical + Behavioral)"]
        )
        
        if st.button("Next", key="step3_submit"):
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
            st.markdown(f'<div class="assistant-message">🤖 {assistant_msg}</div>', unsafe_allow_html=True)
        
        skills = st.text_area(
            "List your key skills/technologies:",
            placeholder="e.g., Python, React, Machine Learning, AWS, SQL, Leadership, Project Management...",
            height=100
        )
        
        if st.button("Continue", key="step4_submit") and skills:
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
            st.markdown(f'<div class="assistant-message">🤖 {assistant_msg}</div>', unsafe_allow_html=True)
        
        duration = st.selectbox(
            "Interview duration:",
            ["15 minutes (5-7 questions)", "30 minutes (8-12 questions)", "45 minutes (13-18 questions)", "60 minutes (20+ questions)"]
        )
        
        if st.button("Finish Setup", key="step5_submit"):
            st.session_state.setup_conversation.append({"role": "user", "content": duration})
            st.session_state.interview_config['duration'] = duration
            st.session_state.setup_step = 6
            st.rerun()
    
    elif st.session_state.setup_step == 6:
        # Final step - save and create interview
        st.markdown("""
        <div class="completion-card">
            <h2>🎉 Setup Complete!</h2>
            <p>Your personalized mock interview has been created and is ready to start.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Save interview configuration
        interview_id = save_interview_setup(
            user_id=st.session_state.user_id,
            job_role=st.session_state.interview_config['job_role'],
            experience_level=st.session_state.interview_config['experience_level'],
            interview_type=st.session_state.interview_config['interview_type'],
            skills=st.session_state.interview_config['skills'],
            duration=st.session_state.interview_config['duration']
        )
        
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col2:
            if st.button("🚀 Start Interview Now", key="start_interview", type="primary"):
                st.session_state.current_interview_id = interview_id
                # Clear setup state
                del st.session_state.setup_conversation
                del st.session_state.setup_step
                del st.session_state.interview_config
                st.switch_page("pages/interview.py")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("📊 Return to Dashboard", key="return_dashboard"):
                # Clear setup state
                del st.session_state.setup_conversation
                del st.session_state.setup_step
                del st.session_state.interview_config
                st.switch_page("main.py")
    
    st.markdown('</div></div>', unsafe_allow_html=True)
if __name__ == "__main__":
    main()
