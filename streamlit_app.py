"""
Fraud Detection System - Streamlit Web Application
Interactive dashboard for fraud detection analysis
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Import our custom modules
from data_processing import FraudDetectionProcessor
from visualizations import *

# Page configuration
st.set_page_config(
    page_title="Fraud Detection System",
    page_icon="🚨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .section-header {
        font-size: 1.5rem;
        color: #ff7f0e;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'processor' not in st.session_state:
    st.session_state.processor = FraudDetectionProcessor()
    st.session_state.data_loaded = False
    st.session_state.model_trained = False

def main():
    """Main Streamlit application"""
    
    # Header
    st.markdown('<h1 class="main-header">🚨 Fraud Detection System</h1>', unsafe_allow_html=True)
    st.markdown("### Interactive Dashboard for Mobile Money Fraud Detection")
    
    # Sidebar
    with st.sidebar:
        st.header("🔧 Configuration")
        
        # Model parameters
        st.subheader("Model Parameters")
        contamination = st.slider(
            "Contamination Rate",
            min_value=0.01,
            max_value=0.10,
            value=0.02,
            step=0.01,
            help="Expected proportion of anomalies in the dataset"
        )
        
        n_estimators = st.slider(
            "Number of Estimators",
            min_value=50,
            max_value=500,
            value=200,
            step=50,
            help="Number of trees in the Isolation Forest"
        )
        
        # Analysis options
        st.subheader("Analysis Options")
        show_suspicious_count = st.number_input(
            "Number of Top Suspicious Transactions",
            min_value=5,
            max_value=50,
            value=10
        )
        
        show_high_risk_users = st.number_input(
            "Number of High-Risk Users",
            min_value=5,
            max_value=20,
            value=10
        )
        
        # Load data button
        if st.button("🔄 Load and Process Data", type="primary"):
            with st.spinner("Loading and processing data..."):
                try:
                    df_original, df_clean, df_model, features = st.session_state.processor.process_complete_pipeline()
                    
                    if df_original is not None:
                        st.session_state.df_original = df_original
                        st.session_state.df_clean = df_clean
                        st.session_state.df_model = df_model
                        st.session_state.features = features
                        st.session_state.data_loaded = True
                        st.session_state.model_trained = True
                        st.success("✅ Data loaded and model trained successfully!")
                    else:
                        st.error("❌ Failed to load data")
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
    
    # Main content
    if not st.session_state.data_loaded:
        st.info("👈 Please load the data using the sidebar to begin analysis")
        
        # Show sample data structure
        st.subheader("📊 Data Structure Preview")
        st.markdown("""
        The fraud detection system analyzes the following features:
        - **Transaction Details**: Amount, type, location, datetime
        - **User Information**: User ID, type, device, network provider
        - **Risk Indicators**: SIM swapping, multiple accounts, foreign numbers
        - **Behavioral Patterns**: Transaction frequency, amount deviations, temporal patterns
        """)
        
        # Show example of what the system detects
        st.subheader("🎯 What the System Detects")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**High-Risk Patterns:**")
            st.markdown("""
            - Unusual transaction amounts
            - Night-time transactions
            - SIM swapping activities
            - Multiple account usage
            - Foreign number transactions
            """)
        
        with col2:
            st.markdown("**Analysis Features:**")
            st.markdown("""
            - Real-time fraud scoring
            - Geographic fraud patterns
            - Temporal trend analysis
            - User risk profiling
            - Interactive visualizations
            """)
        
    else:
        # Get data from session state
        df_original = st.session_state.df_original
        df_clean = st.session_state.df_clean
        df_model = st.session_state.df_model
        features = st.session_state.features
        
        # Get fraud summary
        fraud_summary = st.session_state.processor.get_fraud_summary(df_model)
        
        # Overview Section
        st.markdown('<h2 class="section-header">📊 Fraud Detection Overview</h2>', unsafe_allow_html=True)
        create_summary_metrics_display(fraud_summary)
        
        # Overview chart
        col1, col2 = st.columns([2, 1])
        
        with col1:
            overview_fig = create_fraud_overview_chart(fraud_summary)
            st.plotly_chart(overview_fig, use_container_width=True, key="fraud_overview")
        
        with col2:
            st.markdown("### 🎯 Key Insights")
            st.markdown(f"""
            - **Total Transactions Analyzed**: {fraud_summary['total_transactions']:,}
            - **Fraud Detection Rate**: {fraud_summary['fraud_rate']:.2f}%
            - **Model Algorithm**: Isolation Forest
            - **Detection Method**: Unsupervised Anomaly Detection
            """)
        
        # Tabs for different analyses
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
            "🔍 Transaction Analysis", 
            "📍 Geographic Patterns", 
            "⏰ Temporal Analysis", 
            "👥 User Risk Profiles", 
            "📊 Additional Analysis",
            "🚨 Suspicious Transactions"
        ])
        
        with tab1:
            st.markdown('<h3 class="section-header">Transaction Amount Analysis</h3>', unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                scatter_fig = create_amount_scatter_plot(df_model)
                st.plotly_chart(scatter_fig, use_container_width=True, key="amount_scatter")
            
            with col2:
                box_fig = create_amount_distribution_boxplot(df_model)
                st.plotly_chart(box_fig, use_container_width=True, key="amount_boxplot")
            
            # Anomaly score distribution
            st.markdown("### Anomaly Score Distribution")
            score_dist_fig = create_anomaly_score_distribution(df_model)
            if score_dist_fig:
                st.plotly_chart(score_dist_fig, use_container_width=True, key="anomaly_distribution")
                st.write("Lower anomaly scores indicate higher likelihood of fraud.")
            
            # Fraud patterns by transaction type
            st.markdown("### Transaction Type Analysis")
            patterns = st.session_state.processor.get_fraud_patterns(df_model, df_original)
            
            col1, col2 = st.columns(2)
            
            with col1:
                if 'transaction_type' in patterns:
                    type_fig = create_fraud_by_category_chart(patterns, 'transaction_type')
                    if type_fig:
                        st.plotly_chart(type_fig, use_container_width=True, key="transaction_type_rates")
                    else:
                        st.info("Transaction type analysis not available")
            
            with col2:
                # Show fraud transactions by type
                df_fraud = df_original[df_model['is_fraud_predicted'] == 1]
                count_fig = create_fraud_count_by_type_chart(df_fraud)
                if count_fig:
                    st.plotly_chart(count_fig, use_container_width=True, key="transaction_type_counts")
                else:
                    st.info("Fraud count by type not available")
        
        with tab2:
            st.markdown('<h3 class="section-header">Geographic Fraud Patterns</h3>', unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                if 'location' in patterns:
                    location_fig = create_fraud_by_category_chart(patterns, 'location')
                    if location_fig:
                        st.plotly_chart(location_fig, use_container_width=True, key="location_rates")
                    else:
                        st.info("Location analysis not available")
            
            with col2:
                if 'network_provider' in patterns:
                    provider_fig = create_fraud_by_category_chart(patterns, 'network_provider')
                    if provider_fig:
                        st.plotly_chart(provider_fig, use_container_width=True, key="network_provider_rates")
                    else:
                        st.info("Network provider analysis not available")
            
            # SIM swapped analysis
            st.markdown("### SIM Swapped Analysis")
            df_fraud = df_original[df_model['is_fraud_predicted'] == 1]
            sim_fig = create_sim_swapped_analysis(df_fraud)
            if sim_fig:
                st.plotly_chart(sim_fig, use_container_width=True, key="sim_swapped_analysis")
            else:
                st.info("SIM swapped analysis not available")
        
        with tab3:
            st.markdown('<h3 class="section-header">Temporal Fraud Patterns</h3>', unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                timeline_fig = create_timeline_chart(df_model)
                st.plotly_chart(timeline_fig, use_container_width=True, key="timeline_chart")
            
            with col2:
                if 'time_of_day' in patterns:
                    time_fig = create_fraud_by_category_chart(patterns, 'time_of_day')
                    if time_fig:
                        st.plotly_chart(time_fig, use_container_width=True, key="time_of_day_analysis")
                    else:
                        st.info("Time of day analysis not available")
        
        with tab4:
            st.markdown('<h3 class="section-header">User Risk Analysis</h3>', unsafe_allow_html=True)
            
            # High-risk users
            high_risk_users = st.session_state.processor.get_high_risk_users(df_model, df_original, show_high_risk_users)
            
            col1, col2 = st.columns(2)
            
            with col1:
                user_fig = create_user_risk_chart(high_risk_users)
                if user_fig:
                    st.plotly_chart(user_fig, use_container_width=True, key="user_risk_chart")
            
            with col2:
                if 'device_type' in patterns:
                    device_fig = create_fraud_by_category_chart(patterns, 'device_type')
                    if device_fig:
                        st.plotly_chart(device_fig, use_container_width=True, key="device_type_analysis")
                    else:
                        st.info("Device type analysis not available")
            
            # Risk heatmap
            st.markdown("### Risk Score Heatmap")
            heatmap_fig = create_risk_heatmap(df_model, show_suspicious_count)
            if heatmap_fig:
                st.plotly_chart(heatmap_fig, use_container_width=True, key="risk_heatmap_tab4")
        
        with tab5:
            st.markdown('<h3 class="section-header">Additional Analysis</h3>', unsafe_allow_html=True)
            
            # Network provider analysis
            st.markdown("### Network Provider Fraud Analysis")
            df_fraud = df_original[df_model['is_fraud_predicted'] == 1]
            network_fig = create_fraud_by_network_provider_chart(df_fraud)
            if network_fig:
                st.plotly_chart(network_fig, use_container_width=True, key="network_provider_counts")
            else:
                st.info("Network provider analysis not available")
            
            # Risk heatmap
            st.markdown("### Risk Score Heatmap")
            heatmap_fig = create_risk_heatmap(df_model, show_suspicious_count)
            if heatmap_fig:
                st.plotly_chart(heatmap_fig, use_container_width=True, key="risk_heatmap_tab5")
                st.write("Heatmap showing risk scores for top suspicious transactions across different features.")
            else:
                st.info("Risk heatmap not available")
        
        with tab6:
            st.markdown('<h3 class="section-header">Top Suspicious Transactions</h3>', unsafe_allow_html=True)
            
            # Get suspicious transactions
            suspicious_txns = st.session_state.processor.get_suspicious_transactions(
                df_model, df_original, show_suspicious_count
            )
            
            if not suspicious_txns.empty:
                st.markdown(f"**Top {show_suspicious_count} Most Suspicious Transactions:**")
                
                # Display as a nice table
                suspicious_display = suspicious_txns.copy()
                suspicious_display['amount'] = suspicious_display['amount'].round(2)
                suspicious_display['anomaly_score'] = suspicious_display['anomaly_score'].round(4)
                suspicious_display['risk_score'] = suspicious_display['risk_score'].round(2)
                
                st.dataframe(
                    suspicious_display,
                    use_container_width=True,
                    hide_index=True
                )
                
                # Download option
                csv = suspicious_display.to_csv(index=False)
                st.download_button(
                    label="📥 Download Suspicious Transactions CSV",
                    data=csv,
                    file_name=f"suspicious_transactions_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
            else:
                st.info("No suspicious transactions found with current parameters")
        
        # Footer
        st.markdown("---")
        st.markdown("""
        <div style='text-align: center; color: #666;'>
            <p>🚨 Fraud Detection System | Built with Streamlit & Isolation Forest</p>
            <p>For demonstration purposes only</p>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
