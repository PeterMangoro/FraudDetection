@echo off
echo 🚨 Starting Fraud Detection System...
echo 📊 Loading Streamlit Dashboard...
echo 🌐 The app will open in your default browser
echo ==================================================

REM Activate virtual environment
call .venv\Scripts\activate.bat

REM Run streamlit app
streamlit run streamlit_app.py --server.port 8501 --server.address localhost

pause
