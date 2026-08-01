"""
Digital Habit Explorer Page - Static Matplotlib Charts
Analyze screen time and digital behavior patterns
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

st.set_page_config(page_title="Digital Habit Explorer", layout="wide")

st.title("📱 Digital Habit Explorer")
st.markdown("Understand digital behaviors and their impact on wellness")

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
            st.metric("Avg Daily Screen Time", f"{df_filtered['DAILY_SCREEN_TIME'].mean():.2f} hrs")
        with col2:
            st.metric("Avg App Switches/Day", f"{df_filtered['APP_SWITCH_FREQUENCY'].mean():.1f}")
        with col3:
            st.metric("Avg Doomscrolling", f"{df_filtered['DOOMSCROLLING_DURATION'].mean():.2f} hrs")
        with col4:
            st.metric("Avg Social Media", f"{df_filtered['SOCIAL_MEDIA_HOURS'].mean():.2f} hrs")
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Screen Time Distribution")
            fig, ax = plt.subplots(figsize=(7, 4))
            ax.hist(df_filtered['DAILY_SCREEN_TIME'], bins=25, color='#457B9D', alpha=0.7, edgecolor='white')
            ax.set_xlabel("Daily Screen Time (hours)")
            ax.set_ylabel("Number of Employees")
            ax.grid(alpha=0.3)
            st.pyplot(fig, use_container_width=True)
            plt.close(fig)
        
        with col2:
            st.subheader("App Switch Frequency Distribution")
            fig, ax = plt.subplots(figsize=(7, 4))
            ax.hist(df_filtered['APP_SWITCH_FREQUENCY'], bins=30, color='#F4A300', alpha=0.7, edgecolor='white')
            ax.set_xlabel("App Switches per Day")
            ax.set_ylabel("Number of Employees")
            ax.grid(alpha=0.3)
            st.pyplot(fig, use_container_width=True)
            plt.close(fig)
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Screen Time vs Burnout Risk")
            fig, ax = plt.subplots(figsize=(7, 4))
            scatter = ax.scatter(df_filtered['DAILY_SCREEN_TIME'], df_filtered['BURNOUT_RISK'],
                               c=df_filtered['BURNOUT_RISK'], cmap='Reds', alpha=0.6, s=30)
            ax.set_xlabel("Daily Screen Time (hours)")
            ax.set_ylabel("Burnout Risk Score")
            ax.grid(alpha=0.3)
            cbar = plt.colorbar(scatter, ax=ax)
            cbar.set_label("Burnout Risk")
            st.pyplot(fig, use_container_width=True)
            plt.close(fig)
        
        with col2:
            st.subheader("Digital Habits by Occupation")
            habits = df_filtered.groupby('OCCUPATION').agg({
                'DAILY_SCREEN_TIME': 'mean',
                'APP_SWITCH_FREQUENCY': 'mean',
            }).round(2)
            st.dataframe(habits, use_container_width=True)

except Exception as e:
    st.error(f"Error loading data: {str(e)}")
