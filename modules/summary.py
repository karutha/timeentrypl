"""Summary page for the TimeTracker application."""
import streamlit as st
import data_manager as dm

def render():
    """Render the Summary page."""
    
    # Import Google Fonts and define custom CSS
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
        
        .summary-container {
            font-family: 'Inter', sans-serif;
            display: flex;
            flex-direction: column;
            gap: 16px;
        }
        
        .summary-card {
            background-color: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            padding: 16px;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
            transition: box-shadow 0.2s ease;
        }
        
        .summary-card:hover {
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        }
        
        .card-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 12px;
            padding-bottom: 8px;
            border-bottom: 1px solid #f1f5f9;
        }
        
        .period-label {
            font-size: 14px;
            font-weight: 600;
            color: #1e293b;
        }
        
        .period-badge {
            background-color: #f1f5f9;
            color: #475569;
            font-size: 11px;
            font-weight: 500;
            padding: 4px 8px;
            border-radius: 12px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .user-row {
            display: grid;
            grid-template-columns: 2fr 1fr 1fr;
            gap: 12px;
            align-items: center;
            padding: 8px 0;
            font-size: 13px;
        }
        
        .user-row:not(:last-child) {
            border-bottom: 1px solid #f8fafc;
        }
        
        .user-name {
            font-weight: 500;
            color: #334155;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        .user-avatar {
            width: 24px;
            height: 24px;
            background-color: #3b82f6;
            color: white;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 10px;
            font-weight: 600;
        }
        
        .stat-col {
            display: flex;
            flex-direction: column;
            align-items: flex-end;
        }
        
        .stat-value {
            font-weight: 600;
            color: #0f172a;
        }
        
        .stat-label {
            font-size: 10px;
            color: #94a3b8;
            text-transform: uppercase;
        }
        
        /* Dark mode adjustments */
        @media (prefers-color-scheme: dark) {
            .summary-card {
                background-color: #1e293b;
                border-color: #334155;
            }
            .card-header {
                border-bottom-color: #334155;
            }
            .period-label {
                color: #f8fafc;
            }
            .period-badge {
                background-color: #334155;
                color: #cbd5e1;
            }
            .user-row:not(:last-child) {
                border-bottom-color: #334155;
            }
            .user-name {
                color: #e2e8f0;
            }
            .stat-value {
                color: #f8fafc;
            }
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("## **Bi-Weekly Summary**")
    
    entries = dm.get_entries()
    
    if not entries:
        st.info("No data to summarize.")
        return
    
    # Aggregate by period and user
    summary_data = {}
    for e in entries:
        if not e.get('period'):
            continue
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

    # Sort periods (reverse chronologically)
    sorted_summary = sorted(summary_data.values(), key=lambda x: (x['year'], x['num']), reverse=True)

    # Calculate cumulative totals
    user_cumulatives = {}
    for item in reversed(sorted_summary):  # earliest → latest
        for uid, user_data in item['users'].items():
            user_cumulatives[uid] = user_cumulatives.get(uid, 0) + user_data['total']
            user_data['cumulative'] = user_cumulatives[uid]

    # Generate HTML
    html_content = '<div class="summary-container">'
    
    for item in sorted_summary:
        html_content += f"""
<div class="summary-card">
    <div class="card-header">
        <div class="period-label">{item['label']}</div>
        <div class="period-badge">Period {item['num']}</div>
    </div>
"""
        
        for uid, user_data in item['users'].items():
            initials = "".join([n[0] for n in user_data['name'].split()[:2]]).upper()
            html_content += f"""
    <div class="user-row">
        <div class="user-name">
            <div class="user-avatar">{initials}</div>
            {user_data['name']}
        </div>
        <div class="stat-col">
            <span class="stat-value">{user_data['total']:.2f}h</span>
            <span class="stat-label">Period</span>
        </div>
        <div class="stat-col">
            <span class="stat-value">{user_data['cumulative']:.2f}h</span>
            <span class="stat-label">Cumulative</span>
        </div>
    </div>
"""
            
        html_content += "</div>"
        
    html_content += "</div>"
    
    st.markdown(html_content, unsafe_allow_html=True)
