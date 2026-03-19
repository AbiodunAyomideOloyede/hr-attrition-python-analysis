"""
================================================================
PROJECT: HR Employee Attrition Analysis — Telecoms Company
Author : Oloyede Abiodun Ayomide
Tools  : Python, Pandas, Matplotlib, Seaborn
================================================================

STEP 0 — Generate Raw Dataset
This script creates a realistic raw HR dataset that intentionally
contains the kinds of issues a real analyst would need to clean:
  - Missing values
  - Duplicate rows
  - Inconsistent text formatting
  - Outliers in salary
  - Mixed date formats
"""

import pandas as pd
import numpy as np
import os
import random

random.seed(42)
np.random.seed(42)

# ── Configuration ──────────────────────────────────────────────────────────
N = 300  # number of employee records

departments   = ["Sales", "Customer Service", "Network Operations",
                 "IT", "Finance", "HR", "Marketing"]
genders       = ["Male", "Female"]
education     = ["High School", "OND", "HND", "BSc", "MSc"]
job_levels    = ["Junior", "Mid-Level", "Senior", "Manager"]
attrition_rsn = ["Better Offer", "Low Salary", "Poor Management",
                  "Work-Life Balance", "Career Growth", "Relocation", "Personal"]
satisfaction  = ["Low", "Medium", "High"]

# ── Generate base data ─────────────────────────────────────────────────────
data = {
    "employee_id":       [f"EMP{str(i).zfill(4)}" for i in range(1, N + 1)],
    "full_name":         [f"Employee_{i}" for i in range(1, N + 1)],
    "department":        [random.choice(departments) for _ in range(N)],
    "gender":            [random.choice(genders) for _ in range(N)],
    "age":               [random.randint(22, 58) for _ in range(N)],
    "education_level":   [random.choice(education) for _ in range(N)],
    "job_level":         [random.choice(job_levels) for _ in range(N)],
    "years_at_company":  [random.randint(0, 18) for _ in range(N)],
    "monthly_salary":    [random.randint(80000, 550000) for _ in range(N)],
    "performance_score": [round(random.uniform(1.0, 5.0), 1) for _ in range(N)],
    "job_satisfaction":  [random.choice(satisfaction) for _ in range(N)],
    "promotions":        [random.randint(0, 5) for _ in range(N)],
    "training_hours":    [random.randint(0, 40) for _ in range(N)],
    "left_company":      [random.choices(["Yes", "No"], weights=[30, 70])[0] for _ in range(N)],
    "attrition_reason":  ["" for _ in range(N)],
    "hire_date":         [
        f"20{random.randint(5,23):02d}-{random.randint(1,12):02d}-{random.randint(1,28):02d}"
        for _ in range(N)
    ],
}

df = pd.DataFrame(data)

# Fill attrition reason only for leavers
df.loc[df["left_company"] == "Yes", "attrition_reason"] = [
    random.choice(attrition_rsn)
    for _ in range((df["left_company"] == "Yes").sum())
]

# ── Introduce deliberate data quality issues ────────────────────────────────

# 1. Missing values (~8% of key columns)
for col in ["department", "gender", "job_satisfaction", "performance_score", "training_hours"]:
    idx = np.random.choice(df.index, size=int(N * 0.08), replace=False)
    df.loc[idx, col] = np.nan

# 2. Inconsistent text formatting (mixed case, extra spaces)
inconsistent_idx = np.random.choice(df.index, size=40, replace=False)
df.loc[inconsistent_idx[:20], "department"] = df.loc[inconsistent_idx[:20], "department"].str.upper()
df.loc[inconsistent_idx[20:], "gender"]     = df.loc[inconsistent_idx[20:], "gender"].str.lower()

# 3. Salary outliers (a few unrealistically high/low entries)
df.loc[[5, 47, 112, 203], "monthly_salary"] = [12000, 8000, 950000, 1200000]

# 4. Duplicate rows (10 duplicates)
dup_idx   = np.random.choice(df.index, size=10, replace=False)
dup_rows  = df.loc[dup_idx].copy()
df        = pd.concat([df, dup_rows], ignore_index=True)

# 5. Age anomalies
df.loc[[0, 99, 200], "age"] = [17, 75, -1]

print(f"Raw dataset shape: {df.shape}")
print(f"Missing values:\n{df.isnull().sum()[df.isnull().sum() > 0]}")
print(f"\nDuplicates: {df.duplicated().sum()}")

# Save raw data
os.makedirs("data", exist_ok=True)
df.to_csv("data/hr_raw_data.csv", index=False)
print("\nRaw dataset saved to data/hr_raw_data.csv")
