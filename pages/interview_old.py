import streamlit as st
import json
import time
from utils.auth import get_current_user_id
from utils.database import get_interview_mock, create_interview_session
from utils.audio_utils import text_to_speech, create_audio_player
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

.interview-card {
    background: #FFFFFF;
    border-radius: 12px;
    padding: 24px;
    border: 1px solid #e5e7eb;
    margin: 24px 0;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
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

.recording-indicator {
    background: #ef4444;
    color: white;
    padding: 12px 20px;
    border-radius: 8px;
    text-align: center;
    font-weight: 600;
    font-family: 'Inter', sans-serif;
    margin: 16px 0;
    animation: pulse 2s infinite;
}

@keyframes pulse {
    0% { opacity: 1; }
    50% { opacity: 0.7; }
    100% { opacity: 1; }
}

.voice-controls {
    display: flex;
    gap: 12px;
    justify-content: center;
    margin: 20px 0;
    flex-wrap: wrap;
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
    border: 1px solid #d1d5db !important;
    border-radius: 8px !important;
    padding: 12px 16px !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.95rem !important;
    line-height: 1.5 !important;
    resize: vertical !important;
    min-height: 120px !important;
}

.stTextArea > div > div > textarea:focus {
    border-color: #3b82f6 !important;
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1) !important;
    outline: none !important;
}

.audio-player {
    margin: 16px 0;
    padding: 16px;
    background: #f9fafb;
    border-radius: 8px;
    border: 1px solid #e5e7eb;
}

/* Secondary button styles */
.stButton .secondary-btn {
    background: #f9fafb !important;
    color: #374151 !important;
    border: 1px solid #d1d5db !important;
}

.stButton .secondary-btn:hover {
    background: #f3f4f6 !important;
    border-color: #9ca3af !important;
}

/* Hide Streamlit branding */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)
        border-radius: 15px;
        text-align: center;
        font-weight: 600;
        margin: 20px 0;
        animation: pulse 2s infinite;
        box-shadow: 0 8px 25px rgba(229, 62, 62, 0.3);
    }
    
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.7; }
        100% { opacity: 1; }
    }
    
    .controls-section {
        display: flex;
        gap: 15px;
        justify-content: center;
        flex-wrap: wrap;
        margin: 30px 0;
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
        min-width: 150px;
    }
    
    [data-testid="stButton"] > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 35px rgba(100, 127, 188, 0.4);
    }
    
    .record-button {
        background: linear-gradient(135deg, #e53e3e, #c53030) !important;
        box-shadow: 0 8px 25px rgba(229, 62, 62, 0.3) !important;
    }
    
    .record-button:hover {
        box-shadow: 0 12px 35px rgba(229, 62, 62, 0.4) !important;
    }
    
    .success-button {
        background: linear-gradient(135deg, #48bb78, #38a169) !important;
        box-shadow: 0 8px 25px rgba(72, 187, 120, 0.3) !important;
    }
    
    .success-button:hover {
        box-shadow: 0 12px 35px rgba(72, 187, 120, 0.4) !important;
    }
    
    [data-testid="stTextArea"] > div > div > textarea {
        border-radius: 15px;
        border: 2px solid #AED6CF;
        padding: 20px;
        font-family: 'Crimson Text', serif;
        font-size: 1.1rem;
        min-height: 150px;
        transition: all 0.3s ease;
    }
    
    [data-testid="stTextArea"] > div > div > textarea:focus {
        border-color: #647FBC;
        box-shadow: 0 0 0 3px rgba(100, 127, 188, 0.1);
    }
    
    .completion-card {
        background: linear-gradient(135deg, #91ADC8, #AED6CF);
        color: white;
        padding: 40px;
        border-radius: 20px;
        text-align: center;
        margin: 30px 0;
        box-shadow: 0 15px 40px rgba(145, 173, 200, 0.3);
    }
    
    .completion-title {
        font-family: 'Playfair Display', serif;
        font-size: 2rem;
        font-weight: 800;
        margin-bottom: 15px;
    }
    
    .completion-text {
        font-family: 'Crimson Text', serif;
        font-size: 1.2rem;
        opacity: 0.9;
    }
    </style>
""", unsafe_allow_html=True)

# Custom CSS
st.markdown("""
<style>
.interview-container {
    max-width: 1000px;
    margin: 0 auto;
    padding: 20px;
}

.question-box {
    background-color: #f8f9fa;
    border: 2px solid #1f77b4;
    border-radius: 10px;
    padding: 20px;
    margin: 20px 0;
    text-align: center;
}

.transcript-box {
    background-color: #f9f9f9;
    border: 1px solid #ddd;
    border-radius: 8px;
    padding: 15px;
    margin: 10px 0;
    min-height: 100px;
    max-height: 300px;
    overflow-y: auto;
}

.progress-indicator {
    background-color: #e9ecef;
    border-radius: 10px;
    padding: 10px;
    margin: 15px 0;
    text-align: center;
}

.status-indicator {
    padding: 10px;
    border-radius: 8px;
    margin: 10px 0;
    text-align: center;
    font-weight: bold;
}

.listening {
    background-color: #d4edda;
    color: #155724;
    border: 1px solid #c3e6cb;
}

.speaking {
    background-color: #fff3cd;
    color: #856404;
    border: 1px solid #ffeaa7;
}

.waiting {
    background-color: #e2e3e5;
    color: #383d41;
    border: 1px solid #d6d8db;
}
</style>
""", unsafe_allow_html=True)

def main():
    """Main interview page function"""
    
    # Check if interview ID is set
    if 'current_interview_id' not in st.session_state:
        st.error("No interview selected. Please go back to the dashboard.")
        if st.button("← Back to Dashboard"):
            st.switch_page("main.py")
        return
    
    # Get interview details
    interview = get_interview_mock(st.session_state.current_interview_id)
    if not interview:
        st.error("Interview not found.")
        return
    
    st.markdown('<div class="interview-container">', unsafe_allow_html=True)
    
    # Header
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title("🎙️ Mock Interview in Progress")
        st.write(f"**Position:** {interview['job_role']} ({interview['experience_level']})")
        st.write(f"**Type:** {interview['interview_type']} | **Focus:** {interview['skills']}")
    
    with col2:
        if st.button("🏠 End Interview", type="secondary"):
            if st.session_state.get('interview_started', False):
                finalize_interview()
            else:
                st.switch_page("main.py")
    
    st.markdown("---")
    
    # Initialize session state
    if 'interview_started' not in st.session_state:
        st.session_state.interview_started = False
        st.session_state.current_question_index = 0
        st.session_state.interview_transcript = []
        st.session_state.questions = []
        st.session_state.interview_status = "waiting"  # waiting, speaking, listening
    
    # Load questions
    if not st.session_state.questions and interview['questions']:
        st.session_state.questions = json.loads(interview['questions'])
    
    if not st.session_state.questions:
        st.error("No questions found for this interview. Please recreate the interview.")
        return
    
    # Progress indicator
    total_questions = len(st.session_state.questions)
    current_question = st.session_state.current_question_index + 1
    progress = st.session_state.current_question_index / total_questions
    
    st.markdown('<div class="progress-indicator">', unsafe_allow_html=True)
    st.write(f"**Question {current_question} of {total_questions}**")
    st.progress(progress)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Start interview button
    if not st.session_state.interview_started:
        st.markdown('<div class="question-box">', unsafe_allow_html=True)
        st.write("### Ready to start your mock interview?")
        st.write("The AI interviewer will ask you questions and you can respond using voice or text.")
        st.write("Make sure your microphone is working for the best experience!")
        
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("🎯 Start Interview", type="primary", use_container_width=True):
                st.session_state.interview_started = True
                st.session_state.interview_status = "speaking"
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        return
    
    # Interview in progress
    if st.session_state.current_question_index < total_questions:
        show_current_question()
    else:
        finalize_interview()
    
    st.markdown('</div>', unsafe_allow_html=True)

def show_current_question():
    """Display current question and handle response"""
    
    current_question = st.session_state.questions[st.session_state.current_question_index]
    
    # Status indicator
    status_class = st.session_state.interview_status
    status_text = {
        "speaking": "🔊 AI is asking a question...",
        "listening": "🎤 Your turn to respond",
        "waiting": "⏳ Processing..."
    }
    
    st.markdown(f'<div class="status-indicator {status_class}">{status_text[st.session_state.interview_status]}</div>', unsafe_allow_html=True)
    
    # Question display
    st.markdown('<div class="question-box">', unsafe_allow_html=True)
    st.write("### Current Question:")
    st.write(f"**{current_question}**")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Audio playback for question
    if st.session_state.interview_status == "speaking":
        with st.spinner("Generating audio..."):
            audio_data = text_to_speech(current_question)
            if audio_data:
                play_audio_streamlit(audio_data, autoplay=True)
        
        # Automatically switch to listening after a delay
        time.sleep(2)
        st.session_state.interview_status = "listening"
        st.rerun()
    
    # Response input section
    elif st.session_state.interview_status == "listening":
        st.markdown("### Your Response")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Text input option
            response_text = st.text_area(
                "Type your response:",
                height=150,
                key=f"response_{st.session_state.current_question_index}",
                placeholder="Type your answer here or upload an audio file..."
            )
        
        with col2:
            st.write("**Audio Response:**")
            
            # Audio file upload
            audio_file = st.file_uploader(
                "Upload audio response",
                type=['wav', 'mp3', 'ogg'],
                key=f"audio_{st.session_state.current_question_index}"
            )
            
            if audio_file:
                with st.spinner("Processing audio..."):
                    transcribed_text = process_audio_file(audio_file)
                    if transcribed_text:
                        st.text_area("Transcribed text:", value=transcribed_text, height=100, disabled=True)
                        response_text = transcribed_text
        
        # Submit response
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            if st.button("⏭️ Skip Question", use_container_width=True):
                record_response("Question skipped by user.")
                move_to_next_question()
        
        with col2:
            if st.button("🎤 Record Audio", use_container_width=True, disabled=True):
                st.info("Live audio recording requires additional setup. Please use audio file upload or text input.")
        
        with col3:
            if st.button("✅ Submit Response", type="primary", use_container_width=True, disabled=not response_text.strip()):
                record_response(response_text.strip())
                move_to_next_question()
    
    # Show transcript
    if st.session_state.interview_transcript:
        with st.expander("Interview Transcript", expanded=False):
            st.markdown('<div class="transcript-box">', unsafe_allow_html=True)
            for entry in st.session_state.interview_transcript:
                st.write(f"**Q:** {entry['question']}")
                st.write(f"**A:** {entry['response']}")
                st.write("---")
            st.markdown('</div>', unsafe_allow_html=True)

def record_response(response_text: str):
    """Record user response to transcript"""
    
    current_question = st.session_state.questions[st.session_state.current_question_index]
    
    st.session_state.interview_transcript.append({
        'question': current_question,
        'response': response_text,
        'timestamp': time.time()
    })

def move_to_next_question():
    """Move to next question or finalize interview"""
    
    st.session_state.current_question_index += 1
    st.session_state.interview_status = "speaking"
    st.rerun()

def finalize_interview():
    """Finalize interview and generate feedback"""
    
    st.markdown('<div class="question-box">', unsafe_allow_html=True)
    st.write("### 🎉 Interview Complete!")
    st.write("Thank you for completing the mock interview. Your performance is being analyzed...")
    st.markdown('</div>', unsafe_allow_html=True)
    
    if st.session_state.interview_transcript:
        
        # Generate transcript text
        transcript_text = ""
        for entry in st.session_state.interview_transcript:
            transcript_text += f"Q: {entry['question']}\\n"
            transcript_text += f"A: {entry['response']}\\n\\n"
        
        # Get interview details
        interview = get_interview_mock(st.session_state.current_interview_id)
        
        with st.spinner("Analyzing your performance..."):
            # Generate AI feedback
            analysis = analyze_interview_performance(
                transcript=transcript_text,
                job_role=interview['job_role'],
                experience_level=interview['experience_level'],
                skills=interview['skills']
            )
            
            # Save session to database
            session_id = create_interview_session(
                mock_id=st.session_state.current_interview_id,
                transcript=transcript_text,
                feedback=json.dumps(analysis),
                score=analysis.get('overall_score', 0)
            )
        
        st.success("Analysis complete! Redirecting to your feedback report...")
        
        # Clear interview state
        for key in ['interview_started', 'current_question_index', 'interview_transcript', 'questions', 'interview_status']:
            if key in st.session_state:
                del st.session_state[key]
        
        time.sleep(2)
        st.switch_page("pages/report.py")
    
    else:
        st.warning("No responses recorded. Returning to dashboard...")
        time.sleep(2)
        st.switch_page("main.py")

if __name__ == "__main__":
    main()
