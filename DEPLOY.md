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
