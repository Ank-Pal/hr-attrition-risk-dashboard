# 🏛️ Enterprise Power BI Data Model Architecture

## 1. Architectural Philosophy & Dimensional Modeling
This solution implements a formal **Kimball Star Schema** to model employee attrition dynamics, machine learning flight-risk probabilities, and organizational hierarchy.

Rather than relying on a denormalized single flat table, a Star Schema guarantees:
* **Optimal VertiPaq Compression**: Numerical dimension keys compress significantly better than redundant wide text strings.
* **Filter Integrity & Deterministic Measure Evaluation**: Eliminates bidirectional filtering ambiguity and circular dependencies.
* **Sub-Second Report Performance**: Efficient 1-to-many (`1:*`) relationships with single cross-filter direction.

---

## 2. Conceptual & Logical Data Model Diagram

```
       ┌────────────────────────┐
       │     dim_department     │
       ├────────────────────────┤
       │ PK: department_id      │
       │     department_name    │
       │     cost_center_code   │
       │     division_head      │
       └───────────┬────────────┘
                   │ 1
                   │
                   │ *
┌──────────────────┴──────────────────┐          ┌───────────────────────────┐
│           fact_employees            │          │       dim_job_role        │
├─────────────────────────────────────┤ 1      * ├───────────────────────────┤
│ PK: employee_id                     ├──────────┤ PK: job_role_id           │
│ FK: department_id                   │          │     job_role_name         │
│ FK: job_role_id                     │          │     department_name       │
│ FK: education_id                    │          │     career_track          │
│                                     │          │     standard_min_salary   │
│ -- Metrics & Compensation           │          │     standard_max_salary   │
│     monthly_income                  │          └───────────────────────────┘
│     hourly_rate                     │
│     percent_salary_hike             │
│     stock_option_level              │
│                                     │          ┌───────────────────────────┐
│ -- Tenure & Surveys                 │          │       dim_education       │
│     years_at_company                │ 1      * ├───────────────────────────┤
│     years_with_curr_manager         │──────────┤ PK: education_id          │
│     job_satisfaction                │          │     education_level       │
│     work_life_balance               │          │     education_level_desc  │
│                                     │          │     education_field       │
│ -- Attrition & ML Predictions       │          │     qualification_rank    │
│     attrition (Yes / No)            │          └───────────────────────────┘
│     attrition_flag (1 / 0)          │
│     attrition_probability (0.0-1.0) │          ┌───────────────────────────┐
│     predicted_risk_tier             │          │   dim_satisfaction_scale  │
│     flight_risk_score (0-100)       │ 1      * ├───────────────────────────┤
│     estimated_replacement_cost      │──────────┤ PK: rating_id             │
│     overtime_low_income_cohort      │          │     rating_label          │
└─────────────────────────────────────┘          │     sentiment_band        │
                                                 │     risk_weight           │
                                                 └───────────────────────────┘
```

---

## 3. Detailed Entity Dictionary

### Fact Table: `fact_employees`
* **Granularity**: Exactly 1 record per employee ($N = 1,470$).
* **Primary Key**: `employee_id`
* **Foreign Keys**:
  * `department_id` $\to$ `dim_department.department_id`
  * `job_role_id` $\to$ `dim_job_role.job_role_id`
  * `education_id` $\to$ `dim_education.education_id`
* **Measures Stored**:
  * Numerical metrics: `monthly_income`, `years_at_company`, `job_satisfaction`, `work_life_balance`.
  * Machine Learning predictions: `attrition_probability` (continuous float $0.0 - 1.0$), `predicted_risk_tier` (`Low Risk`, `Moderate Risk`, `High Risk`), `flight_risk_score` ($0 - 100$).
  * Cohort Flags: `below_median_income_flag`, `overtime_flag`, `overtime_low_income_cohort` (flags the 3.4× risk cohort).
  * Financial Metric: `estimated_replacement_cost` (calculated at $1.5 \times \text{Annual Base Salary}$ per industry standards).

### Dimension Table: `dim_department`
* **Primary Key**: `department_id`
* **Attributes**: `department_name` (Sales, Research & Development, Human Resources), `cost_center_code`, `division_head`.
* **Cardinality**: 3 rows.

### Dimension Table: `dim_job_role`
* **Primary Key**: `job_role_id`
* **Attributes**: `job_role_name` (9 distinct organizational job roles), `department_name`, `career_track`, `standard_min_salary`, `standard_max_salary`.
* **Cardinality**: 9 rows.

### Dimension Table: `dim_education`
* **Primary Key**: `education_id`
* **Attributes**: `education_level` (1-5), `education_level_desc` (Below College, College, Bachelor, Master, Doctor), `education_field` (Life Sciences, Medical, Marketing, etc.), `qualification_rank`.
* **Cardinality**: 15 distinct combinations.

### Dimension Table: `dim_satisfaction_scale`
* **Primary Key**: `rating_id`
* **Attributes**: `rating_label` (Low, Medium, High, Very High), `sentiment_band`, `risk_weight`.

---

## 4. Modeling & Performance Rules in Power BI

1. **Relationship Configuration**:
   * Cardinality: `1-to-Many` (`1:*`), where `1` is on Dimension tables and `*` is on `fact_employees`.
   * Cross-Filter Direction: **Single** (Dimensions filter the Fact table). Bidirectional filtering is strictly deactivated to prevent performance degradation and circular lineage.
2. **Key Hiding**:
   * All surrogate keys (`department_id`, `job_role_id`, `education_id`) are set to **Hidden in Report View** in the Fact table. Report authors build visuals and slicers exclusively from Dimension attributes.
3. **Data Types & Categorization**:
   * `monthly_income` & `estimated_replacement_cost` formatted as Currency (`$#,##0`).
   * `attrition_probability` formatted as Percentage (`0.0%`).
   * `flight_risk_score` formatted as Decimal (`0.0`).
4. **Calculated Columns Policy**:
   * Zero calculated columns added in Power BI. All modeling attributes (`overtime_low_income_cohort`, `predicted_risk_tier`) were precomputed in the Python data pipeline / SQLite ETL to minimize VertiPaq RAM footprint.
