"""
Digital Burnout Analytics Platform
----------------------------------
Central configuration file.
"""

import os

# ==========================================================
# BASE DIRECTORY
# ==========================================================
# Anchor all file paths to this file's location, not the process's
# current working directory. Streamlit Cloud does not guarantee the
# working directory matches the folder app.py lives in, which is why
# plain relative paths like "models/....pkl" fail with FileNotFoundError
# even though the files exist in the repo.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ==========================================================
# APP SETTINGS
# ==========================================================

APP_NAME = "Digital Burnout Analytics Platform"

PAGE_TITLE = "Digital Burnout Analytics"

PAGE_ICON = "🧠"

LAYOUT = "wide"

# ==========================================================
# LOGIN
# ==========================================================

APP_USERNAME = os.getenv("APP_USERNAME", "admin")

APP_PASSWORD = os.getenv("APP_PASSWORD", "admin123")

# ==========================================================
# MODEL PATHS
# ==========================================================

MODEL_FOLDER = os.path.join(BASE_DIR, "models")

LOGISTIC_MODEL = os.path.join(
    MODEL_FOLDER,
    "logistic_burnout_model.pkl"
)

LINEAR_MODEL = os.path.join(
    MODEL_FOLDER,
    "linear_productivity_model.pkl"
)

# ==========================================================
# DATABASE
# ==========================================================

SNOWFLAKE = {

    "account": "KGHPDWC-NG01063",

    "user": "AAKASHKUMAR4090760",

    "password": "dbCRbxZTMtv67LC",

    "warehouse": "BURNOUT_WH",

    "database": "DIGITAL_BURNOUT_DB",

    "schema": "ANALYTICS",

    "table": "DIGITAL_BURNOUT_PRODUCTIVITY_CLEAN"

}

# ==========================================================
# COLORS
# ==========================================================

PRIMARY = "#2563EB"

SECONDARY = "#7C3AED"

SUCCESS = "#10B981"

WARNING = "#F59E0B"

DANGER = "#EF4444"

BACKGROUND = "#F4F7FB"

CARD = "#FFFFFF"

TEXT = "#0F172A"

# ==========================================================
# KPI SETTINGS
# ==========================================================

HIGH_BURNOUT_THRESHOLD = 70

LOW_PRODUCTIVITY_THRESHOLD = 50

LOW_SLEEP_THRESHOLD = 6
