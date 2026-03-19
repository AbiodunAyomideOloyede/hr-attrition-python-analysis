"""
================================================================
PROJECT: HR Employee Attrition Analysis — Telecoms Company
Author : Oloyede Abiodun Ayomide
Tools  : Python, Pandas
================================================================

STEP 1 — Data Cleaning
This script takes the raw HR dataset and performs a full
professional cleaning process, documenting every decision made.

Issues addressed:
  1. Duplicate rows removed
  2. Text inconsistencies standardised
  3. Missing values handled appropriately per column
  4. Salary outliers capped using IQR method
  5. Age anomalies corrected
  6. Derived columns added (age group, salary band, tenure group)
  7. Cleaned data saved for analysis
"""

import pandas as pd
import numpy as np

print("=" * 60)
print("HR ATTRITION ANALYSIS — DATA CLEANING")
print("Author: Oloyede Abiodun Ayomide")
print("=" * 60)

# ── Load raw data ──────────────────────────────────────────────────────────
df = pd.read_csv("data/hr_raw_data.csv")
print(f"\n[LOAD] Raw data shape: {df.shape}")
print(f"       Columns: {list(df.columns)}")

# ── 1. Remove duplicates ───────────────────────────────────────────────────
before = len(df)
df.drop_duplicates(inplace=True)
df.reset_index(drop=True, inplace=True)
after = len(df)
print(f"\n[STEP 1] Duplicates removed: {before - after} rows dropped")
print(f"         Shape after: {df.shape}")

# ── 2. Standardise text columns ────────────────────────────────────────────
text_cols = ["department", "gender", "education_level",
             "job_level", "job_satisfaction", "left_company", "attrition_reason"]

for col in text_cols:
    if col in df.columns:
        df[col] = df[col].astype(str).str.strip().str.title()
        df[col] = df[col].replace("Nan", np.nan)

print("\n[STEP 2] Text columns standardised to Title Case, whitespace stripped")

# ── 3. Handle missing values ───────────────────────────────────────────────
print("\n[STEP 3] Handling missing values:")
print(f"         Before:\n{df.isnull().sum()[df.isnull().sum() > 0]}")

# Categorical — fill with mode
for col in ["department", "gender", "job_satisfaction"]:
    mode_val = df[col].mode()[0]
    missing  = df[col].isnull().sum()
    df[col] = df[col].fillna(mode_val)
    print(f"         '{col}': {missing} nulls filled with mode ('{mode_val}')")

# Numerical — fill with median (robust to outliers)
for col in ["performance_score", "training_hours"]:
    median_val = df[col].median()
    missing    = df[col].isnull().sum()
    df[col] = df[col].fillna(median_val)
    print(f"         '{col}': {missing} nulls filled with median ({median_val})")

print(f"\n         After: {df.isnull().sum().sum()} nulls remaining")

# ── 4. Fix age anomalies ───────────────────────────────────────────────────
invalid_age = df[(df["age"] < 18) | (df["age"] > 70)]
print(f"\n[STEP 4] Age anomalies found: {len(invalid_age)} records")
print(f"         Values: {invalid_age['age'].tolist()}")
median_age = int(df[(df["age"] >= 18) & (df["age"] <= 70)]["age"].median())
df.loc[(df["age"] < 18) | (df["age"] > 70), "age"] = median_age
print(f"         Replaced with median age: {median_age}")

# ── 5. Cap salary outliers using IQR method ────────────────────────────────
Q1  = df["monthly_salary"].quantile(0.25)
Q3  = df["monthly_salary"].quantile(0.75)
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

outliers_low  = (df["monthly_salary"] < lower_bound).sum()
outliers_high = (df["monthly_salary"] > upper_bound).sum()

df["monthly_salary"] = df["monthly_salary"].clip(lower=lower_bound, upper=upper_bound)

print(f"\n[STEP 5] Salary outliers capped using IQR method:")
print(f"         Lower bound: NGN {lower_bound:,.0f}")
print(f"         Upper bound: NGN {upper_bound:,.0f}")
print(f"         Low outliers capped:  {outliers_low}")
print(f"         High outliers capped: {outliers_high}")

# ── 6. Fix hire_date column ────────────────────────────────────────────────
df["hire_date"] = pd.to_datetime(df["hire_date"], errors="coerce")
invalid_dates   = df["hire_date"].isnull().sum()
print(f"\n[STEP 6] Hire date parsed to datetime. Invalid dates: {invalid_dates}")

# ── 7. Add derived columns ─────────────────────────────────────────────────
def age_group(age):
    if age < 30:   return "20-29"
    elif age < 40: return "30-39"
    elif age < 50: return "40-49"
    else:          return "50+"

def salary_band(sal):
    if sal < 150000:  return "Entry (<150k)"
    elif sal < 300000: return "Mid (150k-300k)"
    elif sal < 450000: return "Senior (300k-450k)"
    else:             return "Executive (450k+)"

def tenure_group(yrs):
    if yrs <= 2:   return "0-2 Years"
    elif yrs <= 5: return "3-5 Years"
    elif yrs <= 10: return "6-10 Years"
    else:          return "10+ Years"

def perf_band(score):
    if score >= 4.5:  return "Outstanding"
    elif score >= 3.5: return "Good"
    elif score >= 2.5: return "Average"
    else:             return "Poor"

df["age_group"]    = df["age"].apply(age_group)
df["salary_band"]  = df["monthly_salary"].apply(salary_band)
df["tenure_group"] = df["years_at_company"].apply(tenure_group)
df["perf_band"]    = df["performance_score"].apply(perf_band)

print("\n[STEP 7] Derived columns added:")
print("         age_group | salary_band | tenure_group | perf_band")

# ── 8. Final data types ────────────────────────────────────────────────────
df["monthly_salary"]    = df["monthly_salary"].round(0).astype(int)
df["performance_score"] = df["performance_score"].round(1)
df["training_hours"]    = df["training_hours"].round(0).fillna(0).astype(int)

# ── 9. Final summary ───────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("CLEANING COMPLETE — FINAL SUMMARY")
print("=" * 60)
print(f"Final shape:       {df.shape}")
print(f"Remaining nulls:   {df.isnull().sum().sum()}")
print(f"Attrition (Yes):   {(df['left_company'] == 'Yes').sum()}")
print(f"Attrition rate:    {(df['left_company'] == 'Yes').mean() * 100:.1f}%")
print(f"\nColumn dtypes:\n{df.dtypes}")
print(f"\nSample (first 3 rows):\n{df[['employee_id','department','age_group','salary_band','left_company']].head(3)}")

# ── Save cleaned data ──────────────────────────────────────────────────────
df.to_csv("data/hr_cleaned_data.csv", index=False)
print("\n[SAVED] Cleaned data saved to data/hr_cleaned_data.csv")
