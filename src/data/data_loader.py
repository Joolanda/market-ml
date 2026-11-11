"""
Single entry point for market data used by the models, report and app.

Real data in data/raw/ is used when present (see src/data/sources.py).
Otherwise seeded sample data is generated, so everything also runs offline.
Every loader returns the data *and* where it came from ("real" / "sample"),
so the UI and report can say so.
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from typing import Tuple

import pandas as pd

from src.data import sources
from src.data.sample import make_sample_ohlcv, make_sample_rates
from src.features.engineering import load_raw_candles  # re-exported for older pages

__all__ = ["load_raw_candles", "load_daily", "load_rates", "LoadedData"]


@dataclass
class LoadedData:
    df: pd.DataFrame
    source: str  # "real" or "sample"


def _to_daily_frame(raw: pd.DataFrame) -> pd.DataFrame:
    df = raw.copy()
    df["date"] = pd.to_datetime(df["open_time"], utc=True).dt.tz_localize(None).dt.normalize()
    df = df.set_index("date").sort_index()
    df = df[["open", "high", "low", "close", "volume"]].astype(float)
    return df[~df.index.duplicated(keep="last")]


@lru_cache(maxsize=16)
def _load_daily_cached(asset_key: str) -> Tuple[pd.DataFrame, str]:
    path = sources.daily_path(asset_key)
    if path.exists():
        return _to_daily_frame(pd.read_csv(path)), "real"
    return _to_daily_frame(make_sample_ohlcv(asset_key)), "sample"


def load_daily(asset_key: str) -> LoadedData:
    """Daily OHLCV indexed by date (naive, normalised)."""
    df, source = _load_daily_cached(asset_key.lower())
    return LoadedData(df.copy(), source)


@lru_cache(maxsize=1)
def _load_rates_cached() -> Tuple[pd.DataFrame, str]:
    path = sources.rates_path()
    if path.exists():
        df = pd.read_csv(path, parse_dates=["date"]).set_index("date").sort_index()
        return df, "real"
    return make_sample_rates(), "sample"


def load_rates() -> LoadedData:
    """Monthly interest rates in percent, one column per currency."""
    df, source = _load_rates_cached()
    return LoadedData(df.copy(), source)


def clear_cache() -> None:
    _load_daily_cached.cache_clear()
    _load_rates_cached.cache_clear()
