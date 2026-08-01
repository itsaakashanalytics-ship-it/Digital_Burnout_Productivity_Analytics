"""
Occupation & Work-Mode Analysis Page - Static Matplotlib Charts
Deep dive into occupational and work arrangement patterns
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

st.set_page_config(page_title="Occupation & Work-Mode", layout="wide")

st.title("👔 Occupation & Work-Mode Analysis")
st.markdown("Analyze burnout and productivity patterns by job type and work arrangement")

try:
    df = load_main_data()
    mental_state = st.session_state.get("mental_state_filter", "All")
    occupation = st.session_state.get("occupation_filter", "All")
    work_mode = st.session_state.get("work_mode_filter", "All")
    age_range = st.session_state.get("age_filter", (18, 59))
    
    df_filtered = apply_filters(df, mental_state, occupation, work_mode, age_range)
    
    if len(df_filtered) == 0:
        st.warning("No data matches selected filters.")
    else:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Occupations Tracked", df_filtered['OCCUPATION'].nunique())
        with col2:
            st.metric("Unique Employees", df_filtered['USER_ID'].nunique())
        with col3:
            high_risk = len(df_filtered.groupby('OCCUPATION').agg({'BURNOUT_RISK': 'mean'})[
                df_filtered.groupby('OCCUPATION').agg({'BURNOUT_RISK': 'mean'})['BURNOUT_RISK'] > 60])
            st.metric("High-Risk Occupations", high_risk)
        with col4:
            remote_pct = (df_filtered['WORK_MODE'] == 'Remote').sum() / len(df_filtered) * 100
            st.metric("Remote Work %", f"{remote_pct:.1f}%")
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Avg Burnout Risk by Occupation")
            burnout_by_occ = df_filtered.groupby('OCCUPATION')['BURNOUT_RISK'].mean().sort_values(ascending=False)
            fig, ax = plt.subplots(figsize=(8, 5))
            ax.barh(burnout_by_occ.index, burnout_by_occ.values, color='#E63946', alpha=0.7, edgecolor='white')
            ax.set_xlabel("Burnout Risk Score")
            ax.grid(alpha=0.3, axis='x')
            st.pyplot(fig, use_container_width=True)
            plt.close(fig)
        
        with col2:
            st.subheader("Avg Productivity by Occupation")
            prod_by_occ = df_filtered.groupby('OCCUPATION')['PRODUCTIVITY_SCORE'].mean().sort_values(ascending=False)
            fig, ax = plt.subplots(figsize=(8, 5))
            ax.barh(prod_by_occ.index, prod_by_occ.values, color='#F4A300', alpha=0.7, edgecolor='white')
            ax.set_xlabel("Productivity Score")
            ax.grid(alpha=0.3, axis='x')
            st.pyplot(fig, use_container_width=True)
            plt.close(fig)
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Employee-Days by Work Mode")
            work_mode_counts = df_filtered['WORK_MODE'].value_counts()
            colors_wm = {'Remote': '#457B9D', 'Hybrid': '#2EC4B6', 'Office': '#F4A300'}
            colors = [colors_wm.get(mode, '#999') for mode in work_mode_counts.index]
            fig, ax = plt.subplots(figsize=(7, 4))
            wedges, texts, autotexts = ax.pie(work_mode_counts.values, labels=work_mode_counts.index,
                                              autopct='%1.1f%%', colors=colors, textprops={'color': 'white'})
            for autotext in autotexts:
                autotext.set_color('white')
                autotext.set_fontweight('bold')
            st.pyplot(fig, use_container_width=True)
            plt.close(fig)
        
        with col2:
            st.subheader("Avg Productivity by Work Mode")
            prod_by_mode = df_filtered.groupby('WORK_MODE')['PRODUCTIVITY_SCORE'].mean().sort_values(ascending=False)
            fig, ax = plt.subplots(figsize=(7, 4))
            colors = [colors_wm.get(mode, '#999') for mode in prod_by_mode.index]
            ax.bar(prod_by_mode.index, prod_by_mode.values, color=colors, alpha=0.7, edgecolor='white')
            ax.set_ylabel("Avg Productivity Score")
            ax.grid(alpha=0.3, axis='y')
            st.pyplot(fig, use_container_width=True)
            plt.close(fig)

except Exception as e:
    st.error(f"Error loading data: {str(e)}")
