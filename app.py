import streamlit as st
import pandas as pd
from datetime import datetime, date
import data_manager as dm

# --- Configuration ---
st.set_page_config(
    page_title="TimeTracker",
    page_icon="⏱️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Styling ---
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

# --- Sidebar Navigation ---
st.sidebar.title("TimeTracker")
page = st.sidebar.radio("Navigate", ["Time Entry", "Summary", "Users", "Payments", "Periods"])

# --- Helper Functions ---
def format_duration(hours):
    h = int(hours)
    m = int((hours - h) * 60)
    return f"{h}h {m}m"

# --- Pages ---

if page == "Time Entry":
    st.title("Time Entry")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Add New Entry")
        with st.form("entry_form"):
            users = dm.get_users()
            active_users = [u for u in users if u['active']]
            user_names = [u['name'] for u in active_users]
            
            selected_user_name = st.selectbox("User", user_names if user_names else ["No users found"])
            entry_date = st.date_input("Date", date.today())
            start_time = st.time_input("Start Time", datetime.strptime("09:00", "%H:%M").time(), step=60)
            end_time = st.time_input("End Time", datetime.strptime("17:00", "%H:%M").time(), step=60)
            
            submitted = st.form_submit_button("Log Time")
            
            if submitted and selected_user_name != "No users found":
                selected_user = next(u for u in active_users if u['name'] == selected_user_name)
                
                # Check if entry already exists for this user on this date
                existing_entries = dm.get_entries()
                date_str = entry_date.strftime("%Y-%m-%d")
                duplicate = any(
                    e['userId'] == selected_user['id'] and e['date'] == date_str 
                    for e in existing_entries
                )
                
                if duplicate:
                    st.error(f"⚠️ An entry already exists for {selected_user['name']} on {date_str}. Only one entry per user per day is allowed.")
                else:
                    entry_data = {
                        "userId": selected_user['id'],
                        "userName": selected_user['name'], # Store name for easier display
                        "date": date_str,
                        "startTime": start_time.strftime("%H:%M"),
                        "endTime": end_time.strftime("%H:%M")
                    }
                    
                    dm.save_entry(entry_data)
                    st.success("Entry saved!")
                    st.rerun()

    with col2:
        st.subheader("Recent Entries")
        
        # User filter for entries
        users = dm.get_users()
        all_users = [u for u in users if u['active']]
        user_filter_options = ["All Users"] + [u['name'] for u in all_users]
        selected_filter = st.selectbox("Filter by User", user_filter_options, key="entry_filter")
        
        entries = dm.get_entries()
        
        # Apply user filter
        if selected_filter != "All Users":
            selected_user_id = next((u['id'] for u in all_users if u['name'] == selected_filter), None)
            if selected_user_id:
                entries = [e for e in entries if e['userId'] == selected_user_id]
        
        if entries:
            # Sort by date desc, then start time desc
            entries.sort(key=lambda x: (x['date'], x['startTime']), reverse=True)
            
            # Prepare data for dataframe
            df_data = []
            for e in entries:
                period_label = e['period']['label'] if e.get('period') else "Unknown"
                df_data.append({
                    "Date": e['date'],
                    "User": e.get('userName', 'Unknown'),
                    "Period": period_label,
                    "Time": f"{e['startTime']} - {e['endTime']}",
                    "Duration": f"{e['duration']}h",
                    "ID": e['id']
                })
            
            df = pd.DataFrame(df_data)
            
            # Display as a table with delete buttons (simulated with columns)
            # Streamlit data_editor allows deletion but let's stick to simple display for now
            # or use columns for a custom list view
            
            for index, row in df.iterrows():
                c1, c2, c3, c4, c5, c6 = st.columns([2, 2, 3, 2, 1, 1])
                c1.write(row['Date'])
                c2.write(row['User'])
                c3.write(row['Period'])
                c4.write(row['Time'])
                c5.write(row['Duration'])
                if c6.button("🗑️", key=f"del_{row['ID']}"):
                    dm.delete_entry(row['ID'])
                    st.rerun()
                st.divider()
        else:
            st.info("No entries yet.")

elif page == "Summary":
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
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label" style="font-size: 1rem; font-weight: 600; margin-bottom: 0.75rem;">{user_data['name']}</div>
                    <div style="display: flex; justify-content: space-around; margin-top: 0.5rem;">
                        <div>
                            <div style="font-size: 0.875rem; color: #94a3b8;">Period Hours</div>
                            <div class="metric-value" style="font-size: 1.5rem;">{user_data['total']:.2f}</div>
                        </div>
                        <div>
                            <div style="font-size: 0.875rem; color: #94a3b8;">Cumulative</div>
                            <div class="metric-value" style="font-size: 1.5rem; color: #22c55e;">{user_data['cumulative']:.2f}</div>
                        </div>
                    </div>
                </div>
                <div style="margin-bottom: 0.75rem;"></div>
                """, unsafe_allow_html=True)
            
            st.markdown("<div style='margin-bottom: 2rem;'></div>", unsafe_allow_html=True)

elif page == "Users":
    st.title("Manage Users")
    
    with st.form("user_form"):
        c1, c2, c3, c4 = st.columns([3, 2, 1, 1])
        with c1:
            new_name = st.text_input("Name")
        with c2:
            new_role = st.selectbox("Role", ["MOA", "PA", "RPH", "AA"])
        with c3:
            is_active = st.checkbox("Active", value=True)
        with c4:
            st.write("") # Spacer
            st.write("")
            submitted = st.form_submit_button("Add User")
            
        if submitted and new_name:
            dm.save_user(new_name, new_role, is_active)
            st.success(f"User {new_name} added!")
            st.rerun()
            
    st.subheader("Existing Users")
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
            st.divider()
    else:
        st.info("No users found.")

elif page == "Payments":
    st.title("Payment Tracking")
    
    periods = dm.get_periods()
    # Sort periods desc
    periods.sort(key=lambda x: (x['year'], x['periodNum']), reverse=True)
    
    period_options = {p['label']: p['id'] for p in periods}
    selected_period_label = st.selectbox("Select Period", list(period_options.keys()))
    selected_period_id = period_options[selected_period_label]
    
    st.subheader(f"Status for {selected_period_label}")
    
    users = dm.get_users()
    
    # Header
    c1, c2, c3, c4, c5, c6 = st.columns([2, 1.5, 1.5, 2, 3, 1])
    c1.markdown("**User**")
    c2.markdown("**Role**")
    c3.markdown("**Hours**")
    c4.markdown("**Status**")
    c5.markdown("**Notes**")
    c6.markdown("**Action**")
    st.divider()
    
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
        st.divider()

elif page == "Periods":
    st.title("Manage Periods")
    
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
