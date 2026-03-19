"""
================================================================
PROJECT: HR Employee Attrition Analysis — Telecoms Company
Author : Oloyede Abiodun Ayomide
Tools  : Python, Pandas, Matplotlib, Seaborn
================================================================

RUN THIS FILE to execute the full project in order:
  Step 0 → Generate raw data
  Step 1 → Clean the data
  Step 2 → Analyse the data
  Step 3 → Produce all visualisations

Usage:
    python run_project.py
"""

import subprocess
import sys
import os

steps = [
    ("01_generate_data.py",  "STEP 0 — Generating raw dataset"),
    ("02_data_cleaning.py",  "STEP 1 — Cleaning data"),
    ("03_analysis.py",       "STEP 2 — Running analysis"),
    ("04_visualisations.py", "STEP 3 — Building visualisations"),
]

print("=" * 60)
print("HR ATTRITION ANALYSIS — FULL PROJECT RUNNER")
print("Author: Oloyede Abiodun Ayomide")
print("=" * 60)

for script, label in steps:
    print(f"\n{'─'*60}")
    print(f"  {label}")
    print(f"{'─'*60}")
    result = subprocess.run([sys.executable, script], capture_output=False)
    if result.returncode != 0:
        print(f"\n[ERROR] {script} failed. Check the output above.")
        sys.exit(1)

print("\n" + "=" * 60)
print("PROJECT COMPLETE")
print("=" * 60)
print("Outputs saved to:")
print("  data/hr_raw_data.csv          — original dataset with issues")
print("  data/hr_cleaned_data.csv      — cleaned and transformed dataset")
print("  data/dept_attrition_summary.csv")
print("  data/attrition_reasons.csv")
print("  outputs/01_attrition_overview.png")
print("  outputs/02_attrition_by_department.png")
print("  outputs/03_attrition_by_satisfaction.png")
print("  outputs/04_salary_distribution.png")
print("  outputs/05_attrition_by_tenure.png")
print("  outputs/06_attrition_reasons.png")
print("  outputs/07_performance_boxplot.png")
print("  outputs/08_heatmap_dept_satisfaction.png")
print("  outputs/09_full_dashboard.png  ← Main portfolio showcase")
