"""
Productivity Drivers Page - Static Matplotlib Charts
ML insights and personalized recommendations
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from utils.db_connection import load_main_data, apply_filters
from utils.model_loader import ModelManager

sns.set_style("darkgrid")
plt.rcParams['figure.facecolor'] = '#0e1117'
plt.rcParams['axes.facecolor'] = '#1c1f26'
plt.rcParams['text.color'] = 'white'
plt.rcParams['axes.labelcolor'] = 'white'
plt.rcParams['xtick.color'] = 'white'
plt.rcParams['ytick.color'] = 'white'

st.set_page_config(page_title="Productivity Drivers", layout="wide")

st.title("⚡ Productivity Drivers")
st.markdown("ML-powered insights into what drives productivity and wellness")

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
            avg_prod = df_filtered['PRODUCTIVITY_SCORE'].mean()
            st.metric("Avg Productivity Score", f"{avg_prod:.1f}")
        with col2:
            high_performers = (df_filtered['PRODUCTIVITY_SCORE'] >= 80).sum()
            st.metric("High Performers (≥80)", high_performers)
        with col3:
            underperformers = (df_filtered['PRODUCTIVITY_SCORE'] < 50).sum()
            st.metric("Underperformers (<50)", underperformers)
        with col4:
            deep_work_avg = df_filtered['DEEP_WORK_HOURS'].mean()
            st.metric("Avg Deep Work Hours", f"{deep_work_avg:.1f}")
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Productivity Score Distribution")
            fig, ax = plt.subplots(figsize=(7, 4))
            ax.hist(df_filtered['PRODUCTIVITY_SCORE'], bins=30, color='#2EC4B6', alpha=0.7, edgecolor='white')
            ax.axvline(80, color='#2EC4B6', linestyle='--', linewidth=2, label='High Performer Threshold')
            ax.set_xlabel("Productivity Score (0-100)")
            ax.set_ylabel("Number of Employees")
            ax.legend()
            ax.grid(alpha=0.3)
            st.pyplot(fig, use_container_width=True)
            plt.close(fig)
        
        with col2:
            st.subheader("Productivity by Mental State")
            prod_mental = df_filtered.groupby('MENTAL_STATE')['PRODUCTIVITY_SCORE'].mean().sort_values(ascending=False)
            fig, ax = plt.subplots(figsize=(7, 4))
            colors = ['#2EC4B6' if x >= 70 else '#E63946' for x in prod_mental.values]
            ax.bar(prod_mental.index, prod_mental.values, color=colors, alpha=0.7, edgecolor='white')
            ax.set_ylabel("Avg Productivity Score")
            ax.set_xticklabels(prod_mental.index, rotation=45, ha='right')
            ax.grid(alpha=0.3, axis='y')
            st.pyplot(fig, use_container_width=True)
            plt.close(fig)
        
        st.markdown("---")
        
        # Feature Importance
        st.subheader("📊 Productivity Feature Importance (ML Model)")
        
        model_manager = ModelManager()
        feature_importance = model_manager.FEATURE_IMPORTANCE
        
        # Create dataframe for feature importance
        features_df = pd.DataFrame([
            {'Feature': k, 'Importance': v} for k, v in list(feature_importance.items())[:10]
        ]).sort_values('Importance', ascending=True)
        
        fig, ax = plt.subplots(figsize=(8, 5))
        colors = ['#2EC4B6' if x > 0 else '#E63946' for x in features_df['Importance']]
        ax.barh(features_df['Feature'], features_df['Importance'], color=colors, alpha=0.7, edgecolor='white')
        ax.set_xlabel("Importance Score")
        ax.grid(alpha=0.3, axis='x')
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)
        
        st.markdown("---")
        
        # Productivity Tiers
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Productivity Tier Distribution")
            elite = (df_filtered['PRODUCTIVITY_SCORE'] >= 90).sum()
            high = ((df_filtered['PRODUCTIVITY_SCORE'] >= 80) & (df_filtered['PRODUCTIVITY_SCORE'] < 90)).sum()
            medium = ((df_filtered['PRODUCTIVITY_SCORE'] >= 50) & (df_filtered['PRODUCTIVITY_SCORE'] < 80)).sum()
            low = (df_filtered['PRODUCTIVITY_SCORE'] < 50).sum()
            
            tiers = [elite, high, medium, low]
            labels = ['Elite (≥90)', 'High (80-90)', 'Medium (50-80)', 'Low (<50)']
            colors = ['#2EC4B6', '#F4A300', '#457B9D', '#E63946']
            
            fig, ax = plt.subplots(figsize=(7, 4))
            wedges, texts, autotexts = ax.pie(tiers, labels=labels, autopct='%1.1f%%',
                                              colors=colors, textprops={'color': 'white'})
            for autotext in autotexts:
                autotext.set_color('white')
                autotext.set_fontweight('bold')
            st.pyplot(fig, use_container_width=True)
            plt.close(fig)
        
        with col2:
            st.subheader("Correlation: Deep Work Hours vs Productivity")
            fig, ax = plt.subplots(figsize=(7, 4))
            scatter = ax.scatter(df_filtered['DEEP_WORK_HOURS'], df_filtered['PRODUCTIVITY_SCORE'],
                               c=df_filtered['PRODUCTIVITY_SCORE'], cmap='RdYlGn', alpha=0.6, s=30)
            ax.set_xlabel("Deep Work Hours per Day")
            ax.set_ylabel("Productivity Score")
            ax.grid(alpha=0.3)
            cbar = plt.colorbar(scatter, ax=ax)
            cbar.set_label("Productivity")
            st.pyplot(fig, use_container_width=True)
            plt.close(fig)
        
        st.markdown("---")
        
        # Recommendations
        st.subheader("💡 Personalized Recommendations")
        
        tab1, tab2, tab3 = st.tabs(["Organization-Wide", "By Occupation", "By Individual"])
        
        with tab1:
            st.write("**Organization-Wide Insights:**")
            avg_prod_score = df_filtered['PRODUCTIVITY_SCORE'].mean()
            avg_deep_work = df_filtered['DEEP_WORK_HOURS'].mean()
            avg_burnout = df_filtered['BURNOUT_RISK'].mean()
            
            if avg_deep_work < 3:
                st.warning("⚠️ Average deep work hours is low. Consider protecting focus time.")
            if avg_burnout > 60:
                st.error("⚠️ Burnout levels are concerning. Implement wellness initiatives.")
            if avg_prod_score > 75:
                st.success("✅ Strong productivity levels. Maintain current practices.")
        
        with tab2:
            st.write("**By Occupation Recommendations:**")
            occ_prod = df_filtered.groupby('OCCUPATION').agg({
                'PRODUCTIVITY_SCORE': 'mean',
                'BURNOUT_RISK': 'mean',
                'DEEP_WORK_HOURS': 'mean'
            }).round(2)
            st.dataframe(occ_prod, use_container_width=True)
        
        with tab3:
            st.write("**Individual Analysis:**")
            emp_id = st.number_input("Enter Employee ID:", min_value=1)
            emp_data = df_filtered[df_filtered['USER_ID'] == emp_id]
            
            if len(emp_data) > 0:
                emp = emp_data.iloc[0]
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Productivity Score", f"{emp['PRODUCTIVITY_SCORE']:.1f}")
                with col2:
                    st.metric("Burnout Risk", f"{emp['BURNOUT_RISK']:.1f}")
                with col3:
                    st.metric("Sleep Hours", f"{emp['SLEEP_HOURS']:.1f}")
                
                st.write(f"**Recommendations for Employee {emp_id}:**")
                if emp['BURNOUT_RISK'] > 70:
                    st.warning("High burnout risk - Consider intervention")
                if emp['SLEEP_HOURS'] < 7:
                    st.info("Sleep below recommended - Encourage rest")
                if emp['DEEP_WORK_HOURS'] < 2:
                    st.warning("Limited deep work time - Schedule focused work blocks")
            else:
                st.info(f"No data found for Employee ID {emp_id}")

except Exception as e:
    st.error(f"Error loading data: {str(e)}")
