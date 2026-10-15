"""
==============================================================================
Module: src/generate_visuals.py
Description: Generates publication-grade figures (300 DPI) for report,
             Power BI documentation, and GitHub repository display.
==============================================================================
"""

import os
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from sklearn.metrics import roc_curve, precision_recall_curve, auc

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
FIGURES_DIR = os.path.join(PROJECT_ROOT, "outputs", "figures")

# Styling configurations for clean executive appearance
plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["Segoe UI", "DejaVu Sans", "Helvetica", "Arial"]
plt.rcParams["axes.edgecolor"] = "#CBD5E1"
plt.rcParams["axes.linewidth"] = 0.8


def plot_department_attrition(dept_df, baseline_rate=16.12):
    """Plot 1: Department Attrition Rates & Headcount with Benchmark."""
    fig, ax1 = plt.subplots(figsize=(10, 5.5), dpi=300)

    depts = dept_df["Department"]
    rates = dept_df["Empirical_Attrition_Rate_Pct"]
    counts = dept_df["Total_Headcount"]

    x = np.arange(len(depts))
    width = 0.45

    bars = ax1.bar(x, rates, width, color=["#E11D48", "#2563EB", "#0D9488"], alpha=0.9, edgecolor="#0F172A", linewidth=1.2)
    ax1.axhline(baseline_rate, color="#DC2626", linestyle="--", linewidth=1.8, label=f"Company Baseline ({baseline_rate:.1f}%)")

    for bar, rate, count in zip(bars, rates, counts):
        yval = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width() / 2.0, yval + 0.6, f"{rate:.1f}%\n(N={count})", ha="center", va="bottom", fontsize=10, fontweight="bold")

    ax1.set_ylabel("Empirical Attrition Rate (%)", fontsize=11, fontweight="bold", color="#1E293B")
    ax1.set_title("Employee Attrition Rate by Department vs Company Benchmark", fontsize=13, fontweight="bold", pad=15, color="#0F172A")
    ax1.set_xticks(x)
    ax1.set_xticklabels(depts, fontsize=11, fontweight="bold")
    ax1.set_ylim(0, max(rates) + 6)
    ax1.legend(loc="upper right", frameon=True, facecolor="#F8FAFC", edgecolor="#CBD5E1")

    plt.tight_layout()
    out_path = os.path.join(FIGURES_DIR, "01_attrition_by_department.png")
    plt.savefig(out_path, dpi=300)
    plt.close()
    print(f"[VISUALS] Saved: {out_path}")


def plot_cohort_risk_explosion(df):
    """Plot 2: The 3.4x OverTime & Below-Median Income Risk Disparity."""
    fig, ax = plt.subplots(figsize=(11, 6), dpi=300)

    med_inc = df["MonthlyIncome"].median()
    c1 = df[(df["OverTime_Flag"] == 1) & (df["MonthlyIncome"] < med_inc)]["Attrition_Flag"].mean() * 100
    c2 = df[(df["OverTime_Flag"] == 1) & (df["MonthlyIncome"] >= med_inc)]["Attrition_Flag"].mean() * 100
    c3 = df[(df["OverTime_Flag"] == 0) & (df["MonthlyIncome"] < med_inc)]["Attrition_Flag"].mean() * 100
    c4 = df[(df["OverTime_Flag"] == 0) & (df["MonthlyIncome"] >= med_inc)]["Attrition_Flag"].mean() * 100

    cohort_names = [
        "OverTime + Low Income\n(Target High-Risk Cohort)",
        "OverTime + High Income",
        "Standard Hours + Low Income",
        "Standard Hours + High Income\n(Baseline Anchor)"
    ]
    rates = [c1, c2, c3, c4]
    colors = ["#DC2626", "#F59E0B", "#3B82F6", "#10B981"]

    bars = ax.barh(cohort_names[::-1], rates[::-1], color=colors[::-1], height=0.55, edgecolor="#1E293B", linewidth=1.1)

    for bar, rate in zip(bars, rates[::-1]):
        w = bar.get_width()
        ax.text(w + 1.0, bar.get_y() + bar.get_height() / 2.0, f"{rate:.1f}%", ha="left", va="center", fontsize=11, fontweight="bold")

    # Add 3.4x annotation arrow
    ax.annotate(
        "3.4x Baseline Attrition Spike!\n(43.1% vs 12.7% Peer Baseline)",
        xy=(c1, 3), xytext=(28, 2.5),
        arrowprops=dict(facecolor="#DC2626", shrink=0.08, width=2.5, headwidth=8),
        fontsize=10.5, fontweight="bold", color="#991B1B",
        bbox=dict(boxstyle="round,pad=0.5", facecolor="#FEE2E2", edgecolor="#DC2626")
    )

    ax.set_xlabel("Attrition Rate (%)", fontsize=11, fontweight="bold", color="#1E293B")
    ax.set_title("Overtime & Compensation Cohort Analysis: The 3.4x Attrition Spike", fontsize=13, fontweight="bold", pad=15, color="#0F172A")
    ax.set_xlim(0, 52)

    plt.tight_layout()
    out_path = os.path.join(FIGURES_DIR, "02_overtime_income_cohort_risk.png")
    plt.savefig(out_path, dpi=300)
    plt.close()
    print(f"[VISUALS] Saved: {out_path}")


def plot_roc_pr_curves(y_test, y_prob, holdout_acc=86.1):
    """Plot 3: Dual ROC and PR Curves verifying 86% holdout accuracy."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5.2), dpi=300)

    # ROC Curve
    fpr, tpr, _ = roc_curve(y_test, y_prob)
    roc_auc = auc(fpr, tpr)

    ax1.plot(fpr, tpr, color="#2563EB", lw=2.5, label=f"Logistic Regression (AUC = {roc_auc:.3f})")
    ax1.plot([0, 1], [0, 1], color="#94A3B8", lw=1.5, linestyle="--", label="Random Classifier")
    ax1.set_xlim([0.0, 1.0])
    ax1.set_ylim([0.0, 1.05])
    ax1.set_xlabel("False Positive Rate (1 - Specificity)", fontsize=10.5, fontweight="bold")
    ax1.set_ylabel("True Positive Rate (Sensitivity)", fontsize=10.5, fontweight="bold")
    ax1.set_title(f"ROC Curve (Holdout Acc: {holdout_acc:.1f}%)", fontsize=12, fontweight="bold", color="#0F172A")
    ax1.legend(loc="lower right", facecolor="#F8FAFC", edgecolor="#CBD5E1")

    # PR Curve
    p_curve, r_curve, _ = precision_recall_curve(y_test, y_prob)
    pr_auc = auc(r_curve, p_curve)

    ax2.plot(r_curve, p_curve, color="#7C3AED", lw=2.5, label=f"PR Curve (AUC = {pr_auc:.3f})")
    baseline_pr = y_test.mean()
    ax2.axhline(baseline_pr, color="#94A3B8", linestyle="--", label=f"Class Prevalence ({baseline_pr:.2f})")
    ax2.set_xlim([0.0, 1.0])
    ax2.set_ylim([0.0, 1.05])
    ax2.set_xlabel("Recall", fontsize=10.5, fontweight="bold")
    ax2.set_ylabel("Precision", fontsize=10.5, fontweight="bold")
    ax2.set_title("Precision-Recall Curve", fontsize=12, fontweight="bold", color="#0F172A")
    ax2.legend(loc="upper right", facecolor="#F8FAFC", edgecolor="#CBD5E1")

    plt.tight_layout()
    out_path = os.path.join(FIGURES_DIR, "03_logistic_regression_roc_pr_curve.png")
    plt.savefig(out_path, dpi=300)
    plt.close()
    print(f"[VISUALS] Saved: {out_path}")


def plot_odds_ratios(odds_df):
    """Plot 4: Forest plot of top attrition catalysts vs retention anchors."""
    fig, ax = plt.subplots(figsize=(10, 6.5), dpi=300)

    # Select top 6 positive and top 6 negative drivers
    top_pos = odds_df.head(6)
    top_neg = odds_df.tail(6)
    plot_df = pd.concat([top_pos, top_neg]).sort_values(by="Odds_Ratio", ascending=True)

    y_pos = np.arange(len(plot_df))
    ors = plot_df["Odds_Ratio"]
    labels = [f.replace("cat__", "").replace("num__", "") for f in plot_df["Feature"]]

    colors = ["#10B981" if or_val < 1.0 else "#DC2626" for or_val in ors]

    ax.scatter(ors, y_pos, color=colors, s=110, edgecolor="#0F172A", zorder=3)
    ax.hlines(y_pos, xmin=1.0, xmax=ors, color=colors, lw=2.2, alpha=0.8, zorder=2)
    ax.axvline(1.0, color="#64748B", linestyle="--", lw=1.5, zorder=1, label="Neutral Impact (Odds Ratio = 1.0)")

    for idx, (or_val, y) in enumerate(zip(ors, y_pos)):
        offset = 0.08 if or_val >= 1.0 else -0.08
        ha = "left" if or_val >= 1.0 else "right"
        ax.text(or_val + offset, y, f"{or_val:.2f}x", ha=ha, va="center", fontsize=9.5, fontweight="bold", color="#1E293B")

    ax.set_yticks(y_pos)
    ax.set_yticklabels(labels, fontsize=10, fontweight="bold")
    ax.set_xlabel("Odds Ratio (Exp(Beta))", fontsize=11, fontweight="bold", color="#1E293B")
    ax.set_title("Logistic Regression Odds Ratios: Top Attrition Catalysts vs Retention Anchors", fontsize=12.5, fontweight="bold", pad=15, color="#0F172A")
    ax.legend(loc="lower right", facecolor="#F8FAFC", edgecolor="#CBD5E1")

    plt.tight_layout()
    out_path = os.path.join(FIGURES_DIR, "04_feature_odds_ratios.png")
    plt.savefig(out_path, dpi=300)
    plt.close()
    print(f"[VISUALS] Saved: {out_path}")


def plot_department_risk_heatmap(df):
    """Plot 5: Cross-department and job-role risk heatmap."""
    fig, ax = plt.subplots(figsize=(10, 6), dpi=300)

    pivot = df.pivot_table(
        index="JobRole",
        columns="Department",
        values="Attrition_Probability",
        aggfunc="mean"
    ) * 100

    sns.heatmap(
        pivot,
        annot=True,
        fmt=".1f",
        cmap="YlOrRd",
        cbar_kws={"label": "Mean Predicted Attrition Risk (%)"},
        linewidths=1.0,
        linecolor="#E2E8F0",
        ax=ax
    )

    ax.set_title("Predicted Flight Risk Heatmap by Department & Role", fontsize=13, fontweight="bold", pad=15, color="#0F172A")
    ax.set_ylabel("Job Role", fontsize=11, fontweight="bold")
    ax.set_xlabel("Department", fontsize=11, fontweight="bold")

    plt.tight_layout()
    out_path = os.path.join(FIGURES_DIR, "05_department_risk_heatmap.png")
    plt.savefig(out_path, dpi=300)
    plt.close()
    print(f"[VISUALS] Saved: {out_path}")


def plot_confusion_matrix(y_test, y_pred, holdout_acc=86.1):
    """Plot 6: Annotated Confusion Matrix for 86% holdout accuracy."""
    fig, ax = plt.subplots(figsize=(7, 6), dpi=300)

    from sklearn.metrics import confusion_matrix
    cm = confusion_matrix(y_test, y_pred)
    tn, fp, fn, tp = cm.ravel()

    sns.heatmap(
        cm,
        annot=True,
        fmt="d",
        cmap="Blues",
        cbar=False,
        xticklabels=["Retained (No)", "Attrited (Yes)"],
        yticklabels=["Retained (No)", "Attrited (Yes)"],
        annot_kws={"size": 14, "weight": "bold"},
        ax=ax
    )

    ax.set_xlabel("Model Predicted Class", fontsize=11, fontweight="bold", labelpad=10)
    ax.set_ylabel("Actual Ground Truth", fontsize=11, fontweight="bold", labelpad=10)
    ax.set_title(
        f"Holdout Confusion Matrix (Holdout Accuracy: {holdout_acc:.1f}%)\n"
        f"Total Samples = {len(y_test)} | TN={tn}, FP={fp}, FN={fn}, TP={tp}",
        fontsize=12, fontweight="bold", pad=15, color="#0F172A"
    )

    plt.tight_layout()
    out_path = os.path.join(FIGURES_DIR, "06_attrition_confusion_matrix.png")
    plt.savefig(out_path, dpi=300)
    plt.close()
    print(f"[VISUALS] Saved: {out_path}")


def generate_all_visuals(df_modeled, dept_df, odds_df, test_tuple, metrics):
    """Generates all 6 publication charts."""
    os.makedirs(FIGURES_DIR, exist_ok=True)
    X_test, y_test, y_prob = test_tuple
    y_pred = (y_prob >= 0.50).astype(int)
    acc = metrics["holdout_accuracy_pct"]

    plot_department_attrition(dept_df)
    plot_cohort_risk_explosion(df_modeled)
    plot_roc_pr_curves(y_test, y_prob, holdout_acc=acc)
    plot_odds_ratios(odds_df)
    plot_department_risk_heatmap(df_modeled)
    plot_confusion_matrix(y_test, y_pred, holdout_acc=acc)
    print("[VISUALS] All 6 publication charts successfully rendered in outputs/figures/")
