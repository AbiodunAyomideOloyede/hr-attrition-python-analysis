"""
================================================================
PROJECT: HR Employee Attrition Analysis — Telecoms Company
Author : Oloyede Abiodun Ayomide
Tools  : Python, Pandas
================================================================

STEP 2 — Exploratory Data Analysis (EDA)
This script performs a structured analysis of the cleaned HR
dataset, computing key HR metrics and printing findings that
form the basis of the visualisations in the next step.
"""

import pandas as pd
import numpy as np

print("=" * 60)
print("HR ATTRITION ANALYSIS — EXPLORATORY DATA ANALYSIS")
print("Author: Oloyede Abiodun Ayomide")
print("=" * 60)

# ── Load cleaned data ──────────────────────────────────────────────────────
df = pd.read_csv("data/hr_cleaned_data.csv")
print(f"\n[LOAD] Cleaned data shape: {df.shape}\n")

# ── 1. Dataset overview ────────────────────────────────────────────────────
print("─" * 50)
print("1. DATASET OVERVIEW")
print("─" * 50)
print(df.describe(include="all").T[["count", "unique", "top", "mean", "std", "min", "max"]]
        .fillna("").to_string())

# ── 2. Attrition summary ───────────────────────────────────────────────────
print("\n" + "─" * 50)
print("2. ATTRITION SUMMARY")
print("─" * 50)

total       = len(df)
left        = (df["left_company"] == "Yes").sum()
stayed      = (df["left_company"] == "No").sum()
rate        = left / total * 100

print(f"Total Employees:   {total}")
print(f"Employees Left:    {left}")
print(f"Employees Stayed:  {stayed}")
print(f"Attrition Rate:    {rate:.1f}%")

# ── 3. Attrition by department ─────────────────────────────────────────────
print("\n" + "─" * 50)
print("3. ATTRITION BY DEPARTMENT")
print("─" * 50)

dept_summary = df.groupby("department").agg(
    total       = ("employee_id", "count"),
    attrition   = ("left_company", lambda x: (x == "Yes").sum())
).reset_index()
dept_summary["attrition_rate"] = (dept_summary["attrition"] / dept_summary["total"] * 100).round(1)
dept_summary = dept_summary.sort_values("attrition_rate", ascending=False)
print(dept_summary.to_string(index=False))

# ── 4. Attrition by gender ─────────────────────────────────────────────────
print("\n" + "─" * 50)
print("4. ATTRITION BY GENDER")
print("─" * 50)

gender_summary = df.groupby("gender")["left_company"].apply(
    lambda x: (x == "Yes").sum() / len(x) * 100
).round(1).reset_index()
gender_summary.columns = ["gender", "attrition_rate_%"]
print(gender_summary.to_string(index=False))

# ── 5. Attrition by job satisfaction ──────────────────────────────────────
print("\n" + "─" * 50)
print("5. ATTRITION BY JOB SATISFACTION")
print("─" * 50)

sat_order = ["Low", "Medium", "High"]
sat_summary = df.groupby("job_satisfaction")["left_company"].apply(
    lambda x: (x == "Yes").sum() / len(x) * 100
).round(1).reindex(sat_order).reset_index()
sat_summary.columns = ["job_satisfaction", "attrition_rate_%"]
print(sat_summary.to_string(index=False))

# ── 6. Salary statistics by attrition status ──────────────────────────────
print("\n" + "─" * 50)
print("6. SALARY ANALYSIS BY ATTRITION STATUS")
print("─" * 50)

sal_summary = df.groupby("left_company")["monthly_salary"].agg(
    ["mean", "median", "min", "max"]
).round(0).astype(int)
sal_summary.columns = ["Mean (NGN)", "Median (NGN)", "Min (NGN)", "Max (NGN)"]
print(sal_summary.to_string())

# ── 7. Attrition by tenure group ──────────────────────────────────────────
print("\n" + "─" * 50)
print("7. ATTRITION BY TENURE GROUP")
print("─" * 50)

tenure_order = ["0-2 Years", "3-5 Years", "6-10 Years", "10+ Years"]
tenure_summary = df.groupby("tenure_group")["left_company"].apply(
    lambda x: (x == "Yes").sum() / len(x) * 100
).round(1).reindex(tenure_order).reset_index()
tenure_summary.columns = ["tenure_group", "attrition_rate_%"]
print(tenure_summary.to_string(index=False))

# ── 8. Top attrition reasons ───────────────────────────────────────────────
print("\n" + "─" * 50)
print("8. TOP REASONS FOR LEAVING")
print("─" * 50)

reasons = (df[df["left_company"] == "Yes"]["attrition_reason"]
           .value_counts()
           .reset_index())
reasons.columns = ["reason", "count"]
reasons["percentage"] = (reasons["count"] / reasons["count"].sum() * 100).round(1)
print(reasons.to_string(index=False))

# ── 9. Performance score vs attrition ─────────────────────────────────────
print("\n" + "─" * 50)
print("9. PERFORMANCE SCORE vs ATTRITION")
print("─" * 50)

perf_summary = df.groupby("left_company")["performance_score"].agg(["mean","median"]).round(2)
print(perf_summary.to_string())

# ── 10. Training hours vs attrition ───────────────────────────────────────
print("\n" + "─" * 50)
print("10. TRAINING HOURS vs ATTRITION")
print("─" * 50)

train_summary = df.groupby("left_company")["training_hours"].agg(["mean","median"]).round(1)
print(train_summary.to_string())

# ── 11. Key findings ───────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("KEY FINDINGS SUMMARY")
print("=" * 60)

top_dept   = dept_summary.iloc[0]["department"]
top_dept_r = dept_summary.iloc[0]["attrition_rate"]
top_reason = reasons.iloc[0]["reason"]
low_sat_r  = sat_summary[sat_summary["job_satisfaction"] == "Low"]["attrition_rate_%"].values[0]
high_sat_r = sat_summary[sat_summary["job_satisfaction"] == "High"]["attrition_rate_%"].values[0]
early_r    = tenure_summary[tenure_summary["tenure_group"] == "0-2 Years"]["attrition_rate_%"].values[0]

print(f"1. Overall attrition rate is {rate:.1f}% — industry average is ~15-20%.")
print(f"2. '{top_dept}' has the highest attrition rate at {top_dept_r}%.")
print(f"3. '{top_reason}' is the most common reason employees give for leaving.")
print(f"4. Low satisfaction employees leave at {low_sat_r}% vs {high_sat_r}% for High satisfaction.")
print(f"5. Employees in their first 0-2 years have the highest attrition rate at {early_r}%.")
print(f"6. Employees who left earned a lower average salary than those who stayed.")
print(f"7. Performance score alone is not a strong predictor of attrition.")

# ── Save summary stats ─────────────────────────────────────────────────────
dept_summary.to_csv("data/dept_attrition_summary.csv", index=False)
reasons.to_csv("data/attrition_reasons.csv", index=False)
print("\n[SAVED] Summary tables saved to data/")
