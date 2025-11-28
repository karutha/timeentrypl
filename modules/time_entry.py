"""Time Entry page for the TimeTracker application."""
import streamlit as st
import pandas as pd
from datetime import datetime, date
import data_manager as dm

def render():
    
    """Render the Time Entry page."""
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Add New Entry")
        with st.form("entry_form"):
            users = dm.get_users()
            active_users = [u for u in users if u['active']]
            user_names = [u['name'] for u in active_users]
            
            selected_user_name = st.selectbox("Resource", user_names if user_names else ["No resources found"])
            entry_date = st.date_input("Date", date.today())
            start_time = st.time_input("Start Time", datetime.strptime("09:00", "%H:%M").time(), step=60)
            end_time = st.time_input("End Time", datetime.strptime("17:00", "%H:%M").time(), step=60)
            
            submitted = st.form_submit_button("Log Time")
            
            if submitted and selected_user_name != "No resources found":
                selected_user = next(u for u in active_users if u['name'] == selected_user_name)
                
                # Check if entry already exists for this resource on this date
                existing_entries = dm.get_entries()
                date_str = entry_date.strftime("%Y-%m-%d")
                duplicate = any(
                    e['userId'] == selected_user['id'] and e['date'] == date_str 
                    for e in existing_entries
                )
                
                if duplicate:
                    st.error(f"⚠️ An entry already exists for {selected_user['name']} on {date_str}. Only one entry per resource per day is allowed.")
                else:
                    entry_data = {
                        "userId": selected_user['id'],
                        "userName": selected_user['name'],
                        "date": date_str,
                        "startTime": start_time.strftime("%H:%M"),
                        "endTime": end_time.strftime("%H:%M")
                    }
                    
                    dm.save_entry(entry_data)
                    st.success("Entry saved!")
                    st.rerun()

    with col2:
        st.subheader("Recent Entries")
        
        # Resource filter for entries
        users = dm.get_users()
        all_users = [u for u in users if u['active']]
        user_filter_options = ["All Resources"] + [u['name'] for u in all_users]
        selected_filter = st.selectbox("Filter by Resource", user_filter_options, key="entry_filter")
        
        entries = dm.get_entries()
        
        # Apply resource filter
        if selected_filter != "All Resources":
            selected_user_id = next((u['id'] for u in all_users if u['name'] == selected_filter), None)
            if selected_user_id:
                entries = [e for e in entries if e['userId'] == selected_user_id]
        
        if entries:
            # Sort by date desc, then start time desc
            entries.sort(key=lambda x: (x['date'], x['startTime']), reverse=True)
            
            # Display entries
            # Header row
            c1, c2, c3, c4, c5, c6 = st.columns([2, 2, 3, 2, 1, 1])
            c1.markdown("**Date**")
            c2.markdown("**Resource**")
            c3.markdown("**Period**")
            c4.markdown("**Time**")
            c5.markdown("**Hrs**")
            c6.markdown("**Del**")
            
            for e in entries:
                period_label = e['period']['label'] if e.get('period') else "Unknown"
                c1, c2, c3, c4, c5, c6 = st.columns([2, 2, 3, 2, 1, 1])
                c1.write(e['date'])
                c2.write(e.get('userName', 'Unknown'))
                c3.write(period_label)
                c4.write(f"{e['startTime']} - {e['endTime']}")
                c5.write(f"{e['duration']}h")
                if c6.button("🗑️", key=f"del_{e['id']}"):
                    dm.delete_entry(e['id'])
                    st.rerun()
        else:
            st.info("No entries yet.")
