"""TimeTracker - Main Application Entry Point."""
import streamlit as st
from modules import time_entry, summary, users, payments, periods

# --- Configuration ---
st.set_page_config(
    page_icon="⏱️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Reduce gaps with CSS
st.markdown("""
    <style>
        .block-container {
            padding-top: 1rem;
            padding-bottom: 0rem;
        }
    </style>
""", unsafe_allow_html=True)

# --- Sidebar Navigation ---
st.sidebar.title("TimeTracker")
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

