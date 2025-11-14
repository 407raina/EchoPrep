import io
import re
import streamlit as st
from PyPDF2 import PdfReader

# Auth gate
if 'authenticated' not in st.session_state or not st.session_state.authenticated:
    st.error("Please login to access this page")
    if st.button("\u2190 Back to Login"):
        st.switch_page("main.py")
    st.stop()

st.set_page_config(page_title="Resume Analyzer - EchoPrep", page_icon="\ud83d\udcdc", layout="wide")

st.title("\ud83d\udcdc AI Resume Analyzer (Lite)")
st.write("Upload a PDF resume for quick, heuristic feedback.")

uploaded = st.file_uploader("Upload PDF", type=["pdf"])

if uploaded:
    try:
        reader = PdfReader(uploaded)
        text = "\n".join(page.extract_text() or "" for page in reader.pages)
    except Exception as e:
        st.error(f"Failed to read PDF: {e}")
        text = ""

    if text:
        st.subheader("Extracted Text (preview)")
        st.text_area("", value=text[:2000], height=200)

        # Simple heuristics
        score = 70
        hints = []

        if len(text) < 1000:
            hints.append("Resume seems short; consider adding more concrete details.")
            score -= 5
        if not re.search(r"(\b\d+\b|%|\$)", text):
            hints.append("Use quantifiable metrics (numbers, % impact, $ savings).")
            score -= 10
        if not re.search(r"(Python|Java|SQL|AWS|React|TensorFlow|Docker)", text, re.I):
            hints.append("Add or emphasize relevant technical keywords.")
            score -= 5
        if not re.search(r"(Project|Experience|Work|Education)", text, re.I):
            hints.append("Ensure standard sections like Experience/Education are present.")
            score -= 5

        score = max(0, min(100, score))

        st.subheader("Feedback")
        st.metric("Readability/Impact (heuristic)", f"{score}%")
        for h in hints or ["Looks good! Keep tailoring for each role."]:
            st.write("- ", h)

        st.info("Tip: Tailor resume keywords to the specific job description.")
