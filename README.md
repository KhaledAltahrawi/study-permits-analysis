# Canadian Study Permits Data Analysis (2015 – 2026)

[![Live Report](https://img.shields.io/badge/Live_Report-Interactive_Dashboard-2563eb?style=for-the-badge&logo=google-chrome&logoColor=white)](https://KhaledAltahrawi.github.io/study-permits-analysis/)
[![Monthly Data Sync](https://img.shields.io/badge/GitHub_Actions-Auto--Sync_Active-10b981?style=for-the-badge&logo=githubactions&logoColor=white)](https://github.com/KhaledAltahrawi/study-permits-analysis/actions/workflows/auto-update.yml)
[![Python: 3.10+](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-059669?style=for-the-badge)](LICENSE)
[![Data Source](https://img.shields.io/badge/Data_Source-IRCC_Open_Data-0f172a?style=for-the-badge)](https://open.canada.ca/data/en/dataset/90115b00-f9b8-49e8-afa3-b4cff8facaee)

An empirical data analysis examining trends, source countries, seasonality, and the measurable impact of federal policy caps on Canadian study permits issued between **January 2015 and August 2026**.

---

## 🌐 Live Interactive Report

Explore the visual data storytelling report with real-time interactive charts and a dual-country comparison tool:  
👉 **[https://KhaledAltahrawi.github.io/study-permits-analysis/](https://KhaledAltahrawi.github.io/study-permits-analysis/)**

---

## 📊 Key Findings & Policy Cap Impact

- **Decade of Growth & The 2023 Peak:** Total study permits expanded from **226,435 in 2015** to an all-time historic high of **700,395 in 2023**.
- **The Policy Cap Contraction (2024–2025):** 
  - **2024:** Issuance fell **-24.2%** (down to 530,610) following initial cap announcements.
  - **2025:** Contraction deepened by **-24.5%** (down to 400,415) as provincial attestation letters (PALs) took full effect.
- **2026 Stabilization:** Through August 2026, **238,995** permits were issued, tracking at a stabilized rate (-2.4%) relative to the aligned 2025 window.
- **Top Source Nations:** Leading source countries over the 12-year period are **India (1.54M)**, **China (791K)**, **Nigeria (178K)**, **France (167K)**, and **South Korea (158K)**.
- **Seasonal Rhythm:** Permit issuance demonstrates persistent seasonality, peaking heavily in **August (~105K permits/month)** ahead of Fall semester intakes.

---

## 📁 Repository Structure

```text
├── .github/workflows/
│   └── auto-update.yml                  # Monthly automated data sync & CI/CD workflow
├── scripts/
│   └── fetch_data.py                    # Dataset validation, SHA256 diff, & retrieval utility
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
├── requirements.txt                     # Python dependencies
└── README.md
```

---

## 🔄 Automated CI/CD Data Sync (`auto-update.yml`)

The repository runs an automated **GitHub Actions** cron workflow:
1. **Schedule:** Runs automatically on the **5th of every month** (aligned with IRCC open data publication cycles).
2. **Checksum Verification:** `scripts/fetch_data.py` downloads candidate releases, validates the Excel hierarchy, and compares cryptographic SHA256 checksums.
3. **Selective Pipeline Run:** Only if a new dataset is detected does it trigger `pipeline.py`, updating figures and structured JSON/JS.
4. **Auto-Deploy:** Commits updates directly via `github-actions[bot]`, which immediately refreshes the live GitHub Pages dashboard.
5. **Manual Trigger:** Developers can also trigger immediate updates via GitHub's `workflow_dispatch` button.

---

## ⚡ Standalone Pipeline Execution

You can run the end-to-end processing pipeline locally:

```bash
python pipeline.py
```

To force a re-download from the IRCC portal:

```bash
python pipeline.py --force-download
```

---

## 💻 Local Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/KhaledAltahrawi/study-permits-analysis.git
   cd study-permits-analysis
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Explore via Jupyter Notebook:**
   ```bash
   jupyter notebook Canada_Study_Permits_Analysis.ipynb
   ```

---

## 📄 License & Attribution

- **Author**: [Khaled Altahrawi](https://github.com/KhaledAltahrawi) | [Portfolio](https://KhaledAltahrawi.github.io/portfolio/)
- **Data Source**: Immigration, Refugees and Citizenship Canada (IRCC) Open Data Portal under the [Open Government Licence – Canada](https://open.canada.ca/en/open-government-licence-canada).
