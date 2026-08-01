"""
Digital Burnout & Productivity Analytics Dashboard
Main entry point - Home/Welcome page
Uses Streamlit's native multipage app functionality
"""

import streamlit as st
import pandas as pd
from utils.db_connection import test_connection

st.set_page_config(
    page_title="Burnout & Productivity Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    [data-testid="stSidebar"] {
        background-color: #1c1f26;
    }
    .main {
        background-color: #0e1117;
    }
</style>
""", unsafe_allow_html=True)

# Title and description
st.title("📊 Digital Burnout & Productivity Analytics")
st.markdown("Comprehensive workforce wellness and performance monitoring system")

# Sidebar - Global Controls
with st.sidebar:
    st.markdown("## 🎛️ Dashboard Controls")
    
    if st.button("🔄 Refresh Data", use_container_width=True):
        st.cache_data.clear()
        st.success("✅ Cache cleared! Data refreshed.")
    
    st.markdown("---")
    
    # Global Filters Section
    st.markdown("## 🔍 Global Filters")
    
    mental_state = st.selectbox(
        "Mental State",
        ["All", "Burnout", "Distracted", "Balanced", "Focused"],
        key="mental_state_filter"
    )
    
    occupation = st.selectbox(
        "Occupation",
        ["All", "Analyst", "Designer", "Manager", "Software Engineer", "Data Scientist", "Product Manager", "Consultant"],
        key="occupation_filter"
    )
    
    work_mode = st.selectbox(
        "Work Mode",
        ["All", "Remote", "Hybrid", "Office"],
        key="work_mode_filter"
    )
    
    age_range = st.slider(
        "Age Range",
        18, 65, (18, 59),
        key="age_filter"
    )
    
    st.markdown("---")
    
    # Data Source Status
    st.markdown("## 📊 Data Source")
    try:
        if test_connection():
            st.success("✅ CSV Data Loaded")
            st.caption("Source: analysis.csv (local)")
        else:
            st.error("❌ CSV File Not Found")
            st.caption("Place 'analysis.csv' in root directory")
    except Exception as e:
        st.warning("⚠️ Connection check unavailable")
        st.caption(str(e))

# Main content
st.info("""
📱 **Navigation**: Use the sidebar to navigate to different dashboard pages
- 📊 **Executive Overview** - Organization-wide KPIs
- 👔 **Occupation & Work-Mode** - Job type analysis
- 📱 **Digital Habits** - Screen time & behavior
- 😴 **Sleep & Recovery** - Wellness metrics
- ⚠️ **Burnout Monitor** - High-risk tracking
- ⚡ **Productivity Drivers** - ML insights
""")

# Quick stats
st.markdown("---")
st.markdown("## 📈 Quick Overview")

try:
    from utils.db_connection import load_main_data
    df = load_main_data()
    
    if len(df) > 0:
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.metric("Total Records", f"{len(df):,}")
        
        with col2:
            st.metric("Avg Burnout Risk", f"{df['BURNOUT_RISK'].mean():.1f}")
        
        with col3:
            st.metric("Avg Productivity", f"{df['PRODUCTIVITY_SCORE'].mean():.1f}")
        
        with col4:
            high_risk_pct = (df['BURNOUT_RISK'] > 70).sum() / len(df) * 100
            st.metric("High Risk %", f"{high_risk_pct:.1f}%")
        
        with col5:
            st.metric("Avg Sleep Hours", f"{df['SLEEP_HOURS'].mean():.2f}")
    else:
        st.warning("No data loaded. Check CSV file.")
        
except Exception as e:
    st.warning(f"Could not load data: {str(e)}")

st.markdown("---")

# Instructions
st.markdown("""
## How to Use This Dashboard

1. **Select Filters** in the sidebar to narrow down data by:
   - Mental State (Burnout, Distracted, Balanced, Focused)
   - Occupation (job type)
   - Work Mode (Remote, Hybrid, Office)
   - Age Range (18-65)

2. **Navigate Pages** using the sidebar page selector to explore:
   - Executive Overview: KPIs and high-level metrics
   - Occupation & Work-Mode: Departmental analysis
   - Digital Habits: Screen time and digital behavior
   - Sleep & Recovery: Wellness and rest patterns
   - Burnout Monitor: High-risk employee identification
   - Productivity Drivers: ML-powered insights

3. **Charts Load Instantly** - All visualizations use static Matplotlib for speed

4. **Refresh Data** - Click the refresh button to reload from CSV file

## Key Metrics Explained

- **Burnout Risk Score**: ML-predicted burnout likelihood (0-100)
- **Productivity Score**: Work output and quality metric (0-100)
- **Sleep Quality**: Self-reported sleep quality (0-10)
- **Screen Time**: Daily digital device usage (hours)
- **Mental State**: Current mental health categorization
""")

st.markdown("---")

# Footer
st.markdown("""
<div style="text-align: center; color: gray; font-size: 0.8rem; margin-top: 40px;">
    <p>Digital Burnout & Productivity Analytics Dashboard v1.0</p>
    <p>Built with Streamlit | Data from analysis.csv</p>
</div>
""", unsafe_allow_html=True)
