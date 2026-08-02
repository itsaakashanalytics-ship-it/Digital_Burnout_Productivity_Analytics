import streamlit as st

from components.sidebar import render_sidebar
from utils.database import load_data, get_kpis
from utils.charts_descriptive import plot_d4, plot_d7
from utils.charts_diagnostic import plot_g1, plot_g2

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="Executive Dashboard",
    page_icon="📊",
    layout="wide"
)

render_sidebar()

st.title("📊 Executive Dashboard")
st.caption("Organizational KPIs, burnout summary, and productivity overview.")

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------
df = load_data()

if df.empty:
    st.warning("No data returned. Check your Snowflake connection in config.py.")
    st.stop()

# --------------------------------------------------
# KPI ROW
# --------------------------------------------------
kpis = get_kpis()

if not kpis.empty:
    row = kpis.iloc[0]

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Employees", f"{int(row['TOTAL_EMPLOYEES']):,}")
    col2.metric("Avg Burnout Risk", f"{row['AVG_BURNOUT']:.2f}")
    col3.metric("Avg Productivity", f"{row['AVG_PRODUCTIVITY']:.2f}")
    col4.metric("High Risk %", f"{row['HIGH_RISK_PCT']:.2f}%")

st.divider()

# --------------------------------------------------
# CHARTS
# --------------------------------------------------
st.subheader("Mental State & Risk-Productivity Relationship")

col1, col2 = st.columns(2)

with col1:
    st.pyplot(plot_d4(df))

with col2:
    st.pyplot(plot_g1(df))

st.divider()

st.subheader("Stress & Fatigue vs Screen Time")

col3, col4 = st.columns(2)

with col3:
    st.pyplot(plot_d7(df))

with col4:
    st.pyplot(plot_g2(df))
