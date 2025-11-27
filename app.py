"""TimeTracker - Main Application Entry Point."""
import streamlit as st
from pages import time_entry, summary, users, payments, periods

# --- Configuration ---
st.set_page_config(
    page_title="TimeTracker",
    page_icon="⏱️",
    layout="wide",
    initial_sidebar_state="expanded"
)

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
