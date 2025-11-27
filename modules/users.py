"""Users page for the TimeTracker application."""
import streamlit as st
import data_manager as dm

def render():
    """Render the Users page."""
    st.subheader("Manage Users")
    
    with st.form("user_form"):
        c1, c2, c3, c4 = st.columns([3, 2, 1, 1])
        with c1:
            new_name = st.text_input("Name")
        with c2:
            new_role = st.selectbox("Role", ["MOA", "PA", "RPH", "AA"])
        with c3:
            is_active = st.checkbox("Active", value=True)
        with c4:
            st.write("")  # Spacer
            submitted = st.form_submit_button("Add User")
            
        if submitted and new_name:
            dm.save_user(new_name, new_role, is_active)
            st.success(f"User {new_name} added!")
            st.rerun()
            
    st.markdown("**Existing Users**")
    users = dm.get_users()
    
    if users:
        for u in users:
            c1, c2, c3, c4 = st.columns([3, 2, 1, 1])
            c1.write(f"**{u['name']}**")
            c2.write(u['role'])
            c3.write("✅ Active" if u['active'] else "❌ Inactive")
            if c4.button("🗑️", key=f"del_user_{u['id']}"):
                dm.delete_user(u['id'])
                st.rerun()
    else:
        st.info("No users found.")
