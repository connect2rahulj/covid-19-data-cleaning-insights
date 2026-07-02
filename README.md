# COVID-19 Data Cleaning + Insights

A beginner-to-intermediate data analysis project that demonstrates a full pipeline: loading messy data, cleaning it with Pandas, computing key metrics, and visualizing trends.

## Project Overview

This project uses a synthetic (but realistic) COVID-19 dataset to walk through:
- Handling missing values and data type issues
- Computing rolling averages and growth rates
- Identifying peak infection periods
- Visualizing trends with Matplotlib/Seaborn

## Files

| File | Description |
|------|-------------|
| `generate_data.py` | Generates a realistic but intentionally messy CSV dataset |
| `analysis.py` | Cleans the data and computes trend metrics |
| `visualize.py` | Produces charts from the cleaned data |
| `findings.md` | Written summary of key insights |

## How to Run

1. **Install dependencies**
```bash
pip install pandas matplotlib seaborn numpy
```

2. **Generate the dataset**
```bash
python generate_data.py
```

3. **Run the analysis**
```bash
python analysis.py
```

4. **Generate visualizations**
```bash
python visualize.py
```

Charts will be saved as PNG files in the project directory.

## Key Skills Demonstrated

- **Python**: scripting, functions, file I/O
- **Pandas**: data cleaning, groupby, rolling windows, merging
- **Data Visualization**: Matplotlib, Seaborn, multi-panel charts
- **Data Thinking**: identifying trends, handling real-world data messiness

## Sample Findings

See `findings.md` for a written summary of what the data reveals about case trends, peak periods, and vaccination correlation.

## Requirements

- Python 3.8+
- pandas
- numpy
- matplotlib
- seaborn