"""
Data Processing Module for Fraud Detection
Extracted from the Jupyter notebook for use in Streamlit app
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.ensemble import IsolationForest
import warnings
warnings.filterwarnings('ignore')

class FraudDetectionProcessor:
    """Main class for processing fraud detection data"""
    
    def __init__(self):
        self.scaler = StandardScaler()
        self.encoder = OneHotEncoder(sparse_output=False, drop='first')
        self.model = None
        self.is_fitted = False
        
    def load_data(self, file_path='kenya_fraud_detection.csv'):
        """Load and initial data exploration"""
        try:
            df = pd.read_csv(file_path)
            return df
        except FileNotFoundError:
            st.error(f"Data file {file_path} not found!")
            return None
    
    def preprocess_data(self, df):
        """Clean and preprocess the data"""
        # Clean column names
        df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
        
        # Drop unnecessary columns
        columns_to_drop = ['time_of_day(morning,_afternoon,_evening,_night)', 'unnamed:_0']
        for col in columns_to_drop:
            if col in df.columns:
                df = df.drop([col], axis=1)
        
        # Convert datetime
        df['datetime'] = pd.to_datetime(df['datetime'])
        
        # Extract temporal features
        df['year'] = df['datetime'].dt.year
        df['month'] = df['datetime'].dt.month
        df['day'] = df['datetime'].dt.day
        df['hour'] = df['datetime'].dt.hour
        df['day_of_week'] = df['datetime'].dt.day_name()
        
        # Create time of day feature
        def map_time_of_day(hour):
            if 5 <= hour < 12:
                return "Morning"
            elif 12 <= hour < 17:
                return "Afternoon"
            elif 17 <= hour < 21:
                return "Evening"
            else:
                return "Night"
        
        df["time_of_day"] = df["hour"].apply(map_time_of_day)
        
        return df
    
    def engineer_features(self, df):
        """Create advanced features for fraud detection"""
        # Create date column for grouping
        df['date'] = df['datetime'].dt.date
        
        # Transactions per user per day
        user_txn_count = df.groupby(['user_id', 'date'])['transaction_id'].count().reset_index()
        user_txn_count.rename(columns={'transaction_id': 'txn_count_per_day'}, inplace=True)
        df = pd.merge(df, user_txn_count, on=['user_id', 'date'], how='left')
        
        # Average transaction amount per user
        user_avg_txn_amt = df.groupby(['user_id'])['amount'].mean().reset_index()
        user_avg_txn_amt.rename(columns={'amount': 'avg_txn_amt'}, inplace=True)
        df = pd.merge(df, user_avg_txn_amt, on=['user_id'], how='left')
        
        # Amount deviation from user average
        df['txn_amt_deviation'] = df['amount'] - df['avg_txn_amt']
        
        # Night transaction flag
        df['is_night_txn'] = df['time_of_day'].apply(lambda x: 1 if x == 'Night' else 0)
        
        # Risk score for SIM swapping and multiple accounts
        df['sim_multiple_risk_score'] = df['is_sim_recently_swapped'] + df['has_multiple_accounts']
        
        # Foreign number high amount
        df['foreign_high_amt'] = df['is_foreign_number'] * df['amount']
        
        # Count unique locations per user
        user_location_count = df.groupby(['user_id'])['location'].nunique().reset_index()
        user_location_count.rename(columns={'location': 'unique_location_count'}, inplace=True)
        df = pd.merge(df, user_location_count, on=['user_id'], how='left')
        
        return df
    
    def encode_and_scale(self, df):
        """Encode categorical variables and scale numerical features"""
        # Categorical columns for encoding
        categorical_cols = ['transaction_type', 'location', 'device_type', 
                           'network_provider', 'user_type', 'time_of_day', 'day_of_week']
        
        # Encode categorical variables
        encoded_data = self.encoder.fit_transform(df[categorical_cols])
        encoded_df = pd.DataFrame(encoded_data, 
                                columns=self.encoder.get_feature_names_out(categorical_cols))
        
        # Merge with original dataframe (drop original categorical columns)
        df_model = pd.concat([df.drop(columns=categorical_cols), encoded_df], axis=1)
        
        # Numerical columns for scaling
        numerical_cols = [
            'amount', 'month', 'day', 'hour',
            'is_foreign_number', 'is_sim_recently_swapped', 'has_multiple_accounts',
            'txn_count_per_day', 'avg_txn_amt', 'txn_amt_deviation',
            'is_night_txn', 'sim_multiple_risk_score', 'foreign_high_amt',
            'unique_location_count'
        ]
        
        # Scale numerical features
        df_model[numerical_cols] = self.scaler.fit_transform(df_model[numerical_cols])
        
        return df_model
    
    def train_model(self, df_model, contamination=0.02, n_estimators=200):
        """Train the Isolation Forest model"""
        # Select features for modeling (exclude IDs and datetime columns)
        features_model = [col for col in df_model.columns 
                         if col not in ['transaction_id', 'user_id', 'datetime', 'date']]
        
        X = df_model[features_model]
        
        # Initialize and train model
        self.model = IsolationForest(
            n_estimators=n_estimators,
            max_samples='auto',
            contamination=contamination,
            random_state=42
        )
        
        self.model.fit(X)
        self.is_fitted = True
        
        return X, features_model
    
    def predict_fraud(self, df_model, X, features_model):
        """Make fraud predictions"""
        if not self.is_fitted:
            raise ValueError("Model must be trained before making predictions")
        
        # Predict anomalies
        df_model['anomaly_score'] = self.model.decision_function(X)
        df_model['anomaly_label'] = self.model.predict(X)
        df_model['is_fraud_predicted'] = df_model['anomaly_label'].map({1: 0, -1: 1})
        
        return df_model
    
    def get_fraud_summary(self, df_model):
        """Get summary statistics of fraud detection"""
        fraud_count = df_model['is_fraud_predicted'].sum()
        total_count = len(df_model)
        fraud_rate = fraud_count / total_count * 100
        
        return {
            'total_transactions': total_count,
            'fraud_count': fraud_count,
            'fraud_rate': fraud_rate,
            'normal_count': total_count - fraud_count
        }
    
    def get_suspicious_transactions(self, df_model, df_original, top_n=10):
        """Get top suspicious transactions"""
        suspicious = df_model[df_model['is_fraud_predicted'] == 1].sort_values('anomaly_score').head(top_n)
        
        if suspicious.empty:
            return pd.DataFrame()
        
        # Get original transaction details - check which columns exist
        available_cols = ['transaction_id', 'user_id', 'amount']
        optional_cols = ['location', 'time_of_day', 'transaction_type']
        
        # Add optional columns if they exist
        for col in optional_cols:
            if col in df_original.columns:
                available_cols.append(col)
        
        suspicious_details = df_original.loc[suspicious.index, available_cols].copy()
        suspicious_details['anomaly_score'] = suspicious['anomaly_score'].values
        
        # Add risk score if available
        if 'sim_multiple_risk_score' in suspicious.columns:
            suspicious_details['risk_score'] = suspicious['sim_multiple_risk_score'].values
        
        return suspicious_details
    
    def get_fraud_patterns(self, df_model, df_original):
        """Get fraud patterns by various categories"""
        # Merge with original data for categorical analysis
        df_analysis = df_original.copy()
        df_analysis['is_fraud_predicted'] = df_model['is_fraud_predicted'].values
        
        patterns = {}
        
        # Check if columns exist before grouping
        if 'location' in df_analysis.columns:
            patterns['location'] = df_analysis.groupby('location')['is_fraud_predicted'].mean().sort_values(ascending=False)
        
        if 'time_of_day' in df_analysis.columns:
            patterns['time_of_day'] = df_analysis.groupby('time_of_day')['is_fraud_predicted'].mean()
        
        if 'device_type' in df_analysis.columns:
            patterns['device_type'] = df_analysis.groupby('device_type')['is_fraud_predicted'].mean()
        
        if 'transaction_type' in df_analysis.columns:
            patterns['transaction_type'] = df_analysis.groupby('transaction_type')['is_fraud_predicted'].mean()
        
        if 'network_provider' in df_analysis.columns:
            patterns['network_provider'] = df_analysis.groupby('network_provider')['is_fraud_predicted'].mean()
        
        return patterns
    
    def get_high_risk_users(self, df_model, df_original, top_n=10):
        """Get users with highest fraud rates"""
        df_analysis = df_original.copy()
        df_analysis['is_fraud_predicted'] = df_model['is_fraud_predicted'].values
        
        user_fraud_rate = df_analysis.groupby('user_id')['is_fraud_predicted'].mean().sort_values(ascending=False)
        
        return user_fraud_rate.head(top_n)
    
    def process_complete_pipeline(self, file_path='kenya_fraud_detection.csv'):
        """Run the complete data processing pipeline"""
        # Load data
        df = self.load_data(file_path)
        if df is None:
            return None, None, None, None
        
        # Preprocess
        df_clean = self.preprocess_data(df)
        
        # Feature engineering
        df_features = self.engineer_features(df_clean)
        
        # Encode and scale
        df_model = self.encode_and_scale(df_features)
        
        # Train model
        X, features = self.train_model(df_model)
        
        # Make predictions
        df_model = self.predict_fraud(df_model, X, features)
        
        return df, df_clean, df_model, features
