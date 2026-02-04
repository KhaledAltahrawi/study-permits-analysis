## Study Permit Data Analysis (Canada, 2015 – November 2025)

This repository presents a comprehensive data analysis project focused on identifying trends and patterns in **Canadian study permits** issued between **January 2015 and November 2025**.  
The analysis uses **monthly, country-level data** from the Government of Canada’s Open Data portal and applies a structured data-cleaning, validation, and visualization pipeline to ensure accuracy, consistency, and reproducibility.

The project explores:

- Long-term issuance trends
- Top source countries
- Seasonal (monthly) distribution patterns
- Year-over-year (YoY) percentage changes with proper year-to-date (YTD) handling

---

## Data Source

The dataset used in this project was obtained from the Government of Canada's Open Data portal:

📊 [Study permits – Monthly data 2015 to 2025](https://open.canada.ca/data/en/dataset/90115b00-f9b8-49e8-afa3-b4cff8facaee)

> **Important note on data coverage:**  
> The most recent dataset includes data **through November 2025 only**.  
> As a result, all 2025 figures in this analysis are treated explicitly as **year-to-date (YTD)** values, and comparisons are adjusted accordingly to maintain consistency.

---

## Repository Contents

- **`Canada_Study_Permits_Analysis.ipynb`**  
  Main Jupyter Notebook containing the full analysis pipeline:
  - Robust data loading and cleaning
  - Validation and consistency checks
  - Transformation to long-format monthly data
  - Exploratory data analysis
  - Generation of publication-ready visualizations

- **`study_permits_by_country_2015_2025.xlsx`**  
  Original Excel dataset used for analysis (unmodified source data)

- **`images/`**  
  Static `.png` images generated programmatically from the notebook:
  - `yearly_permits_trend.png` – Total study permits per year (2015–November 2025) with smart labels and grand total
  - `top_10_countries.png` – Top 10 countries of citizenship (cumulative total)
  - `top_5_countries_trends_grouped_bars.png` – Grouped bar chart showing YTD trends for the top 5 countries
  - `monthly_distribution.png` – Aggregate monthly distribution across all years (seasonality)
  - `ytd_yoy_change.png` – Year-over-year % change (2016–2024 full years; 2025 YTD through November)

- **`reports/`**  
  Interactive HTML outputs:
  - `yearly_permits_trend.html` – Interactive Plotly visualization of yearly totals

- **`requirements.txt`**  
  Python dependencies required to run the notebook

- **`.gitignore`**  
  Excludes checkpoints, virtual environments, and temporary files

---

## Key Improvements (2026 Update)

Compared to earlier versions, this iteration introduces several structural and analytical improvements:

- Explicit **data validation and cleaning steps** to ensure numeric integrity
- Clear and consistent handling of **partial-year (YTD) data** for 2025
- Year-over-year comparisons computed using **aligned month ranges**
- Improved visualization clarity with annotations, labels, and contextual notes
- Modular notebook structure designed for **future extensions**, such as regional aggregation or additional years of data

---

## Key Findings

- **Overall Trend:**  
  Study permit issuance in Canada shows a sustained upward trend from 2015 through 2024.  
  The partial 2025 data (January–November) indicates continued high issuance levels.  
  ![Yearly Trend](images/yearly_permits_trend.png)

- **Top Source Countries:**  
  Between 2015 and November 2025, the leading source countries are **India**, **China**, **Nigeria**, **Philippines**, and **France**.  
  ![Top 10 Countries](images/top_10_countries.png)

- **Monthly Distribution:**  
  Permit issuance demonstrates strong seasonality, peaking around **August–September** (academic intake periods) and **December**, with notable dips in **February**, **March**, and **October**.  
  ![Monthly Distribution](images/monthly_distribution.png)

- **Year-over-Year Change:**  
  The YoY analysis highlights a strong rebound in 2021 following the pandemic-related decline, followed by more variable growth patterns.  
  The 2025 value is presented strictly as a **YTD comparison (Jan–Nov)**.  
  ![YoY Change](images/ytd_yoy_change.png)

- **Top 5 Countries Trends:**  
  The grouped bar analysis shows consistent growth among major source countries, particularly **India** and **Nigeria**, over the past decade.  
  ![Top 5 Countries Trends](images/top_5_countries_trends_grouped_bars.png)

---

## How to Run

1. **Clone this repository**

   ```bash
   git clone https://github.com/KhaledAltahrawi/study-permits-analysis.git
   cd study-permits-analysis

   ```

2. **Set up a virtual environment (recommended)**

```bash
  python -m venv venv
  source venv/bin/activate
  # on Windows: venv\Scripts\activate

```

3. **Install required packages**

```bash
   pip install -r requirements.txt

```

4. **Run the Jupyter Notebook**

```bash
 jupyter notebook

```

5. **Then open Canada_Study_Permits_Analysis.ipynb and select Run All.**
   This will automatically generate the latest charts under /images/ and the interactive report under /reports/.

## Contact

Khaled Altahrawi
https://github.com/KhaledAltahrawi
Khaled.tahrawi16@gmail.com
