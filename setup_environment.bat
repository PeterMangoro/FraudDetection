@echo off
echo 🚀 Setting up Fraud Detection Environment...
echo.

REM Activate virtual environment
call .venv\Scripts\activate.bat

echo ✅ Virtual environment activated!
echo 📦 Installing/updating dependencies...
pip install -r requirements.txt

echo.
echo 🎉 Environment setup complete!
echo.
echo To activate the environment manually, run:
echo   .venv\Scripts\activate.bat
echo.
echo To run Jupyter notebook:
echo   jupyter notebook
echo.
pause
