# 📊 Power BI Dashboard Visual Blueprint & Design Guide

## 1. Canvas Setup & Design System
* **Canvas Format**: 16:9 Widescreen (1920 × 1080 px or 1280 × 720 px).
* **Color System**:
  * **Critical / Flight Risk**: `#E11D48` (Crimson Rose)
  * **Elevated / Warning**: `#F59E0B` (Amber)
  * **Healthy / Low Risk**: `#10B981` (Emerald Teal)
  * **Primary Neutral**: `#0F172A` (Navy Slate)
  * **Card Container Background**: `#FFFFFF` with `#E2E8F0` border and subtle drop-shadow.
  * **Report Canvas Background**: `#F8FAFC` (Off-White).
* **Typography**:
  * Title: Segoe UI Semibold (20pt)
  * Metric Value (KPI): Segoe UI Bold (28pt)
  * Metric Subtitle / Delta: Segoe UI Regular (10pt)
  * Table & Data Labels: Segoe UI Regular (10pt)

---

## 2. Multi-Page Report Architecture

```
┌────────────────────────────────────────────────────────────────────────┐
│  PAGE 1: C-Suite Executive Flight Risk & Attrition Cockpit             │
│  High-level enterprise overview, total financial risk, macro KPIs      │
├────────────────────────────────────────────────────────────────────────┤
│  PAGE 2: Department Vulnerability & Role Risk Matrix                   │
│  Cross-departmental drilldown, risk index scores, role ranking         │
├────────────────────────────────────────────────────────────────────────┤
│  PAGE 3: The Overtime & Compensation Cohort Deep Dive (3.4x Focus)    │
│  Empirical breakdown of the 3.4x attrition spike & What-If simulator   │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Page 1: Executive Flight Risk & Attrition Cockpit

### Header & Slicer Bar (Top Band: 0 to 110 px)
* **Title**: `Enterprise HR Flight Risk & Attrition Intelligence`
* **Subtitle**: `Predictive Retention Analytics · 1,470 Employees Modeled · Scikit-Learn Logistic Regression (86% Holdout Accuracy)`
* **Global Filters (Dropdown Slicers)**:
  1. Department (`dim_department[department_name]`)
  2. Job Role (`dim_job_role[job_role_name]`)
  3. Risk Tier (`fact_employees[predicted_risk_tier]`)

### Top Metric KPI Cards (120 to 240 px)
| Visual Type | KPI Name | DAX Measure | Formatting | Benchmark / Sub-label |
| :--- | :--- | :--- | :--- | :--- |
| **KPI Card 1** | Total Headcount | `[Total Headcount]` | `#,##0` | Active: `[Active Headcount]` |
| **KPI Card 2** | Overall Attrition Rate | `[Attrition Rate %]` | `0.0%` | Baseline: 16.1% (Company Benchmark) |
| **KPI Card 3** | High-Risk Flight Headcount | `[High Risk Headcount]` | `#,##0` | `[High Risk Proportion %]` of workforce |
| **KPI Card 4** | High-Risk Financial Exposure | `[High Risk Replacement Exposure $]` | `$#,##0` | Replacement Cost @ 1.5x Base |
| **KPI Card 5** | OverTime Cohort Multiplier | `[Cohort Risk Multiplier]` | `0.0x` | OverTime + Low Income: **3.4x Risk** |

### Visual Layout (260 to 700 px)
1. **Visual 1 (Donut Chart - Left)**:
   * **Title**: `Workforce Distribution by Predicted Risk Tier`
   * **Legend**: `fact_employees[predicted_risk_tier]` (`Low Risk`, `Moderate Risk`, `High Risk`)
   * **Values**: `[Total Headcount]`
   * **Colors**: Green (`#10B981`), Amber (`#F59E0B`), Crimson (`#E11D48`).
2. **Visual 2 (Clustered Column Chart - Center)**:
   * **Title**: `Empirical Attrition Rate vs Predicted Model Risk by Department`
   * **X-Axis**: `dim_department[department_name]`
   * **Y-Axis**: `[Attrition Rate %]`, `[Avg Attrition Probability %]`
   * **Reference Line**: Constant line at `16.12%` (`[Company Baseline Attrition Rate %]`).
3. **Visual 3 (Top Flight-Risk Employee Roster - Right Table)**:
   * **Title**: `Priority Flight-Risk Retention Candidates`
   * **Columns**: `Employee ID`, `Job Role`, `Monthly Income`, `OverTime`, `Risk Score`, `Replacement Exposure ($)`.
   * **Filter**: Top 10 sorted by `[Avg Flight Risk Score]` descending.

---

## 4. Page 2: Department Vulnerability & Role Risk Matrix

### Top Row: Department Risk Score Cards
* Visualizing the composite risk score for each department:
  * **Sales**: `Risk Score: 52.8` (Elevated Attrition: 20.6%, High Exposure: $4.1M)
  * **Research & Development**: `Risk Score: 41.2` (Empirical Attrition: 13.8%, High Exposure: $7.9M)
  * **Human Resources**: `Risk Score: 49.6` (Empirical Attrition: 19.0%, High Exposure: $612K)

### Visual Layout
1. **Visual 1 (Matrix Visual with Conditional Formatting)**:
   * **Rows**: `dim_department[department_name]` $\to$ `dim_job_role[job_role_name]`
   * **Values**:
     * Headcount (`[Total Headcount]`)
     * Empirical Attrition Rate (`[Attrition Rate %]`)
     * High Risk Count (`[High Risk Headcount]`)
     * Financial Exposure (`[High Risk Replacement Exposure $]`)
   * **Conditional Formatting**: Background color gradient on `[Attrition Rate %]` (Light Yellow to Dark Red).
2. **Visual 2 (Scatter Plot - Turnover Exposure vs Vulnerability)**:
   * **X-Axis**: `[Attrition Rate %]`
   * **Y-Axis**: `[High Risk Replacement Exposure $]`
   * **Bubble Size**: `[Total Headcount]`
   * **Details**: `dim_job_role[job_role_name]`
   * **Quadrants**: Identifies high-cost / high-attrition roles (e.g. Sales Executive & Research Scientist).

---

## 5. Page 3: The Overtime & Compensation Cohort Deep Dive (3.4× Disparity)

### Highlight Focus: The Empirical 3.4× Finding
* **Header Callout**:
  > *"Employees working Overtime while earning below median monthly income ($4,919) suffer an empirical attrition rate of **43.1%**, which is **3.4× the baseline attrition rate** of standard peers."*

### Visual Layout
1. **Visual 1 (4-Quadrant Cohort Bar Chart)**:
   * **Y-Axis**: 4 Employee Segments:
     1. OverTime + Below-Median Income (43.1%)
     2. OverTime + Above-Median Income (24.7%)
     3. Standard Hours + Below-Median Income (12.7%)
     4. Standard Hours + Above-Median Income (7.1%)
   * **X-Axis**: `[Attrition Rate %]`
   * **Data Label Callout**: `3.4x Risk Multiplier` on Cohort 1.
2. **Visual 2 (Interactive What-If Retention Simulator)**:
   * **Slicers (What-If Parameters)**:
     * OverTime Capping Slider: `[WhatIf OverTime Reduction Pct]` (0% to 50%)
     * Compensation Rebalancing Slider: `[WhatIf Salary Correction Pct]` (0% to 30%)
   * **Dynamic Return Cards**:
     * Projected Attrition Prevented: `[Simulated Attrition Prevention Headcount]`
     * Projected Replacement Cost Savings: `[Simulated Cost Savings ROI $]`
3. **Visual 3 (Tenure Friction / Manager Gap)**:
   * Evaluates the interaction between OverTime and Manager tenure friction (`years_with_curr_manager == 0`).
