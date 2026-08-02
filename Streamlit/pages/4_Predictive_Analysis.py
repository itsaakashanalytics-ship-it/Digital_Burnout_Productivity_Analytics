import streamlit as st

from components.sidebar import render_sidebar
from utils.database import load_data
from utils.predictor import predict, risk_label, recommendations

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="Predictive Analysis",
    page_icon="🤖",
    layout="wide"
)

render_sidebar()

st.title("🤖 Predictive Analysis")
st.caption("Estimate burnout risk and productivity score from an employee's digital habits and lifestyle profile.")

# --------------------------------------------------
# LOAD DATA (used only to pre-fill sensible defaults / dropdown options)
# --------------------------------------------------
df = load_data()

NUMERIC_FEATURES = [
    "AGE", "DAILY_SCREEN_TIME", "SOCIAL_MEDIA_HOURS", "DOOMSCROLLING_DURATION",
    "APP_SWITCH_FREQUENCY", "NOTIFICATION_COUNT", "SMARTPHONE_UNLOCKS",
    "LATE_NIGHT_DEVICE_USAGE", "FOCUS_SESSIONS", "DEEP_WORK_HOURS",
    "DISTRACTION_FREQUENCY", "TASK_COMPLETION_RATE", "CONCENTRATION_SCORE",
    "SLEEP_HOURS", "SLEEP_QUALITY", "CAFFEINE_INTAKE", "PHYSICAL_ACTIVITY",
    "STRESS_LEVEL", "WORKSPACE_QUALITY", "MEETING_HOURS", "INTERNET_STABILITY",
    "REMOTE_WORK_DAYS", "MOTIVATION_LEVEL", "MENTAL_FATIGUE",
    "EMOTIONAL_EXHAUSTION", "WORK_SATISFACTION",
]

CATEGORICAL_FEATURES = ["OCCUPATION", "WORK_MODE", "DEVICE_USAGE_TYPE"]

# --------------------------------------------------
# INPUT FORM
# --------------------------------------------------
st.subheader("Employee Profile")

user_input = {}

with st.form("prediction_form"):

    col1, col2, col3 = st.columns(3)
    columns = [col1, col2, col3]

    for i, feature in enumerate(NUMERIC_FEATURES):

        col = columns[i % 3]

        default = 5.0
        if not df.empty and feature in df.columns:
            default = float(df[feature].mean())

        user_input[feature] = col.number_input(
            feature.replace("_", " ").title(),
            value=round(default, 2),
        )

    st.markdown("#### Categorical Attributes")

    col4, col5, col6 = st.columns(3)

    for col, feature in zip([col4, col5, col6], CATEGORICAL_FEATURES):

        if not df.empty and feature in df.columns:
            options = sorted(df[feature].dropna().unique().tolist())
        else:
            options = ["Unknown"]

        user_input[feature] = col.selectbox(
            feature.replace("_", " ").title(),
            options,
        )

    submitted = st.form_submit_button("Predict", use_container_width=True)

# --------------------------------------------------
# PREDICTION OUTPUT
# --------------------------------------------------
if submitted:

    try:
        burnout_pred, burnout_proba, productivity_pred = predict(user_input)

        st.divider()
        st.subheader("Results")

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Burnout Prediction",
            "High Risk" if burnout_pred == 1 else "Not High Risk",
        )
        col2.metric("Burnout Probability", f"{burnout_proba * 100:.1f}%")
        col3.metric("Predicted Productivity Score", f"{productivity_pred:.1f}")

        st.markdown(f"**Risk Level:** {risk_label(burnout_proba)}")

        st.markdown("### Recommendations")

        for tip in recommendations(user_input):
            st.write(tip)

    except FileNotFoundError:
        st.error(
            "Trained model files not found. Ensure "
            "`models/logistic_burnout_model.pkl` and "
            "`models/linear_productivity_model.pkl` exist in the project root."
        )

    except Exception as e:
        st.error(f"Prediction failed: {e}")

st.divider()

st.info(
    "Model evaluation visuals (confusion matrix, ROC curve, feature importance) "
    "require saved test-set predictions from training, which aren't available "
    "at runtime in this app. If you save `y_test`/`y_proba`/`y_pred` as artifacts "
    "alongside the .pkl models, `utils/charts_predictive.py` already has the "
    "plotting functions ready to use them here."
)
