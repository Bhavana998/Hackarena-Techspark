import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

class AnomalyExplorer:
    """Interactive anomaly exploration component"""
    
    @staticmethod
    def create_3d_scatter(df: pd.DataFrame):
        """Create 3D scatter plot of anomalies"""
        fig = px.scatter_3d(
            df,
            x='base_salary',
            y='years_experience',
            z='total_compensation',
            color='is_anomaly',
            title='3D Anomaly Visualization',
            labels={'base_salary': 'Base Salary', 'years_experience': 'Years Exp', 'total_compensation': 'Total Comp'}
        )
        return fig
    
    @staticmethod
    def create_anomaly_heatmap(df: pd.DataFrame):
        """Create anomaly heatmap by location and level"""
        pivot = df.pivot_table(
            values='anomaly_score',
            index='location',
            columns='level',
            aggfunc='mean'
        )
        
        fig = px.imshow(
            pivot,
            title='Anomaly Score Heatmap by Location and Level',
            color_continuous_scale='Reds'
        )
        return fig