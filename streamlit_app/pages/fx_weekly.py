"""
FX Weekly page: next-week outlook per market, chart with the 80% range and
the honest walk-forward track record. Uses the same code as the Markdown
report (src/fx/report.py), so app and report always agree.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from src.config.assets import ASSETS, DEFAULT_ASSET
from src.fx.report import FEATURE_LABELS, AssetOutlook, build_outlook, verdict

HISTORY_WEEKS = 104


@st.cache_data(ttl=3600, show_spinner="Building weekly models…")
def _outlook(asset_key: str) -> AssetOutlook:
    return build_outlook(asset_key)


def _chart(o: AssetOutlook) -> go.Figure:
    wf = o.history.tail(HISTORY_WEEKS)
    # A forecast made at week t is about the close of week t+1: plot it there.
    target = wf.index + pd.Timedelta(days=7)
    actual_next = wf["close"] * np.exp(wf["y_ret"].astype(float))

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=target, y=wf["high_80"], line=dict(width=0), hoverinfo="skip", showlegend=False))
    fig.add_trace(go.Scatter(
        x=target, y=wf["low_80"], line=dict(width=0), fill="tonexty",
        fillcolor="rgba(99,132,255,0.18)", name="80% range (forecast a week earlier)",
        hovertemplate="%{x|%d %b %Y}<br>low %{y}<extra></extra>"))
    fig.add_trace(go.Scatter(
        x=target, y=actual_next, mode="lines", line=dict(color="#4b6bfb", width=2),
        name="Weekly close", hovertemplate="%{x|%d %b %Y}<br>close %{y}<extra></extra>"))

    # Next week's range, the thing this page is about.
    fig.add_trace(go.Scatter(
        x=[o.week_ending, o.week_ending], y=[o.low_80, o.high_80], mode="lines+markers",
        line=dict(color="#f59e0b", width=6), marker=dict(size=9, symbol="line-ew-open"),
        name=f"Next week ({o.week_ending:%d %b})",
        hovertemplate="%{y}<extra>next week, 80% range</extra>"))
    fig.add_trace(go.Scatter(
        x=[o.as_of], y=[o.close], mode="markers", marker=dict(color="#f59e0b", size=9),
        name=f"Last close ({o.as_of:%d %b})", hovertemplate="%{y}<extra>last close</extra>"))

    fig.update_layout(
        height=420, margin=dict(l=10, r=10, t=10, b=10), hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, x=0),
        yaxis=dict(tickformat=f",.{o.asset.decimals}f"),
    )
    return fig


def _track_table(o: AssetOutlook) -> pd.DataFrame:
    t = o.track
    rows = [
        ("Direction hit rate (vs up-share)", f"{t['hit_rate']:.1%}", f"{t['hit_rate_benchmark']:.1%}"),
        ("Brier score, lower = better (vs up-share)", f"{t['brier']:.3f}", f"{t['brier_benchmark']:.3f}"),
        ("Return RMSE ÷ random walk (Theil's U)", f"{t['theil_u']:.3f}", "1.000"),
        ("Vol RMSE ÷ 4-week average vol", f"{t['vol_rmse_ratio']:.3f}", "1.000"),
        ("80% range coverage", f"{t['band_coverage']:.1%}", "80.0%"),
    ]
    return pd.DataFrame(rows, columns=["Metric", "Model", "Benchmark"])


def render(current_price=None, price_change_24h=None):
    st.title("FX Weekly")
    st.caption("Next-week outlook for EUR/USD, EUR/CHF, EUR/PLN and BTC — "
               "honestly validated against a random walk.")

    keys = list(ASSETS)
    key = st.radio(
        "Market", keys, index=keys.index(DEFAULT_ASSET), horizontal=True,
        format_func=lambda k: ASSETS[k].name, key="fx_asset",
    )
    o = _outlook(key)

    if o.source == "sample":
        st.warning("Showing **sample data** (synthetic, for demo/offline use). "
                   "Run `python cli.py fetch-data` to use real market prices.", icon="⚠️")

    st.markdown(f"*{o.asset.note}*")

    half_width = (o.high_80 / o.low_80) ** 0.5 - 1  # symmetric in log terms
    c1, c2, c3, c4 = st.columns(4)
    c1.metric(f"Close {o.as_of:%d %b}", o.fmt(o.close))
    c2.metric(f"P(higher by {o.week_ending:%d %b})", f"{o.p_up:.0%}", o.direction,
              delta_color="off", delta_arrow="off")
    c3.metric("80% expected range", f"±{half_width:.1%}", f"{o.fmt(o.low_80)} – {o.fmt(o.high_80)}",
              delta_color="off", delta_arrow="off")
    c4.metric("Volatility regime", o.vol_regime.capitalize(), f"{o.vol_hat:.2%} per week",
              delta_color="off", delta_arrow="off")

    st.plotly_chart(_chart(o), width="stretch")
    st.caption("Shaded band: the 80% range the model gave one week before each close "
               "(out of sample). About 8 in 10 closes should fall inside it.")

    left, right = st.columns([1, 1])
    with left:
        st.subheader("What moves the signal")
        for feat, contrib in o.drivers:
            arrow = "▲ pushes up" if contrib >= 0 else "▼ pushes down"
            st.markdown(f"- **{FEATURE_LABELS.get(feat, feat)}** — {arrow}")
        st.caption("Largest contributions to this week's P(up) in the logistic regression.")
    with right:
        st.subheader("Track record")
        st.caption(f"Walk-forward {o.track['from']} → {o.track['to']} ({o.track['weeks']} weeks, out of sample)")
        st.dataframe(_track_table(o), hide_index=True, width="stretch")

    st.info(verdict(o.track).replace("**", ""))

    with st.expander("Method"):
        st.markdown(
            "- **Data:** daily closes (Yahoo Finance) resampled to Friday closes; 3-month interbank "
            "rates (OECD via FRED) for the rate differential, used only after their publication date.\n"
            "- **Models:** logistic regression for direction, ridge regression for the return, "
            "HAR-style regression for volatility. Deliberately simple and explainable.\n"
            "- **Validation:** expanding window, refitted every 4 weeks, never trained on the week it predicts.\n"
            "- **Benchmarks:** random walk, base rate of up-weeks, 4-week average volatility.\n\n"
            "*Educational project — not investment advice.*"
        )
