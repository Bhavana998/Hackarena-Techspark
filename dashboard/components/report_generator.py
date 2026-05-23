import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

class ReportGenerator:
    """Generate validation reports"""
    
    @staticmethod
    def generate_summary_report(df: pd.DataFrame):
        """Generate summary report"""
        
        st.markdown("## Validation Summary Report")
        st.markdown(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Overall statistics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Validations", len(df))
        with col2:
            st.metric("Average Score", f"{df['quality_score'].mean():.1f}")
        with col3:
            st.metric("Pass Rate", f"{(df['quality_score'] > 70).mean() * 100:.1f}%")
        
        # Company breakdown
        st.subheader("Performance by Company")
        company_stats = df.groupby('company').agg({
            'quality_score': 'mean',
            'submission_id': 'count'
        }).round(2)
        company_stats.columns = ['Avg Score', 'Count']
        st.dataframe(company_stats)
        
        return df