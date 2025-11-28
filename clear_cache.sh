#!/bin/bash
# Clear Streamlit cache
rm -rf ~/.streamlit/cache
echo "Streamlit cache cleared"

# Instructions
echo ""
echo "To fix the application:"
echo "1. Stop the running Streamlit server (Ctrl+C)"
echo "2. Clear your browser cache or open in incognito mode"
echo "3. Restart: streamlit run app.py"
echo "4. Navigate to http://localhost:8501"
