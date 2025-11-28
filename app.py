"""TimeTracker - Main Application Entry Point."""
import streamlit as st
from pages import time_entry, summary, users, payments, periods, login

# --- Configuration ---
st.set_page_config(
    page_title="PHARMALIFE TimeTracker",
    page_icon="⏱️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'full_name' not in st.session_state:
    st.session_state.full_name = ""
if 'role' not in st.session_state:
    st.session_state.role = ""

# Reduce gaps with CSS
st.markdown("""
    <style>
        .block-container {
            padding-top: 2rem;
            padding-bottom: 0rem;
        }
    </style>
""", unsafe_allow_html=True)

if not st.session_state.logged_in:
    login.render()
else:
    # Add branding to header bar
    st.markdown(f"""
        <style>
        header[data-testid="stHeader"]::before {{
            content: "PHARMALIFE";
            font-weight: 700;
            font-size: 1.1rem;
            margin-right: auto;
            padding-left: 1rem;
        }}
        
        header[data-testid="stHeader"]::after {{
            content: "{st.session_state.full_name} ({st.session_state.role})";
            font-size: 0.9rem;
            padding-right: 1rem;
        }}
        </style>
    """, unsafe_allow_html=True)
    
    # --- Sidebar Navigation ---
    st.sidebar.title("TimeTracker")
    
    # Logout button
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.full_name = ""
        st.session_state.role = ""
        st.session_state.user_id = ""
        st.rerun()
    
    st.sidebar.divider()
    page = st.sidebar.radio("Navigate", ["Time Entry", "Summary", "Users", "Payments", "Periods"])
    
    # --- Route to Appropriate Page ---
    if page == "Time Entry":
        time_entry.render()
    elif page == "Summary":
        summary.render()
    elif page == "Users":
        users.render()
    elif page == "Payments":
        payments.render()
    elif page == "Periods":
        periods.render()

