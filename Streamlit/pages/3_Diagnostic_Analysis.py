import streamlit as st

from components.sidebar import render_sidebar
from utils.database import load_data
from utils.charts_diagnostic import (
    plot_g1,
    plot_g2,
    plot_g3,
    plot_g4,
    plot_g5,
    plot_g6,
)

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="Diagnostic Analysis",
    page_icon="🔍",
    layout="wide"
)

render_sidebar()

st.title("🔍 Diagnostic Analysis")
st.caption("Relationships and correlations driving burnout and productivity.")

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
    st.pyplot(plot_g1(df))

with col2:
    st.pyplot(plot_g2(df))

st.divider()

st.pyplot(plot_g3(df))

st.divider()

st.pyplot(plot_g4(df))

st.divider()

st.pyplot(plot_g5(df))

st.divider()

st.pyplot(plot_g6(df))
