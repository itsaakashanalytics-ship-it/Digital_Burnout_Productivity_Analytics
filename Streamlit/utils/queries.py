"""
SQL Queries for Digital Burnout Analytics
-----------------------------------------
Central location for all dashboard SQL.
"""

from config import SNOWFLAKE

TABLE = SNOWFLAKE["table"]


# ==========================================================
# DATASET
# ==========================================================

GET_DATASET = f"""
SELECT *
FROM {TABLE}
"""


# ==========================================================
# KPI
# ==========================================================

GET_KPI = f"""
SELECT

    COUNT(*) AS total_employees,

    ROUND(AVG(burnout_risk),2) AS avg_burnout,

    ROUND(AVG(productivity_score),2) AS avg_productivity,

    ROUND(
        100 *
        SUM(
            CASE
                WHEN burnout_risk > 70
                THEN 1
                ELSE 0
            END
        ) / COUNT(*),
        2
    ) AS high_risk_pct

FROM {TABLE}
"""


# ==========================================================
# OCCUPATION
# ==========================================================

OCCUPATION_ANALYSIS = f"""
SELECT

    occupation,

    COUNT(*) employee_count,

    ROUND(AVG(burnout_risk),2) avg_burnout,

    ROUND(AVG(productivity_score),2) avg_productivity

FROM {TABLE}

GROUP BY occupation

ORDER BY avg_burnout DESC;
"""


# ==========================================================
# WORK MODE
# ==========================================================

WORKMODE_ANALYSIS = f"""
SELECT

    work_mode,

    COUNT(*) employee_count,

    ROUND(AVG(burnout_risk),2) burnout,

    ROUND(AVG(productivity_score),2) productivity

FROM {TABLE}

GROUP BY work_mode;
"""


# ==========================================================
# MENTAL STATE
# ==========================================================

MENTAL_STATE = f"""
SELECT

    mental_state,

    COUNT(*) total

FROM {TABLE}

GROUP BY mental_state;
"""


# ==========================================================
# SCREEN TIME
# ==========================================================

SCREEN_TIME = f"""
SELECT

    screen_time_band,

    COUNT(*) total

FROM {TABLE}

GROUP BY screen_time_band

ORDER BY screen_time_band;
"""


# ==========================================================
# CORRELATION DATA
# ==========================================================

CORRELATION_DATA = f"""
SELECT

    burnout_risk,

    productivity_score,

    sleep_hours,

    daily_screen_time,

    social_media_hours,

    deep_work_hours

FROM {TABLE}
"""