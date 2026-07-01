# Punjab Stubble-Burning — Data Insights & Storytelling

Cleans and analyses ~270k satellite stubble-fire detections for Punjab
(2018–2021) and produces a dashboard + a data story for local officials.

> **Note on the brief:** the challenge template says "water governance," but the
> attached dataset is agricultural-fire / air-quality data. The analysis is
> reframed to that domain. See [DATA_STORY.md](DATA_STORY.md).

## Run

```bash
pip install -r requirements.txt
python main.py
```

Outputs (written to `outputs/`):
- `fires_clean.csv` — cleaned, analysis-ready data
- `dashboard.png` — 3-panel data-story visual
- `data_quality_report.txt` — what was cleaned + headline metrics

## Project layout

```
main.py              # pipeline: clean -> analyse -> visualise
src/config.py        # paths, column map, Punjab bounds, constants
src/cleaning.py      # load + clean, returns df + quality report
src/analysis.py      # temporal / district / concentration metrics
src/visualize.py     # dashboard figure
```

## 1. Data cleaning (anomalies handled)

| # | Anomaly | Handling |
|---|---------|----------|
| 1 | **Mixed date formats** (`16-Sep-21` vs `18/9/2021`) | Parsed to one datetime standard (`dayfirst`, mixed format). 0 unparseable. |
| 2 | **District casing duplicate** (`Amritsar` vs `AMRITSAR`) | Upper-cased + trimmed → 27 collapses to 26 real districts. |
| 3 | **Corrupted latitude** (6,865 rows where `lat == lon`, impossible for Punjab) | Unrecoverable from source → flagged `geo_valid=False`; kept for time/district analysis, excluded from maps. |
| 4 | **Column-shifted rows** (35 rows with numbers in the Day/Night field) | Whole row misaligned → dropped. |
| 5 | **Missing values** (1,384 fire power, 68,411 village) | Kept for counts; intensity **not** imputed (would fabricate signal). Documented in the report. |

## 2. The insight

Fires are **hyper-concentrated in time and space**:
- **99.9%** of all detections occur in **October–November**.
- **Top 5 districts** (Sangrur, Firozpur, Bathinda, Muktsar, Patiala) = **~48%** of all fires.

## 3. The data story

See [DATA_STORY.md](DATA_STORY.md) — a 150-word call to action for a district
officer, anchored on the dashboard.
