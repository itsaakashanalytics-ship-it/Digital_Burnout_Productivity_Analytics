-- Prerequisites: warehouse, database, schema, table, file format, and stage setup
-- Co-authored with CoCo
-- Compute resource that runs your queries
CREATE WAREHOUSE IF NOT EXISTS BURNOUT_WH
  WAREHOUSE_SIZE = 'XSMALL'
  AUTO_SUSPEND = 60
  AUTO_RESUME = TRUE;

-- Database and schema to hold the project
CREATE DATABASE IF NOT EXISTS DIGITAL_BURNOUT_DB;
CREATE SCHEMA IF NOT EXISTS DIGITAL_BURNOUT_DB.ANALYTICS;

USE WAREHOUSE BURNOUT_WH;
USE DATABASE DIGITAL_BURNOUT_DB;
USE SCHEMA ANALYTICS;

CREATE TABLE IF NOT EXISTS DIGITAL_BURNOUT_PRODUCTIVITY (
    user_id                  INTEGER,
    age                      INTEGER,
    occupation                VARCHAR(50),
    work_mode                 VARCHAR(20),
    device_usage_type         VARCHAR(30),
    daily_screen_time         FLOAT,
    social_media_hours        FLOAT,
    doomscrolling_duration    FLOAT,
    app_switch_frequency      INTEGER,
    notification_count        INTEGER,
    smartphone_unlocks        INTEGER,
    late_night_device_usage   INTEGER,
    focus_sessions            INTEGER,
    deep_work_hours           FLOAT,
    distraction_frequency     INTEGER,
    task_completion_rate      INTEGER,
    concentration_score       INTEGER,
    sleep_hours               FLOAT,
    sleep_quality              INTEGER,
    caffeine_intake            INTEGER,
    physical_activity          FLOAT,
    stress_level                INTEGER,
    workspace_quality           INTEGER,
    meeting_hours                FLOAT,
    internet_stability            INTEGER,
    remote_work_days              INTEGER,
    motivation_level               FLOAT,
    mental_fatigue                  INTEGER,
    emotional_exhaustion              INTEGER,
    work_satisfaction                  INTEGER,
    mental_state                        VARCHAR(20),
    burnout_risk                          INTEGER,
    productivity_score                     INTEGER,
    productivity_category                   VARCHAR(10)
);

CREATE OR REPLACE FILE FORMAT CSV_STANDARD_FORMAT
  TYPE = 'CSV'
  FIELD_DELIMITER = ','
  SKIP_HEADER = 1
  FIELD_OPTIONALLY_ENCLOSED_BY = '"'
  EMPTY_FIELD_AS_NULL = TRUE
  NULL_IF = ('', 'NULL', 'null')
  TRIM_SPACE = TRUE;

CREATE OR REPLACE STAGE BURNOUT_STAGE
  FILE_FORMAT = CSV_STANDARD_FORMAT;