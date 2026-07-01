"""Central configuration: paths, column mapping, and domain constants.

Keeping every magic value here means the cleaning/analysis/plotting code
reads cleanly and there is a single place to change a path or a threshold.
"""

from pathlib import Path

# --- Paths -------------------------------------------------------------------
ROOT = Path(__file__).resolve().parent.parent
RAW_CSV = ROOT / "data.csv"
OUTPUT_DIR = ROOT / "outputs"
CLEAN_CSV = OUTPUT_DIR / "fires_clean.csv"
DASHBOARD_PNG = OUTPUT_DIR / "dashboard.png"
QUALITY_REPORT = OUTPUT_DIR / "data_quality_report.txt"

# --- Raw -> tidy column names ------------------------------------------------
# The raw header has trailing spaces and a long junk column; we rename to short,
# code-friendly names and drop everything not needed downstream.
COLUMN_MAP = {
    "Year": "year",
    "District": "district",
    "Block": "block",
    "Satellite": "satellite",
    "Date": "date_raw",
    "Time (IST)": "time_ist",
    "Day / Night": "day_night",
    "Fire Power(W/m2)": "fire_power_wm2",
    "Corrected_long": "lon",
    "corrected_lat": "lat",
    "Graama": "village",
}

# --- Domain constants --------------------------------------------------------
# Punjab's geographic bounding box (with a small margin). Used to flag rows
# whose latitude was overwritten by the longitude value.
PUNJAB_LAT = (29.0, 33.0)
PUNJAB_LON = (73.5, 77.0)

# Paddy-harvest burning season; used for labelling and seasonal share metrics.
FIRE_SEASON_MONTHS = (10, 11)

# Valid satellite-detected fire categories; rows with anything else in the
# day/night field are column-shifted and dropped.
VALID_DAY_NIGHT = ("Day", "Night")
