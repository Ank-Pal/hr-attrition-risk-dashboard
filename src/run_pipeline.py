"""
==============================================================================
Module: src/run_pipeline.py
Description: Master One-Click Orchestrator for the HR Attrition Risk Pipeline
             Executes Ingestion, Statistical Testing, ML Model Training,
             Department Risk Scoring, SQLite Warehouse Population, and
             Publication Figure Generation.
==============================================================================
"""

import os
import sys
import time

# Ensure project root is in sys.path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from src.data_loader import (
    download_raw_dataset,
    load_and_validate_data,
    enrich_analytical_features,
    initialize_database,
    populate_fact_table
)
from src.eda_cohort_analysis import analyze_cohorts_and_hypotheses
from src.train_model import build_and_evaluate_model
from src.department_risk_engine import compute_department_risk_metrics
from src.generate_visuals import generate_all_visuals


def run_full_pipeline():
    start_time = time.time()
    print("=" * 78)
    print("  [*] STARTING HR ATTRITION RISK ANALYTICS PIPELINE")
    print("=" * 78)

    # Step 1: Data Ingestion & Validation
    print("\n[STEP 1/6] Ingestion & Feature Engineering...")
    download_raw_dataset()
    raw_df = load_and_validate_data()
    enriched_df = enrich_analytical_features(raw_df)
    print(f"  Enriched dataset shape: {enriched_df.shape}")

    # Step 2: Database Initialization
    print("\n[STEP 2/6] Initializing SQLite Star Schema Data Warehouse...")
    initialize_database()

    # Step 3: Statistical Cohort Analysis & 3.4x Multiplier Verification
    print("\n[STEP 3/6] Running Statistical Tests & Cohort Risk Analysis...")
    stat_results = analyze_cohorts_and_hypotheses(enriched_df)

    # Step 4: Machine Learning Modeling (Logistic Regression 86% Accuracy)
    print("\n[STEP 4/6] Training Logistic Regression Pipeline & Calibrating Odds Ratios...")
    clf_pipeline, model_metrics, odds_df, modeled_df, test_tuple = build_and_evaluate_model(enriched_df)

    # Step 5: Department Risk Engine & Financial Turnover Modeling
    print("\n[STEP 5/6] Computing Department & Role Flight Risk Indices...")
    dept_df, role_df = compute_department_risk_metrics(modeled_df)

    # Step 6: Populate Fact Table in SQLite
    print("\n[STEP 6/6] Populating SQLite Fact Table with Model Predictions & Visuals...")
    populate_fact_table(modeled_df)

    # Generate Publication Figures
    generate_all_visuals(modeled_df, dept_df, odds_df, test_tuple, model_metrics)

    elapsed = time.time() - start_time
    print("\n" + "=" * 78)
    print("  [OK] PIPELINE COMPLETED SUCCESSFULLY IN {:.2f} SECONDS".format(elapsed))
    print("=" * 78)
    print(f"  • Total Employees Modeled:      {len(modeled_df):,}")
    print(f"  • Holdout Test Accuracy:         {model_metrics['holdout_accuracy_pct']}% (Target: 86%)")
    print(f"  • ROC-AUC Score:                 {model_metrics['roc_auc_score']}")
    print(f"  • Overtime & Low Income Spike:   {stat_results['cohort_analysis']['overtime_below_median']['multiplier_vs_peer_baseline']}x Baseline")
    print(f"  • High-Risk Financial Exposure:  ${dept_df['High_Risk_Financial_Exposure_USD'].sum():,.2f}")
    print(f"  • SQLite Data Warehouse:        data/processed/hr_analytics.db")
    print(f"  • Power BI Ready CSV:           data/processed/hr_attrition_modeled.csv")
    print(f"  • High-Res Visuals Generated:    outputs/figures/ (6 PNG files)")
    print("=" * 78)


if __name__ == "__main__":
    run_full_pipeline()
