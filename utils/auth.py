import streamlit as st

def check_authentication_status():
    """Check if user is authenticated"""
    return st.session_state.get('authenticated', False)

def require_authentication():
    """Decorator to require authentication for pages"""
    if not check_authentication_status():
        st.error("Please login to access this page")
        st.stop()

def get_current_user_id():
    """Get current user ID"""
    return st.session_state.get('user_id', None)
