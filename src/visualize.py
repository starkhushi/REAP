"""Build the data-story dashboard as a single PNG.

One figure, three panels: the time concentration, the district concentration,
and the year-on-year trend - the three facts the data story rests on.
"""

from __future__ import annotations

import calendar

import matplotlib.pyplot as plt

from . import analysis, config

ACCENT = "#d7301f"   # fire red
MUTED = "#bdbdbd"


def build_dashboard(df) -> None:
    """Render the 3-panel dashboard and save it to OUTPUT_DIR."""
    metrics = analysis.concentration_metrics(df)
    fig, axes = plt.subplots(1, 3, figsize=(16, 5))
    fig.suptitle(
        "Punjab Stubble Burning (2018-2021): fires cluster in a few weeks "
        "and a few districts",
        fontsize=14, fontweight="bold",
    )

    _plot_months(axes[0], df, metrics)
    _plot_districts(axes[1], df, metrics)
    _plot_years(axes[2], df)

    fig.tight_layout(rect=(0, 0, 1, 0.95))
    fig.savefig(config.DASHBOARD_PNG, dpi=130)
    plt.close(fig)


def _plot_months(ax, df, metrics) -> None:
    by_month = analysis.fires_by_month(df)
    labels = [calendar.month_abbr[m] for m in by_month.index]
    colors = [ACCENT if m in config.FIRE_SEASON_MONTHS else MUTED
              for m in by_month.index]
    ax.bar(labels, by_month.values, color=colors)
    ax.set_title(f"{metrics['season_share']:.0%} of fires fall in Oct-Nov")
    ax.set_ylabel("Fire detections")
    ax.set_xlabel("Month")


def _plot_districts(ax, df, metrics) -> None:
    top = analysis.top_districts(df, n=10).iloc[::-1]
    ax.barh(top.index.str.title(), top.values, color=ACCENT)
    ax.set_title(
        f"Top {metrics['top_n']} districts = "
        f"{metrics['top_district_share']:.0%} of all fires"
    )
    ax.set_xlabel("Fire detections")


def _plot_years(ax, df) -> None:
    by_year = analysis.fires_by_year(df)
    ax.plot(by_year.index, by_year.values, marker="o", color=ACCENT, linewidth=2)
    ax.set_title("Year-on-year detections")
    ax.set_ylabel("Fire detections")
    ax.set_xlabel("Year")
    ax.set_xticks(by_year.index)
    ax.set_ylim(bottom=0)
