"""Interactive Streamlit dashboard for the Punjab stubble-burning analysis.

Reuses the existing pipeline in `src/` (cleaning + analysis) and renders it as
an interactive web app. Deployed free on Streamlit Community Cloud.

Run locally:  streamlit run app.py
"""

from __future__ import annotations

import calendar

import matplotlib.pyplot as plt
import streamlit as st

from src import analysis, cleaning, config

ACCENT = "#d7301f"   # fire red
MUTED = "#bdbdbd"

st.set_page_config(
    page_title="Punjab Stubble Burning",
    page_icon="🔥",
    layout="wide",
)


@st.cache_data(show_spinner="Loading and cleaning ~270k fire detections…")
def load_data():
    """Run the cleaning pipeline once and cache the result across sessions."""
    df, report = cleaning.clean()
    return df, report


df, report = load_data()

# --- Header ------------------------------------------------------------------
st.title("🔥 Punjab Stubble Burning (2018–2021)")
st.markdown(
    "Satellite-detected agricultural fires across Punjab. "
    "Fires are **hyper-concentrated** in a few weeks and a few districts."
)

# --- Sidebar filters ---------------------------------------------------------
st.sidebar.header("Filters")
years = sorted(int(y) for y in df["year"].dropna().unique())
selected_years = st.sidebar.multiselect("Year", years, default=years)
top_n = st.sidebar.slider("Top N districts", min_value=3, max_value=20, value=10)

view = df[df["year"].isin(selected_years)] if selected_years else df

if len(view) == 0:
    st.warning("No data for the selected filters.")
    st.stop()

metrics = analysis.concentration_metrics(view, top_n=min(5, top_n))

# --- Headline metrics --------------------------------------------------------
c1, c2, c3, c4 = st.columns(4)
c1.metric("Total fires", f"{metrics['total_fires']:,}")
c2.metric("Share in Oct–Nov", f"{metrics['season_share']:.1%}")
c3.metric(f"Top {metrics['top_n']} districts", f"{metrics['top_district_share']:.1%}")
c4.metric("Districts", f"{report['districts']}")

st.divider()

# --- Charts ------------------------------------------------------------------
left, right = st.columns(2)

with left:
    st.subheader("When do fires happen?")
    by_month = analysis.fires_by_month(view)
    fig, ax = plt.subplots(figsize=(6, 4))
    labels = [calendar.month_abbr[m] for m in by_month.index]
    colors = [ACCENT if m in config.FIRE_SEASON_MONTHS else MUTED
              for m in by_month.index]
    ax.bar(labels, by_month.values, color=colors)
    ax.set_ylabel("Fire detections")
    ax.set_xlabel("Month")
    st.pyplot(fig)
    plt.close(fig)

with right:
    st.subheader(f"Where do fires happen? (Top {top_n})")
    top = analysis.top_districts(view, n=top_n).iloc[::-1]
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.barh(top.index.str.title(), top.values, color=ACCENT)
    ax.set_xlabel("Fire detections")
    st.pyplot(fig)
    plt.close(fig)

st.subheader("Year-on-year trend")
by_year = analysis.fires_by_year(view)
st.line_chart(by_year, y_label="Fire detections", x_label="Year")

# --- Map (geo-valid rows only) ----------------------------------------------
geo = view[view["geo_valid"]][["lat", "lon"]].dropna()
if len(geo):
    st.subheader(f"Fire locations ({len(geo):,} mappable detections)")
    st.map(geo, size=20, color="#d7301f88")

# --- Data quality ------------------------------------------------------------
with st.expander("Data quality report"):
    st.json(report)

st.caption("Built from the pipeline in src/ · data: satellite stubble-fire detections")
