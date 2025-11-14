import os
import streamlit as st
from pathlib import Path

# Auth gate
if 'authenticated' not in st.session_state or not st.session_state.authenticated:
    st.error("Please login to access this page")
    if st.button("\u2190 Back to Login"):
        st.switch_page("main.py")
    st.stop()

st.set_page_config(page_title="Companies - EchoPrep", page_icon="\ud83d\udcbc", layout="wide")

st.title("\ud83d\udcbc Company Explorer")
st.write("Explore top companies and their tech focus.")

companies = [
    {"name": "Amazon", "desc": "E-commerce and cloud leader (AWS)", "url": "https://www.amazon.com"},
    {"name": "Google", "desc": "Search, ads, cloud, Android", "url": "https://www.google.com"},
    {"name": "TCS", "desc": "Global IT services and consulting", "url": "https://www.tcs.com"},
    {"name": "Infosys", "desc": "Digital services and consulting", "url": "https://www.infosys.com"},
    {"name": "Accenture", "desc": "Consulting and technology services", "url": "https://www.accenture.com"},
    {"name": "Deloitte", "desc": "Consulting, audit, and advisory", "url": "https://www2.deloitte.com"},
]

logos_dir = Path("assets/company_logos")

cols = st.columns(3)
for i, info in enumerate(companies):
    with cols[i % 3]:
        with st.container(border=True):
            logo_path = logos_dir / f"{info['name'].lower()}.png"
            if logo_path.exists():
                st.image(str(logo_path), width=96)
            st.markdown(f"**{info['name']}**")
            st.caption(info['desc'])
            st.link_button("Website", info['url'])
