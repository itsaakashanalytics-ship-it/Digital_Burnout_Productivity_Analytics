
# 📊 Digital Burnout & Workplace Productivity Analytics

<p align="center">
  <h1 align="center">Digital Burnout & Workplace Productivity Analytics</h1>
  <p align="center">
    End-to-End Data Analytics Solution using <b>Snowflake • Databricks • Python • Power BI • Streamlit</b>
  </p>
</p>

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![Snowflake](https://img.shields.io/badge/Snowflake-Data%20Warehouse-29B5E8?logo=snowflake)
![Databricks](https://img.shields.io/badge/Databricks-Analytics-EF3E42?logo=databricks)
![Power BI](https://img.shields.io/badge/Power%20BI-Dashboard-F2C811?logo=powerbi)
![Streamlit](https://img.shields.io/badge/Streamlit-Web%20Application-FF4B4B?logo=streamlit)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-Machine%20Learning-F7931E?logo=scikitlearn)

---

## 📖 Overview

This project presents an end-to-end analytics solution designed to understand the relationship between digital habits, employee wellbeing, burnout risk, and workplace productivity.

The solution integrates:

- **Snowflake** for SQL-based data storage and preparation
- **Databricks** for Python analytics and machine learning
- **Power BI** for executive dashboards
- **Streamlit** for interactive analytics deployment

---

## 🎯 Business Problem

Modern employees are exposed to excessive screen time, notification overload, app switching, doomscrolling, and late-night device usage. These behaviours gradually affect focus, sleep quality, wellbeing, and ultimately workplace productivity.

This project develops a complete analytics workflow to identify burnout drivers, predict employee burnout risk, and estimate productivity using machine learning.

---

# 🏗️ Solution Architecture

```text
Dataset (1.5M Records)
          │
          ▼
Snowflake SQL
(Data Validation & Cleaning)
          │
          ▼
Databricks
(Python + EDA + Machine Learning)
          │
     ┌────┴─────┐
     ▼          ▼
Power BI   Streamlit
Dashboard   Web App
```

---

# 🛠️ Technology Stack

| Layer | Technologies |
|-------|--------------|
| Database | Snowflake |
| Analytics | Databricks |
| Programming | Python |
| Libraries | Pandas, NumPy, Scikit-learn, Matplotlib |
| Dashboard | Power BI |
| Deployment | Streamlit |
| Version Control | Git & GitHub |

---

# 📊 Dataset

- 1.5 Million Employee-Day Records
- 34 Features
- 7 Occupations
- Multiple behavioural, productivity and wellbeing variables

### Feature Categories

- Demographics
- Digital Habits
- Focus & Work
- Sleep & Recovery
- Psychological Indicators
- Workplace Context
- Productivity Metrics
- Burnout Metrics

---

# 🔄 Project Workflow

1. Import raw dataset
2. Store and validate data in Snowflake
3. Clean and transform data
4. Perform EDA in Databricks
5. Conduct diagnostic analytics
6. Build machine learning models
7. Create Power BI dashboards
8. Publish insights using Streamlit

---

# 🧹 Data Preparation

- Missing value analysis
- Median imputation
- Duplicate validation
- Feature engineering
- Derived variables
- Data quality checks

---

# 📈 Exploratory Data Analysis

The project explores:

- Workforce demographics
- Work modes
- Screen time
- Doomscrolling
- Sleep behaviour
- Mental state
- Productivity
- Burnout distribution

---

# 🔍 Diagnostic Analytics

Business questions answered:

- Which digital habits increase burnout?
- Does sleep affect productivity?
- Does excessive screen time increase burnout?
- Which behaviours have the strongest impact?

---

# 🤖 Machine Learning

## Burnout Risk Prediction

**Algorithm**

- Logistic Regression

Evaluation

- Accuracy
- Precision
- Recall
- F1 Score
- ROC-AUC

---

## Productivity Prediction

**Algorithm**

- Linear Regression

Evaluation

- R²
- MAE
- RMSE

---

# 📊 Power BI Dashboard

Six interactive dashboard pages:

1. Executive Overview
2. Occupation & Work Mode
3. Digital Habit Explorer
4. Sleep & Recovery
5. Burnout Risk Monitor
6. Productivity Drivers

> Add dashboard screenshots inside `/images`.

---

# 🌐 Streamlit Application

Interactive application includes:

- Executive Dashboard
- Descriptive Analytics
- Diagnostic Analytics
- Predictive Analytics
- Machine Learning Predictions
- Interactive Visualizations

---

# 📁 Suggested Repository Structure

```text
Digital-Burnout-Workplace-Productivity-Analytics
│
├── data/
├── snowflake/
├── databricks/
├── powerbi/
├── streamlit/
├── report/
├── images/
├── requirements.txt
└── README.md
```

---

# 🚀 Installation

```bash
git clone https://github.com/YOUR_USERNAME/Digital-Burnout-Workplace-Productivity-Analytics.git
cd Digital-Burnout-Workplace-Productivity-Analytics
pip install -r requirements.txt
streamlit run app.py
```

---

# 💼 Business Value

- Identify burnout drivers
- Predict employee burnout risk
- Estimate productivity
- Support HR decision making
- Improve workforce wellbeing
- Enable data-driven interventions

---

# 🔮 Future Improvements

- Real-time Snowflake integration
- Automated retraining
- Ensemble ML models
- Cloud deployment
- HR recommendation engine

---

# 👨‍💻 Author

**Aakash Kumar**

Data Analyst

---

⭐ If you found this project useful, please consider starring the repository.
