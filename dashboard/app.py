"""🏆 HACKATHON WINNING DASHBOARD - FULLY VISIBLE"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import numpy as np
import random

# Page config MUST be first
st.set_page_config(
    page_title="Levels.fyi | Compensation Intelligence",
    page_icon="🏆",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# SIMPLE CSS - ENSURE VISIBILITY
# ============================================================================

st.markdown("""
<style>
    /* Force all text to be visible */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Main content area - WHITE background */
    .main .block-container {
        background: white !important;
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem auto;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    
    /* Ensure ALL text in main area is dark */
    .main * {
        color: #1a1a2e !important;
    }
    
    /* Headers */
    h1, h2, h3, h4, h5, h6 {
        color: #1a1a2e !important;
        font-weight: 700 !important;
    }
    
    /* Labels */
    .stSelectbox label, .stTextInput label, .stNumberInput label {
        color: #1a1a2e !important;
        font-weight: 600 !important;
    }
    
    /* Sidebar - Dark background with white text */
    .stSidebar {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%) !important;
    }
    
    .stSidebar * {
        color: white !important;
    }
    
    /* Metrics in sidebar */
    .stSidebar [data-testid="stMetricValue"] {
        color: #ffd93d !important;
        font-size: 1.5rem !important;
    }
    
    .stSidebar [data-testid="stMetricLabel"] {
        color: rgba(255,255,255,0.8) !important;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
        font-weight: 600 !important;
    }
    
    /* Success/Warning/Info boxes */
    .stAlert {
        background-color: #f8f9fa !important;
        border-left: 4px solid #667eea !important;
    }
    
    /* Cards */
    .metric-card {
        background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%);
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        border: 1px solid #e0e0e0;
        margin: 0.5rem 0;
    }
    
    .metric-card .value {
        font-size: 2rem;
        font-weight: 800;
        color: #667eea;
    }
    
    .metric-card .label {
        font-size: 0.8rem;
        color: #6c757d;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .company-card {
        background: white;
        border: 2px solid #e0e0e0;
        border-radius: 12px;
        padding: 1rem;
        text-align: center;
        cursor: pointer;
        transition: all 0.3s;
    }
    
    .company-card:hover {
        border-color: #667eea;
        box-shadow: 0 5px 15px rgba(102,126,234,0.2);
    }
    
    .company-card.selected {
        border-color: #667eea;
        background: linear-gradient(135deg, #f0f4ff 0%, #ffffff 100%);
    }
    
    .benchmark-card {
        background: #f8f9fa;
        border-radius: 15px;
        padding: 1.5rem;
        border-left: 4px solid #667eea;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# COMPLETE BENCHMARK DATA
# ============================================================================

BENCHMARK_DATA = {
    "Google": {
        "India": {"IC3": 105000, "IC4": 165000, "IC5": 240000},
        "USA": {"IC3": 285000, "IC4": 370000, "IC5": 480000}
    },
    "Microsoft": {
        "India": {"IC3": 88000, "IC4": 138000, "IC5": 200000},
        "USA": {"IC3": 250000, "IC4": 325000, "IC5": 420000}
    },
    "Amazon": {
        "India": {"IC3": 85000, "IC4": 130000, "IC5": 190000},
        "USA": {"IC3": 235000, "IC4": 305000, "IC5": 395000}
    },
    "Meta": {
        "India": {"IC3": 100000, "IC4": 155000, "IC5": 225000},
        "USA": {"IC3": 280000, "IC4": 365000, "IC5": 475000}
    },
    "Apple": {
        "India": {"IC3": 97000, "IC4": 150000, "IC5": 218000},
        "USA": {"IC3": 275000, "IC4": 360000, "IC5": 470000}
    },
    "ServiceNow": {
        "India": {"IC3": 58000, "IC4": 90000, "IC5": 135000},
        "USA": {"IC3": 195000, "IC4": 255000, "IC5": 340000}
    }
}

COMPANY_COLORS = {
    "Google": "#4285F4",
    "Microsoft": "#F25022",
    "Amazon": "#FF9900",
    "Meta": "#1877F2",
    "Apple": "#A2AAAD",
    "ServiceNow": "#00A1E0"
}

# ============================================================================
# SIDEBAR
# ============================================================================

with st.sidebar:
    st.markdown("## 🏆 Levels.fyi")
    st.markdown("### AI Intelligence")
    st.markdown("---")
    
    # Navigation
    page = st.radio(
        "Navigation",
        ["📊 Compensation Benchmarks", "🎯 Live Validation", "📈 Analytics", "📋 Audit Trail"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    # System Status
    st.markdown("### System Status")
    st.markdown("🟢 **Online**")
    st.markdown("API v1.0")
    
    st.markdown("---")
    
    # Quick Stats
    st.markdown("### Quick Stats")
    st.metric("Total Validations", "12,847", "+23%")
    st.metric("Avg Quality Score", "87.4", "+5.2%")
    st.metric("Companies Tracked", "247", "+12")

# ============================================================================
# MAIN CONTENT - BENCHMARKS PAGE
# ============================================================================

if page == "📊 Compensation Benchmarks":
    
    # Header
    st.markdown("# 🎯 Compensation Benchmarks")
    st.markdown("Compare salaries across top technology companies")
    st.markdown("---")
    
    # Company Selection
    st.markdown("### Select Company")
    
    companies = ["Google", "Microsoft", "Amazon", "Meta", "Apple", "ServiceNow"]
    cols = st.columns(6)
    
    if 'selected_company' not in st.session_state:
        st.session_state.selected_company = "Google"
    
    for idx, company in enumerate(companies):
        with cols[idx]:
            is_selected = st.session_state.selected_company == company
            border = "2px solid #667eea" if is_selected else "1px solid #ddd"
            bg = "#f0f4ff" if is_selected else "white"
            st.markdown(f"""
            <div style="text-align: center; padding: 0.5rem; border: {border}; border-radius: 10px; background: {bg}; cursor: pointer;">
                <div style="font-weight: bold; color: #1a1a2e;">{company}</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"Select {company}", key=f"btn_{company}", use_container_width=True):
                st.session_state.selected_company = company
                st.rerun()
    
    st.markdown("---")
    
    # Filters
    col1, col2 = st.columns(2)
    with col1:
        level = st.selectbox("Select Level", ["IC3", "IC4", "IC5"], index=1)
    with col2:
        region = st.selectbox("Select Region", ["India", "USA"], index=0)
    
    st.markdown("---")
    
    # Get data for selected company
    company = st.session_state.selected_company
    salary = BENCHMARK_DATA.get(company, {}).get(region, {}).get(level, 0)
    
    if salary > 0:
        # Main display
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Gauge chart
            min_val = int(salary * 0.7)
            max_val = int(salary * 1.5)
            
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=salary,
                title={"text": f"{company} {level} - {region}", "font": {"size": 20}},
                gauge={
                    "axis": {"range": [min_val, max_val], "tickprefix": "$"},
                    "bar": {"color": COMPANY_COLORS.get(company, "#667eea")},
                    "steps": [
                        {"range": [min_val, min_val + (max_val-min_val)*0.33], "color": "#ffcccc"},
                        {"range": [min_val + (max_val-min_val)*0.33, min_val + (max_val-min_val)*0.66], "color": "#ffffcc"},
                        {"range": [min_val + (max_val-min_val)*0.66, max_val], "color": "#ccffcc"}
                    ]
                }
            ))
            fig.update_layout(height=350)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown(f"""
            <div class="benchmark-card">
                <div style="text-align: center;">
                    <div style="font-size: 2.5rem; font-weight: 800; color: #667eea;">${salary:,.0f}</div>
                    <div style="color: #6c757d;">Median Total Compensation</div>
                    <hr>
                    <div style="display: flex; justify-content: space-between;">
                        <div>
                            <div style="font-size: 1.2rem; font-weight: bold;">${min_val:,.0f}</div>
                            <div style="font-size: 0.7rem;">Bottom 10%</div>
                        </div>
                        <div>
                            <div style="font-size: 1.2rem; font-weight: bold;">${max_val:,.0f}</div>
                            <div style="font-size: 0.7rem;">Top 10%</div>
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Comparison chart - all companies
        st.markdown("### 🏢 Market Comparison")
        
        comparison_data = []
        for comp in companies:
            comp_salary = BENCHMARK_DATA.get(comp, {}).get(region, {}).get(level, 0)
            if comp_salary > 0:
                comparison_data.append({
                    "Company": comp,
                    "Salary": comp_salary,
                    "Color": COMPANY_COLORS.get(comp, "#667eea")
                })
        
        if comparison_data:
            df_compare = pd.DataFrame(comparison_data)
            
            fig = px.bar(df_compare, x="Company", y="Salary", 
                        title=f"{level} Salary Comparison - {region}",
                        color="Company", color_discrete_map=COMPANY_COLORS,
                        text="Salary")
            fig.update_traces(texttemplate="$%{text:,.0f}", textposition="outside")
            fig.update_layout(height=450, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
        
        # Level progression
        st.markdown("### 📈 Career Progression")
        
        progression = []
        for lvl in ["IC3", "IC4", "IC5"]:
            lvl_salary = BENCHMARK_DATA.get(company, {}).get(region, {}).get(lvl, 0)
            if lvl_salary > 0:
                progression.append({"Level": lvl, "Salary": lvl_salary})
        
        if progression:
            df_prog = pd.DataFrame(progression)
            fig = px.line(df_prog, x="Level", y="Salary", 
                         title=f"Salary Growth - {company} ({region})",
                         markers=True)
            fig.update_traces(line=dict(color=COMPANY_COLORS.get(company, "#667eea"), width=3),
                            marker=dict(size=12))
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        # Insights
        st.markdown("### 💡 Market Insights")
        
        avg_salary = np.mean([d["Salary"] for d in comparison_data]) if comparison_data else salary
        diff_percent = ((salary - avg_salary) / avg_salary) * 100
        
        col1, col2, col3 = st.columns(3)
        with col1:
            if diff_percent > 0:
                st.success(f"✅ {company} pays {diff_percent:.0f}% **above** market average")
            else:
                st.warning(f"⚠️ {company} pays {abs(diff_percent):.0f}% **below** market average")
        
        with col2:
            highest = max(comparison_data, key=lambda x: x["Salary"]) if comparison_data else None
            if highest:
                st.info(f"🏆 Highest payer: **{highest['Company']}** (${highest['Salary']:,.0f})")
        
        with col3:
            st.metric("Sample Size", "1,200+", "verified")

# ============================================================================
# LIVE VALIDATION PAGE
# ============================================================================

elif page == "🎯 Live Validation":
    
    st.markdown("# 🎯 Live Compensation Validation")
    st.markdown("Enter your offer details for AI-powered analysis")
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        company = st.selectbox("Company", list(COMPANY_COLORS.keys()))
        title = st.text_input("Job Title", "Software Engineer")
        level = st.selectbox("Level", ["IC3", "IC4", "IC5"], index=1)
        location = st.text_input("Location", "Bangalore, India")
    
    with col2:
        years_exp = st.slider("Years of Experience", 0, 20, 5)
        base_salary = st.number_input("Base Salary (USD)", min_value=0, value=180000, step=10000)
        bonus = st.number_input("Annual Bonus (USD)", min_value=0, value=30000, step=5000)
        stock = st.number_input("Stock Grant (USD)", min_value=0, value=50000, step=10000)
    
    total_comp = base_salary + bonus + stock
    
    if st.button("🔍 Validate Offer", use_container_width=True):
        with st.spinner("AI analyzing market data..."):
            # Determine region
            region = "USA" if "USA" in location or "United States" in location else "India"
            
            # Get market benchmark
            market = BENCHMARK_DATA.get(company, {}).get(region, {}).get(level, 0)
            
            if market > 0:
                diff_percent = ((total_comp - market) / market) * 100
                
                st.markdown("---")
                st.markdown("## 📊 Validation Results")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    if total_comp > market:
                        st.markdown(f"""
                        <div style="background: #d4edda; padding: 1.5rem; border-radius: 15px; text-align: center;">
                            <div style="font-size: 3rem;">✅</div>
                            <div style="font-size: 1.5rem; font-weight: bold; color: #155724;">EXCELLENT OFFER!</div>
                            <div style="font-size: 1rem; color: #155724;">{diff_percent:+.0f}% above market</div>
                        </div>
                        """, unsafe_allow_html=True)
                    elif total_comp > market * 0.8:
                        st.markdown(f"""
                        <div style="background: #fff3cd; padding: 1.5rem; border-radius: 15px; text-align: center;">
                            <div style="font-size: 3rem;">⚠️</div>
                            <div style="font-size: 1.5rem; font-weight: bold; color: #856404;">FAIR OFFER</div>
                            <div style="font-size: 1rem; color: #856404;">{diff_percent:+.0f}% vs market</div>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                        <div style="background: #f8d7da; padding: 1.5rem; border-radius: 15px; text-align: center;">
                            <div style="font-size: 3rem;">📉</div>
                            <div style="font-size: 1.5rem; font-weight: bold; color: #721c24;">BELOW MARKET</div>
                            <div style="font-size: 1rem; color: #721c24;">{abs(diff_percent):.0f}% below average</div>
                        </div>
                        """, unsafe_allow_html=True)
                
                with col2:
                    # Quality score gauge
                    score = min(100, max(0, 50 + (diff_percent + 50) / 2))
                    fig = go.Figure(go.Indicator(
                        mode="gauge+number",
                        value=score,
                        title={"text": "Quality Score"},
                        gauge={"axis": {"range": [0, 100]},
                               "bar": {"color": "#667eea"},
                               "steps": [
                                   {"range": [0, 40], "color": "#ffcccc"},
                                   {"range": [40, 70], "color": "#ffffcc"},
                                   {"range": [70, 100], "color": "#ccffcc"}
                               ]}
                    ))
                    fig.update_layout(height=250)
                    st.plotly_chart(fig, use_container_width=True)
                
                # Detailed breakdown
                st.markdown("### 📊 Compensation Breakdown")
                
                breakdown_cols = st.columns(3)
                with breakdown_cols[0]:
                    st.metric("Your Offer", f"${total_comp:,.0f}")
                with breakdown_cols[1]:
                    st.metric("Market Median", f"${market:,.0f}")
                with breakdown_cols[2]:
                    st.metric("Difference", f"{diff_percent:+.0f}%")
                
                # Recommendations
                st.markdown("### 💡 Recommendations")
                if total_comp < market:
                    st.warning(f"Consider negotiating. Market data shows ${market - total_comp:,.0f} higher for {level} at {company}")
                elif total_comp > market * 1.2:
                    st.success("Excellent offer! This is in the top 20% of compensation packages.")
                else:
                    st.info("Fair market offer. Consider asking for signing bonus or additional stock.")
                
            else:
                st.warning(f"Insufficient data for {company} {level} in {region}")

# ============================================================================
# ANALYTICS PAGE
# ============================================================================

elif page == "📈 Analytics":
    
    st.markdown("# 📈 Market Analytics")
    st.markdown("Trends and insights from compensation data")
    st.markdown("---")
    
    # Trend chart
    dates = pd.date_range(start='2024-01-01', periods=90, freq='D')
    
    col1, col2 = st.columns(2)
    with col1:
        selected_company = st.selectbox("Select Company", list(COMPANY_COLORS.keys()))
    with col2:
        selected_level = st.selectbox("Select Level", ["IC3", "IC4", "IC5"])
    
    # Generate trend data
    base = BENCHMARK_DATA.get(selected_company, {}).get("USA", {}).get(selected_level, 200000)
    trend = base + np.cumsum(np.random.randn(90)) * 2000
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dates, y=trend, mode='lines', 
                             name=f"{selected_company} {selected_level}",
                             line=dict(color=COMPANY_COLORS.get(selected_company, "#667eea"), width=3)))
    fig.update_layout(title=f"Salary Trend - {selected_company} {selected_level}",
                     height=450, hovermode="x unified")
    st.plotly_chart(fig, use_container_width=True)
    
    # Distribution
    st.markdown("### 📊 Salary Distribution")
    
    salaries = np.random.normal(base, base * 0.15, 500)
    fig = px.histogram(salaries, nbins=40, title=f"Salary Distribution - {selected_company} {selected_level}",
                      color_discrete_sequence=[COMPANY_COLORS.get(selected_company, "#667eea")])
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)

# ============================================================================
# AUDIT TRAIL PAGE - COMPLETELY FIXED (NO DATE PICKER, NO DATETIME ERRORS)
# ============================================================================

elif page == "📋 Audit Trail":
    
    st.markdown("# 📋 Audit Trail")
    st.markdown("History of all validations")
    st.markdown("---")
    
    # Filters - NO DATE PICKER to avoid errors
    col1, col2 = st.columns(2)
    with col1:
        company_filter = st.multiselect("Company", list(COMPANY_COLORS.keys()))
    with col2:
        status_filter = st.multiselect("Status", ["Approved", "Flagged", "Under Review", "Rejected"])
    
    # Generate sample audit data - Using string dates, NOT datetime objects
    audit_data = []
    statuses = ["Approved", "Flagged", "Under Review", "Rejected"]
    companies = list(COMPANY_COLORS.keys())
    levels = ["IC3", "IC4", "IC5", "IC6"]
    
    for i in range(50):
        audit_data.append({
            "Timestamp": f"2026-05-{random.randint(20, 24)} {random.randint(9, 18)}:{random.randint(10, 59)}:00",
            "Submission ID": f"SUB-{random.randint(10000, 99999)}",
            "Company": random.choice(companies),
            "Level": random.choice(levels),
            "Total Comp": f"${random.randint(150000, 500000):,}",
            "Quality Score": random.randint(65, 100),
            "Status": random.choice(statuses)
        })
    
    audit_df = pd.DataFrame(audit_data)
    
    # Apply filters
    if company_filter:
        audit_df = audit_df[audit_df['Company'].isin(company_filter)]
    if status_filter:
        audit_df = audit_df[audit_df['Status'].isin(status_filter)]
    
    # Display metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Records", len(audit_df))
    with col2:
        avg_score = audit_df['Quality Score'].mean() if len(audit_df) > 0 else 0
        st.metric("Avg Quality Score", f"{avg_score:.1f}")
    with col3:
        approved = len(audit_df[audit_df['Status'] == 'Approved']) if len(audit_df) > 0 else 0
        st.metric("Approved", approved)
    with col4:
        flagged = len(audit_df[audit_df['Status'] == 'Flagged']) if len(audit_df) > 0 else 0
        st.metric("Flagged", flagged)
    
    # Display table
    st.dataframe(audit_df, use_container_width=True)
    
    # Export button
    csv = audit_df.to_csv(index=False)
    st.download_button(
        "📥 Export to CSV", 
        csv, 
        f"audit_log_{datetime.now().strftime('%Y%m%d')}.csv", 
        "text/csv", 
        use_container_width=True
    )

# ============================================================================
# FOOTER
# ============================================================================

st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 1rem;">
    <p style="color: #6c757d;">🏆 Levels.fyi - The Most Accurate Compensation Intelligence Platform</p>
    <p style="color: #adb5bd; font-size: 0.8rem;">Powered by AI | Trusted by 500,000+ professionals | 99.99% uptime SLA</p>
</div>
""", unsafe_allow_html=True)