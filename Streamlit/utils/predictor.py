import pickle
import pandas as pd
import streamlit as st

from config import LOGISTIC_MODEL, LINEAR_MODEL

# =====================================================
# LOAD MODELS
# =====================================================

@st.cache_resource
def load_models():
    with open(LOGISTIC_MODEL, "rb") as f:
        burnout_model = pickle.load(f)

    with open(LINEAR_MODEL, "rb") as f:
        productivity_model = pickle.load(f)

    return burnout_model, productivity_model


# =====================================================
# MODEL FEATURES
# (Matches the Databricks training notebook)
# =====================================================

FEATURE_COLUMNS = [

    "AGE",
    "DAILY_SCREEN_TIME",
    "SOCIAL_MEDIA_HOURS",
    "DOOMSCROLLING_DURATION",
    "APP_SWITCH_FREQUENCY",
    "NOTIFICATION_COUNT",
    "SMARTPHONE_UNLOCKS",
    "LATE_NIGHT_DEVICE_USAGE",
    "FOCUS_SESSIONS",
    "DEEP_WORK_HOURS",
    "DISTRACTION_FREQUENCY",
    "TASK_COMPLETION_RATE",
    "CONCENTRATION_SCORE",
    "SLEEP_HOURS",
    "SLEEP_QUALITY",
    "CAFFEINE_INTAKE",
    "PHYSICAL_ACTIVITY",
    "STRESS_LEVEL",
    "WORKSPACE_QUALITY",
    "MEETING_HOURS",
    "INTERNET_STABILITY",
    "REMOTE_WORK_DAYS",
    "MOTIVATION_LEVEL",
    "MENTAL_FATIGUE",
    "EMOTIONAL_EXHAUSTION",
    "WORK_SATISFACTION",

    "OCCUPATION",
    "WORK_MODE",
    "DEVICE_USAGE_TYPE"
]


# =====================================================
# PREPARE INPUT
# =====================================================

def prepare_input(user_input: dict):

    row = {}

    for col in FEATURE_COLUMNS:
        row[col] = user_input[col]

    return pd.DataFrame([row])


# =====================================================
# PREDICT
# =====================================================

def predict(user_input):

    burnout_model, productivity_model = load_models()

    X = prepare_input(user_input)

    burnout_prediction = burnout_model.predict(X)[0]

    burnout_probability = burnout_model.predict_proba(X)[0][1]

    productivity_prediction = productivity_model.predict(X)[0]

    return (
        burnout_prediction,
        burnout_probability,
        productivity_prediction,
    )


# =====================================================
# RISK LABEL
# =====================================================

def risk_label(probability):

    if probability < 0.30:
        return "Low"

    elif probability < 0.60:
        return "Moderate"

    return "High"


# =====================================================
# RECOMMENDATIONS
# =====================================================

def recommendations(data):

    tips = []

    if data["SLEEP_HOURS"] < 7:
        tips.append("😴 Increase daily sleep to at least 7–8 hours.")

    if data["DAILY_SCREEN_TIME"] > 8:
        tips.append("📱 Reduce total daily screen time.")

    if data["SOCIAL_MEDIA_HOURS"] > 3:
        tips.append("📵 Limit social media usage.")

    if data["DEEP_WORK_HOURS"] < 3:
        tips.append("🎯 Increase uninterrupted deep work sessions.")

    if data["STRESS_LEVEL"] > 7:
        tips.append("🧘 Practice stress-management techniques.")

    if data["MENTAL_FATIGUE"] > 7:
        tips.append("💤 Schedule breaks to reduce mental fatigue.")

    if data["EMOTIONAL_EXHAUSTION"] > 7:
        tips.append("❤️ Prioritize recovery and work-life balance.")

    if data["WORK_SATISFACTION"] < 5:
        tips.append("💼 Review workload and workplace satisfaction.")

    if not tips:
        tips.append("✅ Your lifestyle indicators look healthy. Keep maintaining these habits.")

    return tips