"""
Database Utility
Handles all Snowflake database operations.
"""

import pandas as pd
import snowflake.connector
import streamlit as st

from config import SNOWFLAKE

# =====================================================
# ROW CAP
# =====================================================
# Streamlit Community Cloud's free tier has limited RAM. Pulling the full
# multi-million row table into a DataFrame on every page load exhausts it
# and causes throttling / crashes. Cap the number of rows loaded for
# row-level analysis; KPI/aggregate queries still run against the full
# table on the Snowflake side (cheap, DB-side aggregation).
MAX_ROWS = 150_000


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
    """Execute SQL query and return DataFrame using Snowflake's native
    Arrow-based fetch (faster than pd.read_sql and avoids the
    'DBAPI2 connectable not supported' warning)."""

    conn = get_connection()

    if conn is None:
        return pd.DataFrame()

    cur = None

    try:
        cur = conn.cursor()
        cur.execute(query)
        return cur.fetch_pandas_all()

    except Exception as e:
        st.error(f"SQL Error\n\n{e}")
        return pd.DataFrame()

    finally:
        if cur is not None:
            cur.close()


# =====================================================
# LOAD DATASET (MAIN FUNCTION)
# =====================================================

@st.cache_data(ttl=600)
def load_data(max_rows: int = MAX_ROWS) -> pd.DataFrame:
    """
    Loads a bounded sample of the dataset from Snowflake for row-level
    charts (scatter plots, histograms, etc). Uses Snowflake's SAMPLE
    clause so the row cap is applied on the warehouse side, not after
    pulling everything into memory.

    This function is used by all Streamlit pages that need row-level data.
    For aggregate KPIs, use get_kpis() instead, which runs a full
    DB-side aggregation and returns a single row.
    """

    query = f"""
    SELECT *
    FROM {SNOWFLAKE["table"]}
    SAMPLE ({max_rows} ROWS)
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
    """Full-table aggregate KPIs. Cheap: aggregation happens on the
    Snowflake warehouse, only a single summary row is returned."""

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
