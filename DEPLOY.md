# Deploy to Streamlit

To run this application in Streamlit:

# Deployment Instructions

## GitHub Repository
This project is hosted at: https://github.com/karutha/timeentrypl

## Local Development

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Run the App
```bash
streamlit run app.py
```

The app will be available at http://localhost:8501

## Deploy to Streamlit Cloud

1. Fork or clone the repository from https://github.com/karutha/timeentrypl
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Sign in with your GitHub account
4. Click "New app"
5. Select the repository: `karutha/timeentrypl`
6. Set the main file path: `app.py`
7. Click "Deploy"

## Git Workflow

### Clone the Repository
```bash
git clone https://github.com/karutha/timeentrypl.git
cd timeentrypl
```

### Make Changes and Push
```bash
git add .
git commit -m "Your commit message"
git push origin main
```

## Notes
- Data is stored locally in the `data/` directory (JSON files)
- The `data/` directory is gitignored to prevent committing user data
- For production deployment, consider using a proper database

## Data Management Strategy

### 1. Operational Data Safety
The `data/` directory is **gitignored**. This is intentional and ensures that:
- **Git Pulls are Safe**: When you pull new code from git to your production server, it will **NOT** overwrite your existing `data/` folder. Your operational data (users, entries) is safe.
- **No Accidental Commits**: You won't accidentally commit real user data to the public repository.

### 2. Dev vs Prod Data
- **Development (Local)**: You have a local `data/` folder with test users and fake entries. This is for you to break and test.
- **Production (Server)**: The server has its own `data/` folder with real data.
- **Rule**: Never copy `data/` from Dev to Prod unless you are setting up the server for the very first time.

### 3. Backups
Since your database is just files, backing up is easy.
- **Manual**: Simply copy the `data/` folder to a safe location.
- **Script**: Use the included `backup_data.sh` script to create a timestamped archive.
  ```bash
  ./backup_data.sh
  ```
- **Recommendation**: Set up a cron job on your server to run this script daily.

### 4. Handling Updates (Migrations)
If you update the code to add new features (e.g., adding a "Phone Number" to users):
- **Lazy Migration**: The code is designed to handle missing fields. If a user record doesn't have a "phone" field, the system will just assume a default (empty) value.
- **No Manual Migration Needed**: You generally don't need to run a migration script. Just deploy the new code, and it will work with the old data files.

