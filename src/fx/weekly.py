"""
Weekly features and targets for the FX Weekly.

One row per week (Friday close). Every feature in row t uses only
information available at the close of week t; every target describes
week t+1. Tests in tests/test_fx_weekly.py check that no future data leaks in.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from src.config.assets import Asset

WEEK_RULE = "W-FRI"
RATE_PUBLICATION_LAG_MONTHS = 1  # a monthly rate is only known after the month ends

FEATURES_COMMON = [
    "ret_1w", "ret_4w", "ret_12w",
    "vol_1w", "vol_4w", "vol_12w",
    "rsi_14w", "dist_sma_26w", "range_1w",
]
FEATURES_RATES = ["rate_diff", "rate_diff_chg_3m"]


def to_weekly(daily: pd.DataFrame) -> pd.DataFrame:
    """Weekly OHLC + realised volatility from daily candles."""
    log_ret = np.log(daily["close"]).diff()
    weekly = daily.resample(WEEK_RULE).agg(
        {"open": "first", "high": "max", "low": "min", "close": "last"}
    )
    # Realised weekly vol = std of daily log returns within the week, scaled to a week (5 days).
    weekly["rv"] = log_ret.resample(WEEK_RULE).std() * np.sqrt(5)
    weekly["n_days"] = daily["close"].resample(WEEK_RULE).count()
    weekly = weekly[weekly["n_days"] >= 2].dropna(subset=["close"])
    # Drop the running week: it is only complete once its Friday has a close.
    if len(weekly) and weekly.index[-1] > daily.index[-1]:
        weekly = weekly.iloc[:-1]
    return weekly


def _rsi(close: pd.Series, period: int = 14) -> pd.Series:
    delta = close.diff()
    gain = delta.clip(lower=0).ewm(alpha=1 / period, adjust=False).mean()
    loss = (-delta.clip(upper=0)).ewm(alpha=1 / period, adjust=False).mean()
    rs = gain / loss.replace(0, np.nan)
    return 100 - 100 / (1 + rs)


def rate_differential(rates: pd.DataFrame, asset: Asset, index: pd.DatetimeIndex) -> pd.DataFrame:
    """Base minus quote 3-month rate (pp), as known at each weekly date."""
    if asset.kind != "fx" or asset.base_ccy not in rates or asset.quote_ccy not in rates:
        return pd.DataFrame(index=index)
    diff = (rates[asset.base_ccy] - rates[asset.quote_ccy]).dropna()
    # The value for month M is published after M ends: make it available from M+1+lag.
    available_from = diff.index + pd.DateOffset(months=1 + RATE_PUBLICATION_LAG_MONTHS)
    diff = pd.Series(diff.to_numpy(), index=available_from).sort_index()
    on_weeks = diff.reindex(diff.index.union(index)).ffill().reindex(index)
    out = pd.DataFrame(index=index)
    out["rate_diff"] = on_weeks
    out["rate_diff_chg_3m"] = on_weeks - on_weeks.shift(13)
    return out


def build_dataset(daily: pd.DataFrame, rates: pd.DataFrame, asset: Asset) -> pd.DataFrame:
    """Features (known at week t) and targets (about week t+1) in one frame."""
    w = to_weekly(daily)
    close = w["close"]
    log_close = np.log(close)

    df = pd.DataFrame(index=w.index)
    df["close"] = close
    df["ret_1w"] = log_close.diff(1)
    df["ret_4w"] = log_close.diff(4)
    df["ret_12w"] = log_close.diff(12)
    df["vol_1w"] = w["rv"]
    df["vol_4w"] = w["rv"].rolling(4).mean()
    df["vol_12w"] = w["rv"].rolling(12).mean()
    df["rsi_14w"] = _rsi(close)
    df["dist_sma_26w"] = close / close.rolling(26).mean() - 1
    df["range_1w"] = (w["high"] - w["low"]) / close

    df = df.join(rate_differential(rates, asset, df.index))

    # Targets: next week's log return, direction and realised volatility.
    df["y_ret"] = df["ret_1w"].shift(-1)
    df["y_up"] = (df["y_ret"] > 0).astype(float).where(df["y_ret"].notna())
    df["y_vol"] = df["vol_1w"].shift(-1)
    return df


def feature_columns(df: pd.DataFrame) -> list[str]:
    cols = list(FEATURES_COMMON)
    if all(c in df.columns for c in FEATURES_RATES) and df["rate_diff"].notna().sum() > 52:
        cols += FEATURES_RATES
    return cols
