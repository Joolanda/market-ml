"""
Synthetic sample data so the app, tests and CI run without internet access.

The series are *fake* but shaped like the real markets: business-day FX
quotes with volatility clustering, a 24/7 crypto series with much higher
volatility, and monthly interest rates. Everything is seeded, so the same
call always returns the same data. The app labels this data as SAMPLE.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from src.config.assets import ASSETS, RATE_SERIES, get_asset

SAMPLE_START = "2015-01-02"

# (start level, annual volatility, annual drift)
_PROFILE = {
    "eurusd": (1.20, 0.075, -0.005),
    "eurchf": (1.20, 0.055, -0.020),
    "eurpln": (4.30, 0.060, 0.000),
    "btcusd": (300.0, 0.65, 0.45),
}

# Rough monthly rate paths (percent) – piecewise linear anchors.
_RATE_ANCHORS = {
    "EUR": [("2015-01", 0.05), ("2016-06", -0.30), ("2021-12", -0.55), ("2022-12", 2.10),
            ("2023-10", 3.95), ("2025-06", 2.00), ("2026-11", 2.00)],
    "USD": [("2015-01", 0.25), ("2018-12", 2.80), ("2020-04", 0.30), ("2022-01", 0.25),
            ("2023-08", 5.60), ("2025-06", 4.30), ("2026-11", 3.80)],
    "CHF": [("2015-01", -0.70), ("2021-12", -0.75), ("2022-12", 0.90), ("2023-10", 1.70),
            ("2025-06", 0.10), ("2026-11", 0.00)],
    "PLN": [("2015-01", 2.00), ("2015-06", 1.70), ("2021-09", 0.25), ("2022-10", 7.20),
            ("2024-12", 5.85), ("2026-11", 4.50)],
}


def _end_date() -> pd.Timestamp:
    return pd.Timestamp.today().normalize()


def make_sample_rates(end: str | None = None) -> pd.DataFrame:
    """Monthly 3-month interest rates in percent, one column per currency."""
    end_ts = pd.Timestamp(end) if end else _end_date()
    idx = pd.date_range(SAMPLE_START, end_ts, freq="MS")
    rng = np.random.default_rng(11)
    out = {}
    for ccy in RATE_SERIES:
        anchors = _RATE_ANCHORS[ccy]
        x = pd.to_datetime([a[0] for a in anchors]).map(pd.Timestamp.toordinal)
        y = [a[1] for a in anchors]
        base = np.interp(idx.map(pd.Timestamp.toordinal), x, y)
        out[ccy] = np.round(base + rng.normal(0, 0.03, len(idx)), 3)
    return pd.DataFrame(out, index=idx).rename_axis("date")


def make_sample_ohlcv(asset_key: str, end: str | None = None) -> pd.DataFrame:
    """Daily OHLCV in the project's raw format (open_time ... close_time)."""
    asset = get_asset(asset_key)
    level, ann_vol, ann_drift = _PROFILE[asset.key]
    end_ts = pd.Timestamp(end) if end else _end_date()

    if asset.kind == "fx":
        days = pd.bdate_range(SAMPLE_START, end_ts)
        per_year = 260
    else:
        days = pd.date_range(SAMPLE_START, end_ts, freq="D")
        per_year = 365

    seed = sum(ord(c) for c in asset.key)
    rng = np.random.default_rng(seed)
    n = len(days)

    # GARCH(1,1)-style volatility clustering around the target annual vol.
    daily_var = (ann_vol ** 2) / per_year
    omega, alpha, beta = daily_var * 0.05, 0.08, 0.87
    var = np.empty(n)
    eps = np.empty(n)
    var[0] = daily_var
    for t in range(n):
        if t > 0:
            var[t] = omega + alpha * eps[t - 1] ** 2 + beta * var[t - 1]
        eps[t] = np.sqrt(var[t]) * rng.standard_t(6) / np.sqrt(6 / 4)

    # Small carry effect for FX: higher base-currency rate → slight drift up.
    drift = np.full(n, ann_drift / per_year)
    if asset.kind == "fx":
        rates = make_sample_rates(end).reindex(days, method="ffill").bfill()
        diff = (rates[asset.base_ccy] - rates[asset.quote_ccy]).to_numpy()
        drift = drift + diff / 100 / per_year * 0.6

    log_ret = drift + eps
    close = level * np.exp(np.cumsum(log_ret))
    open_ = np.concatenate([[level], close[:-1]]) * np.exp(rng.normal(0, np.sqrt(daily_var) * 0.1, n))
    spread = np.abs(rng.normal(0, np.sqrt(var), n)) + np.sqrt(var) * 0.3
    high = np.maximum(open_, close) * np.exp(spread)
    low = np.minimum(open_, close) * np.exp(-spread)
    volume = (rng.lognormal(10, 0.4, n) if asset.kind == "crypto" else np.zeros(n))

    df = pd.DataFrame({
        "open_time": days.strftime("%Y-%m-%dT00:00:00Z"),
        "open": open_, "high": high, "low": low, "close": close, "volume": volume,
        "close_time": (days + pd.Timedelta(hours=23, minutes=59)).strftime("%Y-%m-%dT%H:%M:%SZ"),
    })
    return df


def all_sample_assets() -> list[str]:
    return list(ASSETS)
