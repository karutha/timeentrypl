import json
import os
from datetime import datetime, timedelta

DATA_DIR = "data"
USERS_FILE = os.path.join(DATA_DIR, "users.json")
PERIODS_FILE = os.path.join(DATA_DIR, "periods.json")
ENTRIES_FILE = os.path.join(DATA_DIR, "entries.json")
PAYMENTS_FILE = os.path.join(DATA_DIR, "payments.json")

def _ensure_data_dir():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

def _load_json(filepath, default=None):
    _ensure_data_dir()
    if not os.path.exists(filepath):
        return default if default is not None else []
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        return default if default is not None else []

def _save_json(filepath, data):
    _ensure_data_dir()
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)

# --- Users ---
def get_users():
    users = _load_json(USERS_FILE)
    # Ensure defaults
    for user in users:
        if 'role' not in user:
            user['role'] = 'MOA'
        if 'active' not in user:
            user['active'] = True
        if 'password' not in user:
            user['password'] = "" # Default empty password
        if 'assigned_apps' not in user:
            # Default to all apps if not specified
            user['assigned_apps'] = ["Time Entry", "Summary", "Resource Management", "Payments", "Periods"]
    return users

def save_user(name, role='MOA', active=True, password="", assigned_apps=None):
    users = get_users()
    if assigned_apps is None:
        assigned_apps = ["Time Entry", "Summary", "Resource Management", "Payments", "Periods"]
        
    new_user = {
        "id": str(int(datetime.now().timestamp() * 1000)),
        "name": name,
        "role": role,
        "active": active,
        "password": password,
        "assigned_apps": assigned_apps
    }
    users.append(new_user)
    _save_json(USERS_FILE, users)
    return new_user

def update_user(user_id, user_data):
    users = get_users()
    for i, user in enumerate(users):
        if user['id'] == user_id:
            # specific handling for password update to avoid overwriting with empty if not provided
            if 'password' in user_data and not user_data['password']:
                del user_data['password']
                
            users[i].update(user_data)
            _save_json(USERS_FILE, users)
            return users[i]
    return None

def delete_user(user_id):
    users = get_users()
    users = [u for u in users if u['id'] != user_id]
    _save_json(USERS_FILE, users)

# --- Periods ---
def get_periods():
    periods = _load_json(PERIODS_FILE)
    if not periods:
        periods = generate_default_periods(datetime.now().year)
        _save_json(PERIODS_FILE, periods)
    return periods

def save_periods(periods):
    _save_json(PERIODS_FILE, periods)

def update_period(period_id, start_date, end_date):
    periods = get_periods()
    for period in periods:
        if period['id'] == period_id:
            period['startDate'] = start_date
            period['endDate'] = end_date
            
            # Update label
            s = datetime.strptime(start_date, '%Y-%m-%d')
            e = datetime.strptime(end_date, '%Y-%m-%d')
            period['label'] = f"Period {period['periodNum']}: {s.strftime('%b %-d')} - {e.strftime('%b %-d')}"
            
            _save_json(PERIODS_FILE, periods)
            return True
    return False

def generate_default_periods(year):
    periods = []
    current_start = datetime(year, 1, 1)
    
    for i in range(1, 27):
        current_end = current_start + timedelta(days=13)
        
        label = f"Period {i}: {current_start.strftime('%b %-d')} - {current_end.strftime('%b %-d')}"
        
        periods.append({
            "id": f"{year}-P{i}",
            "periodNum": i,
            "year": year,
            "startDate": current_start.strftime('%Y-%m-%d'),
            "endDate": current_end.strftime('%Y-%m-%d'),
            "label": label
        })
        
        current_start = current_end + timedelta(days=1)
        
    return periods

def get_period_for_date(date_str):
    periods = get_periods()
    # date_str is expected to be YYYY-MM-DD
    for p in periods:
        if p['startDate'] <= date_str <= p['endDate']:
            return p
    return None

# --- Entries ---
def get_entries():
    return _load_json(ENTRIES_FILE)

def calculate_duration(start_time, end_time):
    if not start_time or not end_time:
        return 0.0
    
    # Expecting HH:MM string format
    sh, sm = map(int, start_time.split(':'))
    eh, em = map(int, end_time.split(':'))
    
    start_minutes = sh * 60 + sm
    end_minutes = eh * 60 + em
    
    diff = end_minutes - start_minutes
    if diff < 0:
        diff += 24 * 60
        
    return round(diff / 60.0, 2)

def save_entry(entry_data):
    entries = get_entries()
    period = get_period_for_date(entry_data['date'])
    
    new_entry = {
        "id": str(int(datetime.now().timestamp() * 1000)),
        **entry_data,
        "duration": calculate_duration(entry_data['startTime'], entry_data['endTime']),
        "period": period
    }
    entries.append(new_entry)
    _save_json(ENTRIES_FILE, entries)
    return new_entry

def delete_entry(entry_id):
    entries = get_entries()
    entries = [e for e in entries if e['id'] != entry_id]
    _save_json(ENTRIES_FILE, entries)

# --- Payments ---
def get_payments():
    return _load_json(PAYMENTS_FILE)

def save_payment(period_id, user_id, status, notes):
    payments = get_payments()
    
    # Check if exists
    found = False
    for i, p in enumerate(payments):
        if p['periodId'] == period_id and p['userId'] == user_id:
            payments[i].update({
                "status": status,
                "notes": notes,
                "updatedAt": datetime.now().isoformat()
            })
            found = True
            break
    
    if not found:
        payments.append({
            "periodId": period_id,
            "userId": user_id,
            "status": status,
            "notes": notes,
            "updatedAt": datetime.now().isoformat()
        })
        
    _save_json(PAYMENTS_FILE, payments)

def get_payment_status(period_id, user_id):
    payments = get_payments()
    for p in payments:
        if p['periodId'] == period_id and p['userId'] == user_id:
            return p
    return None

def get_period_user_hours(period_id, user_id):
    entries = get_entries()
    period = next((p for p in get_periods() if p['id'] == period_id), None)
    
    if not period:
        return 0
        
    total = 0
    for e in entries:
        if e['userId'] == user_id and period['startDate'] <= e['date'] <= period['endDate']:
            total += e['duration']
            
    return total
