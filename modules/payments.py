"""Payments page for the TimeTracker application."""
import streamlit as st
import data_manager as dm

def render():
    """Render the Payments page."""
    st.subheader("Payment Tracking")
    
    periods = dm.get_periods()
    # Sort periods desc
    periods.sort(key=lambda x: (x['year'], x['periodNum']), reverse=True)
    
    period_options = {p['label']: p['id'] for p in periods}
    selected_period_label = st.selectbox("Select Period", list(period_options.keys()))
    selected_period_id = period_options[selected_period_label]
    
    st.markdown(f"**{selected_period_label}**")
    
    users = dm.get_users()
    
    # Header
    c1, c2, c3, c4, c5, c6 = st.columns([2, 1.5, 1.5, 2, 3, 1])
    c1.markdown("**Resource**")
    c2.markdown("**Role**")
    c3.markdown("**Hours**")
    c4.markdown("**Status**")
    c5.markdown("**Notes**")
    c6.markdown("**Action**")
    
    for user in users:
        c1, c2, c3, c4, c5, c6 = st.columns([2, 1.5, 1.5, 2, 3, 1])
        
        hours = dm.get_period_user_hours(selected_period_id, user['id'])
        payment = dm.get_payment_status(selected_period_id, user['id'])
        
        status = payment['status'] if payment else "Pending"
        notes = payment['notes'] if payment else ""
        
        c1.write(user['name'])
        c2.write(user['role'])
        c3.write(f"{hours:.2f}")
        
        # Unique keys for inputs
        new_status = c4.selectbox("Status", ["Pending", "Paid", "Processing", "Issue"], 
                                  index=["Pending", "Paid", "Processing", "Issue"].index(status),
                                  key=f"status_{user['id']}", label_visibility="collapsed")
        
        new_notes = c5.text_input("Notes", value=notes, key=f"notes_{user['id']}", label_visibility="collapsed")
        
        if c6.button("Save", key=f"save_pay_{user['id']}"):
            dm.save_payment(selected_period_id, user['id'], new_status, new_notes)
            st.success("Saved")
            st.rerun()
