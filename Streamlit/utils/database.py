"""
Database Utility
Handles all Snowflake database operations.
"""

import pandas as pd
import snowflake.connector
import streamlit as st

from config import SNOWFLAKE


# =====================================================
# CREATE CONNECTION
# =====================================================

@st.cache_resource(show_spinner=False)
def get_connection():
    """Creates and caches a Snowflake connection."""

    try:
        conn = snowflake.connector.connect(
            account=SNOWFLAKE["account"],
            user=SNOWFLAKE["user"],
            password=SNOWFLAKE["password"],
            warehouse=SNOWFLAKE["warehouse"],
            database=SNOWFLAKE["database"],
            schema=SNOWFLAKE["schema"],
        )
        return conn

    except Exception as e:
        st.error(f"❌ Unable to connect to Snowflake.\n\n{e}")
        return None


# =====================================================
# RUN QUERY
# =====================================================

@st.cache_data(ttl=600, show_spinner=False)
def run_query(query: str) -> pd.DataFrame:
    """Execute SQL query and return DataFrame."""

    conn = get_connection()

    if conn is None:
        return pd.DataFrame()

    try:
        return pd.read_sql(query, conn)

    except Exception as e:
        st.error(f"SQL Error\n\n{e}")
        return pd.DataFrame()


# =====================================================
# LOAD DATASET (MAIN FUNCTION)
# =====================================================

@st.cache_data(ttl=600)
def load_data():
    """
    Loads the complete dataset from Snowflake.

    This function is used by all Streamlit pages.
    """

    query = f"""
    SELECT *
    FROM {SNOWFLAKE["table"]}
    """

    return run_query(query)


# =====================================================
# ALIAS
# =====================================================

def get_dataset():
    """Alias kept for compatibility."""
    return load_data()


# =====================================================
# KPI DATA
# =====================================================

@st.cache_data(ttl=600)
def get_kpis():

    query = f"""
    SELECT
        COUNT(*) AS total_employees,
        ROUND(AVG(burnout_risk),2) AS avg_burnout,
        ROUND(AVG(productivity_score),2) AS avg_productivity,
        ROUND(
            100 * SUM(
                CASE
                    WHEN burnout_risk > 70 THEN 1
                    ELSE 0
                END
            ) / COUNT(*),
            2
        ) AS high_risk_pct
    FROM {SNOWFLAKE["table"]}
    """

    return run_query(query)


# =====================================================
# CLOSE CONNECTION
# =====================================================

def close_connection():

    conn = get_connection()

    if conn:
        conn.close()