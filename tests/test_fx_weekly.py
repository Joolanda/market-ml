"""
Tests for the FX Weekly pipeline.

The important ones guard against look-ahead bias: a backtest that peeks at the
future looks great and means nothing.
"""

import importlib
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from src.config.assets import ASSETS, get_asset
from src.data.data_loader import load_daily, load_rates
from src.fx import models as fx_models
from src.fx.models import WeeklyModels, evaluate, walk_forward
from src.fx.report import build_all, render_markdown, verdict
from src.fx.weekly import FEATURES_COMMON, build_dataset, feature_columns, rate_differential, to_weekly


@pytest.fixture(scope="module")
def eurusd():
    asset = get_asset("eurusd")
    daily, rates = load_daily("eurusd"), load_rates()
    assert daily.source == "sample" and rates.source == "sample"
    return asset, daily.df, rates.df


@pytest.fixture(scope="module")
def outlooks():
    return build_all()


# --- Data layer ----------------------------------------------------------------

def test_sample_data_is_deterministic():
    from src.data.sample import make_sample_ohlcv
    a = make_sample_ohlcv("eurpln", end="2024-01-01")
    b = make_sample_ohlcv("eurpln", end="2024-01-01")
    pd.testing.assert_frame_equal(a, b)


def test_weekly_bars_end_on_friday_and_drop_running_week(eurusd):
    _, daily, _ = eurusd
    # Cut the data on a Wednesday: that week is not complete and must not appear.
    wed = daily.index[daily.index.dayofweek == 2][-10]
    weekly = to_weekly(daily[daily.index <= wed])
    assert (weekly.index.dayofweek == 4).all()
    assert weekly.index[-1] < wed


# --- No look-ahead in features ---------------------------------------------------

def test_features_do_not_change_when_future_data_is_added(eurusd):
    asset, daily, rates = eurusd
    full = build_dataset(daily, rates, asset)
    cutoff = full.index[-60]
    past = build_dataset(daily[daily.index <= cutoff], rates, asset)

    cols = feature_columns(full)
    common = past.index.intersection(full.index)
    pd.testing.assert_frame_equal(past.loc[common, cols], full.loc[common, cols])


def test_target_is_next_weeks_return(eurusd):
    asset, daily, rates = eurusd
    df = build_dataset(daily, rates, asset)
    np.testing.assert_allclose(df["y_ret"].iloc[:-1].to_numpy(), df["ret_1w"].iloc[1:].to_numpy())
    assert np.isnan(df["y_ret"].iloc[-1])  # the latest week has no known outcome yet


def test_rate_differential_respects_publication_lag(eurusd):
    asset, _, rates = eurusd
    weeks = pd.date_range("2023-01-06", "2023-12-29", freq="W-FRI")
    base = rate_differential(rates, asset, weeks)["rate_diff"]

    # Changing the March 2023 rate may only affect weeks from 1 May 2023 onwards
    # (month ends 31 March, published with a one-month lag).
    shocked = rates.copy()
    shocked.loc["2023-03-01", "EUR"] += 5.0
    after = rate_differential(shocked, asset, weeks)["rate_diff"]

    changed = after.index[(after - base).abs() > 1e-9]
    assert len(changed) > 0
    assert changed.min() >= pd.Timestamp("2023-05-01")


def test_btc_has_no_rate_features():
    asset = get_asset("btcusd")
    df = build_dataset(load_daily("btcusd").df, load_rates().df, asset)
    assert feature_columns(df) == FEATURES_COMMON


# --- Walk-forward only trains on the past ------------------------------------------

def test_walk_forward_trains_only_on_earlier_weeks(eurusd, monkeypatch):
    asset, daily, rates = eurusd
    data = build_dataset(daily, rates, asset)
    feats = feature_columns(data)

    seen = []
    original_fit = WeeklyModels.fit

    def spy_fit(self, train):
        seen.append(train.index.max())
        return original_fit(self, train)

    original_predict = WeeklyModels.predict
    predicted_at = []

    def spy_predict(self, rows):
        predicted_at.append((rows.index[0], seen[-1]))
        return original_predict(self, rows)

    monkeypatch.setattr(fx_models.WeeklyModels, "fit", spy_fit)
    monkeypatch.setattr(fx_models.WeeklyModels, "predict", spy_predict)
    wf = walk_forward(data, feats, min_train=156, refit_every=4)

    assert len(predicted_at) == len(wf)
    for week, last_train_week in predicted_at:
        # The training row at last_train_week has a target about the week after it,
        # so it must be strictly before the forecast week.
        assert last_train_week < week


def test_evaluation_has_benchmarks_and_sane_band(eurusd):
    asset, daily, rates = eurusd
    data = build_dataset(daily, rates, asset)
    result = evaluate(walk_forward(data, feature_columns(data)))
    for key in ["hit_rate_benchmark", "brier_benchmark", "theil_u", "vol_rmse_ratio"]:
        assert np.isfinite(result[key])
    # An 80% band should hold roughly 80% of outcomes on data like this.
    assert 0.65 < result["band_coverage"] < 0.92


# --- Report ------------------------------------------------------------------------------

def test_report_covers_every_asset(outlooks):
    assert [o.asset.key for o in outlooks] == list(ASSETS)
    md = render_markdown(outlooks)
    for asset in ASSETS.values():
        assert f"## {asset.name}" in md
    assert "Sample data" in md  # sample data must be labelled as such
    assert "Track record" in md


def test_outlook_values_are_consistent(outlooks):
    for o in outlooks:
        assert 0 < o.p_up < 1
        assert o.low_80 < o.close < o.high_80
        assert o.vol_regime in {"low", "normal", "high"}
        assert o.week_ending - o.as_of == pd.Timedelta(days=7)
        assert len(o.drivers) == 3


def test_verdict_mentions_each_benchmark(outlooks):
    text = verdict(outlooks[0].track)
    assert "base rate" in text and "random walk" in text and "4-week average" in text


def test_cli_writes_report(tmp_path, monkeypatch):
    from src.fx import report
    out = report.write_report(report.build_all(["eurchf"]), out_dir=tmp_path)
    assert out.exists() and (tmp_path / "latest.md").read_text() == out.read_text()


# --- App ------------------------------------------------------------------------------------

@pytest.mark.parametrize("module", [
    "streamlit_app.pages.fx_weekly",
    "streamlit_app.pages.overview",
    "streamlit_app.pages.predictions",
    "streamlit_app.pages.technical_analysis",
    "streamlit_app.pages.historical",
    "streamlit_app.pages.scenarios",
])
def test_app_pages_import(module):
    assert hasattr(importlib.import_module(module), "render")


def test_fx_weekly_page_renders_without_errors():
    from streamlit.testing.v1 import AppTest
    at = AppTest.from_file(str(Path(__file__).parents[1] / "app.py"), default_timeout=180)
    at.run()
    assert not at.exception
    assert at.title[0].value == "FX Weekly"
    assert len(at.metric) == 4
