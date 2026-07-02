"""
generate_data.py
Generates a synthetic, intentionally messy COVID-19 dataset for analysis.
"""

import pandas as pd
import numpy as np
import random

np.random.seed(42)
random.seed(42)

# Date range: Jan 2021 - Dec 2022
dates = pd.date_range(start="2021-01-01", end="2022-12-31", freq="D")

states = ["California", "Texas", "Florida", "New York", "Illinois"]

rows = []

for state in states:
    base_cases = np.random.randint(1000, 5000)
    for i, date in enumerate(dates):
        # Simulate waves with a sine curve + noise
        wave = (
            base_cases
            + 8000 * np.abs(np.sin(2 * np.pi * i / 180))
            + np.random.normal(0, 500)
        )
        cases = max(0, int(wave))
        deaths = max(0, int(cases * np.random.uniform(0.005, 0.02) + np.random.normal(0, 10)))
        vaccinations = max(0, int(np.random.uniform(5000, 30000) + i * 50))

        # Introduce messiness
        if random.random() < 0.05:
            cases = None          # ~5% missing cases
        if random.random() < 0.04:
            deaths = None         # ~4% missing deaths
        if random.random() < 0.03:
            vaccinations = None   # ~3% missing vaccinations
        if random.random() < 0.02:
            state_val = "  " + state.lower() + "  "  # dirty state name
        else:
            state_val = state
        if random.random() < 0.01:
            date_val = date.strftime("%m/%d/%Y")  # inconsistent date format
        else:
            date_val = date.strftime("%Y-%m-%d")

        rows.append({
            "date": date_val,
            "state": state_val,
            "new_cases": cases,
            "new_deaths": deaths,
            "vaccinations_administered": vaccinations,
        })

df = pd.DataFrame(rows)

# Shuffle to make it messier
df = df.sample(frac=1, random_state=42).reset_index(drop=True)

df.to_csv("covid_raw.csv", index=False)
print(f"Generated covid_raw.csv with {len(df)} rows.")
print("Sample:")
print(df.head())