"""Summary page for the TimeTracker application."""
import streamlit as st
import data_manager as dm

def render():
    """Render the Summary page."""
    st.title("Bi-Weekly Summary")
    
    entries = dm.get_entries()
    periods = dm.get_periods()
    users = dm.get_users()
    
    if not entries:
        st.info("No data to summarize.")
    else:
        # Aggregate by period and user
        summary_data = {}
        for e in entries:
            if not e.get('period'): continue
            pid = e['period']['id']
            uid = e['userId']
            
            if pid not in summary_data:
                summary_data[pid] = {
                    "label": e['period']['label'],
                    "year": e['period']['year'],
                    "num": e['period']['periodNum'],
                    "users": {}
                }
            
            if uid not in summary_data[pid]['users']:
                summary_data[pid]['users'][uid] = {
                    "name": e.get('userName', 'Unknown'),
                    "total": 0
                }
            
            summary_data[pid]['users'][uid]['total'] += e['duration']
            
        # Sort periods
        sorted_summary = sorted(summary_data.values(), key=lambda x: (x['year'], x['num']), reverse=True)
        
        # Calculate cumulative totals per user
        user_cumulatives = {}
        for item in reversed(sorted_summary):  # Process from earliest to latest
            for uid, user_data in item['users'].items():
                if uid not in user_cumulatives:
                    user_cumulatives[uid] = 0
                user_cumulatives[uid] += user_data['total']
                user_data['cumulative'] = user_cumulatives[uid]
        
        # Display (already in reverse chronological order)
        for item in sorted_summary:
            st.markdown(f"### {item['label']}")
            
            for uid, user_data in item['users'].items():
                col1, col2 = st.columns(2)
                with col1:
                    st.metric(
                        label=f"{user_data['name']} - Period Hours",
                        value=f"{user_data['total']:.2f} hrs"
                    )
                with col2:
                    st.metric(
                        label=f"{user_data['name']} - Cumulative",
                        value=f"{user_data['cumulative']:.2f} hrs"
                    )
            
            st.divider()
