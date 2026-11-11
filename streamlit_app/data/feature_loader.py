"""
Feature loader for the Technical Analysis page.

Uses the capstone CSVs in data/raw/<asset>_<tf>_raw.csv when present.
Otherwise it resamples the daily data (real or sample) to the requested
timeframe; intraday timeframes then fall back to daily candles.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.data.data_loader import load_daily, load_raw_candles
from src.features.engineering import engineer_features

_RESAMPLE = {"1d": "1D", "1w": "W-FRI"}


def _daily_as_raw(asset_key: str, timeframe: str) -> pd.DataFrame:
    daily = load_daily(asset_key).df
    rule = _RESAMPLE.get(timeframe, "1D")
    agg = daily.resample(rule).agg(
        {"open": "first", "high": "max", "low": "min", "close": "last", "volume": "sum"}
    ).dropna(subset=["close"])
    df = agg.reset_index().rename(columns={"date": "open_time"})
    df["close_time"] = df["open_time"]
    return df


def load_features(timeframe: str = "1d", asset_key: str = "btcusd") -> pd.DataFrame:
    path = Path(f"data/raw/{asset_key.replace('usd', '')}_{timeframe}_raw.csv")
    raw = load_raw_candles(str(path)) if path.exists() else _daily_as_raw(asset_key, timeframe)

    df = engineer_features(raw)
    width = (df["bb_upper"] - df["bb_lower"]).replace(0, pd.NA)
    df["bb_position"] = ((df["close"] - df["bb_lower"]) / width).astype(float)
    vol_ma = df["volume_ma"].replace(0, pd.NA)
    df["volume_ratio"] = (df["volume"] / vol_ma).astype(float)
    return df
