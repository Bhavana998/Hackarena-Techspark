import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from datetime import datetime

class RealtimeMonitor:
    """Real-time monitoring component"""
    
    @staticmethod
    def display_metrics(df: pd.DataFrame):
        """Display real-time metrics"""
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Submissions/min", len(df), "+12")
        with col2:
            st.metric("Avg Score", f"{df['score'].mean():.1f}", "+2.3")
        with col3:
            st.metric("Anomaly Rate", f"{(df['is_anomaly'].sum() / len(df) * 100):.1f}%", "-1.2%")
        with col4:
            st.metric("API Latency", f"{df['latency_ms'].mean():.0f}ms", "-5ms")
    
    @staticmethod
    def create_live_chart():
        """Create live updating chart"""
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Quality Score Trend', 'Anomaly Detection', 'Status Distribution', 'Response Time')
        )
        
        # Initialize with empty data
        fig.add_trace(go.Scatter(x=[], y=[], mode='lines+markers', name='Score'), row=1, col=1)
        fig.add_trace(go.Scatter(x=[], y=[], mode='lines', name='Anomalies'), row=1, col=2)
        
        fig.update_layout(height=600, showlegend=True)
        return fig