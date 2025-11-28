"""Resource management page with full CRUD operations."""
import streamlit as st
import data_manager as dm

def render():
    """Render the Resource management page."""
    st.subheader("Resource Management")
    
    # Create new resource section
    st.markdown("**Add New Resource**")
    with st.form("resource_form"):
        c1, c2, c3, c4 = st.columns([3, 2, 2, 1])
        with c1:
            new_name = st.text_input("Name", placeholder="Enter resource name")
        with c2:
            new_role = st.selectbox("Role", ["MOA", "PA", "RPH", "AA"])
        with c3:
            new_password = st.text_input("Password", type="password", placeholder="Optional")
        with c4:
            is_active = st.checkbox("Active", value=True)
            
        assigned_apps = st.multiselect("Assigned Apps", 
                                     ["Time Entry", "Summary", "Resource Management", "Payments", "Periods"],
                                     default=["Time Entry", "Summary", "Resource Management", "Payments", "Periods"])
        
        submitted = st.form_submit_button("Add")
            
        if submitted and new_name:
            dm.save_user(new_name, new_role, is_active, new_password, assigned_apps)
            st.success(f"Resource {new_name} added!")
            st.rerun()
        elif submitted and not new_name:
            st.error("Please enter a name")
    
    st.divider()
    
    # List and manage existing resources
    st.markdown("**Existing Resources**")
    users = dm.get_users()
    
    if users:
        # Header row
        c1, c2, c3, c4, c5 = st.columns([3, 2, 1, 1, 1])
        c1.markdown("**Name**")
        c2.markdown("**Role**")
        c3.markdown("**Status**")
        c4.markdown("**Edit**")
        c5.markdown("**Delete**")
        
        for u in users:
            c1, c2, c3, c4, c5 = st.columns([3, 2, 1, 1, 1])
            
            # Display resource info
            c1.write(u['name'])
            c2.write(u['role'])
            c3.write("✅" if u['active'] else "❌")
            
            # Edit button - opens a dialog/expander
            if c4.button("✏️", key=f"edit_{u['id']}"):
                st.session_state[f"editing_{u['id']}"] = True
            
            # Delete button
            if c5.button("🗑️", key=f"del_user_{u['id']}"):
                dm.delete_user(u['id'])
                st.success(f"Resource {u['name']} deleted!")
                st.rerun()
            
            # Edit form (shown when edit button is clicked)
            if st.session_state.get(f"editing_{u['id']}", False):
                with st.expander(f"Edit {u['name']}", expanded=True):
                    with st.form(f"edit_form_{u['id']}"):
                        edit_name = st.text_input("Name", value=u['name'], key=f"edit_name_{u['id']}")
                        edit_role = st.selectbox("Role", ["MOA", "PA", "RPH", "AA"], 
                                                index=["MOA", "PA", "RPH", "AA"].index(u['role']),
                                                key=f"edit_role_{u['id']}")
                        edit_active = st.checkbox("Active", value=u['active'], key=f"edit_active_{u['id']}")
                        
                        edit_password = st.text_input("New Password", type="password", placeholder="Leave blank to keep unchanged", key=f"edit_pass_{u['id']}")
                        
                        current_apps = u.get('assigned_apps', ["Time Entry", "Summary", "Resource Management", "Payments", "Periods"])
                        edit_apps = st.multiselect("Assigned Apps", 
                                                 ["Time Entry", "Summary", "Resource Management", "Payments", "Periods"],
                                                 default=current_apps,
                                                 key=f"edit_apps_{u['id']}")
                        
                        col_save, col_cancel = st.columns(2)
                        with col_save:
                            if st.form_submit_button("Save Changes"):
                                dm.update_user(u['id'], {
                                    "name": edit_name, 
                                    "role": edit_role, 
                                    "active": edit_active, 
                                    "password": edit_password,
                                    "assigned_apps": edit_apps
                                })
                                st.session_state[f"editing_{u['id']}"] = False
                                st.success(f"Resource {edit_name} updated!")
                                st.rerun()
                        with col_cancel:
                            if st.form_submit_button("Cancel"):
                                st.session_state[f"editing_{u['id']}"] = False
                                st.rerun()
    else:
        st.info("No resources found. Add a resource to get started.")
