"""Analysis of the cleaned fire data.

Each function answers one question and returns a small, plot-ready object.
The headline finding: fires are hyper-concentrated in time and space.
"""

from __future__ import annotations

import pandas as pd

from . import config


def fires_by_month(df: pd.DataFrame) -> pd.Series:
    """Fire-detection count per calendar month (1-12)."""
    return df["month"].value_counts().sort_index()


def fires_by_year(df: pd.DataFrame) -> pd.Series:
    """Fire-detection count per year."""
    return df["year"].value_counts().sort_index()


def top_districts(df: pd.DataFrame, n: int = 10) -> pd.Series:
    """The `n` districts with the most fire detections."""
    return df["district"].value_counts().head(n)


def concentration_metrics(df: pd.DataFrame, top_n: int = 5) -> dict:
    """Quantify how concentrated the fires are in time and space."""
    total = len(df)
    season_share = df["month"].isin(config.FIRE_SEASON_MONTHS).sum() / total
    district_counts = df["district"].value_counts()
    top_share = district_counts.head(top_n).sum() / total
    return {
        "total_fires": total,
        "season_share": season_share,
        "top_n": top_n,
        "top_district_share": top_share,
        "top_districts": district_counts.head(top_n).index.tolist(),
    }
