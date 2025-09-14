import streamlit as st
import json
import time
from utils.auth import get_current_user_id
from utils.database import get_interview_mock, create_interview_session
from utils.audio_utils import text_to_speech, create_audio_player, get_audio_recorder, speech_to_text_local
from utils.ai_services import analyze_interview_performance

# Check authentication
if 'authenticated' not in st.session_state or not st.session_state.authenticated:
    st.error("Please login to access this page")
    if st.button("← Back to Login"):
        st.switch_page("main.py")
    st.stop()

st.set_page_config(
    page_title="Interview in Progress - EchoPrep",
    page_icon="🎙️",
    layout="wide"
)

# Clean white UI styling
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

.stApp {
    background: #FFFFFF;
    font-family: 'Inter', sans-serif;
    color: #1a1a1a;
}

.main-container {
    max-width: 1000px;
    margin: 0 auto;
    padding: 24px;
    background: #FFFFFF;
}

.interview-header {
    text-align: center;
    margin-bottom: 32px;
    padding: 32px 24px;
    background: #FFFFFF;
    border-radius: 12px;
    border: 1px solid #e5e7eb;
}

.interview-title {
    font-family: 'Inter', sans-serif;
    color: #1a1a1a;
    font-size: 2.25rem;
    font-weight: 700;
    margin-bottom: 8px;
    line-height: 1.2;
}

.interview-subtitle {
    font-family: 'Inter', sans-serif;
    color: #6b7280;
    font-size: 1rem;
    font-weight: 400;
    margin: 0;
}

.question-section {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-left: 4px solid #3b82f6;
    border-radius: 8px;
    padding: 24px;
    margin: 20px 0;
}

.question-text {
    color: #1a1a1a;
    font-size: 1.125rem;
    font-weight: 500;
    line-height: 1.6;
    margin: 0;
    font-family: 'Inter', sans-serif;
}

.response-section {
    background: #FFFFFF;
    border: 1px solid #d1d5db;
    border-radius: 8px;
    padding: 24px;
    margin: 20px 0;
    transition: all 0.3s ease;
}

.response-section:hover {
    border-color: #3b82f6;
    box-shadow: 0 4px 12px rgba(59, 130, 246, 0.1);
}

.timer-display {
    background: #3b82f6;
    color: white;
    padding: 12px 20px;
    border-radius: 8px;
    text-align: center;
    font-size: 1.125rem;
    font-weight: 600;
    font-family: 'Inter', sans-serif;
    margin: 16px 0;
    box-shadow: 0 2px 8px rgba(59, 130, 246, 0.3);
}

.progress-container {
    background: #f3f4f6;
    padding: 16px;
    border-radius: 8px;
    border: 1px solid #e5e7eb;
    margin: 20px 0;
}

.progress-bar-bg {
    background: #e5e7eb;
    height: 6px;
    border-radius: 6px;
    overflow: hidden;
}

.progress-bar {
    background: #3b82f6;
    height: 100%;
    border-radius: 6px;
    transition: width 0.5s ease;
}

.question-counter {
    color: #374151;
    font-weight: 600;
    font-size: 0.875rem;
    font-family: 'Inter', sans-serif;
    margin-bottom: 8px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.completion-card {
    background: #f0f9ff;
    border: 1px solid #bae6fd;
    color: #1a1a1a;
    padding: 32px;
    border-radius: 12px;
    text-align: center;
    margin: 24px 0;
}

.stButton > button {
    background: #3b82f6 !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 12px 24px !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    font-family: 'Inter', sans-serif !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1) !important;
}

.stButton > button:hover {
    background: #2563eb !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3) !important;
}

.stTextArea > div > div > textarea {
    border: 2px solid #e5e7eb !important;
    border-radius: 12px !important;
    padding: 1rem 1.25rem !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.95rem !important;
    line-height: 1.5 !important;
    resize: vertical !important;
    min-height: 120px !important;
    background: #ffffff !important;
    box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06) !important;
    transition: all 0.3s ease !important;
    outline: none !important;
}

.stTextArea > div > div > textarea:hover {
    border-color: #cbd5e1 !important;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06) !important;
}

.stTextArea > div > div > textarea:focus {
    border-color: #3b82f6 !important;
    box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.15), 0 4px 6px -1px rgba(0, 0, 0, 0.1) !important;
    outline: none !important;
    transform: translateY(-1px) !important;
}

.audio-player {
    margin: 16px 0;
    padding: 16px;
    background: #f9fafb;
    border-radius: 8px;
    border: 1px solid #e5e7eb;
}

/* Hide Streamlit branding */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

def main():
    """Main interview function with voice functionality"""
    
    # Check if interview ID is provided
    if 'current_interview_id' not in st.session_state:
        st.error("No interview selected. Please go back to dashboard and select an interview.")
        if st.button("← Back to Dashboard"):
            st.switch_page("main.py")
        st.stop()
    
    # Get interview data
    interview_data = get_interview_mock(st.session_state.current_interview_id)
    if not interview_data:
        st.error("Interview not found.")
        if st.button("← Back to Dashboard"):
            st.switch_page("main.py")
        st.stop()
    
    # Parse questions
    questions = json.loads(interview_data.get('questions', '[]'))
    if not questions:
        st.error("No questions found for this interview.")
        if st.button("← Back to Dashboard"):
            st.switch_page("main.py")
        st.stop()
    
    # Initialize session state
    if 'interview_session' not in st.session_state:
        st.session_state.interview_session = {
            'current_question': 0,
            'responses': [],
            'start_time': time.time(),
            'interview_data': interview_data
        }
    
    # Header
    st.markdown("""
    <div class="main-container">
        <div class="interview-header">
            <h1 class="interview-title">🎙️ Interview in Progress</h1>
            <p class="interview-subtitle">Stay confident and answer naturally</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Back button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("← Back to Dashboard", key="back_btn"):
            st.switch_page("main.py")
    
    current_q = st.session_state.interview_session['current_question']
    total_questions = len(questions)
    
    # Progress indicator
    progress = (current_q + 1) / total_questions
    st.markdown(f"""
    <div class="progress-container">
        <div class="question-counter">Question {current_q + 1} of {total_questions}</div>
        <div class="progress-bar-bg">
            <div class="progress-bar" style="width: {progress * 100}%"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if current_q < total_questions:
        question = questions[current_q]
        
        # Display current question
        st.markdown(f"""
        <div class="question-section">
            <div class="question-text">
                <strong>Question {current_q + 1}:</strong><br>
                {question}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Text-to-speech for question
        col_audio1, col_audio2 = st.columns([1, 3])
        with col_audio1:
            if st.button("🔊 Listen to Question", key=f"listen_q_{current_q}"):
                with st.spinner("Generating audio..."):
                    audio_data = text_to_speech(question)
                    if audio_data:
                        audio_html = create_audio_player(audio_data, autoplay=True)
                        st.markdown(audio_html, unsafe_allow_html=True)
                    else:
                        st.error("Could not generate audio for this question.")
        
        # Response section
        st.markdown('<div class="response-section">', unsafe_allow_html=True)
        
        # Voice response option
        st.markdown("### 🎤 Voice Response")
        st.markdown("Record your answer using the microphone:")
        
        # Import and use audio recorder
        try:
            audio = get_audio_recorder()
            
            if len(audio) > 0:
                st.audio(audio.export().read())
                
                if st.button("📝 Convert Speech to Text", key=f"convert_{current_q}"):
                    with st.spinner("Converting speech to text..."):
                        transcribed_text = speech_to_text_local(audio)
                        st.session_state[f'transcribed_response_{current_q}'] = transcribed_text
                        st.success("Speech converted to text!")
                        st.rerun()
        
        except Exception as e:
            st.info("Voice recording not available. Please use the text input below.")
        
        # Text response option
        st.markdown("### ✍️ Text Response")
        
        # Show transcribed text if available
        initial_value = ""
        if f'transcribed_response_{current_q}' in st.session_state:
            initial_value = st.session_state[f'transcribed_response_{current_q}']
            st.info(f"Transcribed from voice: {initial_value}")
        
        response = st.text_area(
            "Type your answer here:",
            value=initial_value,
            placeholder="Share your thoughts and experience...",
            height=150,
            key=f"response_{current_q}"
        )
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Navigation buttons
        col_nav1, col_nav2, col_nav3 = st.columns([1, 1, 1])
        
        with col_nav2:
            if st.button("Next Question ➡️", key=f"next_{current_q}", type="primary"):
                if response.strip():
                    # Save response
                    st.session_state.interview_session['responses'].append({
                        'question': question,
                        'response': response,
                        'timestamp': time.time()
                    })
                    
                    # Move to next question
                    st.session_state.interview_session['current_question'] += 1
                    
                    # Clear transcribed response
                    if f'transcribed_response_{current_q}' in st.session_state:
                        del st.session_state[f'transcribed_response_{current_q}']
                    
                    st.rerun()
                else:
                    st.error("Please provide a response before proceeding.")
        
        # Show timer
        elapsed_time = time.time() - st.session_state.interview_session['start_time']
        minutes = int(elapsed_time // 60)
        seconds = int(elapsed_time % 60)
        
        st.markdown(f"""
        <div class="timer-display">
            ⏱️ Time Elapsed: {minutes:02d}:{seconds:02d}
        </div>
        """, unsafe_allow_html=True)
    
    else:
        # Interview completed
        st.markdown("""
        <div class="completion-card">
            <h2 style="margin-bottom: 16px; font-weight: 700;">🎉 Interview Completed!</h2>
            <p style="margin-bottom: 24px; font-size: 1.1rem;">Congratulations! You've successfully completed your mock interview.</p>
        </div>
        """, unsafe_allow_html=True)
        
        col_final1, col_final2, col_final3 = st.columns([1, 1, 1])
        
        with col_final1:
            if st.button("📊 View Report", type="primary", use_container_width=True):
                # Save final interview session
                try:
                    from utils.database import complete_interview_with_responses
                    complete_interview_with_responses(
                        st.session_state.current_interview_id,
                        st.session_state.interview_session['responses']
                    )
                except:
                    pass  # Handle if function doesn't exist
                st.switch_page("pages/report.py")
        
        with col_final3:
            if st.button("🏠 Back to Dashboard", use_container_width=True):
                st.switch_page("main.py")

if __name__ == "__main__":
    main()
