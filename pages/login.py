"""Login page for the TimeTracker application."""
import streamlit as st
import data_manager as dm

def render():
    """Render the login page."""
    st.markdown("# PHARMALIFE")
    st.subheader("Login")
    
    with st.form("login_form"):
        st.markdown("**Please select your name to continue**")
        
        users = dm.get_users()
        active_users = [u for u in users if u['active']]
        
        if not active_users:
            st.error("No active resources found. Please contact your administrator.")
            st.form_submit_button("Login", disabled=True)
            return
        
        user_names = [u['name'] for u in active_users]
        selected_name = st.selectbox("Select Resource", user_names)
        
        submitted = st.form_submit_button("Login")
        
        if submitted:
            selected_user = next(u for u in active_users if u['name'] == selected_name)
            st.session_state.logged_in = True
            st.session_state.user_id = selected_user['id']
            st.session_state.full_name = selected_user['name']
            st.session_state.role = selected_user['role']
            st.rerun()
