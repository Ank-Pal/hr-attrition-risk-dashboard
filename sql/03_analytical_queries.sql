-- ==============================================================================
-- HR ATTRITION RISK ANALYTICS - ENTERPRISE ANALYTICAL SQL SUITE
-- Dialect: SQLite / ANSI SQL (Compatible with PostgreSQL, Snowflake, SQL Server)
-- ==============================================================================

-- ------------------------------------------------------------------------------
-- QUERY 1: DEPARTMENT-LEVEL ATTRITION RISK & REPLACEMENT COST EXPOSURE
-- Surfaces department headcount, attrition counts, empirical attrition rates,
-- average predicted attrition probabilities, high-risk counts, and financial turnover risk.
-- ------------------------------------------------------------------------------
SELECT 
    d.department_name,
    COUNT(f.employee_id) AS total_headcount,
    SUM(CASE WHEN f.attrition_flag = 1 THEN 1 ELSE 0 END) AS attrition_headcount,
    ROUND(AVG(f.attrition_flag) * 100, 2) AS empirical_attrition_rate_pct,
    ROUND(AVG(f.attrition_probability) * 100, 2) AS avg_predicted_risk_pct,
    SUM(CASE WHEN f.predicted_risk_tier = 'High Risk' THEN 1 ELSE 0 END) AS high_risk_headcount,
    ROUND(
        SUM(CASE WHEN f.predicted_risk_tier = 'High Risk' THEN f.estimated_replacement_cost ELSE 0 END), 2
    ) AS high_risk_turnover_exposure_usd
FROM fact_employees f
JOIN dim_department d ON f.department_id = d.department_id
GROUP BY d.department_name
ORDER BY empirical_attrition_rate_pct DESC;


-- ------------------------------------------------------------------------------
-- QUERY 2: THE 3.4X COHORT DEEP DIVE (OVERTIME + BELOW-MEDIAN INCOME)
-- Analyzes the 4 distinct employee cohorts formed by OverTime and Income Median
-- Demonstrates the empirical risk spike of 43.1% vs peer baseline.
-- ------------------------------------------------------------------------------
WITH cohort_summary AS (
    SELECT 
        CASE 
            WHEN f.overtime_flag = 1 AND f.below_median_income_flag = 1 THEN 'Cohort A: Overtime + Below-Median Income (High Risk)'
            WHEN f.overtime_flag = 1 AND f.below_median_income_flag = 0 THEN 'Cohort B: Overtime + Above-Median Income'
            WHEN f.overtime_flag = 0 AND f.below_median_income_flag = 1 THEN 'Cohort C: Standard Hours + Below-Median Income'
            ELSE 'Cohort D: Standard Hours + Above-Median Income (Baseline Anchor)'
        END AS employee_cohort,
        COUNT(f.employee_id) AS cohort_size,
        SUM(f.attrition_flag) AS attrition_count,
        ROUND(AVG(f.attrition_flag) * 100, 2) AS cohort_attrition_rate_pct,
        ROUND(AVG(f.monthly_income), 2) AS avg_monthly_income,
        ROUND(AVG(f.job_satisfaction), 2) AS avg_job_satisfaction,
        ROUND(AVG(f.work_life_balance), 2) AS avg_work_life_balance
    FROM fact_employees f
    GROUP BY 
        f.overtime_flag,
        f.below_median_income_flag
),
baseline_ref AS (
    SELECT AVG(attrition_flag) * 100 AS overall_company_baseline
    FROM fact_employees
)
SELECT 
    c.employee_cohort,
    c.cohort_size,
    c.attrition_count,
    c.cohort_attrition_rate_pct,
    ROUND(c.cohort_attrition_rate_pct / b.overall_company_baseline, 2) AS relative_risk_vs_company_avg,
    c.avg_monthly_income,
    c.avg_job_satisfaction,
    c.avg_work_life_balance
FROM cohort_summary c
CROSS JOIN baseline_ref b
ORDER BY c.cohort_attrition_rate_pct DESC;


-- ------------------------------------------------------------------------------
-- QUERY 3: SALARY DECILES WITHIN DEPARTMENT USING NTILE(10)
-- Evaluates whether lower salary deciles within each department experience
-- disproportionate attrition and whether compression causes churn.
-- ------------------------------------------------------------------------------
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
    ROUND(MIN(monthly_income), 0) AS min_income,
    ROUND(MAX(monthly_income), 0) AS max_income,
    ROUND(AVG(monthly_income), 0) AS avg_income,
    SUM(attrition_flag) AS attrition_count,
    ROUND(AVG(attrition_flag) * 100, 2) AS attrition_rate_pct,
    ROUND(AVG(overtime_flag) * 100, 2) AS overtime_pct
FROM ranked_salary
GROUP BY department_name, salary_decile
HAVING salary_decile IN (1, 2, 5, 9, 10) -- Display lower deciles, median, and upper deciles
ORDER BY department_name, salary_decile;


-- ------------------------------------------------------------------------------
-- QUERY 4: MANAGER TENURE FRICTION ANALYSIS (TENURE INVERSION)
-- Identifies employees who have been with the company longer than their manager
-- has been managing them, measuring if lack of managerial continuity drives attrition.
-- ------------------------------------------------------------------------------
SELECT 
    d.department_name,
    CASE 
        WHEN f.years_with_curr_manager = 0 THEN 'New Manager (< 1 Year)'
        WHEN f.years_at_company - f.years_with_curr_manager >= 5 THEN 'Tenure Inversion (Tenure exceeds Manager by >= 5 yrs)'
        ELSE 'Balanced Tenure Alignment'
    END AS manager_relationship_segment,
    COUNT(f.employee_id) AS employee_count,
    SUM(f.attrition_flag) AS attrition_count,
    ROUND(AVG(f.attrition_flag) * 100, 2) AS attrition_rate_pct,
    ROUND(AVG(f.relationship_satisfaction), 2) AS avg_relationship_satisfaction,
    ROUND(AVG(f.years_since_last_promotion), 2) AS avg_years_since_promotion
FROM fact_employees f
JOIN dim_department d ON f.department_id = d.department_id
GROUP BY 
    d.department_name,
    manager_relationship_segment
ORDER BY 
    d.department_name,
    attrition_rate_pct DESC;


-- ------------------------------------------------------------------------------
-- QUERY 5: HIGH-RISK FLIGHT ROSTER WITH RETENTION EXPOSURE
-- Identifies currently active employees categorized as 'High Risk' (> 55% prob)
-- sorted by estimated financial replacement cost to guide proactive HR intervention.
-- ------------------------------------------------------------------------------
SELECT 
    f.employee_id,
    d.department_name,
    j.job_role_name,
    f.age,
    f.monthly_income,
    f.overtime,
    f.years_at_company,
    ROUND(f.attrition_probability * 100, 1) AS attrition_probability_pct,
    f.flight_risk_score,
    f.job_satisfaction,
    f.work_life_balance,
    ROUND(f.estimated_replacement_cost, 0) AS estimated_replacement_cost_usd
FROM fact_employees f
JOIN dim_department d ON f.department_id = d.department_id
JOIN dim_job_role j ON f.job_role_id = j.job_role_id
WHERE f.predicted_risk_tier = 'High Risk'
ORDER BY f.attrition_probability DESC, f.estimated_replacement_cost DESC
LIMIT 15;


-- ------------------------------------------------------------------------------
-- QUERY 6: JOB ROLE VULNERABILITY RANKING WITH DENSE_RANK()
-- Ranks roles across the enterprise by flight risk and replacement cost impact.
-- ------------------------------------------------------------------------------
WITH role_stats AS (
    SELECT 
        j.job_role_name,
        d.department_name,
        COUNT(f.employee_id) AS total_employees,
        SUM(f.attrition_flag) AS total_attrition,
        ROUND(AVG(f.attrition_flag) * 100, 2) AS attrition_rate_pct,
        ROUND(AVG(f.attrition_probability) * 100, 2) AS avg_model_risk_pct,
        SUM(CASE WHEN f.predicted_risk_tier = 'High Risk' THEN 1 ELSE 0 END) AS high_risk_count,
        ROUND(SUM(CASE WHEN f.predicted_risk_tier = 'High Risk' THEN f.estimated_replacement_cost ELSE 0 END), 0) AS total_risk_exposure_usd
    FROM fact_employees f
    JOIN dim_job_role j ON f.job_role_id = j.job_role_id
    JOIN dim_department d ON f.department_id = d.department_id
    GROUP BY j.job_role_name, d.department_name
)
SELECT 
    job_role_name,
    department_name,
    total_employees,
    total_attrition,
    attrition_rate_pct,
    avg_model_risk_pct,
    high_risk_count,
    total_risk_exposure_usd,
    DENSE_RANK() OVER (ORDER BY attrition_rate_pct DESC) AS attrition_rate_rank,
    DENSE_RANK() OVER (ORDER BY total_risk_exposure_usd DESC) AS financial_exposure_rank
FROM role_stats
ORDER BY attrition_rate_rank ASC;
