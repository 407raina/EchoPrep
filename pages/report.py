import streamlit as st
import json
from utils.database import get_interview_mock, get_interview_session

# Check authentication
if 'authenticated' not in st.session_state or not st.session_state.authenticated:
    st.error("Please login to access this page")
    if st.button("← Back to Login"):
        st.switch_page("main.py")
    st.stop()

st.set_page_config(
    page_title="Interview Report - EchoPrep",
    page_icon="📊",
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
    max-width: 1200px;
    margin: 0 auto;
    padding: 24px;
    background: #FFFFFF;
}

.report-header {
    text-align: center;
    margin-bottom: 32px;
    padding: 32px 24px;
    background: #FFFFFF;
    border-radius: 12px;
    border: 1px solid #e5e7eb;
}

.report-title {
    font-family: 'Inter', sans-serif;
    color: #1a1a1a;
    font-size: 2.25rem;
    font-weight: 700;
    margin-bottom: 8px;
    line-height: 1.2;
}

.report-subtitle {
    font-family: 'Inter', sans-serif;
    color: #6b7280;
    font-size: 1rem;
    font-weight: 400;
    margin: 0;
}

.score-container {
    text-align: center;
    margin: 32px 0;
    padding: 32px;
    background: #f8fafc;
    border-radius: 12px;
    border: 1px solid #e2e8f0;
}

.score-circle {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 120px;
    height: 120px;
    border-radius: 50%;
    font-size: 2rem;
    font-weight: 700;
    color: white;
    margin-bottom: 16px;
    font-family: 'Inter', sans-serif;
}

.score-excellent { background: #10b981; }
.score-good { background: #3b82f6; }
.score-average { background: #f59e0b; }
.score-poor { background: #ef4444; }

.score-label {
    font-size: 1.125rem;
    font-weight: 600;
    color: #374151;
    margin-top: 8px;
}

.metrics-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 16px;
    margin: 24px 0;
}

.metric-card {
    background: #FFFFFF;
    border: 1px solid #e5e7eb;
    border-radius: 8px;
    padding: 20px;
    text-align: center;
    transition: all 0.3s ease;
}

.metric-card:hover {
    border-color: #3b82f6;
    box-shadow: 0 4px 12px rgba(59, 130, 246, 0.1);
}

.metric-value {
    font-size: 1.5rem;
    font-weight: 700;
    color: #3b82f6;
    margin-bottom: 4px;
}

.metric-label {
    font-size: 0.875rem;
    color: #6b7280;
    font-weight: 500;
}

.feedback-section {
    background: #FFFFFF;
    border: 1px solid #e5e7eb;
    border-radius: 8px;
    padding: 24px;
    margin: 24px 0;
}

.section-title {
    font-size: 1.25rem;
    font-weight: 600;
    color: #1a1a1a;
    margin-bottom: 16px;
    padding-bottom: 8px;
    border-bottom: 2px solid #e5e7eb;
}

.strength-item {
    background: #f0fdf4;
    border: 1px solid #bbf7d0;
    border-left: 4px solid #10b981;
    border-radius: 6px;
    padding: 12px 16px;
    margin: 8px 0;
    font-size: 0.95rem;
    line-height: 1.5;
}

.improvement-item {
    background: #fffbeb;
    border: 1px solid #fed7aa;
    border-left: 4px solid #f59e0b;
    border-radius: 6px;
    padding: 12px 16px;
    margin: 8px 0;
    font-size: 0.95rem;
    line-height: 1.5;
}

.recommendation-item {
    background: #eff6ff;
    border: 1px solid #bfdbfe;
    border-left: 4px solid #3b82f6;
    border-radius: 6px;
    padding: 12px 16px;
    margin: 8px 0;
    font-size: 0.95rem;
    line-height: 1.5;
}

.transcript-section {
    background: #f9fafb;
    border: 1px solid #e5e7eb;
    border-radius: 8px;
    padding: 20px;
    margin: 24px 0;
}

.transcript-box {
    background: #FFFFFF;
    border: 1px solid #d1d5db;
    border-radius: 6px;
    padding: 16px;
    margin: 12px 0;
    max-height: 400px;
    overflow-y: auto;
    font-family: 'Inter', sans-serif;
    font-size: 0.9rem;
    line-height: 1.6;
}

.qa-pair {
    margin-bottom: 20px;
    padding-bottom: 16px;
    border-bottom: 1px solid #e5e7eb;
}

.question-text {
    font-weight: 600;
    color: #1a1a1a;
    margin-bottom: 8px;
}

.answer-text {
    color: #4b5563;
    line-height: 1.6;
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

/* Hide Streamlit branding */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

def get_score_class(score):
    """Get CSS class for score based on value"""
    if score >= 85:
        return "score-excellent"
    elif score >= 70:
        return "score-good"
    elif score >= 50:
        return "score-average"
    else:
        return "score-poor"

def get_score_label(score):
    """Get label for score based on value"""
    if score >= 85:
        return "Excellent"
    elif score >= 70:
        return "Good"
    elif score >= 50:
        return "Average"
    else:
        return "Needs Improvement"

def main():
    """Main report function"""
    
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
    
    # Header
    st.markdown("""
    <div class="main-container">
        <div class="report-header">
            <h1 class="report-title">📊 Interview Report</h1>
            <p class="report-subtitle">Your performance analysis and feedback</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Back button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("← Back to Dashboard", key="back_btn"):
            st.switch_page("main.py")
    
    # Interview details
    st.markdown('<div class="feedback-section">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📋 Interview Details</div>', unsafe_allow_html=True)
    
    col_details1, col_details2 = st.columns(2)
    with col_details1:
        st.markdown(f"**Position:** {interview_data.get('job_role', 'N/A')}")
        st.markdown(f"**Experience Level:** {interview_data.get('experience_level', 'N/A')}")
    
    with col_details2:
        st.markdown(f"**Interview Type:** {interview_data.get('interview_type', 'N/A')}")
        st.markdown(f"**Key Skills:** {interview_data.get('skills', 'N/A')}")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Try to get session data (if available)
    session_data = None
    try:
        session_data = get_interview_session(st.session_state.current_interview_id)
    except:
        pass
    
    if session_data and 'feedback' in session_data:
        try:
            feedback = json.loads(session_data['feedback'])
            overall_score = feedback.get('overall_score', 75)
            
            # Score display
            score_class = get_score_class(overall_score)
            score_label = get_score_label(overall_score)
            
            st.markdown(f"""
            <div class="score-container">
                <div class="score-circle {score_class}">
                    {overall_score}%
                </div>
                <div class="score-label">{score_label} Performance</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Detailed metrics
            if 'detailed_scores' in feedback:
                st.markdown('<div class="metrics-grid">', unsafe_allow_html=True)
                for metric, score in feedback['detailed_scores'].items():
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-value">{score}%</div>
                        <div class="metric-label">{metric.replace('_', ' ').title()}</div>
                    </div>
                    """, unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            # Strengths
            if 'strengths' in feedback and feedback['strengths']:
                st.markdown('<div class="feedback-section">', unsafe_allow_html=True)
                st.markdown('<div class="section-title">💪 Strengths</div>', unsafe_allow_html=True)
                
                for strength in feedback['strengths']:
                    st.markdown(f'<div class="strength-item">✅ {strength}</div>', unsafe_allow_html=True)
                
                st.markdown('</div>', unsafe_allow_html=True)
            
            # Areas for improvement
            if 'improvements' in feedback and feedback['improvements']:
                st.markdown('<div class="feedback-section">', unsafe_allow_html=True)
                st.markdown('<div class="section-title">🎯 Areas for Improvement</div>', unsafe_allow_html=True)
                
                for improvement in feedback['improvements']:
                    st.markdown(f'<div class="improvement-item">🔄 {improvement}</div>', unsafe_allow_html=True)
                
                st.markdown('</div>', unsafe_allow_html=True)
            
            # Recommendations
            if 'recommendations' in feedback and feedback['recommendations']:
                st.markdown('<div class="feedback-section">', unsafe_allow_html=True)
                st.markdown('<div class="section-title">💡 Recommendations</div>', unsafe_allow_html=True)
                
                for recommendation in feedback['recommendations']:
                    st.markdown(f'<div class="recommendation-item">💡 {recommendation}</div>', unsafe_allow_html=True)
                
                st.markdown('</div>', unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"Error parsing feedback data: {e}")
    
    else:
        # Default display when no detailed feedback is available
        st.markdown(f"""
        <div class="score-container">
            <div class="score-circle score-good">
                85%
            </div>
            <div class="score-label">Good Performance</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<div class="feedback-section">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">📝 General Feedback</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="strength-item">✅ You completed the interview successfully</div>
        <div class="strength-item">✅ Good engagement with the questions</div>
        <div class="recommendation-item">💡 Continue practicing to improve your responses</div>
        <div class="recommendation-item">💡 Focus on providing specific examples in your answers</div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Transcript section (if available)
    if session_data and 'transcript' in session_data and session_data['transcript']:
        st.markdown('<div class="transcript-section">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">📝 Interview Transcript</div>', unsafe_allow_html=True)
        
        # Parse and display transcript
        transcript_lines = session_data['transcript'].split('\n\n')
        
        st.markdown('<div class="transcript-box">', unsafe_allow_html=True)
        for i, line_pair in enumerate(transcript_lines):
            if line_pair.strip():
                lines = line_pair.split('\n')
                if len(lines) >= 2:
                    question = lines[0].replace('Q: ', '')
                    answer = lines[1].replace('A: ', '')
                    
                    st.markdown(f"""
                    <div class="qa-pair">
                        <div class="question-text">Q: {question}</div>
                        <div class="answer-text">A: {answer}</div>
                    </div>
                    """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Action buttons
    st.markdown("---")
    col_action1, col_action2, col_action3 = st.columns([1, 1, 1])
    
    with col_action1:
        if st.button("🆕 Create New Interview", use_container_width=True):
            st.switch_page("pages/setup.py")
    
    with col_action2:
        if st.button("🔄 Retake Interview", use_container_width=True):
            # Reset interview session and restart
            if 'interview_session' in st.session_state:
                del st.session_state['interview_session']
            st.switch_page("pages/interview.py")
    
    with col_action3:
        if st.button("🏠 Back to Dashboard", use_container_width=True):
            st.switch_page("main.py")

if __name__ == "__main__":
    main()
