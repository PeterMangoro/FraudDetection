"""
Simple launcher script for the Streamlit Fraud Detection App
"""

import subprocess
import sys
import os

def main():
    """Launch the Streamlit app"""
    print("🚨 Starting Fraud Detection System...")
    print("📊 Loading Streamlit Dashboard...")
    print("🌐 The app will open in your default browser")
    print("=" * 50)
    
    try:
        # Run streamlit app
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "streamlit_app.py",
            "--server.port", "8501",
            "--server.address", "localhost"
        ])
    except KeyboardInterrupt:
        print("\n👋 App stopped by user")
    except Exception as e:
        print(f"❌ Error starting app: {e}")
        print("Make sure you have activated the virtual environment and installed all dependencies")

if __name__ == "__main__":
    main()
