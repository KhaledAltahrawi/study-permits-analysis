"""
Canada Study Permits Data Pipeline (2015 - 2026)
Author: Khaled Altahrawi
Description:
    Automated data retrieval, cleaning, validation, and visualization pipeline.
    Pulls the latest open dataset from Immigration, Refugees and Citizenship Canada (IRCC),
    processes multi-index Excel hierarchies into tidy long-format records,
    and programmatically renders high-resolution analytical visualizations
    and structured JSON for the interactive web dashboard.
"""

import os
import json
import calendar
import urllib.request
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from matplotlib.ticker import FuncFormatter

# 1. Configuration & Constants
IRCC_DATA_URL = "https://www.ircc.canada.ca/opendata-donneesouvertes/data/EN_ODP-TR-Study-IS_CITZ_sign_date.xlsx"
EXCEL_FILE = "study_permits_by_country_2015_2026.xlsx"
IMAGES_DIR = "images"
REPORTS_DIR = "reports"
DATA_DIR = "data"

MONTH_MAP = {
    'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4,
    'May': 5, 'Jun': 6, 'Jul': 7, 'Aug': 8,
    'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12
}

os.makedirs(IMAGES_DIR, exist_ok=True)
os.makedirs(REPORTS_DIR, exist_ok=True)
os.makedirs(DATA_DIR, exist_ok=True)


def download_latest_dataset(force=False):
    """Fetch the latest official XLSX release from the IRCC Open Data portal if not present or forced."""
    if force or not os.path.exists(EXCEL_FILE):
        print("--> Fetching latest official dataset from IRCC Open Data Portal...")
        req = urllib.request.Request(
            IRCC_DATA_URL,
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        )
        with urllib.request.urlopen(req, timeout=90) as response, open(EXCEL_FILE, "wb") as f:
            f.write(response.read())
        size_kb = os.path.getsize(EXCEL_FILE) / 1024
        print(f"--> Downloaded: {EXCEL_FILE} ({size_kb:.1f} KB)")
    else:
        print(f"--> Using existing dataset: {EXCEL_FILE}")


def load_and_clean_data():
    """Parse multi-index Excel file and reshape into a clean, long-format DataFrame."""
    print("--> Loading and parsing Excel MultiIndex hierarchy...")
    # Skip introductory rows (2) and metadata footnotes (7)
    df = pd.read_excel(EXCEL_FILE, skiprows=2, skipfooter=7, header=[0, 1, 2])

    def flatten_multiindex(col):
        if isinstance(col, tuple):
            return ' - '.join(str(x) for x in col if 'Unnamed' not in str(x))
        return col

    df.columns = df.columns.map(flatten_multiindex)
    # Normalize country column name across variants
    country_col = [c for c in df.columns if 'Country of Citizenship' in c][0]
    df.rename(columns={country_col: 'Country of Citizenship'}, inplace=True)

    # Exclude summary rows to prevent double-counting
    df = df[df['Country of Citizenship'] != 'Total unique persons'].copy()

    # Drop aggregate summary columns
    columns_to_drop = [col for col in df.columns if 'Total' in col]
    df_cleaned = df.drop(columns=columns_to_drop, errors='ignore')

    # Melt to long format
    df_long = pd.melt(
        df_cleaned,
        id_vars=['Country of Citizenship'],
        var_name='Period',
        value_name='Number of Students'
    )

    # Extract Year, Quarter, Month
    def extract_period(period_str):
        parts = period_str.split(' - ')
        return pd.Series([int(parts[0]), parts[1], parts[2]])

    df_long[['Year', 'Quarter', 'Month']] = df_long['Period'].apply(extract_period)

    # Clean numeric count
    df_long['Number of Students'] = df_long['Number of Students'].replace('--', 0)
    df_long['Number of Students'] = df_long['Number of Students'].astype(str).str.replace(',', '', regex=False)
    df_long['Number of Students'] = pd.to_numeric(df_long['Number of Students'], errors='coerce').fillna(0).astype(int)

    return df_long


def extract_context(df_long):
    """Determine dynamic temporal boundaries and YTD status."""
    df_time = df_long.copy()
    df_time["MonthNum"] = df_time["Month"].map(MONTH_MAP).astype(int)

    first_year = int(df_time["Year"].min())
    latest_year = int(df_time["Year"].max())
    latest_month = int(df_time.loc[df_time["Year"] == latest_year, "MonthNum"].max())
    latest_month_name = calendar.month_name[latest_month]

    months_in_latest = df_time.loc[df_time["Year"] == latest_year, "MonthNum"].nunique()
    is_partial = months_in_latest < 12

    if is_partial:
        period_label = f"{first_year}–{latest_year} (YTD through {latest_month_name})"
        latest_label = f"{latest_year} YTD ({latest_month_name})"
    else:
        period_label = f"{first_year}–{latest_year}"
        latest_label = f"{latest_year} (Full Year)"

    return {
        "first_year": first_year,
        "latest_year": latest_year,
        "latest_month": latest_month,
        "latest_month_name": latest_month_name,
        "is_partial": is_partial,
        "period_label": period_label,
        "latest_label": latest_label
    }


def generate_visualizations(df_long, ctx):
    """Generate publication-ready visual charts matching the research standard."""
    print("--> Generating updated charts in images/ ...")

    # 1. Yearly Permits Trend
    yearly = df_long.groupby("Year", as_index=False)["Number of Students"].sum().sort_values("Year")
    years = yearly["Year"].tolist()
    values = yearly["Number of Students"].tolist()

    plt.figure(figsize=(12, 6))
    plt.plot(years, values, marker='o', linewidth=2.8, color="#1e3a8a", markersize=8)
    plt.title(f"Total Study Permits Issued in Canada ({ctx['period_label']})", fontsize=15, fontweight="bold", pad=15)
    plt.xlabel("Year", fontsize=12)
    plt.ylabel("Number of Students", fontsize=12)
    plt.gca().yaxis.set_major_formatter(FuncFormatter(lambda v, p: f"{int(v):,}"))
    plt.grid(True, linestyle="--", alpha=0.5)

    for i, (yr, val) in enumerate(zip(years, values)):
        offset = 8000 if i % 2 == 0 else -12000
        plt.annotate(
            f"{val:,}",
            xy=(yr, val),
            xytext=(0, 10 if offset > 0 else -15),
            textcoords="offset points",
            ha='center',
            fontsize=9.5,
            fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="#cbd5e1", alpha=0.9)
        )

    if ctx['is_partial']:
        plt.axvline(ctx['latest_year'], color='#dc2626', linestyle='--', alpha=0.7)
        plt.text(ctx['latest_year'] - 0.1, max(values) * 0.95, f"{ctx['latest_year']} YTD (Aug)",
                 color='#dc2626', ha='right', fontweight='bold', fontsize=10)

    plt.tight_layout()
    plt.savefig(os.path.join(IMAGES_DIR, "yearly_permits_trend.png"), dpi=300)
    plt.close()

    # 2. Top 10 Countries
    top_10 = (
        df_long.groupby("Country of Citizenship")["Number of Students"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

    plt.figure(figsize=(14, 7))
    bars = plt.bar(top_10.index, top_10.values, color="#0284c7")
    plt.title(f"Top 10 Source Countries for Canadian Study Permits ({ctx['period_label']})", fontsize=15, fontweight="bold", pad=15)
    plt.xlabel("Country of Citizenship", fontsize=12)
    plt.ylabel("Total Permits Issued", fontsize=12)
    plt.xticks(rotation=40, ha="right", fontsize=10)
    plt.gca().yaxis.set_major_formatter(FuncFormatter(lambda v, p: f"{int(v):,}"))
    plt.grid(axis="y", linestyle="--", alpha=0.5)

    for bar in bars:
        h = int(bar.get_height())
        plt.text(bar.get_x() + bar.get_width() / 2, h + max(top_10.values) * 0.01, f"{h:,}",
                 ha="center", va="bottom", fontsize=9.5, fontweight="bold")

    plt.tight_layout()
    plt.savefig(os.path.join(IMAGES_DIR, "top_10_countries.png"), dpi=300)
    plt.close()

    # 3. Top 5 Countries Trends (Grouped Bars)
    top_5_countries = top_10.head(5).index.tolist()
    df_ytd = df_long.copy()
    df_ytd["MonthNum"] = df_ytd["Month"].map(MONTH_MAP).astype(int)

    if ctx['is_partial']:
        df_ytd = df_ytd[
            (df_ytd["Year"] < ctx['latest_year']) |
            ((df_ytd["Year"] == ctx['latest_year']) & (df_ytd["MonthNum"] <= ctx['latest_month']))
        ]

    ytd_group = (
        df_ytd[df_ytd["Country of Citizenship"].isin(top_5_countries)]
        .groupby(["Year", "Country of Citizenship"], as_index=False)["Number of Students"]
        .sum()
    )

    all_years = sorted(ytd_group["Year"].unique().tolist())
    x = np.arange(len(all_years))
    width = 0.8 / len(top_5_countries)
    colors = ["#1e3a8a", "#0284c7", "#0d9488", "#d97706", "#dc2626"]

    fig, ax = plt.subplots(figsize=(14, 6.5))
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v, p: f"{int(v):,}"))

    for idx, (country, clr) in enumerate(zip(top_5_countries, colors)):
        vals = [
            int(ytd_group.loc[(ytd_group["Year"] == yr) & (ytd_group["Country of Citizenship"] == country), "Number of Students"].sum())
            for yr in all_years
        ]
        ax.bar(x + idx * width - (len(top_5_countries) - 1) * width / 2, vals, width, label=country, color=clr)

    ax.set_title(f"Top 5 Countries – Study Permit Comparison ({ctx['first_year']}–{ctx['latest_label']})", fontsize=15, fontweight="bold")
    ax.set_xlabel("Year", fontsize=12)
    ax.set_ylabel("Number of Students", fontsize=12)
    ax.set_xticks(x)
    ax.set_xticklabels(all_years)
    ax.grid(axis="y", linestyle="--", alpha=0.4)
    ax.legend(title="Country of Citizenship", frameon=True, fontsize=10)

    plt.tight_layout()
    plt.savefig(os.path.join(IMAGES_DIR, "top_5_countries_trends_grouped_bars.png"), dpi=300)
    plt.close()

    # 4. Monthly Distribution (Seasonality)
    df_m = df_long.copy()
    df_m["MonthNum"] = df_m["Month"].map(MONTH_MAP).astype(int)
    if ctx['is_partial']:
        df_m = df_m[
            (df_m["Year"] < ctx['latest_year']) |
            ((df_m["Year"] == ctx['latest_year']) & (df_m["MonthNum"] <= ctx['latest_month']))
        ]

    monthly_totals = df_m.groupby("MonthNum", as_index=False)["Number of Students"].sum().sort_values("MonthNum")
    monthly_totals["MonthName"] = monthly_totals["MonthNum"].apply(lambda m: calendar.month_abbr[m])

    plt.figure(figsize=(13, 5.5))
    bars = plt.bar(monthly_totals["MonthName"], monthly_totals["Number of Students"], color="#3b82f6")
    plt.title(f"Cumulative Monthly Distribution of Study Permits ({ctx['period_label']})", fontsize=15, fontweight="bold", pad=15)
    plt.xlabel("Month", fontsize=12)
    plt.ylabel("Number of Students", fontsize=12)
    plt.gca().yaxis.set_major_formatter(FuncFormatter(lambda v, p: f"{int(v):,}"))
    plt.grid(axis="y", linestyle="--", alpha=0.4)

    for bar in bars:
        h = int(bar.get_height())
        plt.text(bar.get_x() + bar.get_width() / 2, h + 4000, f"{h:,}", ha="center", va="bottom", fontsize=9)

    plt.tight_layout()
    plt.savefig(os.path.join(IMAGES_DIR, "monthly_distribution.png"), dpi=300)
    plt.close()

    # 5. Year-over-Year % Change (Caps Policy Impact Analysis)
    df_yoy = df_long.copy()
    df_yoy["MonthNum"] = df_yoy["Month"].map(MONTH_MAP).astype(int)

    if ctx['is_partial']:
        # To make YoY fully aligned and fair, evaluate each year up to latest_month
        df_yoy_aligned = df_yoy[df_yoy["MonthNum"] <= ctx['latest_month']]
    else:
        df_yoy_aligned = df_yoy

    yoy_totals = df_yoy_aligned.groupby("Year", as_index=False)["Number of Students"].sum().sort_values("Year")
    yoy_totals["YoY_%"] = yoy_totals["Number of Students"].pct_change() * 100

    y_years = yoy_totals["Year"].tolist()
    y_vals = yoy_totals["YoY_%"].tolist()
    bar_colors = ["#10b981" if v >= 0 else "#ef4444" for v in y_vals]

    plt.figure(figsize=(13, 5.5))
    bars = plt.bar(y_years[1:], y_vals[1:], color=bar_colors[1:])
    plt.title(f"Year-over-Year % Change (Aligned Jan–{ctx['latest_month_name'][:3]} Window, {ctx['first_year']}–{ctx['latest_year']})", fontsize=14, fontweight="bold", pad=15)
    plt.xlabel("Year", fontsize=12)
    plt.ylabel("YoY Change (%)", fontsize=12)
    plt.axhline(0, color="black", linewidth=1)
    plt.gca().yaxis.set_major_formatter(FuncFormatter(lambda v, p: f"{v:+.1f}%"))
    plt.grid(axis="y", linestyle="--", alpha=0.4)
    plt.xticks(y_years[1:])

    for bar, val in zip(bars, y_vals[1:]):
        if np.isnan(val):
            continue
        y_pos = bar.get_height() + (1.2 if val >= 0 else -3.5)
        plt.text(bar.get_x() + bar.get_width() / 2, y_pos, f"{val:+.1f}%",
                 ha="center", va="bottom" if val >= 0 else "top", fontsize=9.5, fontweight="bold",
                 color="#065f46" if val >= 0 else "#991b1b")

    plt.tight_layout()
    plt.savefig(os.path.join(IMAGES_DIR, "ytd_yoy_change.png"), dpi=300)
    plt.close()

    print("--> All 5 visualizations successfully generated.")
    return yearly, top_10, yoy_totals, monthly_totals


def export_interactive_json(df_long, ctx, yearly, top_10, yoy_totals, monthly_totals):
    """
    Export structured, lightweight JSON for the interactive web frontend (Chart.js & Explorer).
    """
    print("--> Exporting structured JSON for interactive frontend...")

    # Grand total and yearly trend
    years_list = yearly["Year"].astype(int).tolist()
    totals_list = yearly["Number of Students"].astype(int).tolist()
    grand_total = int(sum(totals_list))

    # Top 10 countries
    top_10_dict = {
        "countries": top_10.index.tolist(),
        "totals": [int(v) for v in top_10.values]
    }

    # Seasonality
    seasonality_dict = {
        "months": monthly_totals["MonthName"].tolist(),
        "totals": monthly_totals["Number of Students"].astype(int).tolist()
    }

    # YoY Change
    yoy_dict = {
        "years": yoy_totals["Year"].astype(int).tolist()[1:],
        "rates": [round(float(v), 1) if not np.isnan(v) else 0.0 for v in yoy_totals["YoY_%"].tolist()[1:]]
    }

    # Build per-country yearly dictionary for all 220 countries
    country_yearly = df_long.groupby(["Country of Citizenship", "Year"])["Number of Students"].sum().unstack(fill_value=0)
    countries_data = {}
    for country in sorted(country_yearly.index.tolist()):
        c_series = country_yearly.loc[country].astype(int).tolist()
        c_total = int(sum(c_series))
        if c_total > 0:
            countries_data[country] = {
                "total": c_total,
                "values": c_series
            }

    # Calculate key policy metrics
    peak_val = int(yearly.loc[yearly["Year"] == 2023, "Number of Students"].values[0])
    y2024_val = int(yearly.loc[yearly["Year"] == 2024, "Number of Students"].values[0])
    y2025_val = int(yearly.loc[yearly["Year"] == 2025, "Number of Students"].values[0])
    y2026_val = int(yearly.loc[yearly["Year"] == 2026, "Number of Students"].values[0])

    data_payload = {
        "summary": {
            "grand_total": grand_total,
            "peak_year": 2023,
            "peak_permits": peak_val,
            "y2024_permits": y2024_val,
            "y2024_drop_pct": round(((y2024_val - peak_val) / peak_val) * 100, 1),
            "y2025_permits": y2025_val,
            "y2025_drop_pct": round(((y2025_val - y2024_val) / y2024_val) * 100, 1),
            "y2026_permits_ytd": y2026_val,
            "latest_period": ctx["period_label"],
            "latest_month": ctx["latest_month_name"],
            "latest_year": ctx["latest_year"],
            "years": years_list
        },
        "yearly_trend": {
            "years": years_list,
            "totals": totals_list
        },
        "top_10": top_10_dict,
        "seasonality": seasonality_dict,
        "yoy_change": yoy_dict,
        "countries": countries_data
    }

    json_path = os.path.join(DATA_DIR, "study_permits_data.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data_payload, f, ensure_ascii=False)

    js_path = os.path.join(DATA_DIR, "study_permits_data.js")
    with open(js_path, "w", encoding="utf-8") as f:
        f.write("window.PERMITS_DATA = " + json.dumps(data_payload, ensure_ascii=False) + ";\n")

    size_kb = os.path.getsize(json_path) / 1024
    print(f"--> Exported: {json_path} and {js_path} ({size_kb:.1f} KB, {len(countries_data)} countries)")


def run_pipeline(force_download=False):
    download_latest_dataset(force=force_download)
    df_long = load_and_clean_data()
    ctx = extract_context(df_long)
    print("\n=== PIPELINE CONTEXT ===")
    print(f"Data Span: {ctx['period_label']}")
    print(f"Total Rows (tidy): {len(df_long):,}")
    print(f"Distinct Countries: {df_long['Country of Citizenship'].nunique()}")

    yearly, top_10, yoy_totals, monthly_totals = generate_visualizations(df_long, ctx)
    export_interactive_json(df_long, ctx, yearly, top_10, yoy_totals, monthly_totals)

    print("\nPipeline execution finished successfully!")


if __name__ == "__main__":
    import sys
    force_dl = "--force-download" in sys.argv or "--force" in sys.argv
    run_pipeline(force_download=force_dl)
