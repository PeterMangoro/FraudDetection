# 🚨 Fraud Detection System

A comprehensive machine learning system for detecting fraudulent transactions in mobile money services using unsupervised anomaly detection.

## 📋 Project Overview

This project implements an **Isolation Forest** algorithm to identify potentially fraudulent transactions in mobile money services (similar to M-Pesa in Kenya). The system analyzes transaction patterns, user behavior, and risk indicators to detect anomalies.

## 🎯 Features

- **Unsupervised Anomaly Detection**: Works without labeled fraud data
- **Comprehensive Feature Engineering**: Behavioral patterns, risk indicators, temporal features
- **Visual Analytics**: Detailed visualizations of fraud patterns
- **Production Ready**: Scalable and interpretable results

## 🔧 Setup Instructions

### Prerequisites
- Python 3.13+
- Git

### Quick Start

1. **Clone the repository** (if not already done):
   ```bash
   git clone <repository-url>
   cd FraudDetection
   ```

2. **Run the setup script**:
   ```bash
   setup_environment.bat
   ```

3. **Or manually activate the environment**:
   ```bash
   # Activate virtual environment
   .venv\Scripts\activate.bat
   
   # Install dependencies
   pip install -r requirements.txt
   ```

4. **Start Jupyter Notebook**:
   ```bash
   jupyter notebook
   ```

5. **Open `FraudDetection.ipynb`** and run all cells

## 📊 Data

The project uses a dataset of 10,000 mobile money transactions with the following features:
- Transaction details (amount, type, location)
- User information (ID, type, device)
- Risk indicators (SIM swapping, multiple accounts)
- Temporal features (time, date, day of week)

## 🤖 Model

- **Algorithm**: Isolation Forest
- **Type**: Unsupervised anomaly detection
- **Output**: Fraud probability scores and binary classifications
- **Performance**: Identifies ~2% of transactions as potentially fraudulent

## 📈 Results

The system successfully identifies:
- High-risk transaction patterns
- Suspicious user behaviors
- Geographic fraud clusters
- Temporal fraud trends
- Device and network risk factors

## 🛠️ Dependencies

Key packages used:
- `pandas`: Data manipulation
- `numpy`: Numerical computing
- `scikit-learn`: Machine learning
- `matplotlib`: Basic plotting
- `seaborn`: Statistical visualization
- `jupyter`: Notebook environment

## 📁 Project Structure

```
FraudDetection/
├── FraudDetection.ipynb          # Jupyter notebook analysis
├── streamlit_app.py              # Main Streamlit web application
├── data_processing.py            # Data processing and ML pipeline
├── visualizations.py             # Visualization functions
├── run_streamlit.py              # Python launcher script
├── run_streamlit.bat             # Windows batch launcher
├── kenya_fraud_detection.csv     # Dataset
├── requirements.txt              # Python dependencies
├── setup_environment.bat         # Environment setup script
├── README.md                     # This file
└── .venv/                        # Virtual environment
```

## 🚀 Usage

### Option 1: Interactive Web Dashboard (Recommended)
1. **Run the Streamlit App**:
   ```bash
   # Windows
   run_streamlit.bat
   
   # Or manually
   streamlit run streamlit_app.py
   ```
2. **Open your browser** to `http://localhost:8501`
3. **Interact with the dashboard** - adjust parameters, explore visualizations, and analyze fraud patterns

### Option 2: Jupyter Notebook Analysis
1. **Open the notebook**:
   ```bash
   jupyter notebook FraudDetection.ipynb
   ```
2. **Run all cells** to see the complete analysis
3. **Explore the code** and modify parameters as needed

### Dashboard Features:
- **Real-time Parameter Tuning**: Adjust model parameters and see immediate results
- **Interactive Visualizations**: Zoom, filter, and explore fraud patterns
- **Multiple Analysis Views**: Transaction, geographic, temporal, and user analysis
- **Export Capabilities**: Download suspicious transactions and reports
- **Professional Interface**: Clean, intuitive dashboard design

## 🔍 Key Insights

- **Fraud Rate**: ~2% of transactions flagged as suspicious
- **High-Risk Factors**: Night transactions, SIM swapping, multiple accounts
- **Geographic Patterns**: Certain locations show higher fraud rates
- **User Behavior**: Deviations from normal spending patterns

## 📚 Next Steps

- Model validation with labeled data
- Real-time deployment
- Ensemble methods
- Advanced feature engineering
- Business rule integration

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is for educational and research purposes.

---

*Built with ❤️ for fraud detection and prevention*
