"""
Executive Overview Page - Using Static Matplotlib Charts
High-level KPIs and organization-wide metrics
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from utils.db_connection import load_main_data, apply_filters

# Set matplotlib style
sns.set_style("darkgrid")
plt.rcParams['figure.facecolor'] = '#0e1117'
plt.rcParams['axes.facecolor'] = '#1c1f26'
plt.rcParams['text.color'] = 'white'
plt.rcParams['axes.labelcolor'] = 'white'
plt.rcParams['xtick.color'] = 'white'
plt.rcParams['ytick.color'] = 'white'

st.set_page_config(page_title="Executive Overview", layout="wide")

st.title("📊 Executive Overview")
st.markdown("Organization-wide burnout and productivity metrics")

# Load data
try:
    df = load_main_data()
    
    # Apply global filters
    mental_state = st.session_state.get("mental_state_filter", "All")
    occupation = st.session_state.get("occupation_filter", "All")
    work_mode = st.session_state.get("work_mode_filter", "All")
    age_range = st.session_state.get("age_filter", (18, 59))
    
    df_filtered = apply_filters(df, mental_state, occupation, work_mode, age_range)
    
    if len(df_filtered) == 0:
        st.warning("No data matches the selected filters. Please adjust your selection.")
    else:
        # Key Metrics Row 1
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            employee_days = len(df_filtered)
            st.metric("Employee-Days", f"{employee_days:,}", help="Total employee observation days")
        
        with col2:
            avg_burnout = df_filtered['BURNOUT_RISK'].mean()
            st.metric("Avg Burnout Risk", f"{avg_burnout:.2f}", help="Average burnout risk score (0-100)")
        
        with col3:
            avg_productivity = df_filtered['PRODUCTIVITY_SCORE'].mean()
            st.metric("Avg Productivity Score", f"{avg_productivity:.2f}", help="Average productivity score (0-100)")
        
        with col4:
            high_burnout_rate = (df_filtered['BURNOUT_RISK'] > 70).sum() / len(df_filtered) * 100
            st.metric("High Burnout Risk Rate", f"{high_burnout_rate:.2f}%", help="Percentage with burnout risk > 70")
        
        with col5:
            avg_sleep = df_filtered['SLEEP_HOURS'].mean()
            st.metric("Avg Sleep Hours", f"{avg_sleep:.2f}", help="Average sleep hours per night")
        
        st.markdown("---")
        
        # Row 2: Charts
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Burnout Risk Distribution")
            fig, ax = plt.subplots(figsize=(7, 4))
            ax.hist(df_filtered['BURNOUT_RISK'], bins=30, color='#028090', alpha=0.7, edgecolor='white')
            ax.set_xlabel("Burnout Risk Score", color='white')
            ax.set_ylabel("Number of Employees", color='white')
            ax.grid(alpha=0.3)
            st.pyplot(fig, use_container_width=True)
            plt.close(fig)
        
        with col2:
            st.subheader("Mental State Distribution")
            mental_dist = df_filtered['MENTAL_STATE'].value_counts()
            colors = ['#E63946', '#457B9D', '#F4A300', '#2EC4B6']
            
            fig, ax = plt.subplots(figsize=(7, 4))
            wedges, texts, autotexts = ax.pie(mental_dist.values, labels=mental_dist.index, 
                                               autopct='%1.1f%%', colors=colors[:len(mental_dist)],
                                               textprops={'color': 'white'})
            for autotext in autotexts:
                autotext.set_color('white')
                autotext.set_fontweight('bold')
            ax.set_facecolor('#1c1f26')
            st.pyplot(fig, use_container_width=True)
            plt.close(fig)
        
        st.markdown("---")
        
        # Row 3: Productivity and Burnout
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Productivity Score Distribution")
            fig, ax = plt.subplots(figsize=(7, 4))
            ax.hist(df_filtered['PRODUCTIVITY_SCORE'], bins=30, color='#F4A300', alpha=0.7, edgecolor='white')
            ax.set_xlabel("Productivity Score", color='white')
            ax.set_ylabel("Number of Employees", color='white')
            ax.grid(alpha=0.3)
            st.pyplot(fig, use_container_width=True)
            plt.close(fig)
        
        with col2:
            st.subheader("Burnout Risk vs Productivity Score")
            fig, ax = plt.subplots(figsize=(7, 4))
            scatter = ax.scatter(df_filtered['BURNOUT_RISK'], df_filtered['PRODUCTIVITY_SCORE'],
                               c=df_filtered['BURNOUT_RISK'], cmap='Reds', alpha=0.6, s=30)
            ax.set_xlabel("Burnout Risk Score", color='white')
            ax.set_ylabel("Productivity Score", color='white')
            ax.grid(alpha=0.3)
            cbar = plt.colorbar(scatter, ax=ax)
            cbar.set_label("Burnout Risk", color='white')
            st.pyplot(fig, use_container_width=True)
            plt.close(fig)
        
        st.markdown("---")
        
        # Row 4: Key Insights
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.subheader("📈 Top Risk Groups")
            top_risk = df_filtered.nlargest(5, 'BURNOUT_RISK')[['USER_ID', 'OCCUPATION', 'BURNOUT_RISK']]
            st.dataframe(top_risk.rename(columns={'USER_ID': 'Employee', 'BURNOUT_RISK': 'Risk Score'}),
                        hide_index=True, use_container_width=True)
        
        with col2:
            st.subheader("⭐ Top Performers")
            top_prod = df_filtered.nlargest(5, 'PRODUCTIVITY_SCORE')[['USER_ID', 'OCCUPATION', 'PRODUCTIVITY_SCORE']]
            st.dataframe(top_prod.rename(columns={'USER_ID': 'Employee', 'PRODUCTIVITY_SCORE': 'Prod Score'}),
                        hide_index=True, use_container_width=True)
        
        with col3:
            st.subheader("📊 Summary Stats")
            summary = pd.DataFrame({
                'Metric': ['Total Employees', 'Avg Age', 'Avg Sleep Hours', 'Avg Screen Time'],
                'Value': [
                    f"{len(df_filtered):,}",
                    f"{df_filtered['AGE'].mean():.1f}",
                    f"{df_filtered['SLEEP_HOURS'].mean():.2f}",
                    f"{df_filtered['DAILY_SCREEN_TIME'].mean():.2f} hrs"
                ]
            })
            st.dataframe(summary, hide_index=True, use_container_width=True)
        
        st.markdown("---")
        
        # Data Quality
        st.subheader("Data Quality")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            null_pct = (df_filtered.isnull().sum().sum() / (len(df_filtered) * len(df_filtered.columns))) * 100
            st.metric("Data Completeness", f"{100 - null_pct:.1f}%")
        
        with col2:
            unique_occupations = df_filtered['OCCUPATION'].nunique()
            st.metric("Unique Occupations", unique_occupations)
        
        with col3:
            unique_work_modes = df_filtered['WORK_MODE'].nunique()
            st.metric("Work Modes Tracked", unique_work_modes)

except Exception as e:
    st.error(f"Error loading data: {str(e)}")
    st.info("Make sure 'analysis.csv' is in the same directory as app.py")
