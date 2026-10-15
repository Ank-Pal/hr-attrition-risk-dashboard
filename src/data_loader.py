"""
==============================================================================
Module: src/data_loader.py
Description: Ingestion, schema validation, and SQLite Data Warehouse loader
             for the IBM HR Analytics Employee Attrition dataset.
==============================================================================
"""

import os
import sys
import sqlite3
import urllib.request
import pandas as pd
import numpy as np

# Primary and fallback sources for canonical IBM HR dataset (1,470 rows, 35 columns)
DATA_URLS = [
    "https://raw.githubusercontent.com/nelson-wu/employee-attrition-ml/master/WA_Fn-UseC_-HR-Employee-Attrition.csv",
    "https://raw.githubusercontent.com/Ansu-John/IBM-HR-Analytics-Employee-Attrition/main/WA_Fn-UseC_-HR-Employee-Attrition.csv",
    "https://raw.githubusercontent.com/juliaobenauer/Employee-attrition-prediction/main/WA_Fn-UseC_-HR-Employee-Attrition.csv"
]

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
RAW_DATA_PATH = os.path.join(PROJECT_ROOT, "data", "raw", "WA_Fn-UseC_-HR-Employee-Attrition.csv")
DB_PATH = os.path.join(PROJECT_ROOT, "data", "processed", "hr_analytics.db")
SCHEMA_SQL_PATH = os.path.join(PROJECT_ROOT, "sql", "01_schema_ddl.sql")
ETL_SQL_PATH = os.path.join(PROJECT_ROOT, "sql", "02_data_warehouse_etl.sql")


def download_raw_dataset(dest_path=RAW_DATA_PATH):
    """Downloads the canonical IBM HR Analytics dataset if not present locally."""
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    if os.path.exists(dest_path) and os.path.getsize(dest_path) > 10000:
        print(f"[DATA LOADER] Raw dataset exists at: {dest_path}")
        return dest_path

    print("[DATA LOADER] Fetching canonical IBM HR dataset from verified repository...")
    for url in DATA_URLS:
        try:
            print(f"  Attempting: {url} ...")
            urllib.request.urlretrieve(url, dest_path)
            if os.path.exists(dest_path) and os.path.getsize(dest_path) > 10000:
                print(f"  Successfully downloaded ({os.path.getsize(dest_path):,} bytes).")
                return dest_path
        except Exception as e:
            print(f"  Download failed from {url}: {e}")

    raise RuntimeError("Failed to download IBM HR dataset from all remote URLs.")


def load_and_validate_data(csv_path=RAW_DATA_PATH):
    """Loads and runs schema validation on the IBM HR dataset."""
    if not os.path.exists(csv_path):
        download_raw_dataset(csv_path)

    df = pd.read_csv(csv_path)
    print(f"[DATA LOADER] Loaded raw dataset: {df.shape[0]} rows, {df.shape[1]} columns.")

    # Validation Checks
    expected_cols = [
        "Age", "Attrition", "BusinessTravel", "DailyRate", "Department",
        "DistanceFromHome", "Education", "EducationField", "EnvironmentSatisfaction",
        "Gender", "HourlyRate", "JobInvolvement", "JobLevel", "JobRole",
        "JobSatisfaction", "MaritalStatus", "MonthlyIncome", "MonthlyRate",
        "NumCompaniesWorked", "OverTime", "PercentSalaryHike", "PerformanceRating",
        "RelationshipSatisfaction", "StockOptionLevel", "TotalWorkingYears",
        "TrainingTimesLastYear", "WorkLifeBalance", "YearsAtCompany",
        "YearsInCurrentRole", "YearsSinceLastPromotion", "YearsWithCurrManager"
    ]
    for col in expected_cols:
        assert col in df.columns, f"Missing expected column: {col}"

    assert df.isnull().sum().sum() == 0, "Dataset contains unexpected missing values!"
    print("[DATA LOADER] Data validation passed: Zero missing values, all core features present.")
    return df


def enrich_analytical_features(df):
    """
    Enriches dataset with core analytical flags:
    - Attrition_Flag (1/0)
    - Below_Median_Income_Flag
    - OverTime_Flag
    - OverTime_Low_Income_Cohort (The 3.4x risk cohort)
    """
    df = df.copy()
    df["Attrition_Flag"] = (df["Attrition"] == "Yes").astype(int)
    median_income = df["MonthlyIncome"].median()
    df["Below_Median_Income_Flag"] = (df["MonthlyIncome"] < median_income).astype(int)
    df["OverTime_Flag"] = (df["OverTime"] == "Yes").astype(int)
    df["OverTime_Low_Income_Cohort"] = (
        (df["OverTime_Flag"] == 1) & (df["Below_Median_Income_Flag"] == 1)
    ).astype(int)
    
    # Financial replacement cost estimation: standard SHRM metric is 1.5x annual compensation
    df["Estimated_Replacement_Cost"] = df["MonthlyIncome"] * 12 * 1.5

    return df


def initialize_database(db_path=DB_PATH, schema_path=SCHEMA_SQL_PATH, etl_path=ETL_SQL_PATH):
    """Executes DDL and ETL scripts to initialize the SQLite Star Schema."""
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    print(f"[DATA LOADER] Initializing Star Schema in SQLite: {db_path}")
    with open(schema_path, "r", encoding="utf-8") as f:
        schema_sql = f.read()
    cursor.executescript(schema_sql)

    with open(etl_path, "r", encoding="utf-8") as f:
        etl_sql = f.read()
    cursor.executescript(etl_sql)

    conn.commit()
    conn.close()
    print("[DATA LOADER] Database schema initialized with dimension seed records.")


def populate_fact_table(df_modeled, db_path=DB_PATH):
    """
    Populates fact_employees with enriched features and model predictions.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Fetch dimension maps
    dept_map = dict(cursor.execute("SELECT department_name, department_id FROM dim_department").fetchall())
    role_map = dict(cursor.execute("SELECT job_role_name, job_role_id FROM dim_job_role").fetchall())

    # Build education lookup
    edu_tuples = cursor.execute("SELECT education_level, education_field, education_id FROM dim_education").fetchall()
    edu_map = {(row[0], row[1]): row[2] for row in edu_tuples}

    # Ensure education records exist for all combinations
    unique_edus = df_modeled[["Education", "EducationField"]].drop_duplicates()
    for _, r in unique_edus.iterrows():
        lvl, fld = int(r["Education"]), str(r["EducationField"])
        if (lvl, fld) not in edu_map:
            edu_desc_map = {1: "Below College", 2: "College", 3: "Bachelor", 4: "Master", 5: "Doctor"}
            desc = edu_desc_map.get(lvl, "Unknown")
            cursor.execute(
                "INSERT INTO dim_education (education_level, education_level_desc, education_field, qualification_rank) VALUES (?, ?, ?, ?)",
                (lvl, desc, fld, lvl)
            )
            edu_map[(lvl, fld)] = cursor.lastrowid
    conn.commit()

    # Clear and insert into fact_employees
    cursor.execute("DELETE FROM fact_employees;")

    insert_rows = []
    for idx, row in df_modeled.iterrows():
        emp_id = int(row.get("EmployeeNumber", idx + 1))
        dept_id = dept_map.get(row["Department"])
        role_id = role_map.get(row["JobRole"])
        edu_id = edu_map.get((int(row["Education"]), str(row["EducationField"])))

        prob = float(row.get("Attrition_Probability", 0.0))
        tier = str(row.get("Predicted_Risk_Tier", "Low Risk"))
        flight_score = round(prob * 100, 1)

        insert_rows.append((
            emp_id, int(row["Age"]), str(row["Gender"]), str(row["MaritalStatus"]),
            str(row["BusinessTravel"]), int(row["DistanceFromHome"]),
            dept_id, role_id, edu_id,
            int(row["JobLevel"]), float(row["DailyRate"]), float(row["HourlyRate"]),
            float(row["MonthlyIncome"]), float(row["MonthlyRate"]),
            float(row["PercentSalaryHike"]), int(row["StockOptionLevel"]),
            str(row["OverTime"]), int(row["TotalWorkingYears"]),
            int(row["TrainingTimesLastYear"]), int(row["YearsAtCompany"]),
            int(row["YearsInCurrentRole"]), int(row["YearsSinceLastPromotion"]),
            int(row["YearsWithCurrManager"]), int(row["NumCompaniesWorked"]),
            int(row["EnvironmentSatisfaction"]), int(row["JobInvolvement"]),
            int(row["JobSatisfaction"]), int(row["RelationshipSatisfaction"]),
            int(row["WorkLifeBalance"]), int(row["PerformanceRating"]),
            str(row["Attrition"]), int(row["Attrition_Flag"]),
            int(row["Below_Median_Income_Flag"]), int(row["OverTime_Flag"]),
            int(row["OverTime_Low_Income_Cohort"]),
            prob, tier, flight_score, float(row["Estimated_Replacement_Cost"])
        ))

    insert_sql = """
    INSERT INTO fact_employees (
        employee_id, age, gender, marital_status, business_travel, distance_from_home,
        department_id, job_role_id, education_id, job_level, daily_rate, hourly_rate,
        monthly_income, monthly_rate, percent_salary_hike, stock_option_level,
        overtime, total_working_years, training_times_last_year, years_at_company,
        years_in_current_role, years_since_last_promotion, years_with_curr_manager,
        num_companies_worked, environment_satisfaction, job_involvement, job_satisfaction,
        relationship_satisfaction, work_life_balance, performance_rating,
        attrition, attrition_flag, below_median_income_flag, overtime_flag,
        overtime_low_income_cohort, attrition_probability, predicted_risk_tier,
        flight_risk_score, estimated_replacement_cost
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    cursor.executemany(insert_sql, insert_rows)
    conn.commit()
    print(f"[DATA LOADER] Populated fact_employees with {len(insert_rows):,} records.")
    conn.close()


if __name__ == "__main__":
    download_raw_dataset()
    raw_df = load_and_validate_data()
    enriched_df = enrich_analytical_features(raw_df)
    initialize_database()
    print("[DATA LOADER] Ingestion pipeline test completed successfully.")
