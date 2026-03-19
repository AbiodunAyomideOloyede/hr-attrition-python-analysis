"""
================================================================
PROJECT: HR Employee Attrition Analysis — Telecoms Company
Author : Oloyede Abiodun Ayomide
Tools  : Python, Pandas, Matplotlib, Seaborn
================================================================

STEP 3 — Data Visualisation
This script produces 8 professional charts covering:
  1.  Attrition rate overview (pie chart)
  2.  Attrition by department (horizontal bar)
  3.  Attrition by job satisfaction (bar)
  4.  Salary distribution by attrition status (histogram)
  5.  Attrition by tenure group (bar)
  6.  Top reasons for leaving (horizontal bar)
  7.  Performance score distribution by attrition (boxplot)
  8.  Attrition heatmap — department vs satisfaction (heatmap)
  9.  Full dashboard — all charts in one figure
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import os

os.makedirs("outputs", exist_ok=True)

print("=" * 60)
print("HR ATTRITION ANALYSIS — VISUALISATIONS")
print("Author: Oloyede Abiodun Ayomide")
print("=" * 60)

# ── Load cleaned data ──────────────────────────────────────────────────────
df = pd.read_csv("data/hr_cleaned_data.csv")

# ── Global style ───────────────────────────────────────────────────────────
DARK_BLUE   = "#1F4E79"
MID_BLUE    = "#2563EB"
LIGHT_BLUE  = "#D6E4F7"
ORANGE      = "#E67E22"
RED         = "#C0392B"
GREEN       = "#1E8449"
GRAY        = "#7F8C8D"
BG          = "#F8FAFC"

plt.rcParams.update({
    "figure.facecolor":  BG,
    "axes.facecolor":    BG,
    "axes.edgecolor":    GRAY,
    "axes.labelcolor":   DARK_BLUE,
    "axes.titlecolor":   DARK_BLUE,
    "axes.titlesize":    13,
    "axes.labelsize":    11,
    "xtick.color":       GRAY,
    "ytick.color":       GRAY,
    "xtick.labelsize":   9,
    "ytick.labelsize":   9,
    "font.family":       "DejaVu Sans",
    "text.color":        DARK_BLUE,
    "grid.color":        "#E0E0E0",
    "grid.linestyle":    "--",
    "grid.linewidth":    0.6,
})

def add_signature(fig):
    fig.text(0.99, 0.01,
             "Oloyede Abiodun Ayomide | HR Analytics Portfolio | Python + Pandas + Matplotlib",
             ha="right", va="bottom", fontsize=7, color=GRAY, style="italic")

def save_chart(fig, name):
    path = f"outputs/{name}.png"
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"[SAVED] {path}")

# ── Prepare reusable data ──────────────────────────────────────────────────
attr_counts = df["left_company"].value_counts()

dept_data = df.groupby("department").agg(
    total     = ("employee_id", "count"),
    attrition = ("left_company", lambda x: (x == "Yes").sum())
).reset_index()
dept_data["rate"] = dept_data["attrition"] / dept_data["total"] * 100
dept_data = dept_data.sort_values("rate", ascending=True)

sat_order   = ["Low", "Medium", "High"]
sat_data    = df.groupby("job_satisfaction")["left_company"].apply(
    lambda x: (x == "Yes").sum() / len(x) * 100
).reindex(sat_order)

tenure_order = ["0-2 Years", "3-5 Years", "6-10 Years", "10+ Years"]
tenure_data  = df.groupby("tenure_group")["left_company"].apply(
    lambda x: (x == "Yes").sum() / len(x) * 100
).reindex(tenure_order)

reasons = (df[df["left_company"] == "Yes"]["attrition_reason"]
           .value_counts()
           .sort_values(ascending=True))

sal_left   = df[df["left_company"] == "Yes"]["monthly_salary"]
sal_stayed = df[df["left_company"] == "No"]["monthly_salary"]

# ══════════════════════════════════════════════════════════════════
# CHART 1 — Attrition Overview (Pie)
# ══════════════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(7, 5))
fig.patch.set_facecolor(BG)

colors   = [RED, GREEN]
explode  = (0.05, 0)
wedges, texts, autotexts = ax.pie(
    attr_counts,
    labels     = ["Left", "Stayed"],
    colors     = colors,
    explode    = explode,
    autopct    = "%1.1f%%",
    startangle = 140,
    textprops  = {"fontsize": 11, "color": "white", "fontweight": "bold"},
)
for autotext in autotexts:
    autotext.set_fontsize(12)
    autotext.set_fontweight("bold")
    autotext.set_color("white")
for text in texts:
    text.set_color(DARK_BLUE)
    text.set_fontsize(12)

ax.set_title("Overall Attrition Overview\nLeft vs Stayed", fontsize=14,
             fontweight="bold", color=DARK_BLUE, pad=20)

rate = (df["left_company"] == "Yes").mean() * 100
ax.text(0, -1.35, f"Overall Attrition Rate: {rate:.1f}%",
        ha="center", fontsize=11, color=DARK_BLUE, fontweight="bold")

add_signature(fig)
save_chart(fig, "01_attrition_overview")


# ══════════════════════════════════════════════════════════════════
# CHART 2 — Attrition Rate by Department (Horizontal Bar)
# ══════════════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(9, 5))

colors_dept = [RED if r > 30 else MID_BLUE for r in dept_data["rate"]]
bars = ax.barh(dept_data["department"], dept_data["rate"],
               color=colors_dept, edgecolor="white", height=0.6)

# Value labels
for bar in bars:
    w = bar.get_width()
    ax.text(w + 0.5, bar.get_y() + bar.get_height() / 2,
            f"{w:.1f}%", va="center", ha="left", fontsize=9,
            color=DARK_BLUE, fontweight="bold")

ax.axvline(x=rate, color=ORANGE, linestyle="--", linewidth=1.5, label=f"Avg Rate ({rate:.1f}%)")
ax.set_xlabel("Attrition Rate (%)")
ax.set_title("Attrition Rate by Department", fontweight="bold")
ax.legend(fontsize=9)
ax.grid(axis="x", alpha=0.4)
ax.set_xlim(0, dept_data["rate"].max() + 12)

red_patch  = mpatches.Patch(color=RED,      label="Above Average")
blue_patch = mpatches.Patch(color=MID_BLUE, label="Below Average")
ax.legend(handles=[red_patch, blue_patch,
          mpatches.Patch(color=ORANGE, label=f"Avg ({rate:.1f}%)")],
          fontsize=9, loc="lower right")

add_signature(fig)
save_chart(fig, "02_attrition_by_department")


# ══════════════════════════════════════════════════════════════════
# CHART 3 — Attrition by Job Satisfaction
# ══════════════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(7, 5))

sat_colors = [RED, ORANGE, GREEN]
bars = ax.bar(sat_data.index, sat_data.values,
              color=sat_colors, edgecolor="white", width=0.5)

for bar in bars:
    h = bar.get_height()
    ax.text(bar.get_x() + bar.get_width() / 2, h + 0.5,
            f"{h:.1f}%", ha="center", va="bottom",
            fontsize=11, fontweight="bold", color=DARK_BLUE)

ax.set_ylabel("Attrition Rate (%)")
ax.set_xlabel("Job Satisfaction Level")
ax.set_title("Attrition Rate by Job Satisfaction Level\nLow Satisfaction = Highest Risk", fontweight="bold")
ax.grid(axis="y", alpha=0.4)
ax.set_ylim(0, sat_data.max() + 12)
ax.axhline(y=rate, color=GRAY, linestyle="--", linewidth=1, label=f"Overall avg ({rate:.1f}%)")
ax.legend(fontsize=9)

add_signature(fig)
save_chart(fig, "03_attrition_by_satisfaction")


# ══════════════════════════════════════════════════════════════════
# CHART 4 — Salary Distribution by Attrition Status (Histogram)
# ══════════════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(9, 5))

ax.hist(sal_stayed / 1000, bins=25, color=GREEN, alpha=0.65,
        label="Stayed", edgecolor="white")
ax.hist(sal_left / 1000,   bins=25, color=RED,   alpha=0.65,
        label="Left",   edgecolor="white")

ax.axvline(sal_stayed.mean() / 1000, color=GREEN, linestyle="--", linewidth=1.8,
           label=f"Stayed Avg: NGN {sal_stayed.mean()/1000:.0f}k")
ax.axvline(sal_left.mean() / 1000,   color=RED,   linestyle="--", linewidth=1.8,
           label=f"Left Avg: NGN {sal_left.mean()/1000:.0f}k")

ax.set_xlabel("Monthly Salary (NGN Thousands)")
ax.set_ylabel("Number of Employees")
ax.set_title("Salary Distribution — Employees Who Left vs Stayed\nLower Salaries Correlate with Higher Attrition", fontweight="bold")
ax.legend(fontsize=9)
ax.grid(axis="y", alpha=0.4)

add_signature(fig)
save_chart(fig, "04_salary_distribution")


# ══════════════════════════════════════════════════════════════════
# CHART 5 — Attrition by Tenure Group
# ══════════════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(8, 5))

tenure_colors = [RED if v == tenure_data.max() else MID_BLUE for v in tenure_data.values]
bars = ax.bar(tenure_data.index, tenure_data.values,
              color=tenure_colors, edgecolor="white", width=0.5)

for bar in bars:
    h = bar.get_height()
    ax.text(bar.get_x() + bar.get_width() / 2, h + 0.4,
            f"{h:.1f}%", ha="center", va="bottom",
            fontsize=11, fontweight="bold", color=DARK_BLUE)

ax.set_ylabel("Attrition Rate (%)")
ax.set_xlabel("Tenure Group")
ax.set_title("Attrition Rate by Tenure Group\nNew Employees Are Most At Risk", fontweight="bold")
ax.grid(axis="y", alpha=0.4)
ax.set_ylim(0, tenure_data.max() + 12)
ax.axhline(y=rate, color=GRAY, linestyle="--", linewidth=1, label=f"Overall avg ({rate:.1f}%)")
ax.legend(fontsize=9)

add_signature(fig)
save_chart(fig, "05_attrition_by_tenure")


# ══════════════════════════════════════════════════════════════════
# CHART 6 — Top Reasons for Leaving (Horizontal Bar)
# ══════════════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(9, 5))

reason_colors = [RED if v == reasons.max() else MID_BLUE for v in reasons.values]
bars = ax.barh(reasons.index, reasons.values,
               color=reason_colors, edgecolor="white", height=0.55)

for bar in bars:
    w = bar.get_width()
    ax.text(w + 0.3, bar.get_y() + bar.get_height() / 2,
            str(int(w)), va="center", ha="left",
            fontsize=10, fontweight="bold", color=DARK_BLUE)

ax.set_xlabel("Number of Employees")
ax.set_title("Top Reasons Employees Give for Leaving\nBetter Offer & Low Salary Are Primary Drivers", fontweight="bold")
ax.grid(axis="x", alpha=0.4)
ax.set_xlim(0, reasons.max() + 8)

red_patch  = mpatches.Patch(color=RED,      label="Top Reason")
blue_patch = mpatches.Patch(color=MID_BLUE, label="Other Reasons")
ax.legend(handles=[red_patch, blue_patch], fontsize=9)

add_signature(fig)
save_chart(fig, "06_attrition_reasons")


# ══════════════════════════════════════════════════════════════════
# CHART 7 — Performance Score Distribution (Boxplot)
# ══════════════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(7, 5))

left_scores   = df[df["left_company"] == "Yes"]["performance_score"]
stayed_scores = df[df["left_company"] == "No"]["performance_score"]

bp = ax.boxplot(
    [left_scores, stayed_scores],
    labels      = ["Left", "Stayed"],
    patch_artist= True,
    notch       = False,
    medianprops = {"color": "white", "linewidth": 2},
    whiskerprops= {"color": GRAY},
    capprops    = {"color": GRAY},
    flierprops  = {"marker": "o", "color": GRAY, "markersize": 4, "alpha": 0.5},
)
bp["boxes"][0].set_facecolor(RED)
bp["boxes"][1].set_facecolor(GREEN)

ax.set_ylabel("Performance Score (1-5)")
ax.set_title("Performance Score Distribution\nLeft vs Stayed Employees", fontweight="bold")
ax.grid(axis="y", alpha=0.4)

left_med   = left_scores.median()
stayed_med = stayed_scores.median()
ax.text(1, left_med + 0.05,   f"Median: {left_med}",   ha="center", fontsize=9, color="white", fontweight="bold")
ax.text(2, stayed_med + 0.05, f"Median: {stayed_med}", ha="center", fontsize=9, color="white", fontweight="bold")

red_patch   = mpatches.Patch(color=RED,   label="Left")
green_patch = mpatches.Patch(color=GREEN, label="Stayed")
ax.legend(handles=[red_patch, green_patch], fontsize=9)

add_signature(fig)
save_chart(fig, "07_performance_boxplot")


# ══════════════════════════════════════════════════════════════════
# CHART 8 — Heatmap: Attrition by Department & Satisfaction
# ══════════════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(9, 5))

pivot = df.groupby(["department", "job_satisfaction"])["left_company"].apply(
    lambda x: round((x == "Yes").sum() / len(x) * 100, 1)
).unstack()[sat_order]

sns.heatmap(
    pivot,
    annot      = True,
    fmt        = ".1f",
    cmap       = "RdYlGn_r",
    linewidths = 0.5,
    linecolor  = "white",
    ax         = ax,
    cbar_kws   = {"label": "Attrition Rate (%)"},
    annot_kws  = {"size": 10, "weight": "bold"},
)

ax.set_title("Attrition Rate Heatmap\nDepartment vs Job Satisfaction Level", fontweight="bold")
ax.set_xlabel("Job Satisfaction")
ax.set_ylabel("Department")

add_signature(fig)
save_chart(fig, "08_heatmap_dept_satisfaction")


# ══════════════════════════════════════════════════════════════════
# CHART 9 — FULL DASHBOARD (4x2 grid)
# ══════════════════════════════════════════════════════════════════
print("\n[BUILDING] Full dashboard (4x2 grid)...")

fig = plt.figure(figsize=(20, 22))
fig.patch.set_facecolor(BG)

# Title banner
fig.text(0.5, 0.98,
         "HR Employee Attrition Analysis — Telecoms Company",
         ha="center", va="top",
         fontsize=20, fontweight="bold", color=DARK_BLUE)
fig.text(0.5, 0.965,
         "Author: Oloyede Abiodun Ayomide  |  Tools: Python • Pandas • Matplotlib • Seaborn",
         ha="center", va="top", fontsize=11, color=GRAY, style="italic")

axes = []
positions = [
    (0.03, 0.72, 0.28, 0.22),  # pie
    (0.37, 0.72, 0.30, 0.22),  # dept bar
    (0.71, 0.72, 0.28, 0.22),  # satisfaction
    (0.03, 0.48, 0.28, 0.22),  # salary histogram
    (0.37, 0.48, 0.28, 0.22),  # tenure
    (0.71, 0.48, 0.28, 0.22),  # reasons
    (0.03, 0.24, 0.28, 0.22),  # boxplot
    (0.37, 0.24, 0.60, 0.22),  # heatmap
]

for pos in positions:
    axes.append(fig.add_axes(pos, facecolor=BG))

# ── Panel 1: Pie ──────────────────────────────────────────────────
ax = axes[0]
wedges, texts, autotexts = ax.pie(
    attr_counts, labels=["Left", "Stayed"],
    colors=colors, explode=explode,
    autopct="%1.1f%%", startangle=140,
    textprops={"fontsize": 9, "color": "white", "fontweight": "bold"}
)
for t in texts: t.set_color(DARK_BLUE); t.set_fontsize(9)
ax.set_title("Attrition Overview", fontsize=11, fontweight="bold", color=DARK_BLUE)

# ── Panel 2: Dept bar ─────────────────────────────────────────────
ax = axes[1]
c2 = [RED if r > rate else MID_BLUE for r in dept_data["rate"]]
ax.barh(dept_data["department"], dept_data["rate"], color=c2, edgecolor="white", height=0.6)
ax.axvline(x=rate, color=ORANGE, linestyle="--", linewidth=1.2)
for i, (val, name) in enumerate(zip(dept_data["rate"], dept_data["department"])):
    ax.text(val + 0.3, i, f"{val:.1f}%", va="center", fontsize=7, color=DARK_BLUE, fontweight="bold")
ax.set_title("By Department", fontsize=11, fontweight="bold", color=DARK_BLUE)
ax.set_xlabel("Attrition Rate (%)", fontsize=8)
ax.grid(axis="x", alpha=0.4)
ax.tick_params(axis="y", labelsize=8)
ax.set_xlim(0, dept_data["rate"].max() + 14)

# ── Panel 3: Satisfaction ─────────────────────────────────────────
ax = axes[2]
ax.bar(sat_data.index, sat_data.values, color=sat_colors, edgecolor="white", width=0.5)
for i, v in enumerate(sat_data.values):
    ax.text(i, v + 0.5, f"{v:.1f}%", ha="center", fontsize=9, fontweight="bold", color=DARK_BLUE)
ax.set_title("By Job Satisfaction", fontsize=11, fontweight="bold", color=DARK_BLUE)
ax.set_ylabel("Attrition Rate (%)", fontsize=8)
ax.grid(axis="y", alpha=0.4)
ax.axhline(y=rate, color=GRAY, linestyle="--", linewidth=1)
ax.set_ylim(0, sat_data.max() + 14)

# ── Panel 4: Salary histogram ─────────────────────────────────────
ax = axes[3]
ax.hist(sal_stayed / 1000, bins=20, color=GREEN, alpha=0.65, label="Stayed", edgecolor="white")
ax.hist(sal_left / 1000,   bins=20, color=RED,   alpha=0.65, label="Left",   edgecolor="white")
ax.axvline(sal_stayed.mean() / 1000, color=GREEN, linestyle="--", linewidth=1.5)
ax.axvline(sal_left.mean() / 1000,   color=RED,   linestyle="--", linewidth=1.5)
ax.set_title("Salary Distribution", fontsize=11, fontweight="bold", color=DARK_BLUE)
ax.set_xlabel("Salary (NGN thousands)", fontsize=8)
ax.legend(fontsize=8)
ax.grid(axis="y", alpha=0.4)

# ── Panel 5: Tenure ───────────────────────────────────────────────
ax = axes[4]
t_colors = [RED if v == tenure_data.max() else MID_BLUE for v in tenure_data.values]
ax.bar(range(len(tenure_data)), tenure_data.values, color=t_colors, edgecolor="white", width=0.5)
ax.set_xticks(range(len(tenure_data)))
ax.set_xticklabels(tenure_data.index, fontsize=7, rotation=10)
for i, v in enumerate(tenure_data.values):
    ax.text(i, v + 0.4, f"{v:.1f}%", ha="center", fontsize=9, fontweight="bold", color=DARK_BLUE)
ax.set_title("By Tenure Group", fontsize=11, fontweight="bold", color=DARK_BLUE)
ax.set_ylabel("Attrition Rate (%)", fontsize=8)
ax.grid(axis="y", alpha=0.4)
ax.set_ylim(0, tenure_data.max() + 14)

# ── Panel 6: Reasons ──────────────────────────────────────────────
ax = axes[5]
r_colors = [RED if v == reasons.max() else MID_BLUE for v in reasons.values]
ax.barh(reasons.index, reasons.values, color=r_colors, edgecolor="white", height=0.55)
for i, v in enumerate(reasons.values):
    ax.text(v + 0.2, i, str(int(v)), va="center", fontsize=8, fontweight="bold", color=DARK_BLUE)
ax.set_title("Reasons for Leaving", fontsize=11, fontweight="bold", color=DARK_BLUE)
ax.set_xlabel("Count", fontsize=8)
ax.grid(axis="x", alpha=0.4)
ax.tick_params(axis="y", labelsize=8)
ax.set_xlim(0, reasons.max() + 8)

# ── Panel 7: Boxplot ──────────────────────────────────────────────
ax = axes[6]
bp = ax.boxplot(
    [left_scores, stayed_scores],
    labels=["Left", "Stayed"],
    patch_artist=True,
    medianprops={"color": "white", "linewidth": 2},
    whiskerprops={"color": GRAY},
    capprops={"color": GRAY},
    flierprops={"marker": "o", "color": GRAY, "markersize": 3, "alpha": 0.5},
)
bp["boxes"][0].set_facecolor(RED)
bp["boxes"][1].set_facecolor(GREEN)
ax.set_title("Performance Score", fontsize=11, fontweight="bold", color=DARK_BLUE)
ax.set_ylabel("Score (1-5)", fontsize=8)
ax.grid(axis="y", alpha=0.4)

# ── Panel 8: Heatmap ──────────────────────────────────────────────
ax = axes[7]
sns.heatmap(
    pivot, annot=True, fmt=".1f", cmap="RdYlGn_r",
    linewidths=0.5, linecolor="white", ax=ax,
    cbar_kws={"label": "Attrition %", "shrink": 0.8},
    annot_kws={"size": 9, "weight": "bold"}
)
ax.set_title("Heatmap: Dept vs Satisfaction", fontsize=11, fontweight="bold", color=DARK_BLUE)
ax.set_xlabel("Job Satisfaction", fontsize=8)
ax.set_ylabel("Department", fontsize=8)
ax.tick_params(axis="both", labelsize=8)

# Key findings box
findings_text = (
    "KEY FINDINGS\n"
    f"1. Overall attrition rate: {rate:.1f}%\n"
    f"2. Highest-risk dept: {dept_data.iloc[-1]['department']} ({dept_data.iloc[-1]['rate']:.1f}%)\n"
    f"3. Low satisfaction attrition: {sat_data['Low']:.1f}%\n"
    f"4. High satisfaction attrition: {sat_data['High']:.1f}%\n"
    f"5. New hires (0-2 yrs) attrition: {tenure_data['0-2 Years']:.1f}%\n"
    "6. Employees who left earned lower avg salary\n"
    "7. Performance score is not a strong predictor"
)

fig.text(0.03, 0.21, findings_text,
         fontsize=9.5, color=DARK_BLUE,
         va="top", ha="left",
         bbox=dict(boxstyle="round,pad=0.6", facecolor=LIGHT_BLUE, edgecolor=MID_BLUE, linewidth=1.5))

add_signature(fig)
save_chart(fig, "09_full_dashboard")

print("\n" + "=" * 60)
print("ALL CHARTS SAVED TO outputs/ FOLDER")
print("=" * 60)
print("\nFiles generated:")
for i in range(1, 10):
    prefix = f"0{i}" if i < 10 else str(i)
    names = {
        "01": "01_attrition_overview.png",
        "02": "02_attrition_by_department.png",
        "03": "03_attrition_by_satisfaction.png",
        "04": "04_salary_distribution.png",
        "05": "05_attrition_by_tenure.png",
        "06": "06_attrition_reasons.png",
        "07": "07_performance_boxplot.png",
        "08": "08_heatmap_dept_satisfaction.png",
        "09": "09_full_dashboard.png",
    }
    print(f"  {names[prefix]}")
