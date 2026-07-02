"""
analysis.py
Cleans the raw COVID-19 dataset and computes key trend metrics.
Outputs a cleaned CSV for use by visualize.py.
"""

import pandas as pd
import numpy as np

# ── 1. Load ──────────────────────────────────────────────────────────────────
df = pd.read_csv("covid_raw.csv")
print(f"Loaded {len(df)} rows, {df.shape[1]} columns.")
print("\nMissing values before cleaning:")
print(df.isnull().sum())

# ── 2. Clean ─────────────────────────────────────────────────────────────────

# Normalize state names: strip whitespace, title-case
df["state"] = df["state"].str.strip().str.title()

# Parse dates — handle multiple formats
df["date"] = pd.to_datetime(df["date"], infer_datetime_format=True)

# Sort by state and date before filling
df = df.sort_values(["state", "date"]).reset_index(drop=True)

# Fill missing numeric values with forward-fill within each state, then backfill
numeric_cols = ["new_cases", "new_deaths", "vaccinations_administered"]
df[numeric_cols] = (
    df.groupby("state")[numeric_cols]
    .transform(lambda s: s.ffill().bfill())
)

# Clip negatives (shouldn't exist after generation, but just in case)
for col in numeric_cols:
    df[col] = df[col].clip(lower=0)

# Cast to int
df[numeric_cols] = df[numeric_cols].astype(int)

print("\nMissing values after cleaning:")
print(df.isnull().sum())

# ── 3. Feature Engineering ───────────────────────────────────────────────────

# 7-day rolling average of new cases per state
df["cases_7day_avg"] = (
    df.groupby("state")["new_cases"]
    .transform(lambda s: s.rolling(7, min_periods=1).mean().round(1))
)

# 7-day rolling average of new deaths per state
df["deaths_7day_avg"] = (
    df.groupby("state")["new_deaths"]
    .transform(lambda s: s.rolling(7, min_periods=1).mean().round(1))
)

# Week-over-week case growth rate (%)
df["cases_wow_growth"] = (
    df.groupby("state")["new_cases"]
    .transform(lambda s: s.pct_change(periods=7).mul(100).round(2))
)

# Cumulative cases and deaths per state
df["cumulative_cases"] = df.groupby("state")["new_cases"].cumsum()
df["cumulative_deaths"] = df.groupby("state")["new_deaths"].cumsum()

# Case fatality rate (rolling 7-day, avoid divide-by-zero)
df["cfr_7day"] = (
    df["deaths_7day_avg"] / df["cases_7day_avg"].replace(0, np.nan) * 100
).round(3)

# ── 4. Summary Statistics ─────────────────────────────────────────────────────

print("\n── Peak single-day cases per state ──")
peak_cases = (
    df.loc[df.groupby("state")["new_cases"].idxmax(), ["state", "date", "new_cases"]]
    .reset_index(drop=True)
)
print(peak_cases.to_string(index=False))

print("\n── Total cases & deaths by state ──")
totals = (
    df.groupby("state")[["new_cases", "new_deaths"]]
    .sum()
    .rename(columns={"new_cases": "total_cases", "new_deaths": "total_deaths"})
)
totals["overall_cfr_%"] = (totals["total_deaths"] / totals["total_cases"] * 100).round(2)
print(totals.to_string())

print("\n── National 7-day avg case peak ──")
national = df.groupby("date")["new_cases"].sum().reset_index()
national["national_7day_avg"] = national["new_cases"].rolling(7, min_periods=1).mean()
peak_date = national.loc[national["national_7day_avg"].idxmax(), "date"]
peak_val = national["national_7day_avg"].max()
print(f"  Peak date: {peak_date.date()}  |  Avg daily cases: {peak_val:,.0f}")

# ── 5. Save ───────────────────────────────────────────────────────────────────
df.to_csv("covid_clean.csv", index=False)
print("\nSaved cleaned data to covid_clean.csv")