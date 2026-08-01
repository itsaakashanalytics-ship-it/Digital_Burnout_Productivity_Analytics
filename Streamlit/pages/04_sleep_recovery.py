"""
Sleep & Recovery Monitoring Page - Static Matplotlib Charts
Track sleep patterns and wellness indicators
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

st.set_page_config(page_title="Sleep & Recovery", layout="wide")

st.title("😴 Sleep & Recovery Monitoring")
st.markdown("Monitor sleep patterns and their correlation with wellness metrics")

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
            st.metric("Avg Sleep Hours", f"{df_filtered['SLEEP_HOURS'].mean():.2f} hrs")
        with col2:
            sleep_deficit = (df_filtered['SLEEP_HOURS'] < 7).sum() / len(df_filtered) * 100
            st.metric("Sleep Deficit %", f"{sleep_deficit:.1f}%")
        with col3:
            st.metric("Avg Sleep Quality", f"{df_filtered['SLEEP_QUALITY'].mean():.2f}/10")
        with col4:
            chronic_deficit = (df_filtered['SLEEP_HOURS'] < 6).sum() / len(df_filtered) * 100
            st.metric("Chronic Sleep Loss %", f"{chronic_deficit:.1f}%")
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Sleep Hours Distribution (7h Reference)")
            fig, ax = plt.subplots(figsize=(7, 4))
            ax.hist(df_filtered['SLEEP_HOURS'], bins=20, color='#2EC4B6', alpha=0.7, edgecolor='white')
            ax.axvline(7, color='#F4A300', linestyle='--', linewidth=2, label='Recommended (7h)')
            ax.set_xlabel("Sleep Hours per Night")
            ax.set_ylabel("Number of Employees")
            ax.legend()
            ax.grid(alpha=0.3)
            st.pyplot(fig, use_container_width=True)
            plt.close(fig)
        
        with col2:
            st.subheader("Sleep Quality Distribution")
            fig, ax = plt.subplots(figsize=(7, 4))
            ax.hist(df_filtered['SLEEP_QUALITY'], bins=10, color='#457B9D', alpha=0.7, edgecolor='white')
            ax.set_xlabel("Sleep Quality Score (0-10)")
            ax.set_ylabel("Number of Employees")
            ax.grid(alpha=0.3)
            st.pyplot(fig, use_container_width=True)
            plt.close(fig)
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Avg Sleep Hours by Occupation")
            sleep_by_occ = df_filtered.groupby('OCCUPATION')['SLEEP_HOURS'].mean().sort_values(ascending=False)
            fig, ax = plt.subplots(figsize=(8, 5))
            colors = ['#2EC4B6' if x >= 7 else '#E63946' for x in sleep_by_occ.values]
            ax.barh(sleep_by_occ.index, sleep_by_occ.values, color=colors, alpha=0.7, edgecolor='white')
            ax.axvline(7, color='#F4A300', linestyle='--', linewidth=2, label='Recommended')
            ax.set_xlabel("Average Sleep Hours")
            ax.legend()
            ax.grid(alpha=0.3, axis='x')
            st.pyplot(fig, use_container_width=True)
            plt.close(fig)
        
        with col2:
            st.subheader("Sleep vs Burnout Risk")
            fig, ax = plt.subplots(figsize=(7, 4))
            scatter = ax.scatter(df_filtered['SLEEP_HOURS'], df_filtered['BURNOUT_RISK'],
                               c=df_filtered['BURNOUT_RISK'], cmap='RdYlGn_r', alpha=0.6, s=30)
            ax.set_xlabel("Sleep Hours per Night")
            ax.set_ylabel("Burnout Risk Score")
            ax.grid(alpha=0.3)
            cbar = plt.colorbar(scatter, ax=ax)
            cbar.set_label("Burnout Risk")
            st.pyplot(fig, use_container_width=True)
            plt.close(fig)
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Sleep vs Productivity Score")
            fig, ax = plt.subplots(figsize=(7, 4))
            scatter = ax.scatter(df_filtered['SLEEP_HOURS'], df_filtered['PRODUCTIVITY_SCORE'],
                               c=df_filtered['PRODUCTIVITY_SCORE'], cmap='RdYlGn', alpha=0.6, s=30)
            ax.set_xlabel("Sleep Hours per Night")
            ax.set_ylabel("Productivity Score")
            ax.grid(alpha=0.3)
            cbar = plt.colorbar(scatter, ax=ax)
            cbar.set_label("Productivity")
            st.pyplot(fig, use_container_width=True)
            plt.close(fig)
        
        with col2:
            st.subheader("Chronic Sleep Deficit Cases (< 6 hours)")
            deficit_cases = df_filtered[df_filtered['SLEEP_HOURS'] < 6].groupby('OCCUPATION').size()
            if len(deficit_cases) > 0:
                fig, ax = plt.subplots(figsize=(7, 4))
                ax.barh(deficit_cases.index, deficit_cases.values, color='#E63946', alpha=0.7, edgecolor='white')
                ax.set_xlabel("Number of Cases")
                ax.grid(alpha=0.3, axis='x')
                st.pyplot(fig, use_container_width=True)
                plt.close(fig)
            else:
                st.info("No employees with chronic sleep deficit in current filters")

except Exception as e:
    st.error(f"Error loading data: {str(e)}")
