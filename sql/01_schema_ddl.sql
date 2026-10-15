-- ==============================================================================
-- HR ATTRITION RISK ANALYTICS DATA WAREHOUSE - STAR SCHEMA DDL
-- Database Dialect: SQLite 3 / ANSI SQL-92 Compliant
-- Design Pattern: Kimball Dimensional Model (Star Schema)
-- ==============================================================================

PRAGMA foreign_keys = ON;

-- ------------------------------------------------------------------------------
-- 1. DIMENSION TABLE: dim_department
-- ------------------------------------------------------------------------------
DROP TABLE IF EXISTS fact_employees;
DROP TABLE IF EXISTS dim_department;
DROP TABLE IF EXISTS dim_job_role;
DROP TABLE IF EXISTS dim_education;
DROP TABLE IF EXISTS dim_satisfaction_scale;

CREATE TABLE dim_department (
    department_id       INTEGER PRIMARY KEY AUTOINCREMENT,
    department_name     TEXT NOT NULL UNIQUE,
    cost_center_code    TEXT NOT NULL,
    division_head       TEXT DEFAULT 'Executive Leadership',
    created_at          TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ------------------------------------------------------------------------------
-- 2. DIMENSION TABLE: dim_job_role
-- ------------------------------------------------------------------------------
CREATE TABLE dim_job_role (
    job_role_id         INTEGER PRIMARY KEY AUTOINCREMENT,
    job_role_name       TEXT NOT NULL UNIQUE,
    department_name     TEXT NOT NULL,
    career_track        TEXT NOT NULL,
    standard_min_salary REAL NOT NULL,
    standard_max_salary REAL NOT NULL,
    created_at          TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ------------------------------------------------------------------------------
-- 3. DIMENSION TABLE: dim_education
-- ------------------------------------------------------------------------------
CREATE TABLE dim_education (
    education_id        INTEGER PRIMARY KEY AUTOINCREMENT,
    education_level     INTEGER NOT NULL,
    education_level_desc TEXT NOT NULL,
    education_field     TEXT NOT NULL,
    qualification_rank  INTEGER NOT NULL,
    UNIQUE(education_level, education_field)
);

-- ------------------------------------------------------------------------------
-- 4. DIMENSION TABLE: dim_satisfaction_scale
-- ------------------------------------------------------------------------------
CREATE TABLE dim_satisfaction_scale (
    rating_id           INTEGER PRIMARY KEY,
    rating_label        TEXT NOT NULL,
    sentiment_band      TEXT NOT NULL,
    risk_weight         REAL NOT NULL
);

-- ------------------------------------------------------------------------------
-- 5. FACT TABLE: fact_employees
-- Granularity: 1 row per employee
-- ------------------------------------------------------------------------------
CREATE TABLE fact_employees (
    employee_id                     INTEGER PRIMARY KEY,
    age                             INTEGER NOT NULL,
    gender                          TEXT NOT NULL,
    marital_status                  TEXT NOT NULL,
    business_travel                 TEXT NOT NULL,
    distance_from_home              INTEGER NOT NULL,
    
    -- Dimensional Foreign Keys
    department_id                   INTEGER NOT NULL REFERENCES dim_department(department_id),
    job_role_id                     INTEGER NOT NULL REFERENCES dim_job_role(job_role_id),
    education_id                    INTEGER NOT NULL REFERENCES dim_education(education_id),
    
    -- Organizational & Compensation Metrics
    job_level                       INTEGER NOT NULL,
    daily_rate                      REAL NOT NULL,
    hourly_rate                     REAL NOT NULL,
    monthly_income                  REAL NOT NULL,
    monthly_rate                    REAL NOT NULL,
    percent_salary_hike             REAL NOT NULL,
    stock_option_level              INTEGER NOT NULL,
    overtime                        TEXT NOT NULL CHECK(overtime IN ('Yes', 'No')),
    
    -- Experience & Tenure
    total_working_years             INTEGER NOT NULL,
    training_times_last_year        INTEGER NOT NULL,
    years_at_company                INTEGER NOT NULL,
    years_in_current_role           INTEGER NOT NULL,
    years_since_last_promotion      INTEGER NOT NULL,
    years_with_curr_manager         INTEGER NOT NULL,
    num_companies_worked            INTEGER NOT NULL,
    
    -- Survey & Engagement Metrics (1-4 scale)
    environment_satisfaction        INTEGER NOT NULL CHECK(environment_satisfaction BETWEEN 1 AND 4),
    job_involvement                 INTEGER NOT NULL CHECK(job_involvement BETWEEN 1 AND 4),
    job_satisfaction                INTEGER NOT NULL CHECK(job_satisfaction BETWEEN 1 AND 4),
    relationship_satisfaction       INTEGER NOT NULL CHECK(relationship_satisfaction BETWEEN 1 AND 4),
    work_life_balance               INTEGER NOT NULL CHECK(work_life_balance BETWEEN 1 AND 4),
    performance_rating              INTEGER NOT NULL CHECK(performance_rating IN (3, 4)),
    
    -- Target & Analytical Attributes
    attrition                       TEXT NOT NULL CHECK(attrition IN ('Yes', 'No')),
    attrition_flag                  INTEGER NOT NULL CHECK(attrition_flag IN (0, 1)),
    below_median_income_flag        INTEGER NOT NULL CHECK(below_median_income_flag IN (0, 1)),
    overtime_flag                   INTEGER NOT NULL CHECK(overtime_flag IN (0, 1)),
    overtime_low_income_cohort      INTEGER NOT NULL CHECK(overtime_low_income_cohort IN (0, 1)),
    
    -- Machine Learning Predictive Outputs
    attrition_probability           REAL NOT NULL CHECK(attrition_probability BETWEEN 0.0 AND 1.0),
    predicted_risk_tier             TEXT NOT NULL CHECK(predicted_risk_tier IN ('Low Risk', 'Moderate Risk', 'High Risk')),
    flight_risk_score               REAL NOT NULL CHECK(flight_risk_score BETWEEN 0.0 AND 100.0),
    estimated_replacement_cost      REAL NOT NULL
);

-- ------------------------------------------------------------------------------
-- PERFORMANCE INDEXES
-- ------------------------------------------------------------------------------
CREATE INDEX idx_fact_dept ON fact_employees(department_id);
CREATE INDEX idx_fact_job_role ON fact_employees(job_role_id);
CREATE INDEX idx_fact_attrition ON fact_employees(attrition_flag);
CREATE INDEX idx_fact_cohort ON fact_employees(overtime_low_income_cohort);
CREATE INDEX idx_fact_risk_tier ON fact_employees(predicted_risk_tier);
CREATE INDEX idx_fact_income ON fact_employees(monthly_income);
