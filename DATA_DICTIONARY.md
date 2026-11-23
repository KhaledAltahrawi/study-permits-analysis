# Data Dictionary: Canadian Study Permits Dataset (2015 – 2026)

**Data Provider:** Immigration, Refugees and Citizenship Canada (IRCC)  
**License:** [Open Government Licence – Canada](https://open.canada.ca/en/open-government-licence-canada)  
**Maintenance Policy:** Synchronized monthly via automated GitHub Actions pipeline.

---

## 1. Dataset Overview

This dataset captures monthly counts of initial and extension Canadian study permits issued to international students by country of citizenship. The original release is distributed in hierarchical multi-index Excel workbooks, transformed by our ingestion pipeline into tidy long-format records and consumed by analytical dashboards.

---

## 2. Entity Schema & Attributes (Tidy Long Format: `df_long`)

| Attribute | Data Type | Nullable | Primary Key | Valid Values / Range | Description & Business Rules |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `Country of Citizenship` | `string` | No | Compound (1/4) | 181 standardized nations | Recognized country or territory of passport citizenship. Excludes summary and aggregate metadata rows. |
| `Year` | `integer` | No | Compound (2/4) | `2015` – `2026` | Calendar year in which the study permit became effective. |
| `Quarter` | `string` | No | Compound (3/4) | `Q1`, `Q2`, `Q3`, `Q4` | Fiscal/calendar quarter corresponding to the effective month. |
| `Month` | `string` | No | Compound (4/4) | `Jan` – `Dec` | Three-letter calendar month abbreviation. |
| `Number of Students` | `integer` | No | No | `≥ 0` | Total count of study permits issued. Small cell privacy suppressions (`--`) are mapped to `0`. |

---

## 3. Data Hygiene & Contract Integrity Rules

### Rule 1: Exclusion of Aggregate Summary Rows (Double-Counting Prevention)
* **Raw Column:** `Country of Citizenship`
* **Raw Value:** `'Total unique persons'`
* **Contract Rule:** **MUST BE FILTERED OUT.**
* **Rationale:** In IRCC open data releases, the row labeled `Total unique persons` is a pre-aggregated sum of all countries. Retaining this row within granular melts artificially doubles all national, quarterly, and annual figures.

### Rule 2: Privacy Suppression Handling
* **Raw Value:** `'--'`
* **Contract Rule:** Mapped to `0`.
* **Rationale:** In accordance with federal privacy protocols, cells with values between 1 and 4 are occasionally masked as `--` to prevent individual re-identification. They are imputed as `0` for numeric aggregation stability.

### Rule 3: Dynamic Temporal Boundaries
* **Contract Rule:** The latest tracked year is evaluated for month completeness (`months_count < 12`).
* **Rationale:** Partial years are dynamically annotated as **YTD (Year-to-Date)** in all figures and percentages to prevent false negative annual comparisons.

---

## 4. Analytical Data Outputs (`data/`)

* **`data/study_permits_data.json`**: Key-value JSON payload containing precomputed summaries, 12-year longitudinal totals, seasonality distributions, and country-level historical arrays for programmatic ingestion.
* **`data/study_permits_data.js`**: Zero-latency JavaScript wrapper (`window.PERMITS_DATA`) enabling static client-side rendering on GitHub Pages without CORS dependencies.
