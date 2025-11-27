"""Periods page for the TimeTracker application."""
import streamlit as st
from datetime import datetime
import data_manager as dm

def render():
    """Render the Periods page."""
    st.subheader("Manage Periods")
    
    periods = dm.get_periods()
    periods.sort(key=lambda x: (x['year'], x['periodNum']), reverse=True)
    
    for p in periods:
        with st.expander(p['label']):
            with st.form(f"period_form_{p['id']}"):
                c1, c2 = st.columns(2)
                new_start = c1.date_input("Start Date", datetime.strptime(p['startDate'], '%Y-%m-%d'))
                new_end = c2.date_input("End Date", datetime.strptime(p['endDate'], '%Y-%m-%d'))
                
                if st.form_submit_button("Update"):
                    dm.update_period(p['id'], new_start.strftime('%Y-%m-%d'), new_end.strftime('%Y-%m-%d'))
                    st.success("Period updated")
                    st.rerun()
