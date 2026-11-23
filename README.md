# Canadian Study Permits Data Analysis (2015 – 2026)

[![Live Report](https://img.shields.io/badge/Live_Report-Interactive_Dashboard-2563eb?style=for-the-badge&logo=google-chrome&logoColor=white)](https://KhaledAltahrawi.github.io/study-permits-analysis/)
[![Monthly Data Sync](https://img.shields.io/badge/GitHub_Actions-Auto--Sync_Active-10b981?style=for-the-badge&logo=githubactions&logoColor=white)](https://github.com/KhaledAltahrawi/study-permits-analysis/actions/workflows/auto-update.yml)
[![Test Suite](https://img.shields.io/badge/pytest-8%20passed-10b981?style=for-the-badge&logo=pytest&logoColor=white)](tests/)
[![Data Dictionary](https://img.shields.io/badge/Data_Governance-DATA__DICTIONARY.md-0284c7?style=for-the-badge&logo=markdown&logoColor=white)](DATA_DICTIONARY.md)
[![Python: 3.10+](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-059669?style=for-the-badge)](LICENSE)
[![Data Source](https://img.shields.io/badge/Data_Source-IRCC_Open_Data-0f172a?style=for-the-badge)](https://open.canada.ca/data/en/dataset/90115b00-f9b8-49e8-afa3-b4cff8facaee)

An empirical data analysis examining trends, source countries, seasonality, and the measurable impact of federal policy caps on Canadian study permits issued between **January 2015 and September 2026**.

---

## 🌐 Live Interactive Report

Explore the visual data storytelling report featuring real-time interactive charts, dual-country comparisons, and one-click CSV export:  
👉 **[https://KhaledAltahrawi.github.io/study-permits-analysis/](https://KhaledAltahrawi.github.io/study-permits-analysis/)**

---

## 📊 Key Findings & Policy Cap Impact

- **Decade of Growth & The 2023 Peak:** Total study permits expanded from **226,860 in 2015** to an all-time historic high of **700,395 in 2023**.
- **The Policy Cap Contraction (2024–2025):** 
  - **2024:** Issuance fell **-24.2%** (down to 530,590) following initial cap announcements.
  - **2025:** Contraction deepened by **-24.6%** (down to 400,245) as provincial attestation letters (PALs) took full effect.
- **2026 Stabilization:** Through September 2026, **273,805** permits were issued, tracking at a stabilized rate relative to the post-cap baseline.
- **Top Source Nations:** Leading source countries over the 12-year period are **India (1.54M)**, **China (795K)**, **Nigeria (180K)**, **France (168K)**, and **South Korea (159K)**.
- **Seasonal Rhythm:** Permit issuance demonstrates persistent seasonality, peaking heavily in **August (~1.09M cumulative permits)** ahead of Fall semester intakes.

---

## 💡 Strategic Implications for Canadian Institutions

1. **Source Corridor Diversification:** Over-reliance on singular source corridors (India accounted for >40% of peak volumes) generated severe institutional volatility under PAL allocation caps. Recruitment strategy must pivot toward Latin America (Brazil, Colombia) and Francophone West Africa.
2. **Curriculum Realignment:** As Post-Graduation Work Permit (PGWP) eligibility ties closer to national labor market priorities, academic portfolios must lean into healthcare, STEM, and skilled trades.
3. **Housing Capacity as the New Ceiling:** Provincial attestation allocations increasingly factor municipal rental vacancy rates, shifting the institutional bottleneck from lecture hall capacity to community housing availability.

---

## 📁 Repository Structure

```text
├── .github/workflows/
│   └── auto-update.yml                  # Monthly automated data sync & CI/CD workflow
├── scripts/
│   ├── fetch_data.py                    # Dataset validation, SHA256 diff, & retrieval utility
│   └── sync_notebook.py                 # Jupyter notebook synchronization utility
├── tests/
│   └── test_pipeline.py                 # Automated test suite (8 unit & data assertion tests)
├── data/
│   ├── study_permits_data.json          # Structured dataset for analytical consumption
│   └── study_permits_data.js            # Zero-latency data bundle for interactive web report
├── images/                              # High-resolution programmatically rendered figures
│   ├── yearly_permits_trend.png
│   ├── top_10_countries.png
│   ├── top_5_countries_trends_grouped_bars.png
│   ├── monthly_distribution.png
│   └── ytd_yoy_change.png
├── index.html                           # Modern interactive dashboard (Chart.js & Inter UI)
├── pipeline.py                          # End-to-end data processing & figure generation
├── Canada_Study_Permits_Analysis.ipynb  # Interactive Jupyter notebook
├── study_permits_by_country_2015_2026.xlsx # Official IRCC dataset (latest release)
├── DATA_DICTIONARY.md                   # Data governance, schema definitions & validation rules
├── requirements.txt                     # Python dependencies
└── README.md
```

---

## 🔄 Automated CI/CD Data Sync & Testing

The repository runs an automated **GitHub Actions** cron workflow:
1. **Schedule:** Runs automatically on the **5th of every month** (aligned with IRCC open data publication cycles).
2. **Checksum Verification:** `scripts/fetch_data.py` downloads candidate releases, validates the Excel hierarchy, and compares cryptographic SHA256 checksums.
3. **Selective Pipeline Run:** Only if a new dataset is detected does it trigger `pipeline.py`, updating figures and structured JSON/JS.
4. **Automated Testing:** Runs `pytest tests/ -v` to assert data integrity, non-negativity, and schema validity before pushing.
5. **Auto-Deploy:** Commits updates directly via `github-actions[bot]`, which immediately refreshes the live GitHub Pages dashboard.

---

## 🧪 Running Automated Tests

Run the test suite locally using `pytest`:

```bash
pytest tests/ -v
```

---

## 📄 License & Attribution

- **Author**: [Khaled Altahrawi](https://github.com/KhaledAltahrawi) | [Portfolio](https://KhaledAltahrawi.github.io/portfolio/)
- **Data Source**: Immigration, Refugees and Citizenship Canada (IRCC) Open Data Portal under the [Open Government Licence – Canada](https://open.canada.ca/en/open-government-licence-canada).
