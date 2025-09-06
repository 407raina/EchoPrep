import sst.set_page_config(
    page_title="Interview Report - EchoPrep",
    page_icon="📊",
    layout="wide"
)lit as st
import json
from utils.auth import require_authentication
from utils.database import get_interview_mock, get_interview_session

# Require authentication
require_authentication()

st.set_page_config(
    page_title="Interview Report - EchoPrep AI",
    page_icon="📊",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
.report-container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
}

.score-circle {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 120px;
    height: 120px;
    border-radius: 50%;
    font-size: 2rem;
    font-weight: bold;
    color: white;
    margin: 0 auto;
}

.score-excellent { background-color: #28a745; }
.score-good { background-color: #17a2b8; }
.score-average { background-color: #ffc107; color: #333; }
.score-poor { background-color: #dc3545; }

.feedback-section {
    background-color: #f8f9fa;
    border-left: 4px solid #1f77b4;
    padding: 20px;
    margin: 15px 0;
    border-radius: 8px;
}

.strength-item {
    background-color: #d4edda;
    border: 1px solid #c3e6cb;
    border-radius: 6px;
    padding: 10px;
    margin: 8px 0;
}

.improvement-item {
    background-color: #fff3cd;
    border: 1px solid #ffeaa7;
    border-radius: 6px;
    padding: 10px;
    margin: 8px 0;
}

.recommendation-item {
    background-color: #cce7ff;
    border: 1px solid #9bd7ff;
    border-radius: 6px;
    padding: 10px;
    margin: 8px 0;
}

.transcript-box {
    background-color: #f9f9f9;
    border: 1px solid #ddd;
    border-radius: 8px;
    padding: 15px;
    margin: 10px 0;
    max-height: 400px;
    overflow-y: auto;
}

.metric-card {
    background-color: white;
    border: 1px solid #ddd;
    border-radius: 8px;
    padding: 15px;
    text-align: center;
    margin: 10px 0;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}
</style>
""", unsafe_allow_html=True)

def main():
    """Main report page function"""
    
    # Check if interview ID is set
    if 'current_interview_id' not in st.session_state:
        st.error("No interview selected. Please go back to the dashboard.")
        if st.button("← Back to Dashboard"):
            st.switch_page("main.py")
        return
    
    # Get interview and session details
    interview = get_interview_mock(st.session_state.current_interview_id)
    session = get_interview_session(st.session_state.current_interview_id)
    
    if not interview or not session:
        st.error("Interview report not found.")
        if st.button("← Back to Dashboard"):
            st.switch_page("main.py")
        return
    
    st.markdown('<div class="report-container">', unsafe_allow_html=True)
    
    # Header
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title("📊 Interview Performance Report")
        st.write(f"**Position:** {interview['job_role']} ({interview['experience_level']})")
        st.write(f"**Type:** {interview['interview_type']} | **Focus:** {interview['skills']}")
        st.write(f"**Completed:** {session['completed_at']}")
    
    with col2:
        if st.button("← Back to Dashboard"):
            st.switch_page("main.py")
        
        if st.button("📄 Download Report", disabled=True):
            st.info("Download feature coming soon!")
    
    st.markdown("---")
    
    # Parse feedback
    try:
        feedback = json.loads(session['feedback'])
    except (json.JSONDecodeError, TypeError):
        st.error("Error loading feedback data.")
        return
    
    # Overall Score Section
    show_overall_score(feedback.get('overall_score', 0))
    
    st.markdown("---")
    
    # Detailed Feedback Sections
    col1, col2 = st.columns(2)
    
    with col1:
        show_detailed_feedback(feedback.get('feedback', {}))
        show_strengths(feedback.get('strengths', []))
    
    with col2:
        show_improvements(feedback.get('areas_for_improvement', []))
        show_recommendations(feedback.get('recommendations', []))
    
    st.markdown("---")
    
    # Transcript Section
    show_transcript(session['transcript'])
    
    st.markdown('</div>', unsafe_allow_html=True)

def show_overall_score(score):
    """Display overall performance score"""
    
    st.subheader("Overall Performance")
    
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col2:
        # Determine score category and color
        if score >= 85:
            score_class = "score-excellent"
            score_text = "Excellent"
        elif score >= 70:
            score_class = "score-good"
            score_text = "Good"
        elif score >= 50:
            score_class = "score-average"
            score_text = "Average"
        else:
            score_class = "score-poor"
            score_text = "Needs Work"
        
        st.markdown(f'''
        <div class="score-circle {score_class}">
            {score}%
        </div>
        <div style="text-align: center; margin-top: 10px; font-size: 1.2rem; font-weight: bold;">
            {score_text}
        </div>
        ''', unsafe_allow_html=True)

def show_detailed_feedback(feedback_details):
    """Display detailed feedback metrics"""
    
    st.subheader("Detailed Analysis")
    
    metrics = {
        "Communication Clarity": feedback_details.get('clarity', 'No feedback available'),
        "Technical Accuracy": feedback_details.get('technical_accuracy', 'No feedback available'),
        "Problem Solving": feedback_details.get('problem_solving', 'No feedback available'),
        "Confidence Level": feedback_details.get('confidence', 'No feedback available')
    }
    
    for metric, feedback_text in metrics.items():
        st.markdown(f'''
        <div class="feedback-section">
            <h4>{metric}</h4>
            <p>{feedback_text}</p>
        </div>
        ''', unsafe_allow_html=True)

def show_strengths(strengths):
    """Display identified strengths"""
    
    st.subheader("✅ Key Strengths")
    
    if strengths:
        for strength in strengths:
            st.markdown(f'''
            <div class="strength-item">
                <strong>✓</strong> {strength}
            </div>
            ''', unsafe_allow_html=True)
    else:
        st.write("No specific strengths identified in this session.")

def show_improvements(improvements):
    """Display areas for improvement"""
    
    st.subheader("📈 Areas for Improvement")
    
    if improvements:
        for improvement in improvements:
            st.markdown(f'''
            <div class="improvement-item">
                <strong>⚠️</strong> {improvement}
            </div>
            ''', unsafe_allow_html=True)
    else:
        st.write("No specific areas for improvement identified.")

def show_recommendations(recommendations):
    """Display actionable recommendations"""
    
    st.subheader("💡 Recommendations")
    
    if recommendations:
        for rec in recommendations:
            st.markdown(f'''
            <div class="recommendation-item">
                <strong>💡</strong> {rec}
            </div>
            ''', unsafe_allow_html=True)
    else:
        st.write("No specific recommendations available.")

def show_transcript(transcript):
    """Display interview transcript"""
    
    st.subheader("📝 Interview Transcript")
    
    with st.expander("View Full Transcript", expanded=False):
        st.markdown('<div class="transcript-box">', unsafe_allow_html=True)
        
        if transcript:
            # Format transcript for better readability
            lines = transcript.split('\\n')
            for line in lines:
                if line.strip():
                    if line.startswith('Q:'):
                        st.markdown(f"**{line}**")
                    elif line.startswith('A:'):
                        st.markdown(f"*{line}*")
                    else:
                        st.write(line)
        else:
            st.write("No transcript available.")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Action buttons
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔄 Practice Again", use_container_width=True):
            st.switch_page("pages/setup.py")
    
    with col2:
        if st.button("📊 View All Reports", use_container_width=True):
            st.switch_page("main.py")
    
    with col3:
        if st.button("📤 Share Report", use_container_width=True, disabled=True):
            st.info("Share feature coming soon!")

if __name__ == "__main__":
    main()
