import streamlit as st
from pathlib import Path

from components.sidebar import render_sidebar

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------
st.set_page_config(
    page_title="Digital Burnout Analytics Platform",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------------------------------
# LOAD CSS
# --------------------------------------------------
# Anchor to this file's location, not the working directory - Streamlit
# Cloud does not guarantee cwd matches the folder app.py lives in.
BASE_DIR = Path(__file__).resolve().parent
css_file = BASE_DIR / "css" / "style.css"

if css_file.exists():
    with open(css_file) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------
render_sidebar()

# --------------------------------------------------
# HOME PAGE
# --------------------------------------------------

st.title("🧠 Digital Burnout Analytics Platform")

st.markdown(
"""
### Project Overview

This platform analyzes employee digital behavior and workplace habits to identify
burnout risk, productivity trends, and key behavioural drivers.

The solution combines **Snowflake**, **Databricks**, **Machine Learning**, and
**Streamlit** into a complete end-to-end analytics platform.
"""
)

st.write("")

# --------------------------------------------------
# FEATURE CARDS
# --------------------------------------------------

col1, col2 = st.columns(2)

with col1:

    with st.container(border=True):

        st.subheader("📊 Executive Dashboard")

        st.write(
            """
- Organizational KPIs
- Mental State Overview
- Burnout Summary
- Productivity Overview
- Executive Insights
"""
        )

    with st.container(border=True):

        st.subheader("📈 Descriptive Analysis")

        st.write(
            """
- Digital Habits
- Sleep Analysis
- Mental State Distribution
- Productivity Categories
- Stress & Fatigue Indicators
"""
        )


with col2:

    with st.container(border=True):

        st.subheader("🔍 Diagnostic Analysis")

        st.write(
            """
- Burnout vs Productivity
- Screen Time vs Burnout
- Sleep vs Burnout
- Occupation Comparison
- Habit Correlations
"""
        )

    with st.container(border=True):

        st.subheader("🤖 Predictive Analytics")

        st.write(
            """
- Burnout Prediction
- Productivity Prediction
- Model Evaluation
- ROC Curve
- Feature Importance
"""
        )

st.write("")

# --------------------------------------------------
# PROJECT WORKFLOW
# --------------------------------------------------

st.subheader("Project Workflow")

with st.container(border=True):

    st.markdown(
        """
### Data Analytics Pipeline
CSV Dataset
│
▼
Snowflake
(Database & SQL)
│
▼
Databricks
(Data Cleaning & Analysis)
│
▼
Machine Learning
(Logistic & Linear Regression)
│
▼
Streamlit Dashboard
(Visualization & Prediction)
"""
    )

st.write("")

# --------------------------------------------------
# PROJECT INFORMATION
# --------------------------------------------------

left, right = st.columns(2)

with left:

    with st.container(border=True):

        st.subheader("📂 Dataset")

        st.write("""
- Employee Digital Behaviour
- Lifestyle Indicators
- Workplace Environment
- Burnout Risk
- Productivity Score
""")

with right:

    with st.container(border=True):

        st.subheader("🛠 Technology Stack")

        st.write("""
- Python
- SQL
- Snowflake
- Databricks
- Pandas
- Scikit-Learn
- Matplotlib
- Streamlit
""")

st.write("")

st.success(
    "Application connected successfully. Use the navigation menu to explore the analytics modules."
)
