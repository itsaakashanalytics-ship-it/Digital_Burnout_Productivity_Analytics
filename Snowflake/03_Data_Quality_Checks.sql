-- Data quality checks for DIGITAL_BURNOUT_PRODUCTIVITY table
-- Co-authored with CoCo
-- ============================================================================
-- SECTION 1: SCHEMA & BASIC INVENTORY
-- ==========================================================================
 
-- 1.1 Table Structure Audit
SELECT 
    COLUMN_NAME,
    DATA_TYPE,
    IS_NULLABLE,
    CHARACTER_MAXIMUM_LENGTH
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'DIGITAL_BURNOUT_PRODUCTIVITY'
ORDER BY ORDINAL_POSITION;
 
-- 1.2 Total Record Count
SELECT 
    COUNT(*) AS total_records,
FROM DIGITAL_BURNOUT_PRODUCTIVITY;
 
-- ============================================================================
-- SECTION 2: NULL & MISSING DATA AUDIT
-- ============================================================================
 
-- 2.1 Null Counts by Column (presentation mentions ~2% nulls in 4 columns)
SELECT 
    'occupation' AS column_name, 
    COUNT(*) - COUNT(occupation) AS null_count,
    ROUND(100.0 * (COUNT(*) - COUNT(occupation)) / COUNT(*), 2) AS pct_null
FROM DIGITAL_BURNOUT_PRODUCTIVITY
UNION ALL
SELECT 'work_mode', COUNT(*) - COUNT(work_mode), 
    ROUND(100.0 * (COUNT(*) - COUNT(work_mode)) / COUNT(*), 2)
FROM DIGITAL_BURNOUT_PRODUCTIVITY
UNION ALL
SELECT 'daily_screen_time', COUNT(*) - COUNT(daily_screen_time),
    ROUND(100.0 * (COUNT(*) - COUNT(daily_screen_time)) / COUNT(*), 2)
FROM DIGITAL_BURNOUT_PRODUCTIVITY
UNION ALL
SELECT 'sleep_hours', COUNT(*) - COUNT(sleep_hours),
    ROUND(100.0 * (COUNT(*) - COUNT(sleep_hours)) / COUNT(*), 2)
FROM DIGITAL_BURNOUT_PRODUCTIVITY
UNION ALL
SELECT 'social_media_hours', COUNT(*) - COUNT(social_media_hours),
    ROUND(100.0 * (COUNT(*) - COUNT(social_media_hours)) / COUNT(*), 2)
FROM DIGITAL_BURNOUT_PRODUCTIVITY
UNION ALL
SELECT 'deep_work_hours', COUNT(*) - COUNT(deep_work_hours),
    ROUND(100.0 * (COUNT(*) - COUNT(deep_work_hours)) / COUNT(*), 2)
FROM DIGITAL_BURNOUT_PRODUCTIVITY
UNION ALL
SELECT 'motivation_level', COUNT(*) - COUNT(motivation_level),
    ROUND(100.0 * (COUNT(*) - COUNT(motivation_level)) / COUNT(*), 2)
FROM DIGITAL_BURNOUT_PRODUCTIVITY
UNION ALL
SELECT 'burnout_risk', COUNT(*) - COUNT(burnout_risk),
    ROUND(100.0 * (COUNT(*) - COUNT(burnout_risk)) / COUNT(*), 2)
FROM DIGITAL_BURNOUT_PRODUCTIVITY
UNION ALL
SELECT 'productivity_score', COUNT(*) - COUNT(productivity_score),
    ROUND(100.0 * (COUNT(*) - COUNT(productivity_score)) / COUNT(*), 2)
FROM DIGITAL_BURNOUT_PRODUCTIVITY
UNION ALL
SELECT 'mental_state', COUNT(*) - COUNT(mental_state),
    ROUND(100.0 * (COUNT(*) - COUNT(mental_state)) / COUNT(*), 2)
FROM DIGITAL_BURNOUT_PRODUCTIVITY
ORDER BY pct_null DESC;

 -- Duplicate user_id check — expect 0 rows returned
SELECT user_id, COUNT(*) AS occurrences
FROM DIGITAL_BURNOUT_PRODUCTIVITY
GROUP BY user_id
HAVING COUNT(*) > 1;
 
-- Range/impossible-value check (e.g., screen time can't exceed 24 hrs/day)
SELECT
    MIN(age) AS min_age, MAX(age) AS max_age,                                       -- expect 18–59
    MIN(burnout_risk) AS min_burnout_risk, MAX(burnout_risk) AS max_burnout_risk,           -- expect 0–100
    MIN(productivity_score) AS min_productivity, MAX(productivity_score) AS max_productivity, -- expect 0–100
    MIN(daily_screen_time) AS min_screen_time, MAX(daily_screen_time) AS max_screen_time      -- expect 0–24
FROM DIGITAL_BURNOUT_PRODUCTIVITY;
 
-- Category/domain check — confirms categorical values match the data dictionary
SELECT DISTINCT occupation FROM DIGITAL_BURNOUT_PRODUCTIVITY ORDER BY 1;             -- expect 7 values
SELECT DISTINCT work_mode FROM DIGITAL_BURNOUT_PRODUCTIVITY ORDER BY 1;              -- expect 3 values
SELECT DISTINCT mental_state FROM DIGITAL_BURNOUT_PRODUCTIVITY ORDER BY 1;           -- expect 4 values
 
 
-- ---- 2.2  Build the cleaned table: median-impute the 4 null-prone columns ---
-- Median (not mean) is used because these are behavioural/count-like variables
-- that can be skewed by outliers. We also keep a "_was_null" flag per column so
-- imputed rows stay identifiable for the Databricks/ML phase later.
 
CREATE OR REPLACE TABLE DIGITAL_BURNOUT_PRODUCTIVITY_CLEAN AS
WITH medians AS (
    SELECT
        MEDIAN(social_media_hours) AS med_social_media_hours,
        MEDIAN(deep_work_hours)    AS med_deep_work_hours,
        MEDIAN(sleep_hours)        AS med_sleep_hours,
        MEDIAN(motivation_level)   AS med_motivation_level
    FROM DIGITAL_BURNOUT_PRODUCTIVITY
)
SELECT
    t.* EXCLUDE (social_media_hours, deep_work_hours, sleep_hours, motivation_level),
    COALESCE(t.social_media_hours, m.med_social_media_hours) AS social_media_hours,
    COALESCE(t.deep_work_hours, m.med_deep_work_hours)       AS deep_work_hours,
    COALESCE(t.sleep_hours, m.med_sleep_hours)               AS sleep_hours,
    COALESCE(t.motivation_level, m.med_motivation_level)     AS motivation_level,
    CASE WHEN t.social_media_hours IS NULL THEN TRUE ELSE FALSE END AS social_media_hours_was_null,
    CASE WHEN t.deep_work_hours IS NULL THEN TRUE ELSE FALSE END    AS deep_work_hours_was_null,
    CASE WHEN t.sleep_hours IS NULL THEN TRUE ELSE FALSE END        AS sleep_hours_was_null,
    CASE WHEN t.motivation_level IS NULL THEN TRUE ELSE FALSE END   AS motivation_level_was_null
FROM DIGITAL_BURNOUT_PRODUCTIVITY t
CROSS JOIN medians m;
 
-- Verify: no nulls remain in the 4 target columns
SELECT COUNT(*) AS remaining_nulls
FROM DIGITAL_BURNOUT_PRODUCTIVITY_CLEAN
WHERE social_media_hours IS NULL
   OR deep_work_hours IS NULL
   OR sleep_hours IS NULL
   OR motivation_level IS NULL;
-- expect 0
 
 
-- ---- 2.3  Standardize categorical text fields (defensive cleaning) ---------
-- Even if the source data is already consistent, trimming whitespace and
-- normalizing case protects every GROUP BY downstream from silent duplicates
-- like "Remote" vs "remote " being counted as different categories.
 
UPDATE DIGITAL_BURNOUT_PRODUCTIVITY_CLEAN
SET occupation             = INITCAP(TRIM(occupation)),
    work_mode               = INITCAP(TRIM(work_mode)),
    device_usage_type        = INITCAP(TRIM(device_usage_type)),
    mental_state               = INITCAP(TRIM(mental_state)),
    productivity_category        = INITCAP(TRIM(productivity_category));
 
 
-- ---- 2.4  Feature engineering: derived columns used throughout the EDA ----
 
ALTER TABLE DIGITAL_BURNOUT_PRODUCTIVITY_CLEAN ADD COLUMN IF NOT EXISTS screen_time_band VARCHAR(10);
ALTER TABLE DIGITAL_BURNOUT_PRODUCTIVITY_CLEAN ADD COLUMN IF NOT EXISTS is_high_burnout_risk BOOLEAN;
ALTER TABLE DIGITAL_BURNOUT_PRODUCTIVITY_CLEAN ADD COLUMN IF NOT EXISTS is_sleep_deficient BOOLEAN;
 
UPDATE DIGITAL_BURNOUT_PRODUCTIVITY_CLEAN
SET screen_time_band = CASE
        WHEN daily_screen_time < 6  THEN 'Low'
        WHEN daily_screen_time <= 10 THEN 'Medium'
        ELSE 'High'
    END,
    is_high_burnout_risk = (burnout_risk > 70),
    is_sleep_deficient   = (sleep_hours < 6);
 
-- Confirm the transformation table is ready for analysis
SELECT COUNT(*) AS total_rows, COUNT(DISTINCT screen_time_band) AS screen_time_bands
FROM DIGITAL_BURNOUT_PRODUCTIVITY_CLEAN;

-- ============================================================================
-- SECTION 3: CATEGORICAL CONSISTENCY CHECKS
-- ============================================================================
 
-- 3.1 Occupation Distribution (expecting 7 unique occupations)
SELECT 
    occupation,
    COUNT(*) AS record_count,
    ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM DIGITAL_BURNOUT_PRODUCTIVITY), 2) AS pct_share
FROM DIGITAL_BURNOUT_PRODUCTIVITY
WHERE occupation IS NOT NULL
GROUP BY occupation
ORDER BY record_count DESC;
 
-- 3.2 Work Mode Distribution (expecting 3 modes: Remote, Hybrid, Office)
SELECT 
    work_mode,
    COUNT(*) AS record_count,
    ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM DIGITAL_BURNOUT_PRODUCTIVITY), 2) AS pct_share
FROM DIGITAL_BURNOUT_PRODUCTIVITY
WHERE work_mode IS NOT NULL
GROUP BY work_mode
ORDER BY record_count DESC;
 
-- 3.3 Mental State Distribution (expecting 4 states)
SELECT 
    mental_state,
    COUNT(*) AS record_count,
    ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM DIGITAL_BURNOUT_PRODUCTIVITY), 2) AS pct_share
FROM DIGITAL_BURNOUT_PRODUCTIVITY
WHERE mental_state IS NOT NULL
GROUP BY mental_state
ORDER BY record_count DESC;
 
-- Expected: Focused, Balanced, Distracted, Burnout
 
-- 3.4 Productivity Category Distribution
SELECT 
    productivity_category,
    COUNT(*) AS record_count,
    ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM DIGITAL_BURNOUT_PRODUCTIVITY), 2) AS pct_share
FROM DIGITAL_BURNOUT_PRODUCTIVITY
WHERE productivity_category IS NOT NULL
GROUP BY productivity_category
ORDER BY record_count DESC;
 
-- ============================================================================
-- SECTION 4: NUMERIC RANGE & DISTRIBUTION CHECKS
-- ============================================================================
 
-- 4.1 Burnout Risk Score Range (0-100 scale)
SELECT 
    'burnout_risk' AS metric,
    MIN(burnout_risk) AS min_val,
    MAX(burnout_risk) AS max_val,
    ROUND(AVG(burnout_risk), 2) AS avg_val,
    ROUND(STDDEV(burnout_risk), 2) AS stdev_val,
    COUNT(*) - COUNT(burnout_risk) AS null_count
FROM DIGITAL_BURNOUT_PRODUCTIVITY;
 
-- 4.2 Productivity Score Range (0-100 scale)
SELECT 
    'productivity_score' AS metric,
    MIN(productivity_score) AS min_val,
    MAX(productivity_score) AS max_val,
    ROUND(AVG(productivity_score), 2) AS avg_val,
    ROUND(STDDEV(productivity_score), 2) AS stdev_val,
    COUNT(*) - COUNT(productivity_score) AS null_count
FROM DIGITAL_BURNOUT_PRODUCTIVITY;
 
-- 4.3 Sleep Hours (expecting mostly 0-12 range, presentation: 35% under 6 hrs)
SELECT 
    'sleep_hours' AS metric,
    MIN(sleep_hours) AS min_val,
    MAX(sleep_hours) AS max_val,
    ROUND(AVG(sleep_hours), 2) AS avg_val,
    ROUND(STDDEV(sleep_hours), 2) AS stdev_val,
    ROUND(100.0 * SUM(CASE WHEN sleep_hours < 6 THEN 1 ELSE 0 END) 
        / COUNT(*), 2) AS pct_under_6hrs,
    COUNT(*) - COUNT(sleep_hours) AS null_count
FROM DIGITAL_BURNOUT_PRODUCTIVITY;
 
-- 4.4 Daily Screen Time (hours)
SELECT 
    'daily_screen_time' AS metric,
    MIN(daily_screen_time) AS min_val,
    MAX(daily_screen_time) AS max_val,
    ROUND(AVG(daily_screen_time), 2) AS avg_val,
    ROUND(STDDEV(daily_screen_time), 2) AS stdev_val,
    COUNT(*) - COUNT(daily_screen_time) AS null_count
FROM DIGITAL_BURNOUT_PRODUCTIVITY;
 
-- 4.5 Notification Count Distribution
SELECT 
    'notification_count' AS metric,
    MIN(notification_count) AS min_val,
    MAX(notification_count) AS max_val,
    ROUND(AVG(notification_count), 2) AS avg_val,
    ROUND(STDDEV(notification_count), 2) AS stdev_val,
    COUNT(*) - COUNT(notification_count) AS null_count
FROM DIGITAL_BURNOUT_PRODUCTIVITY;
 
-- ============================================================================
-- SECTION 5: BUSINESS RULE VALIDATION
-- ============================================================================
 
-- 5.1 High Burnout Risk Rate (presentation: 16.8%)
SELECT 
    ROUND(100.0 * SUM(CASE WHEN burnout_risk > 70 THEN 1 ELSE 0 END) 
        / COUNT(*), 2) AS high_burnout_risk_pct
FROM DIGITAL_BURNOUT_PRODUCTIVITY;
 
-- 5.2 Burnout Mental State Rate (presentation: ~20%, "1 in 5")
SELECT 
    ROUND(100.0 * SUM(CASE WHEN mental_state = 'Burnout' THEN 1 ELSE 0 END) 
        / COUNT(*), 2) AS burnout_mental_state_pct
FROM DIGITAL_BURNOUT_PRODUCTIVITY;
 
-- 5.3 Sleep Deficit Validation (presentation: 35% under 6 hours)
SELECT 
    ROUND(100.0 * SUM(CASE WHEN sleep_hours < 6 THEN 1 ELSE 0 END) 
        / COUNT(*), 2) AS sleep_deficit_pct
FROM DIGITAL_BURNOUT_PRODUCTIVITY
WHERE sleep_hours IS NOT NULL;
 
-- 5.4 Late-Night Device Usage (flag analysis)
SELECT 
    late_night_device_usage,
    COUNT(*) AS record_count,
    ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM DIGITAL_BURNOUT_PRODUCTIVITY), 2) AS pct_share
FROM DIGITAL_BURNOUT_PRODUCTIVITY
WHERE late_night_device_usage IS NOT NULL
GROUP BY late_night_device_usage;
 
-- ============================================================================
-- SECTION 6: CORRELATION & RELATIONSHIP CHECKS
-- ============================================================================
 
-- 6.1 Burnout Risk vs. Productivity Score Correlation (presentation: r = -0.38)
SELECT 
    ROUND(
        (SUM((burnout_risk - (SELECT AVG(burnout_risk) FROM DIGITAL_BURNOUT_PRODUCTIVITY WHERE burnout_risk IS NOT NULL))
            * (productivity_score - (SELECT AVG(productivity_score) FROM DIGITAL_BURNOUT_PRODUCTIVITY WHERE productivity_score IS NOT NULL)))
        / SQRT(
            SUM(SQUARE(burnout_risk - (SELECT AVG(burnout_risk) FROM DIGITAL_BURNOUT_PRODUCTIVITY WHERE burnout_risk IS NOT NULL)))
            * SUM(SQUARE(productivity_score - (SELECT AVG(productivity_score) FROM DIGITAL_BURNOUT_PRODUCTIVITY WHERE productivity_score IS NOT NULL)))
        )), 4) AS correlation
FROM DIGITAL_BURNOUT_PRODUCTIVITY
WHERE burnout_risk IS NOT NULL AND productivity_score IS NOT NULL;
 
-- 6.2 Screen Time vs. Burnout Risk Correlation
-- Simplified correlation check using aggregation
SELECT 
    COUNT(*) AS records_analyzed,
    ROUND(AVG(daily_screen_time), 2) AS avg_screen_time,
    ROUND(AVG(burnout_risk), 2) AS avg_burnout_risk
FROM DIGITAL_BURNOUT_PRODUCTIVITY
WHERE daily_screen_time IS NOT NULL AND burnout_risk IS NOT NULL;
 
-- 6.3 Sleep Hours vs. Burnout Risk Correlation (presentation: r = -0.13)
SELECT 
    COUNT(*) AS records_analyzed,
    ROUND(AVG(sleep_hours), 2) AS avg_sleep_hours,
    ROUND(AVG(burnout_risk), 2) AS avg_burnout_risk
FROM DIGITAL_BURNOUT_PRODUCTIVITY
WHERE sleep_hours IS NOT NULL AND burnout_risk IS NOT NULL;
 
-- ============================================================================
-- SECTION 7: OUTLIER & ANOMALY DETECTION
-- ============================================================================
 
-- 7.1 Records with Extreme Screen Time (>20 hours per day)
SELECT 
    COUNT(*) AS extreme_screen_time_records,
    ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM DIGITAL_BURNOUT_PRODUCTIVITY), 2) AS pct_of_total
FROM DIGITAL_BURNOUT_PRODUCTIVITY
WHERE daily_screen_time > 20;
 
-- 7.2 Records with Sleep > 12 hours (potential data quality issues)
SELECT 
    COUNT(*) AS excessive_sleep_records,
    ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM DIGITAL_BURNOUT_PRODUCTIVITY), 2) AS pct_of_total
FROM DIGITAL_BURNOUT_PRODUCTIVITY
WHERE sleep_hours > 12;
 
-- 7.3 Records with 0 sleep hours (data quality flag)
SELECT 
    COUNT(*) AS zero_sleep_records,
    ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM DIGITAL_BURNOUT_PRODUCTIVITY), 2) AS pct_of_total
FROM DIGITAL_BURNOUT_PRODUCTIVITY
WHERE sleep_hours = 0;
 
-- ============================================================================
-- SECTION 8: DATA QUALITY SUMMARY REPORT
-- ============================================================================
 
SELECT 
    COUNT(*) AS total_records,
    COUNT(DISTINCT occupation) AS unique_occupations,
    COUNT(DISTINCT work_mode) AS unique_work_modes,
    COUNT(DISTINCT mental_state) AS unique_mental_states,
    ROUND(100.0 * SUM(CASE WHEN burnout_risk IS NULL THEN 1 ELSE 0 END) / COUNT(*), 2) AS pct_burnout_null,
    ROUND(100.0 * SUM(CASE WHEN sleep_hours IS NULL THEN 1 ELSE 0 END) / COUNT(*), 2) AS pct_sleep_null,
    ROUND(100.0 * SUM(CASE WHEN burnout_risk > 70 THEN 1 ELSE 0 END) / COUNT(*), 2) AS high_risk_pct,
    ROUND(100.0 * SUM(CASE WHEN sleep_hours < 6 THEN 1 ELSE 0 END) / COUNT(*), 2) AS sleep_deficit_pct
FROM DIGITAL_BURNOUT_PRODUCTIVITY;
 
-- ============================================================================
-- SECTION 9: DATA CLEANING & IMPUTATION RECOMMENDATIONS
-- ============================================================================
 
-- 9.1 Imputation Strategy for Sleep Hours (forward-fill or occupation median)
SELECT 
    occupation,
    ROUND(AVG(sleep_hours), 2) AS median_sleep_by_occupation
FROM DIGITAL_BURNOUT_PRODUCTIVITY
WHERE sleep_hours IS NOT NULL
GROUP BY occupation
ORDER BY occupation;
 
-- 9.2 Imputation Strategy for Social Media Hours
SELECT 
    occupation,
    work_mode,
    ROUND(AVG(social_media_hours), 2) AS avg_social_media
FROM DIGITAL_BURNOUT_PRODUCTIVITY
WHERE social_media_hours IS NOT NULL
GROUP BY occupation, work_mode
ORDER BY occupation, work_mode;
 
-- 9.3 Records Flagged for Manual Review (multiple data quality issues)
SELECT 
    COUNT(*) AS records_needing_review
FROM DIGITAL_BURNOUT_PRODUCTIVITY
WHERE 
    (sleep_hours IS NULL OR daily_screen_time IS NULL)
    AND (burnout_risk > 80 OR burnout_risk < 20);
 
-- ============================================================================
-- END OF AUDIT SCRIPT
-- ============================================================================

select * from DIGITAL_BURNOUT_PRODUCTIVITY
limit 10;