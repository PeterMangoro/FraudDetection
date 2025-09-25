# Fraud Detection App - Deployment Guide

## 🚀 Local Deployment

### Prerequisites
- Python 3.8 or higher
- Virtual environment activated

### Quick Start
```bash
# Activate virtual environment
.venv\Scripts\activate.bat

# Run the app
streamlit run streamlit_app.py
```

## 🌐 Cloud Deployment Options

### Option 1: Streamlit Cloud (Recommended)
1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repository
4. Use `requirements_minimal.txt` for dependencies

### Option 2: Heroku
1. Create a `Procfile`:
   ```
   web: streamlit run streamlit_app.py --server.port=$PORT --server.address=0.0.0.0
   ```
2. Use `requirements_minimal.txt`
3. Deploy using Heroku CLI

### Option 3: Docker
1. Create `Dockerfile`:
   ```dockerfile
   FROM python:3.9-slim
   WORKDIR /app
   COPY requirements_minimal.txt .
   RUN pip install -r requirements_minimal.txt
   COPY . .
   EXPOSE 8501
   CMD ["streamlit", "run", "streamlit_app.py", "--server.address", "0.0.0.0"]
   ```

## 📁 Required Files for Deployment
- `streamlit_app.py` - Main application
- `data_processing.py` - Data processing module
- `visualizations.py` - Visualization functions
- `kenya_fraud_detection.csv` - Dataset
- `requirements_minimal.txt` - Minimal dependencies

## 🔧 Troubleshooting

### Common Issues:
1. **Missing dependencies**: Use `requirements_minimal.txt`
2. **File paths**: Ensure CSV file is in the same directory
3. **Memory issues**: Reduce dataset size if needed
4. **Port conflicts**: Use `--server.port` parameter

### Environment Variables:
- `STREAMLIT_SERVER_PORT`: Port number (default: 8501)
- `STREAMLIT_SERVER_ADDRESS`: Server address (default: localhost)

## 📊 App Features
- Interactive fraud detection dashboard
- Real-time parameter tuning
- Multiple analysis tabs
- Export functionality
- Professional visualizations
