import streamlit as st
from components.sidebar import render_sidebar

st.set_page_config(
    page_title="About",
    page_icon="ℹ️",
    layout="wide"
)

render_sidebar()

st.title("ℹ️ About the Project")

st.markdown("""
## Digital Burnout Analytics Platform

This project is an end-to-end Data Analytics and Machine Learning solution
designed to analyze employee digital habits, identify burnout risks, and
predict productivity using historical behavioral data.

The application integrates cloud data warehousing, SQL, data analysis,
machine learning, and interactive dashboards into a single platform.
""")

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.subheader("🎯 Objectives")
    st.markdown("""
- Analyze employee digital behavior
- Identify burnout indicators
- Understand productivity drivers
- Build predictive ML models
- Deliver interactive business dashboards
""")

with col2:
    st.subheader("🛠 Technology Stack")
    st.markdown("""
- Snowflake
- Databricks
- SQL
- Python
- Pandas
- Plotly
- Streamlit
- Scikit-learn
""")

st.divider()

st.subheader("📊 Dataset Highlights")

st.markdown("""
The project analyzes employee digital activity, work habits, lifestyle factors,
and workplace behavior to generate descriptive, diagnostic, and predictive insights.
""")

st.divider()

st.subheader("🚀 Future Enhancements")

st.markdown("""
- Real-time data ingestion
- Power BI integration
- Automated alerts
- Explainable AI (SHAP)
- Employee recommendation engine
- Cloud deployment
""")

st.divider()

st.success("Version 2.0 | Digital Burnout Analytics Platform")