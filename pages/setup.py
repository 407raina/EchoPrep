import stst.set_page_config(
    page_title="Create Mock Interview - EchoPrep",
    page_icon="🎯",
    layout="wide"
)it as st
import json
from utils.auth import require_authentication, get_current_user_id
from utils.ai_services import conversational_setup_assistant, generate_interview_questions
from utils.database import create_interview_mock, update_interview_questions

# Require authentication
require_authentication()

st.set_page_config(
    page_title="Create Mock Interview - EchoPrep AI",
    page_icon="🎯",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
.setup-container {
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
}

.chat-message {
    padding: 15px;
    margin: 10px 0;
    border-radius: 10px;
    border-left: 4px solid #1f77b4;
}

.user-message {
    background-color: #e8f4f8;
    margin-left: 50px;
}

.ai-message {
    background-color: #f0f2f6;
    margin-right: 50px;
}

.info-box {
    background-color: #fff3cd;
    border: 1px solid #ffeaa7;
    border-radius: 8px;
    padding: 15px;
    margin: 15px 0;
}

.success-box {
    background-color: #d4edda;
    border: 1px solid #c3e6cb;
    border-radius: 8px;
    padding: 15px;
    margin: 15px 0;
}
</style>
""", unsafe_allow_html=True)

def main():
    """Main setup page function"""
    
    st.markdown('<div class="setup-container">', unsafe_allow_html=True)
    
    # Header
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title("🎯 Create New Mock Interview")
        st.write("Let me help you set up a personalized mock interview!")
    
    with col2:
        if st.button("← Back to Dashboard"):
            st.switch_page("main.py")
    
    st.markdown("---")
    
    # Initialize session state
    if 'setup_conversation' not in st.session_state:
        st.session_state.setup_conversation = []
        st.session_state.extracted_info = {
            'job_role': None,
            'experience_level': None,
            'interview_type': None,
            'skills': None
        }
        st.session_state.setup_complete = False
    
    # Display conversation history
    if st.session_state.setup_conversation:
        st.subheader("Conversation")
        
        for message in st.session_state.setup_conversation:
            if message['role'] == 'user':
                st.markdown(f'<div class="chat-message user-message"><strong>You:</strong> {message["content"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="chat-message ai-message"><strong>AI Assistant:</strong> {message["content"]}</div>', unsafe_allow_html=True)
    
    # Show current extracted information
    if any(st.session_state.extracted_info.values()):
        st.subheader("Interview Details")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.session_state.extracted_info['job_role']:
                st.success(f"**Job Role:** {st.session_state.extracted_info['job_role']}")
            if st.session_state.extracted_info['experience_level']:
                st.success(f"**Experience Level:** {st.session_state.extracted_info['experience_level']}")
        
        with col2:
            if st.session_state.extracted_info['interview_type']:
                st.success(f"**Interview Type:** {st.session_state.extracted_info['interview_type']}")
            if st.session_state.extracted_info['skills']:
                st.success(f"**Skills/Technologies:** {st.session_state.extracted_info['skills']}")
    
    # Input section
    if not st.session_state.setup_complete:
        st.markdown("---")
        
        # Initial message if no conversation yet
        if not st.session_state.setup_conversation:
            initial_message = "Hi! I'm here to help you create a personalized mock interview. To get started, could you tell me what job role you're preparing for?"
            st.session_state.setup_conversation.append({
                'role': 'assistant',
                'content': initial_message
            })
            st.markdown(f'<div class="chat-message ai-message"><strong>AI Assistant:</strong> {initial_message}</div>', unsafe_allow_html=True)
        
        # User input
        user_input = st.text_input("Your response:", key="user_input", placeholder="Type your response here...")
        
        col1, col2 = st.columns([1, 3])
        
        with col1:
            if st.button("Send", type="primary", disabled=not user_input.strip()):
                process_user_input(user_input.strip())
                st.rerun()
        
        with col2:
            if st.button("Skip Setup (Use Defaults)"):
                use_default_setup()
                st.rerun()
    
    else:
        # Setup complete - show summary and create interview
        st.markdown("---")
        st.markdown('<div class="success-box">', unsafe_allow_html=True)
        st.success("🎉 Great! I have all the information needed to create your mock interview.")
        
        st.write("**Interview Summary:**")
        st.write(f"• **Job Role:** {st.session_state.extracted_info['job_role']}")
        st.write(f"• **Experience Level:** {st.session_state.extracted_info['experience_level']}")
        st.write(f"• **Interview Type:** {st.session_state.extracted_info['interview_type']}")
        st.write(f"• **Skills/Technologies:** {st.session_state.extracted_info['skills']}")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            if st.button("Create Interview", type="primary", use_container_width=True):
                create_interview()
        
        with col2:
            if st.button("Modify Details", use_container_width=True):
                st.session_state.setup_complete = False
                st.rerun()
        
        with col3:
            if st.button("Start Over", use_container_width=True):
                reset_setup()
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

def process_user_input(user_input: str):
    """Process user input through AI assistant"""
    
    # Add user message to conversation
    st.session_state.setup_conversation.append({
        'role': 'user',
        'content': user_input
    })
    
    # Get AI response
    conversation_history = [msg['content'] for msg in st.session_state.setup_conversation]
    
    ai_response = conversational_setup_assistant(user_input, conversation_history)
    
    # Add AI response to conversation
    st.session_state.setup_conversation.append({
        'role': 'assistant',
        'content': ai_response['response']
    })
    
    # Update extracted information
    for key, value in ai_response.get('extracted_info', {}).items():
        if value:
            st.session_state.extracted_info[key] = value
    
    # Check if setup is complete
    if all(st.session_state.extracted_info.values()):
        st.session_state.setup_complete = True

def use_default_setup():
    """Use default setup for quick start"""
    st.session_state.extracted_info = {
        'job_role': 'Software Engineer',
        'experience_level': 'Mid Level',
        'interview_type': 'Mixed',
        'skills': 'Python, JavaScript, React'
    }
    st.session_state.setup_complete = True
    
    # Add message to conversation
    st.session_state.setup_conversation.append({
        'role': 'assistant',
        'content': "I've set up a default interview for a Mid Level Software Engineer position with Mixed (technical and behavioral) questions focusing on Python, JavaScript, and React. You can modify these details if needed."
    })

def create_interview():
    """Create the interview mock and redirect to interview page"""
    
    user_id = get_current_user_id()
    
    # Create interview mock in database
    mock_id = create_interview_mock(
        user_id=user_id,
        job_role=st.session_state.extracted_info['job_role'],
        experience_level=st.session_state.extracted_info['experience_level'],
        interview_type=st.session_state.extracted_info['interview_type'],
        skills=st.session_state.extracted_info['skills']
    )
    
    # Generate questions
    with st.spinner("Generating interview questions..."):
        questions = generate_interview_questions(
            job_role=st.session_state.extracted_info['job_role'],
            experience_level=st.session_state.extracted_info['experience_level'],
            interview_type=st.session_state.extracted_info['interview_type'],
            skills=st.session_state.extracted_info['skills']
        )
        
        # Store questions in database
        update_interview_questions(mock_id, json.dumps(questions))
    
    # Set current interview and redirect
    st.session_state.current_interview_id = mock_id
    
    # Clear setup state
    reset_setup()
    
    st.success("Interview created successfully! Redirecting to interview...")
    st.switch_page("pages/interview.py")

def reset_setup():
    """Reset setup state"""
    st.session_state.setup_conversation = []
    st.session_state.extracted_info = {
        'job_role': None,
        'experience_level': None,
        'interview_type': None,
        'skills': None
    }
    st.session_state.setup_complete = False

if __name__ == "__main__":
    main()
