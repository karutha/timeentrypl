"""Shared utilities and styling for the TimeTracker application."""
import streamlit as st

def apply_custom_styles():
    """Apply custom CSS styling to the application."""
    st.markdown("""
        <style>
        .stApp {
            background-color: #0f172a;
            color: #f8fafc;
        }
        .stSidebar {
            background-color: #1e293b;
        }
        .stButton>button {
            width: 100%;
            border-radius: 8px;
            height: 3em;
            background-color: #38bdf8;
            color: #0f172a;
            font-weight: 600;
            border: none;
        }
        .stButton>button:hover {
            background-color: #0ea5e9;
            color: #0f172a;
        }
        h1, h2, h3 {
            color: #f8fafc;
        }
        .metric-card {
            background-color: #1e293b;
            padding: 1rem;
            border-radius: 12px;
            border: 1px solid #334155;
            text-align: center;
        }
        .metric-value {
            font-size: 2rem;
            font-weight: bold;
            color: #38bdf8;
        }
        .metric-label {
            color: #94a3b8;
        }
        </style>
    """, unsafe_allow_html=True)

def format_duration(hours):
    """Format hours as 'Xh Ym'."""
    h = int(hours)
    m = int((hours - h) * 60)
    return f"{h}h {m}m"
