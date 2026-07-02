"""
visualize.py
Generates charts from the cleaned COVID-19 dataset.
Saves PNGs to the current directory.
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns

sns.set_theme(style="darkgrid", palette="tab10")

df = pd.read_csv("covid_clean.csv", parse_dates=["date"])
states = df["state"].unique()

# ── Chart 1: 7-Day Rolling Average Cases — All States ────────────────────────
fig, ax = plt.subplots(figsize=(12, 5))

for state in sorted(states):
    sub = df[df["state"] == state]
    ax.plot(sub["date"], sub["cases_7day_avg"], label=state, linewidth=1.8)

ax.set_title("COVID-19: 7-Day Rolling Average New Cases by State", fontsize=14)
ax.set_xlabel("Date")
ax.set_ylabel("Avg Daily New Cases")
ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
ax.legend(loc="upper left", fontsize=9)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("chart1_rolling_avg_cases.png", dpi=150)
plt.close()
print("Saved chart1_rolling_avg_cases.png")

# ── Chart 2: Cumulative Cases — All States ───────────────────────────────────
fig, ax = plt.subplots(figsize=(12, 5))

for state in sorted(states):
    sub = df[df["state"] == state]
    ax.plot(sub["date"], sub["cumulative_cases"] / 1e6, label=state, linewidth=1.8)

ax.set_title("COVID-19: Cumulative Cases by State (Millions)", fontsize=14)
ax.set_xlabel("Date")
ax.set_ylabel("Cumulative Cases (Millions)")
ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
ax.legend(loc="upper left", fontsize=9)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("chart2_cumulative_cases.png", dpi=150)
plt.close()
print("Saved chart2_cumulative_cases.png")

# ── Chart 3: Total Cases vs Deaths — Bar Chart ───────────────────────────────
totals = (
    df.groupby("state")[["new_cases", "new_deaths"]]
    .sum()
    .reset_index()
    .rename(columns={"new_cases": "total_cases", "new_deaths": "total_deaths"})
    .sort_values("total_cases", ascending=False)
)

fig, axes = plt.subplots(1, 2, figsize=(13, 5))

sns.barplot(data=totals, x="state", y="total_cases", ax=axes[0], palette="tab10")
axes[0].set_title("Total Reported Cases by State")
axes[0].set_xlabel("")
axes[0].set_ylabel("Total Cases")
axes[0].tick_params(axis="x", rotation=20)
for bar in axes[0].patches:
    axes[0].text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() * 1.01,
        f"{bar.get_height()/1e6:.1f}M",
        ha="center", va="bottom", fontsize=8
    )

sns.barplot(data=totals, x="state", y="total_deaths", ax=axes[1], palette="tab10")
axes[1].set_title("Total Reported Deaths by State")
axes[1].set_xlabel("")
axes[1].set_ylabel("Total Deaths")
axes[1].tick_params(axis="x", rotation=20)

plt.suptitle("COVID-19 Totals by State (Jan 2021 – Dec 2022)", fontsize=13, y=1.02)
plt.tight_layout()
plt.savefig("chart3_totals_by_state.png", dpi=150, bbox_inches="tight")
plt.close()
print("Saved chart3_totals_by_state.png")

# ── Chart 4: Vaccinations vs 7-Day Case Avg (California) ─────────────────────
ca = df[df["state"] == "California"].copy()

fig, ax1 = plt.subplots(figsize=(12, 5))

color_cases = "#e45756"
color_vacc = "#4c78a8"

ax1.set_xlabel("Date")
ax1.set_ylabel("7-Day Avg New Cases", color=color_cases)
ax1.plot(ca["date"], ca["cases_7day_avg"], color=color_cases, linewidth=1.8, label="7-day avg cases")
ax1.tick_params(axis="y", labelcolor=color_cases)

ax2 = ax1.twinx()
ax2.set_ylabel("Vaccinations Administered", color=color_vacc)
ax2.plot(ca["date"], ca["vaccinations_administered"], color=color_vacc,
         linewidth=1.4, alpha=0.7, linestyle="--", label="Vaccinations")
ax2.tick_params(axis="y", labelcolor=color_vacc)

ax1.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
ax1.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
plt.xticks(rotation=45)

lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper left", fontsize=9)

plt.title("California: COVID Cases vs. Vaccinations (2021–2022)", fontsize=13)
plt.tight_layout()
plt.savefig("chart4_ca_cases_vs_vaccinations.png", dpi=150)
plt.close()
print("Saved chart4_ca_cases_vs_vaccinations.png")