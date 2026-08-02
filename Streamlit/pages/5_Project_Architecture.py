import streamlit as st

from components.sidebar import render_sidebar

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Project Architecture",
    page_icon="🏗️",
    layout="wide"
)

render_sidebar()

st.title("🏗️ Project Architecture")
st.caption("End-to-end architecture of the Digital Burnout Analytics platform.")

# =====================================================
# OVERVIEW
# =====================================================

st.markdown("""
## 📌 Project Overview

This project demonstrates a complete modern analytics pipeline for predicting
employee burnout and productivity.

The solution combines:

- ❄️ Snowflake Cloud Data Warehouse
- 🧠 Databricks for Data Analysis & Machine Learning
- 🐍 Python
- 📊 Streamlit
- 📈 Plotly
- 🤖 Scikit-learn
""")

st.divider()

# =====================================================
# ARCHITECTURE
# =====================================================

st.subheader("System Architecture")

st.code("""
             CSV Dataset
                  │
                  ▼
        Snowflake Data Warehouse
                  │
                  ▼
         SQL Cleaning & Validation
                  │
                  ▼
        Databricks Data Analysis
                  │
                  ▼
      Feature Engineering Pipeline
                  │
                  ▼
 Machine Learning Model Training
(Logistic + Linear Regression)
                  │
                  ▼
     Saved .pkl Model Files
                  │
                  ▼
        Streamlit Web Application
                  │
                  ▼
 Interactive Dashboard & Prediction
""", language="text")

st.divider()

# =====================================================
# PROJECT WORKFLOW
# =====================================================

st.subheader("Project Workflow")

workflow = [
    "1. Import dataset into Snowflake",
    "2. Perform SQL data cleaning and validation",
    "3. Connect Databricks with Snowflake",
    "4. Exploratory Data Analysis (EDA)",
    "5. Descriptive Analytics",
    "6. Diagnostic Analytics",
    "7. Feature Engineering",
    "8. Train Logistic Regression model",
    "9. Train Linear Regression model",
    "10. Save trained models (.pkl)",
    "11. Build Streamlit application",
    "12. Deploy dashboard"
]

for step in workflow:
    st.write("✅", step)

st.divider()

# =====================================================
# TECHNOLOGY STACK
# =====================================================

st.subheader("Technology Stack")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
### Data Engineering
- Snowflake
- SQL
- Databricks
- Python
""")

with col2:
    st.markdown("""
### Data Science & Visualization
- Pandas
- Scikit-learn
- Plotly
- Streamlit
""")

st.divider()

# =====================================================
# MACHINE LEARNING
# =====================================================

st.subheader("Machine Learning Models")

st.markdown("""
### Burnout Prediction
- Algorithm: Logistic Regression
- Target: High Burnout Risk
- Output: Burnout Probability

### Productivity Prediction
- Algorithm: Linear Regression
- Target: Productivity Score
- Output: Predicted Productivity
""")

st.divider()

# =====================================================
# BUSINESS VALUE
# =====================================================

st.subheader("Business Value")

st.success("""
✔ Identify employees at risk of burnout

✔ Improve productivity using predictive analytics

✔ Support HR decision-making

✔ Reduce employee fatigue

✔ Improve work-life balance

✔ Enable proactive interventions
""")