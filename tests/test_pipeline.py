"""
Automated Test Suite for Canada Study Permits Data Pipeline
Author: Khaled Altahrawi
"""
import os
import json
import pytest
import pandas as pd
import numpy as np

REPO_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
JSON_PATH = os.path.join(REPO_DIR, "data", "study_permits_data.json")
JS_PATH = os.path.join(REPO_DIR, "data", "study_permits_data.js")
EXCEL_PATH = os.path.join(REPO_DIR, "study_permits_by_country_2015_2026.xlsx")


def load_dataset_payload():
    assert os.path.exists(JSON_PATH), f"Missing data output: {JSON_PATH}"
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


class TestDataIntegrity:
    """Validate data output contract, consistency, and sanity bounds."""

    def test_json_payload_structure(self):
        payload = load_dataset_payload()
        required_keys = ["summary", "yearly_trend", "top_10", "seasonality", "yoy_change", "countries"]
        for key in required_keys:
            assert key in payload, f"Missing required payload key: {key}"

    def test_summary_kpi_bounds(self):
        payload = load_dataset_payload()
        s = payload["summary"]
        assert s["peak_year"] == 2023
        assert 650000 <= s["peak_permits"] <= 750000, "2023 peak out of verified bounds"
        assert s["grand_total"] > 4500000, "Grand total lower than expected"
        assert s["latest_year"] == 2026
        assert s["y2024_drop_pct"] < 0, "2024 cap should indicate contraction"
        assert s["y2025_drop_pct"] < 0, "2025 cap should indicate contraction"

    def test_double_counting_absence(self):
        payload = load_dataset_payload()
        # Verify 2023 permits is ~700K (NOT 1.4M from duplicate row)
        years = payload["yearly_trend"]["years"]
        totals = payload["yearly_trend"]["totals"]
        idx_2023 = years.index(2023)
        assert 690000 <= totals[idx_2023] <= 710000, "2023 total exhibits duplicate counting anomaly"

    def test_non_negative_values(self):
        payload = load_dataset_payload()
        for c_name, c_data in payload["countries"].items():
            assert c_data["total"] >= 0, f"Negative total detected for {c_name}"
            assert all(v >= 0 for v in c_data["values"]), f"Negative value in history for {c_name}"

    def test_seasonality_months_complete(self):
        payload = load_dataset_payload()
        months = payload["seasonality"]["months"]
        assert len(months) == 12, "Seasonality must contain 12 calendar months"
        assert payload["seasonality"]["totals"][months.index("Aug")] > 900000, "August must reflect peak volume"

    def test_key_source_countries_present(self):
        payload = load_dataset_payload()
        countries = payload["countries"]
        key_nations = ["India", "Nigeria", "France", "Philippines", "Brazil"]
        for nation in key_nations:
            assert nation in countries, f"Key nation {nation} missing from dataset"


class TestPipelineFunctions:
    """Validate data transformation logic."""

    def test_multiindex_flattening(self):
        import pipeline
        assert pipeline.flatten_multiindex(('2023', 'Q1', 'Jan')) == '2023 - Q1 - Jan'
        assert pipeline.flatten_multiindex(('Country', 'Unnamed: 0_level_1')) == 'Country'

    def test_temporal_extraction(self):
        import pipeline
        assert pipeline.MONTH_MAP['Jan'] == 1
        assert pipeline.MONTH_MAP['Dec'] == 12
        assert len(pipeline.MONTH_MAP) == 12
