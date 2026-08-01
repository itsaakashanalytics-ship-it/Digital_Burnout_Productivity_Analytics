"""
Data connection module - supports both Snowflake and local CSV files
Handles secure credential management and data fetching with caching
"""

import streamlit as st
import pandas as pd
import logging
from pathlib import Path
from functools import wraps
from typing import Optional, Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CSVConnection:
    """Loads data from local CSV files"""
    
    def __init__(self, csv_file: str = "analysis.csv"):
        """Initialize CSV file path"""
        self.csv_file = Path(csv_file)
        self.data = None
        logger.info(f"CSV Connection initialized for: {self.csv_file}")
    
    def load_data(self) -> pd.DataFrame:
        """Load data from CSV file"""
        try:
            if not self.csv_file.exists():
                raise FileNotFoundError(f"CSV file not found: {self.csv_file}")
            
            df = pd.read_csv(self.csv_file)
            logger.info(f"CSV loaded successfully: {len(df)} rows, {len(df.columns)} columns")
            return df
        except Exception as e:
            logger.error(f"CSV loading failed: {str(e)}")
            raise
    
    def close(self):
        """No connection to close for CSV"""
        logger.info("CSV Connection closed")

class SnowflakeConnection:
    """Manages Snowflake database connections and queries (Optional)"""
    
    def __init__(self):
        """Initialize connection parameters from Streamlit secrets"""
        try:
            import snowflake.connector
            self.sf_url = st.secrets.get("snowflake", {}).get("sf_url", "")
            self.sf_user = st.secrets.get("snowflake", {}).get("sf_user", "")
            self.sf_password = st.secrets.get("snowflake", {}).get("sf_password", "")
            self.sf_database = st.secrets.get("snowflake", {}).get("sf_database", "DIGITAL_BURNOUT_DB")
            self.sf_schema = st.secrets.get("snowflake", {}).get("sf_schema", "ANALYTICS")
            self.sf_warehouse = st.secrets.get("snowflake", {}).get("sf_warehouse", "BURNOUT_WH")
            self.connection = None
        except ImportError:
            logger.warning("Snowflake connector not installed, using CSV mode")
            raise
    
    def connect(self) -> Optional:
        """Establish Snowflake connection"""
        try:
            import snowflake.connector
            if self.connection is None:
                self.connection = snowflake.connector.connect(
                    user=self.sf_user,
                    password=self.sf_password,
                    account=self.sf_url.split('.')[0],
                    database=self.sf_database,
                    schema=self.sf_schema,
                    warehouse=self.sf_warehouse,
                    region="us-east-1"
                )
                logger.info("Snowflake connection established")
            return self.connection
        except Exception as e:
            logger.error(f"Snowflake connection failed: {str(e)}")
            raise
    
    def execute_query(self, query: str) -> pd.DataFrame:
        """Execute SQL query and return pandas DataFrame"""
        try:
            conn = self.connect()
            cursor = conn.cursor()
            cursor.execute(query)
            df = cursor.fetch_pandas_all()
            cursor.close()
            logger.info(f"Query executed successfully, returned {len(df)} rows")
            return df
        except Exception as e:
            logger.error(f"Query execution failed: {str(e)}")
            raise
    
    def close(self):
        """Close Snowflake connection"""
        if self.connection:
            self.connection.close()
            logger.info("Snowflake connection closed")

@st.cache_data(ttl=3600)  # Cache for 1 hour
def load_main_data() -> pd.DataFrame:
    """Load main dataset from CSV with caching"""
    try:
        # Try to load from CSV first
        csv_conn = CSVConnection("analysis.csv")
        df = csv_conn.load_data()
        csv_conn.close()
        
        # Data type optimization
        categorical_cols = ['OCCUPATION', 'WORK_MODE', 'MENTAL_STATE', 'DEVICE_USAGE_TYPE', 
                           'PRODUCTIVITY_CATEGORY', 'SCREEN_TIME_BAND']
        for col in categorical_cols:
            if col in df.columns:
                df[col] = df[col].astype('category')
        
        logger.info(f"Loaded {len(df)} rows from CSV")
        return df
    except Exception as e:
        logger.error(f"Failed to load main data: {str(e)}")
        st.error(f"Failed to load data from CSV: {str(e)}")
        st.info("Make sure 'analysis.csv' is in the same directory as app.py")
        return pd.DataFrame()

@st.cache_data(ttl=3600)
def load_occupation_stats() -> pd.DataFrame:
    """Load occupation-level aggregated statistics from CSV"""
    try:
        df = load_main_data()
        
        if len(df) == 0:
            return pd.DataFrame()
        
        stats = df.groupby('OCCUPATION').agg({
            'USER_ID': 'count',
            'BURNOUT_RISK': 'mean',
            'PRODUCTIVITY_SCORE': 'mean',
            'SLEEP_HOURS': 'mean',
            'DAILY_SCREEN_TIME': 'mean'
        }).round(2)
        
        stats.columns = ['EMPLOYEE_COUNT', 'AVG_BURNOUT_RISK', 'AVG_PRODUCTIVITY_SCORE', 
                        'AVG_SLEEP_HOURS', 'AVG_SCREEN_TIME']
        
        # Calculate high burnout rate
        high_burnout = df[df['BURNOUT_RISK'] > 70].groupby('OCCUPATION').size()
        stats['HIGH_BURNOUT_RATE'] = (high_burnout / stats['EMPLOYEE_COUNT']).fillna(0).round(2)
        
        return stats.sort_values('AVG_BURNOUT_RISK', ascending=False)
    except Exception as e:
        logger.error(f"Failed to load occupation stats: {str(e)}")
        return pd.DataFrame()

@st.cache_data(ttl=3600)
def load_mental_state_distribution() -> pd.DataFrame:
    """Load mental state distribution data from CSV"""
    try:
        df = load_main_data()
        
        if len(df) == 0:
            return pd.DataFrame()
        
        distribution = df['MENTAL_STATE'].value_counts()
        percentage = (distribution / len(df) * 100).round(2)
        
        result = pd.DataFrame({
            'MENTAL_STATE': distribution.index,
            'COUNT': distribution.values,
            'PERCENTAGE': percentage.values
        })
        
        return result.sort_values('COUNT', ascending=False)
    except Exception as e:
        logger.error(f"Failed to load mental state distribution: {str(e)}")
        return pd.DataFrame()

@st.cache_data(ttl=3600)
def load_high_risk_employees() -> pd.DataFrame:
    """Load high-risk employees watchlist from CSV"""
    try:
        df = load_main_data()
        
        if len(df) == 0:
            return pd.DataFrame()
        
        high_risk = df[df['BURNOUT_RISK'] > 70].sort_values('BURNOUT_RISK', ascending=False)
        
        columns_to_keep = ['USER_ID', 'OCCUPATION', 'BURNOUT_RISK', 'PRODUCTIVITY_SCORE', 
                          'MENTAL_STATE', 'SLEEP_HOURS', 'DAILY_SCREEN_TIME']
        
        # Keep only columns that exist in the dataframe
        available_cols = [col for col in columns_to_keep if col in high_risk.columns]
        
        return high_risk[available_cols].head(100)
    except Exception as e:
        logger.error(f"Failed to load high-risk employees: {str(e)}")
        return pd.DataFrame()

def apply_filters(df: pd.DataFrame, 
                  mental_state: str = "All",
                  occupation: str = "All",
                  work_mode: str = "All",
                  age_range: tuple = (18, 59)) -> pd.DataFrame:
    """Apply global filters to dataframe"""
    df_filtered = df.copy()
    
    if mental_state != "All":
        df_filtered = df_filtered[df_filtered['MENTAL_STATE'] == mental_state]
    
    if occupation != "All":
        df_filtered = df_filtered[df_filtered['OCCUPATION'] == occupation]
    
    if work_mode != "All":
        df_filtered = df_filtered[df_filtered['WORK_MODE'] == work_mode]
    
    if age_range:
        df_filtered = df_filtered[
            (df_filtered['AGE'] >= age_range[0]) & 
            (df_filtered['AGE'] <= age_range[1])
        ]
    
    return df_filtered

def test_connection() -> bool:
    """Test CSV file availability"""
    try:
        csv_conn = CSVConnection("analysis.csv")
        df = csv_conn.load_data()
        csv_conn.close()
        return len(df) > 0
    except Exception as e:
        logger.error(f"Connection test failed: {str(e)}")
        return False

# Initialize session state
if "data_loaded" not in st.session_state:
    st.session_state.data_loaded = False
if "main_df" not in st.session_state:
    st.session_state.main_df = pd.DataFrame()
