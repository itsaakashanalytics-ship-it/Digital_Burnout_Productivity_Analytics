"""
Digital Burnout Analytics Platform
----------------------------------
Central configuration file.
"""

import os

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

MODEL_FOLDER = "models"

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