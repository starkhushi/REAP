"""End-to-end pipeline: clean -> analyse -> visualise.

Run with:  python main.py
Outputs land in ./outputs (cleaned CSV, dashboard PNG, quality report).
"""

from src import analysis, cleaning, config, visualize


def _write_quality_report(report: dict, metrics: dict) -> None:
    lines = [
        "STUBBLE-BURNING DATA QUALITY REPORT",
        "=" * 38,
        f"Raw rows ................. {report['rows_raw']:,}",
        f"Dropped (column-shifted) . {report['rows_dropped_shifted']:,}",
        f"Clean rows ............... {report['rows_clean']:,}",
        f"Districts (deduped) ...... {report['districts']}",
        f"Unparseable dates ........ {report['unparseable_dates']:,}",
        f"Geo-invalid (lat corrupt). {report['geo_invalid']:,}  (flagged, kept)",
        f"Missing fire power ....... {report['missing_fire_power']:,}",
        f"Missing village .......... {report['missing_village']:,}",
        "",
        "HEADLINE INSIGHT",
        "-" * 38,
        f"Total fires .............. {metrics['total_fires']:,}",
        f"Share in Oct-Nov ......... {metrics['season_share']:.1%}",
        f"Top {metrics['top_n']} districts share .... {metrics['top_district_share']:.1%}",
        f"Top {metrics['top_n']} districts .......... {', '.join(metrics['top_districts'])}",
    ]
    text = "\n".join(lines)
    config.QUALITY_REPORT.write_text(text, encoding="utf-8")
    print(text)


def main() -> None:
    config.OUTPUT_DIR.mkdir(exist_ok=True)

    df, report = cleaning.clean()
    df.to_csv(config.CLEAN_CSV, index=False)

    metrics = analysis.concentration_metrics(df)
    _write_quality_report(report, metrics)

    visualize.build_dashboard(df)
    print(f"\nSaved: {config.CLEAN_CSV.name}, {config.DASHBOARD_PNG.name}, "
          f"{config.QUALITY_REPORT.name}")


if __name__ == "__main__":
    main()
