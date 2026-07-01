"""Load and clean the raw stubble-burning CSV.

Each step is a small pure function so the pipeline is easy to read, test, and
audit. `clean()` chains them together and returns the tidy DataFrame plus a
quality report describing exactly what was changed.
"""

from __future__ import annotations

import pandas as pd

from . import config


def load_raw() -> pd.DataFrame:
    """Read the raw CSV, keep only mapped columns, and rename to tidy names."""
    df = pd.read_csv(config.RAW_CSV, low_memory=False)
    df = df[list(config.COLUMN_MAP)].rename(columns=config.COLUMN_MAP)
    return df


def drop_shifted_rows(df: pd.DataFrame) -> pd.DataFrame:
    """Drop rows whose `day_night` is not Day/Night (whole row is misaligned)."""
    return df[df["day_night"].isin(config.VALID_DAY_NIGHT)].copy()


def standardize_district(df: pd.DataFrame) -> pd.DataFrame:
    """Collapse casing/whitespace variants (e.g. 'Amritsar' vs 'AMRITSAR')."""
    df["district"] = df["district"].str.upper().str.strip()
    df["block"] = df["block"].str.upper().str.strip()
    return df


def parse_dates(df: pd.DataFrame) -> pd.DataFrame:
    """Unify mixed date formats ('16-Sep-21' and '18/9/2021') into datetimes."""
    df["date"] = pd.to_datetime(
        df["date_raw"], format="mixed", dayfirst=True, errors="coerce"
    )
    df["month"] = df["date"].dt.month
    return df.drop(columns=["date_raw"])


def flag_geo_validity(df: pd.DataFrame) -> pd.DataFrame:
    """Flag rows whose coordinates fall outside Punjab (latitude corruption).

    In ~6.8k rows the latitude was overwritten with the longitude value, so the
    point is unmappable. We keep these rows for time/district analysis but mark
    `geo_valid=False` so mapping code can exclude them.
    """
    lat_ok = df["lat"].between(*config.PUNJAB_LAT)
    lon_ok = df["lon"].between(*config.PUNJAB_LON)
    df["geo_valid"] = lat_ok & lon_ok
    return df


def clean() -> tuple[pd.DataFrame, dict]:
    """Run the full cleaning pipeline and return (clean_df, quality_report)."""
    raw = load_raw()
    report = {"rows_raw": len(raw)}

    df = drop_shifted_rows(raw)
    report["rows_dropped_shifted"] = len(raw) - len(df)

    df = standardize_district(df)
    df = parse_dates(df)
    df = flag_geo_validity(df)

    report["rows_clean"] = len(df)
    report["unparseable_dates"] = int(df["date"].isna().sum())
    report["geo_invalid"] = int((~df["geo_valid"]).sum())
    report["missing_fire_power"] = int(df["fire_power_wm2"].isna().sum())
    report["missing_village"] = int(df["village"].isna().sum())
    report["districts"] = int(df["district"].nunique())
    return df, report
