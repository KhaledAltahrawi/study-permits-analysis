# Canadian Study Permits Data Analysis (2015 – 2026)

[![Live Report](https://img.shields.io/badge/Live_Report-Interactive_Dashboard-2563eb?style=for-the-badge&logo=google-chrome&logoColor=white)](https://KhaledAltahrawi.github.io/study-permits-analysis/)
[![Python: 3.10+](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-059669?style=for-the-badge)](LICENSE)
[![Data Source](https://img.shields.io/badge/Data_Source-IRCC_Open_Data-0f172a?style=for-the-badge)](https://open.canada.ca/data/en/dataset/90115b00-f9b8-49e8-afa3-b4cff8facaee)

An empirical data analysis examining trends, source countries, seasonality, and the measurable impact of federal policy caps on Canadian study permits issued between **January 2015 and August 2026**.

---

## 🌐 Live Interactive Report

Explore the visual data storytelling report:  
👉 **[https://KhaledAltahrawi.github.io/study-permits-analysis/](https://KhaledAltahrawi.github.io/study-permits-analysis/)**

---

## 📊 Key Findings & Policy Cap Impact

- **Decade of Growth & The 2023 Peak:** Total study permits expanded from ~352,000 in 2015 to an all-time historic high of **1,401,690 in 2023**.
- **The Policy Cap Contraction (2024–2025):** 
  - **2024:** Issuance fell **-19.9%** (to 1,062,375) following initial cap announcements.
  - **2025:** Contraction deepened by **-34.8%** (to 802,015) as provincial attestation letters (PALs) took full effect.
- **2026 Stabilization:** Through August 2026, **478,690** permits were issued, tracking at a stabilized rate (-2.4%) relative to the aligned 2025 window.
- **Top Source Nations:** The leading countries of citizenship over the 12-year period are **India**, **China**, **Nigeria**, the **Philippines**, and **France**.
- **Seasonal Rhythm:** Permit issuance demonstrates persistent seasonality, peaking heavily in **August and September** ahead of Fall semester university intakes.

---

## 📁 Repository Structure

```text
├── Canada_Study_Permits_Analysis.ipynb  # Interactive Jupyter notebook
├── pipeline.py                          # Automated data retrieval & chart generation
├── index.html                           # Visual storytelling web report (GitHub Pages)
├── study_permits_by_country_2015_2026.xlsx # Official IRCC dataset (latest release)
├── images/                              # Programmatically rendered figures
│   ├── yearly_permits_trend.png
│   ├── top_10_countries.png
│   ├── top_5_countries_trends_grouped_bars.png
│   ├── monthly_distribution.png
│   └── ytd_yoy_change.png
├── requirements.txt                     # Python dependencies
└── README.md
```

---

## ⚡ Automated Pipeline (`pipeline.py`)

This repository includes a standalone automated Python pipeline that pulls the latest official XLSX directly from the IRCC portal, handles multi-index restructuring, and regenerates all visualizations in a single run:

```bash
python pipeline.py
```

---

## 💻 Local Setup & Execution

1. **Clone the repository:**
   ```bash
   git clone https://github.com/KhaledAltahrawi/study-permits-analysis.git
   cd study-permits-analysis
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the pipeline or Jupyter Notebook:**
   ```bash
   # Run automated pipeline
   python pipeline.py

   # Or explore interactively
   jupyter notebook Canada_Study_Permits_Analysis.ipynb
   ```

---

## 📄 License & Attribution

- **Author**: [Khaled Altahrawi](https://github.com/KhaledAltahrawi) | [Portfolio](https://KhaledAltahrawi.github.io/portfolio/)
- **Data Source**: Immigration, Refugees and Citizenship Canada (IRCC) Open Data Portal under the [Open Government Licence – Canada](https://open.canada.ca/en/open-government-licence-canada).
