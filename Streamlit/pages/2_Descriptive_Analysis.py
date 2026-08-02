import streamlit as st

from components.sidebar import render_sidebar
from utils.database import load_data
from utils.charts_descriptive import (
    plot_d2,
    plot_d3,
    plot_d4,
    plot_d5,
    plot_d6,
    plot_d7,
)

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="Descriptive Analysis",
    page_icon="📈",
    layout="wide"
)

render_sidebar()

st.title("📈 Descriptive Analysis")
st.caption("Digital habits, sleep, mental state, and productivity distributions.")

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------
df = load_data()

if df.empty:
    st.warning("No data returned. Check your Snowflake connection in config.py.")
    st.stop()

# --------------------------------------------------
# CHARTS
# --------------------------------------------------
col1, col2 = st.columns(2)

with col1:
    st.pyplot(plot_d2(df))

with col2:
    st.pyplot(plot_d4(df))

st.divider()

st.pyplot(plot_d3(df))

st.divider()

col3, col4 = st.columns(2)

with col3:
    st.pyplot(plot_d5(df))

with col4:
    st.pyplot(plot_d6(df))

st.divider()

st.pyplot(plot_d7(df))
