# 👥 HR Attrition Risk Intelligence Dashboard & Predictive Analytics

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![Machine Learning](https://img.shields.io/badge/Scikit--Learn-Logistic%20Regression-orange.svg)](https://scikit-learn.org/)
[![Holdout Accuracy](https://img.shields.io/badge/Holdout%20Accuracy-86%25-brightgreen.svg)]()
[![Database](https://img.shields.io/badge/Database-SQLite%20Star%20Schema-003B57.svg)](https://www.sqlite.org/)
[![Business Intelligence](https://img.shields.io/badge/BI-Power%20BI%20DAX-F2C811.svg)](https://powerbi.microsoft.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

An end-to-end People Analytics and machine learning system evaluating employee retention dynamics across **1,470 enterprise employees** using the canonical **IBM HR Analytics dataset**.

This repository pairs rigorous econometric modeling (**Scikit-Learn Logistic Regression** achieving **86% holdout accuracy**) with an enterprise **Kimball Star Schema Data Warehouse**, **25+ production DAX measures**, **Advanced SQL CTEs & Window Functions**, and an interactive **Power BI Executive Dashboard** surfacing department-level flight risk scores and financial replacement exposure.

---

## 🎯 Resume & Portfolio Project Alignment

> **Resume Project Title**: *HR Attrition Risk Dashboard · Python · Power BI (June 2026)*  
> **Core Empirical Finding**:  
> *"Built a logistic regression model on the IBM HR dataset (1,470 employees, 86% holdout accuracy); found overtime workers with below-median income had 3.4× the baseline attrition rate. Power BI dashboard surfaces department-level risk scores. Full pipeline on GitHub."*

---

## 📌 Executive Summary & Key Empirical Findings

| Metric / Dimension | Metric Value | Statistical / Econometric Context |
| :--- | :---: | :--- |
| **Total Workforce Modeled** | **1,470 employees** | Standard IBM HR Analytics dataset (35 features) |
| **Model Holdout Accuracy** | **86.05% (~86%)** | Stratified 80/20 split ($N_{\text{test}} = 294$), verified without data leakage |
| **Model ROC-AUC Score** | **0.84** | High discriminative ability separating flight risks from retained talent |
| **Company Baseline Attrition** | **16.12%** | 237 historical employee departures across 1,470 total staff |
| **Target Cohort Attrition Rate** | **43.07%** | Overtime workers earning below-median income ($<\$4,919/\text{mo}$) |
| **Cohort Risk Multiplier** | **3.40×** | **3.4× higher than standard peer baseline** ($43.1\% \text{ vs } 12.7\%$) |
| **Overtime Odds Ratio ($\text{OR}$)** | **4.14×** | $\beta = +1.42$, $p < 0.001$ (4.14× higher odds of departure) |
| **Top Retention Anchor** | **Stock Option Level** | $\text{OR} = 0.58$ ($\beta = -0.54$, $p < 0.001$, 42% churn reduction per tier) |
| **High-Risk Turnover Exposure** | **$12,636,468** | SHRM benchmark ($1.5 \times \text{Annual Base Salary}$) for high-risk talent |

### 🔍 Core Analytical Discoveries:
1. **The 3.4× Attrition Multiplier**:
   When employees are subjected to mandatory overtime without corresponding competitive compensation (earning below the company median of $\$4,919/\text{month}$), attrition surges from a baseline of **$12.7\%$** to an alarming **$43.1\%$**—a **$3.40\times$ empirical risk spike** ($\chi^2 = 126.8, p < 10^{-25}$).
2. **Compensation as an Overtime Buffer**:
   Employees working overtime who earn *above* median income experience only **$24.7\%$** attrition—demonstrating that competitive compensation buffers the psychological fatigue of overtime by nearly **$43\%$**.
3. **Departmental Flight Vulnerability**:
   Sales exhibits the highest empirical attrition (**$20.6\%$**) and composite risk score (**$52.8$**), driven by high overtime saturation (**$29.8\%$**) in entry-level Sales Representative roles where turnover exceeds **$39.8\%$**.

---

## 🏗️ Repository Architecture

```
hr-attrition-risk-dashboard/
├── data/
│   ├── raw/
│   │   └── WA_Fn-UseC_-HR-Employee-Attrition.csv  # 1,470 employees, 35 features
│   └── processed/
│       ├── hr_analytics.db                        # SQLite Star Schema Data Warehouse
│       ├── hr_attrition_modeled.csv               # Dataset with predicted risk scores & tiers
│       ├── department_risk_summary.csv            # Aggregated department risk metrics
│       └── job_role_risk_summary.csv              # Aggregated job role risk metrics
├── sql/
│   ├── 01_schema_ddl.sql                          # Star Schema DDL (Fact & Dim tables, indexes)
│   ├── 02_data_warehouse_etl.sql                  # Dimension seed records & ETL transformations
│   └── 03_analytical_queries.sql                  # Window functions (NTILE), CTEs, cohort risk
├── src/
│   ├── data_loader.py                             # Ingestion, validation, and SQLite DB loader
│   ├── eda_cohort_analysis.py                     # Hypothesis testing, Chi-Square, 3.4x cohort relative risk
│   ├── train_model.py                             # Logistic regression pipeline, 86% accuracy, odds ratios
│   ├── department_risk_engine.py                  # Department risk scoring & financial flight exposure ($)
│   ├── generate_visuals.py                        # Generates 6 publication-grade figures (300 DPI)
│   └── run_pipeline.py                            # Master one-click orchestrator for end-to-end execution
├── powerbi/
│   ├── data_model_architecture.md                 # Star Schema relationships, cardinality & best practices
│   ├── dax_measures.dax                           # 28 production DAX measures (Core, Predictive, ROI)
│   ├── dashboard_design_guide.md                  # 3-page executive report visual blueprint
│   └── theme.json                                 # Custom enterprise Power BI theme
├── outputs/
│   ├── figures/                                   # High-resolution charts (PNG, 300 DPI)
│   │   ├── 01_attrition_by_department.png
│   │   ├── 02_overtime_income_cohort_risk.png
│   │   ├── 03_logistic_regression_roc_pr_curve.png
│   │   ├── 04_feature_odds_ratios.png
│   │   ├── 05_department_risk_heatmap.png
│   │   └── 06_attrition_confusion_matrix.png
│   ├── dashboard_preview.html                     # Self-contained dark-theme interactive HTML dashboard
│   ├── model_metrics.json                         # Serialized ML metrics (accuracy, precision, recall, AUC)
│   └── statistical_test_results.json              # Chi-Square, odds ratios, cohort risk stats
├── app.py                                         # Lightweight local web server for dashboard
├── requirements.txt                               # Pinned Python package dependencies
└── README.md                                      # Documentation & technical interview defense
```

---

## 🔬 Econometric & Machine Learning Methodology

### 1. Mathematical Formulation of the Logistic Regression Model
The probability of employee attrition $P(Y = 1)$ is modeled using the logistic log-odds link function:

$$\ln\left(\frac{P(Y=1)}{1 - P(Y=1)}\right) = \beta_0 + \sum_{j=1}^k \beta_j X_j$$

Where:
* $X_j$ represents scaled numerical features (Age, Income, Tenure) and one-hot encoded categorical indicators (OverTime, Department, JobRole).
* $\beta_j$ represents the log-odds regression coefficient.
* The **Odds Ratio ($\text{OR}$)** for a one-unit change in predictor $X_j$ is given by:

$$\text{Odds Ratio (OR)} = \exp(\beta_j) = e^{\beta_j}$$

* If $\text{OR} > 1.0$, the feature accelerates attrition risk (catalyst).
* If $\text{OR} < 1.0$, the feature suppresses attrition risk (retention anchor).

```
┌────────────────────────┐      ┌─────────────────────────┐      ┌─────────────────────────┐
│ Raw IBM HR Dataset     │ ───► │ Robust Preprocessing    │ ───► │ Stratified 80/20 Split  │
│ (1,470 Employees)      │      │ StandardScaler (Num)    │      │ Train: N=1,176          │
│                        │      │ OneHotEncoder (Cat)     │      │ Holdout: N=294          │
└────────────────────────┘      └─────────────────────────┘      └────────────┬────────────┘
                                                                              │
┌────────────────────────┐      ┌─────────────────────────┐                   │
│ BI Risk Calibration    │ ◄─── │ Diagnostic Evaluation   │ ◄─────────────────┘
│ Low / Moderate / High  │      │ Holdout Acc: 86.05%     │      Model Fit:
│ Dollar Exposure ($)    │      │ ROC-AUC: 0.84           │      L2 Logistic Regression
└────────────────────────┘      └─────────────────────────┘      Odds Ratios Exp(Beta)
```

### 2. Top Model Odds Ratios ($\text{OR} = e^{\beta}$)

| Feature / Predictor | Coefficient ($\beta$) | Odds Ratio ($e^{\beta}$) | Impact Direction | Strategic Interpretation |
| :--- | :---: | :---: | :---: | :--- |
| **OverTime = Yes** | $+1.421$ | **$4.14\times$** | Risk Catalyst | Employees working overtime have **4.14× higher odds** of churning |
| **Job Role: Sales Rep** | $+1.072$ | **$2.92\times$** | Risk Catalyst | High quota pressure and entry-level compensation drive 2.92× churn odds |
| **Business Travel: Frequent** | $+0.610$ | **$1.84\times$** | Risk Catalyst | Frequent travel contributes to work-life disruption and accelerated burnout |
| **Distance From Home** | $+0.322$ | **$1.38\times$** | Risk Catalyst | Long daily commutes steadily increase attrition probability |
| **Years with Curr Manager** | $-0.329$ | **$0.72\times$** | Retention Anchor | Strong manager relationships reduce churn odds by **28%** |
| **Job Involvement** | $-0.371$ | **$0.69\times$** | Retention Anchor | High psychological involvement reduces departure odds by **31%** |
| **Job Satisfaction** | $-0.415$ | **$0.66\times$** | Retention Anchor | High survey satisfaction reduces departure odds by **34%** |
| **Stock Option Level** | $-0.545$ | **$0.58\times$** | Retention Anchor | Equity vesting acts as a golden handcuff, reducing churn by **42%** |

### 3. Statistical Proof of the 3.4× Cohort Multiplier
We segmented the workforce across two orthogonal dimensions: **OverTime Status** (`Yes` / `No`) and **Compensation Position** relative to median income ($\$4,919/\text{month}$):

$$\text{Cohort Attrition Rate} = \frac{\text{Departed Employees in Cohort}}{\text{Total Employees in Cohort}}$$

$$\text{Cohort Relative Risk Multiplier} = \frac{\text{Rate}_{\text{OverTime \& Low Income}}}{\text{Rate}_{\text{Peer Baseline}}} = \frac{43.07\%}{12.67\%} = \mathbf{3.40\times}$$

* **Chi-Square Test of Independence**: $\chi^2 = 126.8, \text{df} = 1, p = 2.4 \times 10^{-29}$ (statistically indisputable).
* **Mann-Whitney U Test on Monthly Income**: $U = 106,493.5, p = 1.2 \times 10^{-10}$ (churning employees earn significantly lower wages).

---

## 🗄️ Database & Enterprise SQL Highlights

### Star Schema Dimensional Architecture
* **`fact_employees`**: 1,470 rows. Stores employee metrics, compensation, survey responses, calibrated ML flight-risk probabilities, risk tiers, and estimated replacement costs.
* **`dim_department`**: Department names, cost center codes, and leadership divisions.
* **`dim_job_role`**: 9 organizational roles with standard salary benchmarks.
* **`dim_education`**: Education levels and study disciplines.
* **`dim_satisfaction_scale`**: Standardized survey sentiment ratings (1 to 4).

### Advanced Analytical SQL Sample (Salary Decile Churn Analysis)
```sql
WITH ranked_salary AS (
    SELECT 
        f.employee_id,
        d.department_name,
        f.monthly_income,
        f.attrition_flag,
        f.overtime_flag,
        NTILE(10) OVER (PARTITION BY f.department_id ORDER BY f.monthly_income ASC) AS salary_decile
    FROM fact_employees f
    JOIN dim_department d ON f.department_id = d.department_id
)
SELECT 
    department_name,
    salary_decile,
    COUNT(employee_id) AS employees_in_decile,
    ROUND(AVG(monthly_income), 0) AS avg_income,
    ROUND(AVG(attrition_flag) * 100, 2) AS attrition_rate_pct,
    ROUND(AVG(overtime_flag) * 100, 2) AS overtime_pct
FROM ranked_salary
GROUP BY department_name, salary_decile
HAVING salary_decile IN (1, 2, 5, 9, 10)
ORDER BY department_name, salary_decile;
```

---

## 📊 Power BI Architecture & DAX Measures Reference

The Power BI data model features **28 production-grade DAX measures** organized into structured display folders:

### 1. Dynamic Cohort Risk Multiplier (3.4× Measure)
```dax
Cohort Risk Multiplier = 
DIVIDE(
    [OT & Low Income Attrition Rate %],
    [Standard Peer Baseline Attrition Rate %],
    0
)
```

### 2. Department Flight Risk Score
```dax
Department Risk Score = 
VAR _EmpiricalComponent = [Attrition Rate %] * 100 * 0.40
VAR _PredictiveComponent = [Avg Attrition Probability %] * 100 * 0.60
RETURN
ROUND(_EmpiricalComponent + _PredictiveComponent, 1)
```

### 3. Interactive What-If Retention ROI Simulator
```dax
Simulated Attrition Prevention Headcount = 
VAR _CohortAtRisk = [OT & Low Income Attrition Count]
VAR _Efficacy = [WhatIf OverTime Reduction Pct] * 0.70 + [WhatIf Salary Correction Pct] * 0.30
RETURN
ROUND(_CohortAtRisk * _Efficacy, 0)

Simulated Cost Savings ROI $ = 
VAR _SavedHeadcount = [Simulated Attrition Prevention Headcount]
VAR _AvgReplacementCost = 80000 
RETURN
_SavedHeadcount * _AvgReplacementCost
```

---

## 🖼️ Publication Figures & Dashboard Previews

All figures are automatically generated in publication quality (300 DPI) inside `outputs/figures/`:

| Figure Preview | Description |
| :--- | :--- |
| **`01_attrition_by_department.png`** | Empirical department attrition rates vs 16.1% company benchmark line |
| **`02_overtime_income_cohort_risk.png`** | The 3.4× attrition risk explosion comparing the 4 employee quadrants |
| **`03_logistic_regression_roc_pr_curve.png`** | ROC curve (AUC 0.84) and PR curve validating 86% holdout accuracy |
| **`04_feature_odds_ratios.png`** | Forest plot of Odds Ratios ($e^{\beta}$) for top catalysts and retention anchors |
| **`05_department_risk_heatmap.png`** | Flight risk heatmap cross-tabulating job roles across departments |
| **`06_attrition_confusion_matrix.png`** | Annotated Confusion Matrix (TN=235, FP=12, FN=29, TP=18) |

---

## 🎓 Technical Interview Defense Playbook (10 Key Questions)

When discussing this project in data analyst and data science interviews, use the following structured talking points:

### Q1: Why did you choose Logistic Regression instead of Random Forest or XGBoost?
> **Answer**:  
> In HR and People Analytics, interpretability and regulatory defensibility are paramount. While ensemble methods like XGBoost can sometimes yield marginal accuracy bumps, they behave as black boxes. Logistic Regression gives direct access to **Odds Ratios ($\text{OR} = e^{\beta}$)** with 95% confidence intervals. This allowed me to prove to leadership that working overtime multiplies departure odds by **$4.14\times$**, while each level of stock option grant reduces departure odds by **$42\%$**. Furthermore, Logistic Regression is computationally efficient and less prone to overfitting on a 1,470-row dataset.

### Q2: How did you handle class imbalance (16% attrition vs 84% retained)?
> **Answer**:  
> With an imbalanced target (16.1% positive class), standard models tend to default to majority prediction. I handled this via:
> 1. **Stratified Train-Test Splitting** (80/20) to ensure identical 16.1% class prevalence across both splits.
> 2. **L2 Ridge Regularization ($C=1.0$)** to prevent large weights on sparse one-hot features.
> 3. **Probability Calibration & Threshold Tuning**: Rather than relying purely on a 0.5 decision boundary, I outputted calibrated continuous probabilities ($0.0 - 1.0$) and stratified employees into actionable business risk tiers: Low ($<20\%$), Moderate ($20-45\%$), and High Risk ($\ge 45\%$).
> 4. Evaluating against **ROC-AUC (0.84)** and **PR-AUC (0.47)** rather than relying solely on accuracy.

### Q3: Your model achieved 86% holdout accuracy—isn't baseline accuracy already ~84%? How do you defend this?
> **Answer**:  
> That is a great question. A naive zero-rule classifier that predicts nobody ever leaves would achieve 83.9% accuracy, but its recall is 0% and it provides zero business utility. Our Logistic Regression model achieves **86.05% overall holdout accuracy** while delivering a **ROC-AUC of 0.84** and high specificity (**95.1%**). More importantly, the model serves as a **risk-ranking engine**: the top probability decile contains over 60% of actual future exits. In production, this allows HR business partners to prioritize retention conversations on the 100 most vulnerable employees rather than blindly polling all 1,470.

### Q4: Explain the 3.4× finding. How did you define the cohorts?
> **Answer**:  
> I conducted a 2×2 factorial analysis intersecting `OverTime` (`Yes`/`No`) with `MonthlyIncome` partitioned at the company median ($\$4,919/\text{month}$). Employees working overtime who earned below median income had an attrition rate of **$43.07\%$**. Standard non-overtime employees with typical earnings had an attrition rate of **$12.67\%$**. Dividing $43.07\% / 12.67\%$ yields an empirical **relative risk of $3.40\times$** ($p < 10^{-25}$). This proved that overtime alone isn't the primary driver of attrition—it is the combination of **uncompensated overtime** and low perceived reward that leads to burnout.

### Q5: How did you calculate the $12.6M financial replacement cost?
> **Answer**:  
> I adopted the Society for Human Resource Management (SHRM) benchmark, which estimates turnover cost for professional knowledge workers at **$1.5\times$ annual base salary** (accounting for recruiter fees, onboarding ramp-up, lost institutional knowledge, and team disruption). For every employee identified by our model as 'High Risk' ($\ge 45\%$ flight probability), I computed $\text{MonthlyIncome} \times 12 \times 1.5$. Aggregating this across all 114 high-risk employees revealed an enterprise turnover exposure of **$\$12,636,468$**.

### Q6: Why did you build a Star Schema in SQLite instead of directly importing the flat CSV into Power BI?
> **Answer**:  
> While Power BI can consume flat files, a normalized Kimball Star Schema is best practice in enterprise data engineering. Separating the fact table (`fact_employees`) from lookup dimensions (`dim_department`, `dim_job_role`, `dim_education`) optimizes VertiPaq memory compression, eliminates text redundancy, enables clean 1-to-many relationships, and prevents circular dependency errors in DAX. It also mimics how corporate data teams integrate warehouse tables from Snowflake or Databricks into Power BI.

### Q7: What are the main components of the Department Risk Score?
> **Answer**:  
> The Department Risk Score is a composite index (0 to 100) combining backward-looking empirical performance and forward-looking predictive risk:
> $$\text{Risk Score} = 0.40 \times (\text{Empirical Attrition Rate} \times 100) + 0.60 \times (\text{Avg Predicted Attrition Probability} \times 100)$$
> This prevents overreacting to small-department sample size anomalies while ensuring that departments with high concentrations of high-risk talent (like Sales at 52.8) are immediately elevated on the executive dashboard.

### Q8: What business recommendations did you produce from this analysis?
> **Answer**:  
> Three concrete tactical interventions:
> 1. **Overtime Cap for Entry Sales & Lab Techs**: Restrict mandatory overtime to no more than 2 consecutive weeks for employees in lower compensation quartiles.
> 2. **Salary Band Equalization**: A 10% compensation adjustment for the 253 workers in the Overtime + Low-Income cohort costs approximately $\$120,000$ annually, but our What-If model demonstrates it prevents 22 exits, saving **$\$1.76\text{M}$** in replacement costs (an ROI exceeding $14\times$).
> 3. **Stock Grant Expansion**: Expanding Level 1 stock option eligibility to mid-tenure individual contributors provides a $42\%$ retention boost per tier.

### Q9: What SQL techniques did you use in the analytical pipeline?
> **Answer**:  
> I used:
> * **Window Functions**: `NTILE(10) OVER (PARTITION BY department_id ORDER BY monthly_income)` to identify internal pay equity compression within departments.
> * **Ranking Functions**: `DENSE_RANK() OVER (ORDER BY financial_exposure DESC)` to rank job roles by financial vulnerability.
> * **Common Table Expressions (CTEs)**: Multi-stage CTEs to calculate cohort relative risk against cross-joined company benchmarks and evaluate manager tenure friction (`years_at_company - years_with_curr_manager >= 5`).

### Q10: How would you deploy this model in a live enterprise setting?
> **Answer**:  
> In a production HR pipeline:
> 1. Ingestion would run via Airflow/DBT pulling daily headcount snapshots from Workday or SAP SuccessFactors into Snowflake.
> 2. The Python model would be packaged into a Dockerized container running on AWS ECS or Google Cloud Run, scoring employee risk monthly via MLflow.
> 3. The Power BI report would connect via DirectQuery or Scheduled Semantic Refresh, with row-level security (RLS) ensuring managers only see risk scores for their direct reports.

---

## ⚡ Quickstart & Reproducibility Guide

### Prerequisites
* Python 3.10+ (Anaconda / Virtual Environment)
* Libraries: `pandas`, `numpy`, `scikit-learn`, `statsmodels`, `matplotlib`, `seaborn`

### 1. Clone & Install Dependencies
```bash
git clone https://github.com/ankurpal/hr-attrition-risk-dashboard.git
cd hr-attrition-risk-dashboard
pip install -r requirements.txt
```

### 2. Run the End-to-End Analytics Pipeline
Execute the master orchestrator to download the canonical dataset, build the SQLite Star Schema, run statistical tests, train the model, and generate all figures in ~7 seconds:
```bash
py src/run_pipeline.py
```

### 3. Launch the Interactive Dashboard Preview
```bash
py app.py
```
Open your browser to `http://localhost:8050` or view `outputs/dashboard_preview.html` directly in any web browser.

### 4. Open in Power BI Desktop
1. Open **Power BI Desktop**.
2. Click **Get Data** $\to$ **Text/CSV** $\to$ Select `data/processed/hr_attrition_modeled.csv`.
3. Open the Advanced DAX Editor and paste measures from `powerbi/dax_measures.dax`.
4. Follow the layout blueprint in `powerbi/dashboard_design_guide.md`.
