import os
import json
import requests
import streamlit as st

# Auth gate
if 'authenticated' not in st.session_state or not st.session_state.authenticated:
    st.error("Please login to access this page")
    if st.button("\u2190 Back to Login"):
        st.switch_page("main.py")
    st.stop()

st.set_page_config(page_title="Jobs - EchoPrep", page_icon="\ud83d\udcbc", layout="wide")

st.title("\ud83d\udcbc Job Search")
st.write("Search and save roles to practice for.")

query = st.text_input("Keywords (e.g., Python Developer, Data Analyst)")
location = st.text_input("Location (optional)")

col1, col2 = st.columns([1,1])
with col1:
    use_api = st.toggle("Use JSearch API (if key configured)")

with col2:
    st.caption("Fallback to mock results if API is unavailable")

results = []

if st.button("Search", type="primary"):
    if use_api and os.getenv("JSEARCH_API_KEY"):
        try:
            # Example JSearch (RapidAPI) endpoint; adjust if needed
            url = "https://jsearch.p.rapidapi.com/search"
            headers = {
                "x-rapidapi-key": os.getenv("JSEARCH_API_KEY"),
                "x-rapidapi-host": "jsearch.p.rapidapi.com"
            }
            params = {
                "query": f"{query} {location}".strip(),
                "page": 1,
                "num_pages": 1
            }
            resp = requests.get(url, headers=headers, params=params, timeout=20)
            if resp.status_code == 200:
                data = resp.json()
                results = data.get("data", [])
            else:
                st.warning("API error. Showing mock results.")
        except Exception as e:
            st.warning(f"API error: {e}. Showing mock results.")

    if not results:
        # Mock data
        results = [
            {
                "employer_name": "TechNova",
                "job_title": "Software Engineer (Python)",
                "job_city": "Remote",
                "job_country": "USA",
                "job_apply_link": "https://example.com/apply/1"
            },
            {
                "employer_name": "DataWorx",
                "job_title": "Data Analyst",
                "job_city": "Bengaluru",
                "job_country": "India",
                "job_apply_link": "https://example.com/apply/2"
            },
            {
                "employer_name": "CyberShield",
                "job_title": "Cybersecurity Analyst",
                "job_city": "London",
                "job_country": "UK",
                "job_apply_link": "https://example.com/apply/3"
            }
        ]

# Simple local saved jobs store
if 'saved_jobs' not in st.session_state:
    st.session_state.saved_jobs = []

if results:
    st.subheader("Results")
    for idx, job in enumerate(results):
        with st.container(border=True):
            title = job.get("job_title") or job.get("title")
            company = job.get("employer_name") or job.get("company_name")
            city = job.get("job_city") or job.get("city")
            country = job.get("job_country") or job.get("country")
            link = job.get("job_apply_link") or job.get("apply_link")

            st.markdown(f"**{title}** at **{company}**")
            st.markdown(f"{city or ''} {country or ''}")
            col_a, col_b = st.columns([1,1])
            with col_a:
                if link:
                    st.link_button("Apply", link)
            with col_b:
                if st.button("Save", key=f"save_{idx}"):
                    st.session_state.saved_jobs.append({
                        "title": title,
                        "company": company,
                        "location": f"{city or ''} {country or ''}",
                        "link": link
                    })
                    st.success("Saved")

if st.session_state.saved_jobs:
    st.subheader("Saved Jobs")
    for saved in st.session_state.saved_jobs:
        with st.container(border=True):
            st.markdown(f"**{saved['title']}** at **{saved['company']}**")
            st.markdown(saved['location'])
            if saved.get('link'):
                st.link_button("Apply", saved['link'])
