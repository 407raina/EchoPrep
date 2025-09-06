import strest.set_page_config(
    page_title="Interview in Progress - EchoPrep",
    page_icon="🎙️",
    layout="wide"
) as st
import json
import time
from utils.auth import require_authentication, get_current_user_id
from utils.database import get_interview_mock, create_interview_session
from utils.audio_utils import text_to_speech, play_audio_streamlit, get_microphone_input, process_audio_file
from utils.ai_services import analyze_interview_performance

# Require authentication
require_authentication()

st.set_page_config(
    page_title="Interview in Progress - EchoPrep AI",
    page_icon="🎙️",
    layout="wide"
)

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
