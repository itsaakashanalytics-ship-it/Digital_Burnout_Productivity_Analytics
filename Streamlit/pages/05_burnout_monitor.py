"""
Burnout Risk Monitor Page - Static Matplotlib Charts
High-risk employee identification and monitoring
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from utils.db_connection import load_main_data, apply_filters

sns.set_style("darkgrid")
plt.rcParams['figure.facecolor'] = '#0e1117'
plt.rcParams['axes.facecolor'] = '#1c1f26'
plt.rcParams['text.color'] = 'white'
plt.rcParams['axes.labelcolor'] = 'white'
plt.rcParams['xtick.color'] = 'white'
plt.rcParams['ytick.color'] = 'white'

st.set_page_config(page_title="Burnout Risk Monitor", layout="wide")

st.title("⚠️ Burnout Risk Monitor")
st.markdown("Identify and track high-risk employees for intervention")

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
            total_high_risk = (df_filtered['BURNOUT_RISK'] > 70).sum()
            st.metric("High-Risk Employees", total_high_risk)
        with col2:
            high_risk_pct = (df_filtered['BURNOUT_RISK'] > 70).sum() / len(df_filtered) * 100
            st.metric("High-Risk %", f"{high_risk_pct:.1f}%")
        with col3:
            critical_risk = (df_filtered['BURNOUT_RISK'] > 85).sum()
            st.metric("Critical Risk (>85)", critical_risk)
        with col4:
            avg_risk = df_filtered['BURNOUT_RISK'].mean()
            st.metric("Avg Risk Score", f"{avg_risk:.1f}")
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Burnout Risk Tiers")
            low = (df_filtered['BURNOUT_RISK'] <= 35).sum()
            medium = ((df_filtered['BURNOUT_RISK'] > 35) & (df_filtered['BURNOUT_RISK'] <= 70)).sum()
            high = ((df_filtered['BURNOUT_RISK'] > 70) & (df_filtered['BURNOUT_RISK'] <= 85)).sum()
            critical = (df_filtered['BURNOUT_RISK'] > 85).sum()
            
            tiers = [low, medium, high, critical]
            labels = ['Low (≤35)', 'Medium (35-70)', 'High (70-85)', 'Critical (>85)']
            colors = ['#2EC4B6', '#F4A300', '#E63946', '#8B0000']
            
            fig, ax = plt.subplots(figsize=(7, 4))
            wedges, texts, autotexts = ax.pie(tiers, labels=labels, autopct='%1.1f%%', 
                                              colors=colors, textprops={'color': 'white'})
            for autotext in autotexts:
                autotext.set_color('white')
                autotext.set_fontweight('bold')
            st.pyplot(fig, use_container_width=True)
            plt.close(fig)
        
        with col2:
            st.subheader("Burnout by Mental State")
            burnout_by_mental = df_filtered.groupby('MENTAL_STATE')['BURNOUT_RISK'].mean().sort_values(ascending=False)
            fig, ax = plt.subplots(figsize=(7, 4))
            ax.bar(burnout_by_mental.index, burnout_by_mental.values, 
                   color=['#E63946' if x > 70 else '#F4A300' for x in burnout_by_mental.values],
                   alpha=0.7, edgecolor='white')
            ax.set_ylabel("Avg Burnout Risk Score")
            ax.set_xticklabels(burnout_by_mental.index, rotation=45, ha='right')
            ax.grid(alpha=0.3, axis='y')
            st.pyplot(fig, use_container_width=True)
            plt.close(fig)
        
        st.markdown("---")
        
        # High-Risk Watchlist
        st.subheader("🚨 High-Risk Employees Watchlist (Risk > 70)")
        
        high_risk_employees = df_filtered[df_filtered['BURNOUT_RISK'] > 70].sort_values('BURNOUT_RISK', ascending=False)
        
        if len(high_risk_employees) > 0:
            # Show top 20
            watchlist = high_risk_employees.head(20)[['USER_ID', 'OCCUPATION', 'BURNOUT_RISK', 
                                                        'PRODUCTIVITY_SCORE', 'MENTAL_STATE', 'SLEEP_HOURS']].copy()
            watchlist.columns = ['Employee ID', 'Occupation', 'Burnout Risk', 'Productivity', 'Mental State', 'Sleep Hours']
            
            st.dataframe(watchlist.reset_index(drop=True), use_container_width=True)
            
            # Download option
            csv = watchlist.to_csv(index=False)
            st.download_button(
                label="Download High-Risk List (CSV)",
                data=csv,
                file_name="high_risk_employees.csv",
                mime="text/csv"
            )
        else:
            st.success("✅ No high-risk employees detected in current filters!")
        
        st.markdown("---")
        
        # Mental State Distribution
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Mental State Distribution")
            mental_dist = df_filtered['MENTAL_STATE'].value_counts()
            colors_mental = {'Burnout': '#E63946', 'Distracted': '#457B9D', 
                           'Balanced': '#F4A300', 'Focused': '#2EC4B6'}
            colors = [colors_mental.get(state, '#999') for state in mental_dist.index]
            
            fig, ax = plt.subplots(figsize=(7, 4))
            wedges, texts, autotexts = ax.pie(mental_dist.values, labels=mental_dist.index,
                                              autopct='%1.1f%%', colors=colors, textprops={'color': 'white'})
            for autotext in autotexts:
                autotext.set_color('white')
                autotext.set_fontweight('bold')
            st.pyplot(fig, use_container_width=True)
            plt.close(fig)
        
        with col2:
            st.subheader("Mental State Risk Levels")
            mental_high_risk = df_filtered[df_filtered['BURNOUT_RISK'] > 70].groupby('MENTAL_STATE').size()
            if len(mental_high_risk) > 0:
                fig, ax = plt.subplots(figsize=(7, 4))
                colors = [colors_mental.get(state, '#999') for state in mental_high_risk.index]
                ax.bar(mental_high_risk.index, mental_high_risk.values, color=colors, alpha=0.7, edgecolor='white')
                ax.set_ylabel("Number of High-Risk Cases")
                ax.grid(alpha=0.3, axis='y')
                st.pyplot(fig, use_container_width=True)
                plt.close(fig)

except Exception as e:
    st.error(f"Error loading data: {str(e)}")
