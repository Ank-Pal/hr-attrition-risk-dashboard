"""
==============================================================================
Module: src/department_risk_engine.py
Description: Computes department-level composite risk scores, financial turnover
             exposure ($), and role vulnerability rankings for Power BI surfaces.
==============================================================================
"""

import os
import pandas as pd
import numpy as np

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")


def compute_department_risk_metrics(df_modeled):
    """
    Computes executive risk indices and financial exposure per department and role.
    """
    df = df_modeled.copy()

    # Department level aggregation
    dept_rows = []
    for dept, grp in df.groupby("Department"):
        headcount = len(grp)
        attr_count = int(grp["Attrition_Flag"].sum())
        attr_rate = float(grp["Attrition_Flag"].mean()) * 100
        avg_prob = float(grp["Attrition_Probability"].mean()) * 100
        high_risk_count = int((grp["Predicted_Risk_Tier"] == "High Risk").sum())
        high_risk_pct = (high_risk_count / headcount) * 100
        ot_pct = float(grp["OverTime_Flag"].mean()) * 100
        low_inc_pct = float(grp["Below_Median_Income_Flag"].mean()) * 100
        
        # Replacement exposure for high-risk headcount (SHRM 1.5x annual salary)
        high_risk_emps = grp[grp["Predicted_Risk_Tier"] == "High Risk"]
        turnover_exposure = float(high_risk_emps["Estimated_Replacement_Cost"].sum())

        # Composite Risk Index (0 - 100 scale)
        # Weighted by attrition rate (30%), model risk (30%), overtime (20%), low income (20%)
        composite_risk_score = (
            0.30 * min(attr_rate * 3.5, 100) +
            0.30 * min(high_risk_pct * 4.0, 100) +
            0.20 * min(ot_pct * 2.5, 100) +
            0.20 * min(low_inc_pct * 1.5, 100)
        )

        dept_rows.append({
            "Department": dept,
            "Total_Headcount": headcount,
            "Attrition_Count": attr_count,
            "Empirical_Attrition_Rate_Pct": round(attr_rate, 2),
            "Avg_Predicted_Risk_Pct": round(avg_prob, 2),
            "High_Risk_Headcount": high_risk_count,
            "High_Risk_Proportion_Pct": round(high_risk_pct, 2),
            "OverTime_Saturation_Pct": round(ot_pct, 2),
            "Below_Median_Income_Pct": round(low_inc_pct, 2),
            "Avg_Monthly_Income_USD": round(float(grp["MonthlyIncome"].mean()), 2),
            "Composite_Risk_Index": round(composite_risk_score, 1),
            "High_Risk_Financial_Exposure_USD": round(turnover_exposure, 2),
        })

    dept_df = pd.DataFrame(dept_rows).sort_values(by="Composite_Risk_Index", ascending=False)

    # Job Role Level Breakdown
    role_rows = []
    for (dept, role), grp in df.groupby(["Department", "JobRole"]):
        headcount = len(grp)
        attr_count = int(grp["Attrition_Flag"].sum())
        attr_rate = float(grp["Attrition_Flag"].mean()) * 100
        avg_prob = float(grp["Attrition_Probability"].mean()) * 100
        high_risk_count = int((grp["Predicted_Risk_Tier"] == "High Risk").sum())
        role_exposure = float(grp[grp["Predicted_Risk_Tier"] == "High Risk"]["Estimated_Replacement_Cost"].sum())

        role_rows.append({
            "Department": dept,
            "JobRole": role,
            "Headcount": headcount,
            "Attrition_Count": attr_count,
            "Attrition_Rate_Pct": round(attr_rate, 2),
            "Avg_Predicted_Risk_Pct": round(avg_prob, 2),
            "High_Risk_Count": high_risk_count,
            "Financial_Exposure_USD": round(role_exposure, 2),
        })

    role_df = pd.DataFrame(role_rows).sort_values(by="Attrition_Rate_Pct", ascending=False)

    # Save summary files for Power BI ingestion
    dept_summary_path = os.path.join(DATA_DIR, "processed", "department_risk_summary.csv")
    dept_df.to_csv(dept_summary_path, index=False)
    print(f"[DEPT RISK] Department risk summary exported: {dept_summary_path}")

    role_summary_path = os.path.join(DATA_DIR, "processed", "job_role_risk_summary.csv")
    role_df.to_csv(role_summary_path, index=False)
    print(f"[DEPT RISK] Job role risk summary exported: {role_summary_path}")

    return dept_df, role_df


if __name__ == "__main__":
    from data_loader import load_and_validate_data, enrich_analytical_features
    from train_model import build_and_evaluate_model
    raw = load_and_validate_data()
    enriched = enrich_analytical_features(raw)
    _, _, _, modeled_df, _ = build_and_evaluate_model(enriched)
    compute_department_risk_metrics(modeled_df)
