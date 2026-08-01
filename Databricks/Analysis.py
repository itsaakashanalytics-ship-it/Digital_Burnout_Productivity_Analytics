# Databricks notebook source
# MAGIC %pip install seaborn scipy
# MAGIC
# MAGIC import pandas as pd
# MAGIC import numpy as np
# MAGIC import matplotlib.pyplot as plt
# MAGIC import seaborn as sns
# MAGIC from scipy import stats
# MAGIC from scipy.stats import pearsonr, spearmanr
# MAGIC import warnings
# MAGIC  
# MAGIC warnings.filterwarnings('ignore')
# MAGIC  
# MAGIC # Set style for visualizations
# MAGIC sns.set_style("whitegrid")
# MAGIC plt.rcParams['figure.figsize'] = (14, 8)
# MAGIC plt.rcParams['font.size'] = 10

# COMMAND ----------

# Configure Snowflake connection options
sfOptions = {
  "sfUrl": "KGHPDWC-NG01063.snowflakecomputing.com",
  "sfUser": "AAKASHKUMAR4090760",
  "sfPassword": "***",
  "sfDatabase": "DIGITAL_BURNOUT_DB",
  "sfSchema": "ANALYTICS",
  "sfWarehouse": "BURNOUT_WH"
}

# Read data from Snowflake table into Spark DataFrame
spark_df = (spark.read.format("snowflake") \
  .options(**sfOptions) \
  .option("dbtable", "DIGITAL_BURNOUT_PRODUCTIVITY_CLEAN") \
  .load())

# COMMAND ----------

df = spark_df.toPandas()

# COMMAND ----------

# ============================================================================
# SECTION 1 - DATA LOADING & INITIAL EXPLORATION
# ============================================================================

# COMMAND ----------

print(f"Dataset Shape: {df.shape}")
print(f"\nColumn Names & Data Types:")
print(df.dtypes)
print(f"\nFirst 5 Records:")
print(df.head())

# COMMAND ----------

# DBTITLE 1,Cell 6
# ============================================================================
# SECTION 2 — DATA CLEANING & TRANSFORMATION
# ============================================================================
"""
Mirrors the Snowflake SQL cleaning: median-impute the 4 null-prone columns,
keep a "_was_null" flag per column, and engineer the same derived columns.
"""
 
NULL_PRONE_COLS = ["SOCIAL_MEDIA_HOURS", "DEEP_WORK_HOURS", "SLEEP_HOURS", "MOTIVATION_LEVEL"]
 
for c in NULL_PRONE_COLS:
    df[f"{c}_WAS_NULL"] = df[c].isnull().astype(int)
    df[c] = df[c].fillna(df[c].median())
 
df["IS_HIGH_BURNOUT_RISK"] = (df["BURNOUT_RISK"] > 70).astype(int)
df["IS_SLEEP_DEFICIENT"] = (df["SLEEP_HOURS"] < 6).astype(int)
df["SCREEN_TIME_BAND"] = pd.cut(
    df["DAILY_SCREEN_TIME"], bins=[-1, 6, 10, 100], labels=["Low", "Medium", "High"]
)
 
print("Remaining nulls in target columns:", df[NULL_PRONE_COLS].isnull().sum().sum())

# COMMAND ----------

# ============================================================================
# SECTION 3: DESCRIPTIVE ANALYSIS - What is Happening?
# ============================================================================

# COMMAND ----------

d1 = df.groupby(["OCCUPATION", "WORK_MODE"]).size().reset_index(name="EMPLOYEE_DAYS")
d1_pivot = d1.pivot(index="OCCUPATION", columns="WORK_MODE", values="EMPLOYEE_DAYS").fillna(0)
print("\nD1. Employee-day counts:\n", d1_pivot)

# COMMAND ----------

ax = d1_pivot.plot(kind="bar", figsize=(13, 6), color=['#457B9D', '#2EC4B6', '#E63946', '#F4A300'])
plt.title("D1. Employee-Day Counts by Occupation & Work Mode", fontsize=13, fontweight='bold', pad=15)
plt.xlabel("Occupation", fontsize=11, fontweight='bold')
plt.ylabel("Employee-Day Count", fontsize=11, fontweight='bold')
plt.xticks(rotation=45, ha="right")
plt.legend(title="Work Mode", fontsize=9)

# Add value labels on bars
for container in ax.containers:
    labels = [f'{int(v.get_height()):,}' if v.get_height() > 0 else '' for v in container]
    ax.bar_label(container, labels=labels, fontsize=8, fontweight='bold')

plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.show()

# COMMAND ----------

 # ---- D2. Digital-habit distributions ----
d2 = df[["DAILY_SCREEN_TIME", "SOCIAL_MEDIA_HOURS", "DOOMSCROLLING_DURATION"]].agg(["mean", "median", "std"]).round(2)
print("\nD2. Digital habit distributions:\n", d2)

# COMMAND ----------

means = d2.loc["mean"]
labels = ["Screen Time", "Social Media", "Doomscrolling"]

plt.figure(figsize=(6, 4))
bars = plt.bar(labels, means.values, color=["#457B9D", "#2EC4B6", "#E63946"], 
               edgecolor='black', linewidth=0.7)

# Add value labels on bars
for bar, value in zip(bars, means.values):
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height,
            f'{value:.2f} hrs',
            ha='center', va='bottom', fontsize=11, fontweight='bold')

plt.title("D2. Average Digital-Habit Hours", fontsize=13, fontweight='bold', pad=15)
plt.ylabel("Hours / Day", fontsize=11, fontweight='bold')
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig("D2_digital_habits.png", dpi=120, bbox_inches='tight')
plt.show()

# COMMAND ----------

sleep_mean = round(df["SLEEP_HOURS"].mean(), 2)
sleep_median = round(df["SLEEP_HOURS"].median(), 2)
sleep_quality = round(df["SLEEP_QUALITY"].mean(), 2)

print("\nD3. Sleep hours: mean =", sleep_mean, "| median =", sleep_median)
print("D3. Sleep quality: mean =", sleep_quality)

plt.figure(figsize=(13, 10))
n, bins, patches = plt.hist(df["SLEEP_HOURS"], bins=20, color="#457B9D", edgecolor="black", linewidth=0.7)

# Add count labels on histogram bars
for count, patch in zip(n, patches):
    height = patch.get_height()
    if height > 0:
        plt.text(patch.get_x() + patch.get_width()/2., height,
                f'{int(count):,}',
                ha='center', va='bottom', fontsize=8, fontweight='bold')

# Add statistics box
stats_text = f"Mean: {sleep_mean} hrs\nMedian: {sleep_median} hrs\nQuality: {sleep_quality}/10\nn = {len(df):,}"
plt.text(0.98, 0.97, stats_text, transform=plt.gca().transAxes,
        fontsize=10, fontweight='bold', verticalalignment='top', horizontalalignment='right',
        bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.7))

plt.title("D3. Sleep Hours Distribution", fontsize=13, fontweight='bold', pad=15)
plt.xlabel("Sleep Hours", fontsize=8, fontweight='bold')
plt.ylabel("Employee-Day Count", fontsize=8, fontweight='bold')
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig("D3_sleep_distribution.png", dpi=120, bbox_inches='tight')
plt.show()

# COMMAND ----------

d4 = df["MENTAL_STATE"].value_counts()
d4_pct = (d4 / len(df) * 100).round(1)
print("\nD4. Mental state breakdown:\n", pd.DataFrame({"count": d4, "pct_share": d4_pct}))

plt.figure(figsize=(4, 4))
colors = ["#E63946", "#457B9D", "#2EC4B6", "#F4A300"]
wedges, texts, autotexts = plt.pie(d4.values, labels=d4.index, autopct='%1.1f%%',
                                     colors=colors, startangle=90, textprops={'fontsize': 11, 'fontweight': 'bold'})

# Style the percentage text
for autotext in autotexts:
    autotext.set_color('white')
    autotext.set_fontsize(11)
    autotext.set_fontweight('bold')

# Add count labels
for i, (label, count) in enumerate(zip(d4.index, d4.values)):
    angle = (wedges[i].theta2 + wedges[i].theta1) / 2
    x = 1.3 * np.cos(np.radians(angle))
    y = 1.3 * np.sin(np.radians(angle))
    plt.text(x, y, f'n={count:,}', ha='center', va='center', fontsize=9, fontweight='bold')

plt.title("D4. Mental State Breakdown", fontsize=13, fontweight='bold', pad=15)
plt.tight_layout()
plt.savefig("D4_mental_state_breakdown.png", dpi=120, bbox_inches='tight')
plt.show()

# COMMAND ----------

# ---- D5. Productivity score distribution ----
d5 = (
    df.groupby("PRODUCTIVITY_CATEGORY")["PRODUCTIVITY_SCORE"]
    .agg(["count", "mean"]).round(2)
    .sort_values("mean", ascending=False)
)
print("\nD5. Productivity by category:\n", d5)

plt.figure(figsize=(4, 4))
bars = plt.bar(d5.index, d5["mean"], color="#2EC4B6", edgecolor='black', linewidth=0.7)

# Add value labels on bars
for bar, (idx, row) in zip(bars, d5.iterrows()):
    height = bar.get_height()
    count = int(row["count"])
    plt.text(bar.get_x() + bar.get_width()/2., height,
            f'{height:.2f}\n(n={count:,})',
            ha='center', va='bottom', fontsize=10, fontweight='bold')

plt.title("D5. Average Productivity Score by Category", fontsize=13, fontweight='bold', pad=15)
plt.ylabel("Avg Productivity Score", fontsize=11, fontweight='bold')
plt.xlabel("Productivity Category", fontsize=11, fontweight='bold')
plt.ylim(0, 110)
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig("D5_productivity_by_category.png", dpi=120)
plt.show()


# COMMAND ----------

plt.figure(figsize=(4, 4))

bars = plt.bar(
    ["Notifications", "Unlocks", "App Switches"],
    d6.values,
    color="#F4A300",
    edgecolor="black",
    linewidth=0.7
)

for bar, value in zip(bars, d6.values):
    height = bar.get_height()
    plt.text(
        bar.get_x() + bar.get_width()/2,
        height + 2,
        f"{value:.0f}",
        ha="center",
        va="bottom",
        fontsize=12,
        fontweight="bold"
    )

plt.ylim(0, max(d6.values) * 1.15)

plt.title("D6. Average Daily Interruption Load",
          fontsize=13, fontweight="bold", pad=15)
plt.ylabel("Count / Day", fontsize=11, fontweight="bold")
plt.tight_layout()
plt.savefig("D6_interruption_load.png", dpi=120, bbox_inches="tight")
plt.show()

# COMMAND ----------

# ---- D7. Stress & fatigue indicator profile ----
d7 = df[["STRESS_LEVEL", "MENTAL_FATIGUE", "EMOTIONAL_EXHAUSTION"]].mean().round(2)
print("\nD7. Stress & fatigue profile:\n", d7)

plt.figure(figsize=(5, 4))
bars = plt.bar(["Stress", "Mental Fatigue", "Emotional Exhaustion"], d7.values,
               color="#E63946", edgecolor='black', linewidth=0.7)

# Add value labels on bars
for bar, value in zip(bars, d7.values):
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height,
            f'{value:.2f}/10',
            ha='center', va='bottom', fontsize=12, fontweight='bold')

plt.title("D7. Average Stress & Fatigue Indicators", fontsize=13, fontweight='bold', pad=15)
plt.ylabel("Score (1-10)", fontsize=11, fontweight='bold')
plt.grid(axis='y', alpha=0.3)
plt.ylim(0, d7.max() * 1.15)
plt.tight_layout()
plt.savefig("D7_stress_fatigue_profile.png", dpi=120, bbox_inches='tight')
plt.show()

# COMMAND ----------

# ============================================================================
# SECTION 4 — DIAGNOSTIC ANALYSIS  ("why is it happening?")
# Matches the Diagnostic Analysis Plan slide, same 6 items, same order.
# Scatter plots use a 0.2% random sample purely for visualization -- the
# correlation numbers themselves come from the full dataset.
# ============================================================================

# COMMAND ----------

# ---- G1. Why burnout risk correlates with lower productivity ----
corr_g1 = df["BURNOUT_RISK"].corr(df["PRODUCTIVITY_SCORE"])
print(f"\nG1. corr(BURNOUT_RISK, PRODUCTIVITY_SCORE) = {corr_g1:.3f}")

sample_g1 = df[["BURNOUT_RISK", "PRODUCTIVITY_SCORE"]].sample(frac=0.002, random_state=42)
plt.figure(figsize=(6, 6))
plt.scatter(sample_g1["BURNOUT_RISK"], sample_g1["PRODUCTIVITY_SCORE"], 
           alpha=0.4, s=15, color="#E63946", edgecolor='none')

# Add trend line
z = np.polyfit(sample_g1["BURNOUT_RISK"].astype(float), sample_g1["PRODUCTIVITY_SCORE"].astype(float), 1)
p = np.poly1d(z)
burnout_range = np.linspace(float(sample_g1["BURNOUT_RISK"].min()), float(sample_g1["BURNOUT_RISK"].max()), 100)
plt.plot(burnout_range, p(burnout_range), "b--", linewidth=2, alpha=0.7, label="Trend Line")

# Add correlation box
corr_text = f"Correlation: {corr_g1:.4f}\nSample Size: {len(sample_g1):,}\nInterpretation: Strong Negative"
plt.text(0.05, 0.95, corr_text, transform=plt.gca().transAxes,
        fontsize=10, fontweight='bold', verticalalignment='top',
        bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.7))

plt.title("G1. Burnout Risk vs. Productivity Score", fontsize=13, fontweight='bold', pad=15)
plt.xlabel("Burnout Risk", fontsize=11, fontweight='bold')
plt.ylabel("Productivity Score", fontsize=11, fontweight='bold')
plt.legend(fontsize=10)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("G1_burnout_vs_productivity.png", dpi=120, bbox_inches='tight')
plt.show()

# COMMAND ----------

# ---- G2. Why screen time predicts burnout risk ----
corr_g2 = df["DAILY_SCREEN_TIME"].corr(df["BURNOUT_RISK"])
print(f"G2. corr(DAILY_SCREEN_TIME, BURNOUT_RISK) = {corr_g2:.3f}")

sample_g2 = df[["DAILY_SCREEN_TIME", "BURNOUT_RISK"]].sample(frac=0.002, random_state=42)
plt.figure(figsize=(8, 6))
plt.scatter(sample_g2["DAILY_SCREEN_TIME"], sample_g2["BURNOUT_RISK"], 
           alpha=0.4, s=15, color="#457B9D", edgecolor='none')

# Add trend line
z = np.polyfit(sample_g2["DAILY_SCREEN_TIME"].astype(float), sample_g2["BURNOUT_RISK"].astype(float), 1)
p = np.poly1d(z)
screen_range = np.linspace(float(sample_g2["DAILY_SCREEN_TIME"].min()), float(sample_g2["DAILY_SCREEN_TIME"].max()), 100)
plt.plot(screen_range, p(screen_range), "r--", linewidth=2, alpha=0.7, label="Trend Line")

# Add correlation box
corr_text = f"Correlation: {corr_g2:.4f}\nSample Size: {len(sample_g2):,}\nInterpretation: Moderate Positive"
plt.text(0.05, 0.95, corr_text, transform=plt.gca().transAxes,
        fontsize=10, fontweight='bold', verticalalignment='top',
        bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.7))

plt.title("G2. Screen Time vs. Burnout Risk", fontsize=13, fontweight='bold', pad=15)
plt.xlabel("Daily Screen Time (hrs)", fontsize=11, fontweight='bold')
plt.ylabel("Burnout Risk", fontsize=11, fontweight='bold')
plt.legend(fontsize=10)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("G2_screentime_vs_burnout.png", dpi=120, bbox_inches='tight')
plt.show()

# COMMAND ----------

# ---- G3. Why sleep deficit relates to burnout ----
corr_g3 = df["SLEEP_HOURS"].corr(df["BURNOUT_RISK"])
print(f"G3. corr(SLEEP_HOURS, BURNOUT_RISK) = {corr_g3:.3f}")

sample_g3 = df[["SLEEP_HOURS", "BURNOUT_RISK"]].sample(frac=0.002, random_state=42)
plt.figure(figsize=(8, 6))
plt.scatter(sample_g3["SLEEP_HOURS"], sample_g3["BURNOUT_RISK"], 
           alpha=0.4, s=15, color="#2EC4B6", edgecolor='none')

# Add trend line
z = np.polyfit(sample_g3["SLEEP_HOURS"].astype(float), sample_g3["BURNOUT_RISK"].astype(float), 1)
p = np.poly1d(z)
sleep_range = np.linspace(float(sample_g3["SLEEP_HOURS"].min()), float(sample_g3["SLEEP_HOURS"].max()), 100)
plt.plot(sleep_range, p(sleep_range), "r--", linewidth=2, alpha=0.7, label="Trend Line")

# Add correlation box
corr_text = f"Correlation: {corr_g3:.4f}\nSample Size: {len(sample_g3):,}\nInterpretation: Strong Negative"
plt.text(0.05, 0.95, corr_text, transform=plt.gca().transAxes,
        fontsize=10, fontweight='bold', verticalalignment='top',
        bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.7))

plt.title("G3. Sleep Hours vs. Burnout Risk", fontsize=13, fontweight='bold', pad=15)
plt.xlabel("Sleep Hours", fontsize=11, fontweight='bold')
plt.ylabel("Burnout Risk", fontsize=11, fontweight='bold')
plt.legend(fontsize=10)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("G3_sleep_vs_burnout.png", dpi=120, bbox_inches='tight')
plt.show()

# COMMAND ----------

# ---- G4. Why OCCUPATION barely moves burnout risk ----
g4 = df.groupby("OCCUPATION")["BURNOUT_RISK"].mean().sort_values(ascending=False)
print("\nG4. Burnout risk by OCCUPATION:\n", g4.round(3))

plt.figure(figsize=(9, 6))
bars = plt.barh(g4.index[::-1], g4.values[::-1], color="#457B9D", edgecolor='black', linewidth=0.7)

# Add value labels on bars
for i, (bar, value) in enumerate(zip(bars, g4.values[::-1])):
    width = bar.get_width()
    plt.text(width, bar.get_y() + bar.get_height()/2.,
            f'{value:.2f}',
            ha='left', va='center', fontsize=11, fontweight='bold', 
            bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.7))

plt.title("G4. Average Burnout Risk by Occupation", fontsize=13, fontweight='bold', pad=15)
plt.xlabel("Avg Burnout Risk", fontsize=11, fontweight='bold')
plt.grid(axis='x', alpha=0.3)
plt.xlim(0, g4.max() + 6)
plt.tight_layout()
plt.savefig("G4_burnout_by_occupation.png", dpi=120, bbox_inches='tight')
plt.show()


# COMMAND ----------

# ---- G5. What drives the Focused vs. Burnout productivity gap ----
g5 = (
    df[df["MENTAL_STATE"].isin(["Focused", "Burnout"])]
    .groupby("MENTAL_STATE")[["PRODUCTIVITY_SCORE", "DAILY_SCREEN_TIME", "SLEEP_HOURS", "STRESS_LEVEL"]]
    .mean().round(2)
)
print("\nG5. Focused vs. Burnout comparison:\n", g5)

metrics_g5 = ["PRODUCTIVITY_SCORE", "DAILY_SCREEN_TIME", "SLEEP_HOURS", "STRESS_LEVEL"]
metric_labels = ["Productivity", "Screen Time", "Sleep Hrs", "Stress"]
x = np.arange(len(metrics_g5))
width = 0.35

plt.figure(figsize=(8, 4))
bars1 = plt.bar(x - width/2, g5.loc["Focused", metrics_g5], width, label="Focused", 
               color="#2EC4B6", edgecolor='black', linewidth=0.7)
bars2 = plt.bar(x + width/2, g5.loc["Burnout", metrics_g5], width, label="Burnout", 
               color="#E63946", edgecolor='black', linewidth=0.7)

# Add value labels on bars
for bars in [bars1, bars2]:
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.2f}',
                ha='center', va='bottom', fontsize=9, fontweight='bold')

plt.xticks(x, metric_labels, fontsize=11)
plt.title("G5. Focused vs. Burnout: Habit & Outcome Comparison", fontsize=13, fontweight='bold', pad=15)
plt.ylabel("Value", fontsize=11, fontweight='bold')
plt.legend(fontsize=11, loc='upper right')
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig("G5_focused_vs_burnout.png", dpi=120, bbox_inches='tight')
plt.show()

# COMMAND ----------

# ---- G6. Which habits most strongly predict low productivity ----
habit_cols = [
    "DAILY_SCREEN_TIME",
    "SOCIAL_MEDIA_HOURS",
    "SLEEP_HOURS",
    "STRESS_LEVEL",
    "DEEP_WORK_HOURS",
    "NOTIFICATION_COUNT"
]

g6 = (
    df[habit_cols + ["PRODUCTIVITY_SCORE"]]
    .corr()["PRODUCTIVITY_SCORE"]
    .drop("PRODUCTIVITY_SCORE")
)

# Sort by absolute correlation
g6_sorted = g6.reindex(g6.abs().sort_values(ascending=False).index).round(3)

print("\nG6. Productivity driver correlations (ranked):\n", g6_sorted)

plt.figure(figsize=(7, 5))

# Color positive and negative bars
colors = ["#2EC4B6" if x > 0 else "#E63946" for x in g6_sorted.values]

bars = plt.barh(
    g6_sorted.index[::-1],
    g6_sorted.values[::-1],
    color=colors[::-1],
    edgecolor="black",
    linewidth=0.7
)

# Value labels
for bar, value in zip(bars, g6_sorted.values[::-1]):
    width = bar.get_width()

    if width >= 0:
        plt.text(
            width + 0.01,
            bar.get_y() + bar.get_height()/2,
            f"{value:.3f}",
            ha="left",
            va="center",
            fontsize=10,
            fontweight="bold"
        )
    else:
        plt.text(
            width - 0.01,
            bar.get_y() + bar.get_height()/2,
            f"{value:.3f}",
            ha="right",
            va="center",
            fontsize=10,
            fontweight="bold"
        )

# Formatting
plt.title(
    "G6. Habit Correlation with Productivity Score (Ranked)",
    fontsize=13,
    fontweight="bold",
    pad=18
)

plt.xlabel(
    "Correlation Coefficient",
    fontsize=11,
    fontweight="bold"
)

# Zero reference line
plt.axvline(0, color="black", linewidth=1.2)

# Give labels breathing room
plt.xlim(-0.3, 0.70)

# Light grid
plt.grid(axis="x", alpha=0.2)

plt.tight_layout()

plt.savefig(
    "G6_productivity_driver_correlations.png",
    dpi=120,
    bbox_inches="tight"
)

plt.show()

# COMMAND ----------

# DBTITLE 1,Cell 22
import pickle
import numpy as np
import pandas as pd
import matplotlib
# matplotlib.use("Agg")
import matplotlib.pyplot as plt
 
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score, roc_auc_score,
    confusion_matrix, roc_curve, r2_score, mean_absolute_error, mean_squared_error
)

# COMMAND ----------

# ============================================================================
# SECTION 1 — FEATURE ENGINEERING & SELECTION
# ============================================================================

# COMMAND ----------

"""
Feature set is deliberately restricted to genuine digital-habit, lifestyle
and workplace variables -- excludes BURNOUT_RISK, PRODUCTIVITY_SCORE,
PRODUCTIVITY_CATEGORY and MENTAL_STATE as inputs (those are the targets /
target-adjacent columns for the two models below -- see the Data
Understanding & Analysis Guide for the full leakage-avoidance reasoning).
"""

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

X = df[NUMERIC_FEATURES + CATEGORICAL_FEATURES]

preprocessor = ColumnTransformer(transformers=[
    ("num", StandardScaler(), NUMERIC_FEATURES),
    ("cat", OneHotEncoder(drop="first", handle_unknown="ignore"), CATEGORICAL_FEATURES),
])

# Quick feature-selection pass: rank numeric features by correlation with
# each target, as a sanity check on what the models should surface as important.
print("\nTop correlations with IS_HIGH_BURNOUT_RISK:")
print(df[NUMERIC_FEATURES + ["IS_HIGH_BURNOUT_RISK"]].corr()["IS_HIGH_BURNOUT_RISK"]
      .drop("IS_HIGH_BURNOUT_RISK").abs().sort_values(ascending=False).head(10))

# COMMAND ----------

print("\nTop correlations with PRODUCTIVITY_SCORE:")
print(df[NUMERIC_FEATURES + ["PRODUCTIVITY_SCORE"]].corr()["PRODUCTIVITY_SCORE"]
      .drop("PRODUCTIVITY_SCORE").abs().sort_values(ascending=False).head(10))

# COMMAND ----------

# ============================================================================
# SECTION 2 — PREDICTIVE MODEL 1: LOGISTIC REGRESSION (Burnout Risk)
# ============================================================================

# COMMAND ----------

"""
Target: IS_HIGH_BURNOUT_RISK (1 if BURNOUT_RISK > 70, else 0)
class_weight='balanced' compensates for the ~17% positive-class imbalance.
"""

y_clf = df["IS_HIGH_BURNOUT_RISK"]
X_train, X_test, y_train, y_test = train_test_split(
    X, y_clf, test_size=0.2, random_state=42, stratify=y_clf
)

burnout_clf = Pipeline([
    ("prep", preprocessor),
    ("model", LogisticRegression(max_iter=1000, class_weight="balanced", random_state=42)),
])
burnout_clf.fit(X_train, y_train)

y_pred = burnout_clf.predict(X_test)
y_proba = burnout_clf.predict_proba(X_test)[:, 1]

acc = accuracy_score(y_test, y_pred)
prec = precision_score(y_test, y_pred)
rec = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)
auc = roc_auc_score(y_test, y_proba)
cm = confusion_matrix(y_test, y_pred)

print("\n=== Logistic Regression -- High Burnout Risk Classification ===")
print(f"Accuracy:  {acc:.4f}")
print(f"Precision: {prec:.4f}")
print(f"Recall:    {rec:.4f}")
print(f"F1 Score:  {f1:.4f}")
print(f"ROC-AUC:   {auc:.4f}")
print("Confusion Matrix:\n", cm)

# COMMAND ----------

# DBTITLE 1,Model 2: Linear Regression (Productivity Score)
# ============================================================================
# SECTION 3 — PREDICTIVE MODEL 2: LINEAR REGRESSION (Productivity Score)
# ============================================================================

# COMMAND ----------

"""
Target: IS_HIGH_BURNOUT_RISK (1 if BURNOUT_RISK > 70, else 0)
class_weight='balanced' compensates for the ~17% positive-class imbalance.
"""

y_clf = df["IS_HIGH_BURNOUT_RISK"]
X_train, X_test, y_train, y_test = train_test_split(
    X, y_clf, test_size=0.2, random_state=42, stratify=y_clf
)

burnout_clf = Pipeline([
    ("prep", preprocessor),
    ("model", LogisticRegression(max_iter=1000, class_weight="balanced", random_state=42)),
])
burnout_clf.fit(X_train, y_train)

y_pred = burnout_clf.predict(X_test)
y_proba = burnout_clf.predict_proba(X_test)[:, 1]

acc = accuracy_score(y_test, y_pred)
prec = precision_score(y_test, y_pred)
rec = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)
auc = roc_auc_score(y_test, y_proba)
cm = confusion_matrix(y_test, y_pred)

print("\n=== Logistic Regression -- High Burnout Risk Classification ===")
print(f"Accuracy:  {acc:.4f}")
print(f"Precision: {prec:.4f}")
print(f"Recall:    {rec:.4f}")
print(f"F1 Score:  {f1:.4f}")
print(f"ROC-AUC:   {auc:.4f}")
print("Confusion Matrix:\n", cm)

# COMMAND ----------

# ---- Chart 1: Confusion matrix heatmap ----
plt.figure(figsize=(5, 5))
plt.imshow(cm, cmap="Blues")
plt.title("Confusion Matrix -- High Burnout Risk")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.xticks([0, 1], ["Not High Risk", "High Risk"])
plt.yticks([0, 1], ["Not High Risk", "High Risk"])
for i in range(2):
    for j in range(2):
        plt.text(j, i, str(cm[i, j]), ha="center", va="center",
                  color="white" if cm[i, j] > cm.max() / 2 else "black", fontsize=14)
plt.colorbar()
plt.tight_layout()
plt.savefig("Model1_confusion_matrix.png", dpi=120)
plt.show()

# COMMAND ----------

# ---- Chart 2: ROC curve ----
fpr, tpr, _ = roc_curve(y_test, y_proba)
plt.figure(figsize=(6, 6))
plt.plot(fpr, tpr, color="#E63946", label=f"ROC curve (AUC = {auc:.3f})")
plt.plot([0, 1], [0, 1], linestyle="--", color="gray", label="Random guess")
plt.title("ROC Curve -- High Burnout Risk Model")
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.legend()
plt.tight_layout()
plt.savefig("Model1_roc_curve.png", dpi=120)
plt.show()

# COMMAND ----------

# ---- Chart 3: Feature importance (coefficients) ----
feature_names_clf = (
    NUMERIC_FEATURES
    + list(burnout_clf.named_steps["prep"].named_transformers_["cat"].get_feature_names_out(CATEGORICAL_FEATURES))
)
coefs = burnout_clf.named_steps["model"].coef_[0]
coef_df = pd.DataFrame({"feature": feature_names_clf, "coefficient": coefs})
coef_df = coef_df.reindex(coef_df["coefficient"].abs().sort_values(ascending=False).index).head(10)

plt.figure(figsize=(8, 5))
plt.barh(coef_df["feature"][::-1], coef_df["coefficient"][::-1], color="#457B9D")
plt.title("Top 10 Feature Coefficients -- Burnout Risk Model")
plt.xlabel("Coefficient (standardized features)")
plt.tight_layout()
plt.savefig("Model1_feature_importance.png", dpi=120)
plt.show()

# COMMAND ----------

# ============================================================================
# SECTION 3 — PREDICTIVE MODEL 2: LINEAR REGRESSION (Productivity Score)
# ============================================================================

# COMMAND ----------

y_reg = df["PRODUCTIVITY_SCORE"]
X_train2, X_test2, y_train2, y_test2 = train_test_split(X, y_reg, test_size=0.2, random_state=42)

productivity_reg = Pipeline([
    ("prep", preprocessor),
    ("model", LinearRegression()),
])
productivity_reg.fit(X_train2, y_train2)

y_pred2 = productivity_reg.predict(X_test2)

r2 = r2_score(y_test2, y_pred2)
mae = mean_absolute_error(y_test2, y_pred2)
rmse = np.sqrt(mean_squared_error(y_test2, y_pred2))

print("\n=== Linear Regression -- Productivity Score Prediction ===")
print(f"R\u00b2:   {r2:.4f}")
print(f"MAE:  {mae:.4f}")
print(f"RMSE: {rmse:.4f}")

# COMMAND ----------

# ---- Chart 1: Actual vs. Predicted (sampled for a readable scatter) ----
sample_idx = np.random.RandomState(42).choice(len(y_test2), size=min(15000, len(y_test2)), replace=False)
plt.figure(figsize=(7, 6))
plt.scatter(y_test2.values[sample_idx], y_pred2[sample_idx], alpha=0.25, s=8, color="#2EC4B6")
plt.plot([0, 100], [0, 100], linestyle="--", color="gray")
plt.title(f"Actual vs. Predicted Productivity Score (R\u00b2 = {r2:.2f})")
plt.xlabel("Actual Productivity Score")
plt.ylabel("Predicted Productivity Score")
plt.tight_layout()
plt.savefig("Model2_actual_vs_predicted.png", dpi=120)
plt.show()

# COMMAND ----------

# ---- Chart 2: Residual plot ----
residuals = y_test2.values[sample_idx].astype(float) - y_pred2[sample_idx]
plt.figure(figsize=(7, 5))
plt.scatter(y_pred2[sample_idx], residuals, alpha=0.25, s=8, color="#E63946")
plt.axhline(0, linestyle="--", color="gray")
plt.title("Residual Plot -- Productivity Score Model")
plt.xlabel("Predicted Productivity Score")
plt.ylabel("Residual (Actual - Predicted)")
plt.tight_layout()
plt.savefig("Model2_residuals.png", dpi=120)
plt.show()

# COMMAND ----------

# ---- Chart 3: Feature importance (coefficients) ----
feature_names_reg = (
    NUMERIC_FEATURES
    + list(productivity_reg.named_steps["prep"].named_transformers_["cat"].get_feature_names_out(CATEGORICAL_FEATURES))
)
reg_coefs = productivity_reg.named_steps["model"].coef_
reg_coef_df = pd.DataFrame({"feature": feature_names_reg, "coefficient": reg_coefs})
reg_coef_df = reg_coef_df.reindex(reg_coef_df["coefficient"].abs().sort_values(ascending=False).index).head(10)

plt.figure(figsize=(8, 5))
plt.barh(reg_coef_df["feature"][::-1], reg_coef_df["coefficient"][::-1], color="#F4A300")
plt.title("Top 10 Feature Coefficients -- Productivity Score Model")
plt.xlabel("Coefficient (standardized features)")
plt.tight_layout()
plt.savefig("Model2_feature_importance.png", dpi=120)
plt.show()


# COMMAND ----------

# ============================================================================
# SECTION 4 — SAVE MODELS
# ============================================================================

# COMMAND ----------

with open("logistic_burnout_model.pkl", "wb") as f:
    pickle.dump(burnout_clf, f)

with open("linear_productivity_model.pkl", "wb") as f:
    pickle.dump(productivity_reg, f)

print("\nModels saved: logistic_burnout_model.pkl, linear_productivity_model.pkl")
print("These are the same files streamlit_app.py loads for the web app.")
