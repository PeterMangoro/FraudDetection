"""
Visualization functions for Fraud Detection Streamlit App
"""

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

def create_fraud_overview_chart(fraud_summary):
    """Create overview metrics chart"""
    fig = go.Figure()
    
    # Add fraud vs normal comparison
    categories = ['Normal', 'Fraud']
    values = [fraud_summary['normal_count'], fraud_summary['fraud_count']]
    colors = ['#2E8B57', '#DC143C']
    
    fig.add_trace(go.Bar(
        x=categories,
        y=values,
        marker_color=colors,
        text=values,
        textposition='auto',
    ))
    
    fig.update_layout(
        title="Fraud Detection Overview",
        xaxis_title="Transaction Type",
        yaxis_title="Number of Transactions",
        showlegend=False,
        height=400
    )
    
    return fig

def create_amount_scatter_plot(df_model):
    """Create scatter plot of anomalies vs normal transactions"""
    fig = px.scatter(
        df_model,
        x='amount',
        y='avg_txn_amt',
        color='is_fraud_predicted',
        color_discrete_map={0: 'blue', 1: 'red'},
        title="Transaction Amount vs User Average (Anomalies in Red)",
        labels={
            'amount': 'Transaction Amount (Scaled)',
            'avg_txn_amt': 'User Average Amount (Scaled)',
            'is_fraud_predicted': 'Fraud Prediction'
        },
        opacity=0.6
    )
    
    fig.update_layout(height=500)
    return fig

def create_timeline_chart(df_model):
    """Create timeline of fraud detection"""
    df_model['date'] = pd.to_datetime(df_model['date'])
    timeline_data = df_model.groupby('date')['is_fraud_predicted'].apply(lambda x: (x==1).sum()).reset_index()
    timeline_data.columns = ['date', 'fraud_count']
    
    fig = px.line(
        timeline_data,
        x='date',
        y='fraud_count',
        title="Fraud Detection Over Time",
        labels={
            'date': 'Date',
            'fraud_count': 'Number of Fraudulent Transactions'
        },
        markers=True
    )
    
    fig.update_layout(height=400)
    return fig

def create_amount_distribution_boxplot(df_model):
    """Create boxplot of transaction amounts by fraud status"""
    # Convert fraud prediction to string for better display
    df_model['fraud_status'] = df_model['is_fraud_predicted'].map({0: 'Normal', 1: 'Fraud'})
    
    fig = px.box(
        df_model,
        x='fraud_status',
        y='amount',
        title="Transaction Amount Distribution: Fraud vs Normal",
        labels={
            'fraud_status': 'Transaction Status',
            'amount': 'Transaction Amount (Scaled)'
        }
    )
    
    fig.update_layout(height=400)
    return fig

def create_fraud_by_category_chart(patterns, category):
    """Create bar chart for fraud patterns by category"""
    if category not in patterns or patterns[category].empty:
        return None
    
    try:
        df_chart = patterns[category].reset_index()
        df_chart.columns = ['category', 'fraud_rate']
        df_chart['fraud_rate'] = df_chart['fraud_rate'] * 100  # Convert to percentage
        
        fig = px.bar(
            df_chart,
            x='category',
            y='fraud_rate',
            title=f"Fraud Rate by {category.replace('_', ' ').title()}",
            labels={
                'category': category.replace('_', ' ').title(),
                'fraud_rate': 'Fraud Rate (%)'
            }
        )
        
        fig.update_layout(
            height=400,
            xaxis_tickangle=-45
        )
        
        return fig
    except Exception as e:
        print(f"Error creating chart for {category}: {e}")
        return None

def create_fraud_count_by_type_chart(df_fraud):
    """Create count chart for fraud transactions by type"""
    if df_fraud.empty:
        return None
    
    fraud_counts = df_fraud['transaction_type'].value_counts()
    
    fig = px.bar(
        x=fraud_counts.index,
        y=fraud_counts.values,
        title="Fraud Transactions by Type",
        labels={
            'x': 'Transaction Type',
            'y': 'Number of Fraudulent Transactions'
        }
    )
    
    fig.update_layout(
        height=400,
        xaxis_tickangle=-45
    )
    
    return fig

def create_risk_heatmap(df_model, top_n=20):
    """Create risk score heatmap for top suspicious transactions"""
    # Get top suspicious transactions
    suspicious = df_model[df_model['is_fraud_predicted'] == 1].nlargest(top_n, 'anomaly_score')
    
    if suspicious.empty:
        return None
    
    # Create heatmap data
    risk_features = ['amount', 'avg_txn_amt', 'txn_amt_deviation', 
                    'sim_multiple_risk_score', 'foreign_high_amt', 'unique_location_count']
    
    heatmap_data = suspicious[risk_features].T
    heatmap_data.columns = [f"TXN {i}" for i in range(1, len(suspicious) + 1)]
    
    fig = px.imshow(
        heatmap_data,
        aspect="auto",
        title=f"Risk Score Heatmap - Top {top_n} Suspicious Transactions",
        labels={
            'x': 'Transaction',
            'y': 'Risk Features',
            'color': 'Scaled Value'
        }
    )
    
    fig.update_layout(height=500)
    return fig

def create_user_risk_chart(high_risk_users):
    """Create chart for high-risk users"""
    if high_risk_users.empty:
        return None
    
    df_chart = high_risk_users.reset_index()
    df_chart.columns = ['user_id', 'fraud_rate']
    df_chart['fraud_rate'] = df_chart['fraud_rate'] * 100  # Convert to percentage
    
    fig = px.bar(
        df_chart,
        x='user_id',
        y='fraud_rate',
        title="Top High-Risk Users by Fraud Rate",
        labels={
            'user_id': 'User ID',
            'fraud_rate': 'Fraud Rate (%)'
        }
    )
    
    fig.update_layout(
        height=400,
        xaxis_tickangle=-45
    )
    
    return fig

def create_sim_swapped_analysis(df_fraud):
    """Create analysis of SIM swapped transactions"""
    if df_fraud.empty or 'is_sim_recently_swapped' not in df_fraud.columns:
        return None
    
    try:
        sim_counts = df_fraud['is_sim_recently_swapped'].value_counts().reset_index()
        sim_counts.columns = ['is_sim_recently_swapped', 'count']
        sim_counts['is_sim_recently_swapped'] = sim_counts['is_sim_recently_swapped'].map({0: 'No', 1: 'Yes'})
        
        fig = px.bar(
            sim_counts,
            x='is_sim_recently_swapped',
            y='count',
            title="Fraud Transactions by SIM Swapped Status",
            labels={
                'is_sim_recently_swapped': 'SIM Recently Swapped',
                'count': 'Number of Fraudulent Transactions'
            },
            color='is_sim_recently_swapped',
            color_discrete_map={'No': 'lightblue', 'Yes': 'orange'}
        )
        
        fig.update_layout(height=400)
        return fig
    except Exception as e:
        print(f"Error creating SIM swapped analysis: {e}")
        return None

def create_fraud_by_network_provider_chart(df_fraud):
    """Create chart showing fraud by network provider"""
    if df_fraud.empty or 'network_provider' not in df_fraud.columns:
        return None
    
    try:
        provider_counts = df_fraud['network_provider'].value_counts().reset_index()
        provider_counts.columns = ['network_provider', 'count']
        
        fig = px.bar(
            provider_counts,
            x='network_provider',
            y='count',
            title="Fraud Transactions by Network Provider",
            labels={
                'network_provider': 'Network Provider',
                'count': 'Number of Fraudulent Transactions'
            }
        )
        
        fig.update_layout(height=400)
        return fig
    except Exception as e:
        print(f"Error creating network provider chart: {e}")
        return None

def create_anomaly_score_distribution(df_model):
    """Create distribution of anomaly scores"""
    try:
        fig = px.histogram(
            df_model,
            x='anomaly_score',
            color='is_fraud_predicted',
            color_discrete_map={0: 'blue', 1: 'red'},
            title='Distribution of Anomaly Scores',
            labels={
                'anomaly_score': 'Anomaly Score',
                'count': 'Number of Transactions',
                'is_fraud_predicted': 'Status'
            },
            nbins=50
        )
        
        fig.update_layout(height=400)
        return fig
    except Exception as e:
        print(f"Error creating anomaly score distribution: {e}")
        return None

def create_summary_metrics_display(fraud_summary):
    """Create summary metrics display"""
    import streamlit as st
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Total Transactions",
            value=f"{fraud_summary['total_transactions']:,}"
        )
    
    with col2:
        st.metric(
            label="Fraudulent Transactions",
            value=f"{fraud_summary['fraud_count']:,}",
            delta=f"{fraud_summary['fraud_rate']:.1f}%"
        )
    
    with col3:
        st.metric(
            label="Normal Transactions",
            value=f"{fraud_summary['normal_count']:,}"
        )
    
    with col4:
        st.metric(
            label="Fraud Detection Rate",
            value=f"{fraud_summary['fraud_rate']:.2f}%"
        )
