"""
IRCC Study Permits Data Ingestion & Sync Utility
Author: Khaled Altahrawi
Description:
    Fetches candidate releases from the official IRCC Open Data Portal,
    validates Excel structure, checks cryptographic SHA256 checksums,
    and selectively triggers the analytical data pipeline upon new data releases.
"""

import os
import sys
import hashlib
import urllib.request
import pandas as pd

IRCC_DATA_URL = "https://www.ircc.canada.ca/opendata-donneesouvertes/data/EN_ODP-TR-Study-IS_CITZ_sign_date.xlsx"
LOCAL_DATASET = "study_permits_by_country_2015_2026.xlsx"
TEMP_FILE = "temp_latest_dataset.xlsx"


def file_sha256(path):
    """Compute SHA256 hex digest for a file."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()


def check_and_update():
    """
    Download candidate dataset, validate Excel integrity, and compare checksums.
    Returns True if a new dataset was applied, False otherwise.
    """
    print(f"--> Connecting to IRCC Open Data Portal: {IRCC_DATA_URL}")
    req = urllib.request.Request(
        IRCC_DATA_URL,
        headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    )

    try:
        with urllib.request.urlopen(req, timeout=90) as response, open(TEMP_FILE, "wb") as out_file:
            out_file.write(response.read())
        download_size_kb = os.path.getsize(TEMP_FILE) / 1024
        print(f"--> Downloaded candidate dataset: {download_size_kb:.1f} KB")
    except Exception as e:
        print(f"[!] Warning: Network retrieval from IRCC failed: {e}")
        # Return False rather than crashing workflow to tolerate temporary upstream downtime
        return False

    # Validation: Ensure candidate file is a non-empty, readable Excel workbook
    try:
        with pd.ExcelFile(TEMP_FILE) as xl:
            if len(xl.sheet_names) == 0:
                raise ValueError("Downloaded file contains 0 Excel sheets.")
            print(f"--> Validation passed: Workbook readable with sheets: {xl.sheet_names}")
    except Exception as e:
        print(f"[!] Validation failed: Candidate file is not valid Excel ({e})")
        if os.path.exists(TEMP_FILE):
            os.remove(TEMP_FILE)
        return False

    # Checksum comparison
    current_hash = file_sha256(LOCAL_DATASET) if os.path.exists(LOCAL_DATASET) else None
    temp_hash = file_sha256(TEMP_FILE)

    print(f"--> Current dataset SHA256: {current_hash}")
    print(f"--> Candidate dataset SHA256: {temp_hash}")

    if current_hash == temp_hash:
        print("--> Dataset is identical (no new release detected).")
        if os.path.exists(TEMP_FILE):
            os.remove(TEMP_FILE)
        return False
    else:
        print("--> NEW DATASET RELEASE DETECTED! Updating local dataset file...")
        import shutil
        if os.path.exists(LOCAL_DATASET):
            os.remove(LOCAL_DATASET)
        shutil.move(TEMP_FILE, LOCAL_DATASET)
        return True


if __name__ == "__main__":
    force_run = "--force" in sys.argv or "--run-always" in sys.argv
    has_update = check_and_update()

    # Export outcome for GitHub Actions
    if "GITHUB_OUTPUT" in os.environ:
        with open(os.environ["GITHUB_OUTPUT"], "a") as gh_out:
            gh_out.write(f"updated={'true' if (has_update or force_run) else 'false'}\n")

    if has_update or force_run:
        print("--> Launching analytical data pipeline...")
        # Add root directory to sys.path so pipeline can be imported
        sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
        import pipeline
        pipeline.run_pipeline()
    else:
        print("--> System is up to date. No pipeline execution needed.")
