"""
Reusable Sidebar Component
"""

import streamlit as st


def render_sidebar():
    """Render application sidebar."""

    with st.sidebar:

        st.markdown(
            """
            <h2 style="text-align:center;">🧠</h2>
            <h2 style="text-align:center;margin-top:-10px;">
            Digital Burnout
            </h2>
            <p style="text-align:center;color:gray;">
            Analytics Platform
            </p>
            """,
            unsafe_allow_html=True,
        )

        st.divider()

        st.subheader("Navigation")

        pages = [
            ("🏠 Home", "app.py"),
            ("📊 Executive Dashboard", "pages/1_Executive_Dashboard.py"),
            ("📈 Descriptive Analysis", "pages/2_Descriptive_Analysis.py"),
            ("🔍 Diagnostic Analysis", "pages/3_Diagnostic_Analysis.py"),
            ("🤖 Predictive Analysis", "pages/4_Predictive_Analysis.py"),
            ("🏗️ Project Architecture", "pages/5_Project_Architecture.py"),
            ("ℹ️ About", "pages/6_About.py"),
        ]

        for label, page in pages:
            st.page_link(page, label=label)

        st.divider()

        st.subheader("Technology Stack")

        col1, col2 = st.columns(2)

        with col1:
            st.caption("❄️ Snowflake")
            st.caption("⚡ Databricks")
            st.caption("🐍 Python")
            st.caption("🧮 SQL")

        with col2:
            st.caption("📊 Streamlit")
            st.caption("🤖 Scikit-Learn")
            st.caption("📈 Matplotlib")
            st.caption("📁 Pandas")

        st.divider()

        st.success("System Status")

        st.markdown(
            """
🟢 Snowflake Connected

🟢 ML Models Loaded

🟢 Streamlit Running
"""
        )

        st.divider()

        st.caption("Digital Burnout Analytics Platform")
        st.caption("Version 2.0")