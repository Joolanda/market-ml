"""
Download real market data into data/raw/.

    python cli.py fetch-data

Sources (no API keys needed):
- Daily OHLCV for every asset in src/config/assets.py via Yahoo Finance (yfinance)
- Monthly 3-month interbank rates (OECD) via the FRED CSV endpoint

Files written:
    data/raw/<asset>_1d_raw.csv   open_time, open, high, low, close, volume, close_time
    data/raw/rates_monthly.csv    date, EUR, USD, CHF, PLN   (percent)
"""

from __future__ import annotations

import io
import logging
from pathlib import Path

import pandas as pd
import requests

from src.config.assets import ASSETS, RATE_SERIES, get_asset

log = logging.getLogger("market_ml.sources")

RAW_DIR = Path("data/raw")
FRED_CSV = "https://fred.stlouisfed.org/graph/fredgraph.csv?id={series}"
HISTORY_START = "2010-01-01"


def daily_path(asset_key: str) -> Path:
    return RAW_DIR / f"{asset_key}_1d_raw.csv"


def rates_path() -> Path:
    return RAW_DIR / "rates_monthly.csv"


def fetch_daily_yf(asset_key: str, start: str = HISTORY_START) -> pd.DataFrame:
    """Daily candles from Yahoo Finance, converted to the project's raw format."""
    import yfinance as yf  # imported lazily: not needed for offline use

    asset = get_asset(asset_key)
    hist = yf.Ticker(asset.yf_ticker).history(start=start, interval="1d", auto_adjust=False)
    if hist.empty:
        raise RuntimeError(f"No data returned for {asset.yf_ticker}")

    hist = hist.rename(columns=str.lower)
    idx = pd.DatetimeIndex(hist.index).tz_localize(None).normalize()
    df = pd.DataFrame({
        "open_time": idx.strftime("%Y-%m-%dT00:00:00Z"),
        "open": hist["open"].to_numpy(),
        "high": hist["high"].to_numpy(),
        "low": hist["low"].to_numpy(),
        "close": hist["close"].to_numpy(),
        "volume": hist.get("volume", pd.Series(0, index=hist.index)).fillna(0).to_numpy(),
        "close_time": (idx + pd.Timedelta(hours=23, minutes=59)).strftime("%Y-%m-%dT%H:%M:%SZ"),
    })
    # Yahoo sometimes returns rows with zeros or NaNs on holidays.
    df = df[(df["close"] > 0) & df["close"].notna()].drop_duplicates("open_time")
    return df.reset_index(drop=True)


def fetch_fred_series(series_id: str, timeout: int = 30) -> pd.Series:
    """One FRED series as a monthly Series (index = first day of month)."""
    resp = requests.get(FRED_CSV.format(series=series_id), timeout=timeout)
    resp.raise_for_status()
    df = pd.read_csv(io.StringIO(resp.text))
    date_col = "observation_date" if "observation_date" in df.columns else df.columns[0]
    s = pd.to_numeric(df[series_id], errors="coerce")
    s.index = pd.to_datetime(df[date_col])
    return s.dropna()


def fetch_rates() -> pd.DataFrame:
    cols = {}
    for ccy, series_id in RATE_SERIES.items():
        try:
            cols[ccy] = fetch_fred_series(series_id)
        except Exception as exc:  # keep going: one missing rate shouldn't block the rest
            log.warning("Rate %s (%s) not downloaded: %s", ccy, series_id, exc)
    if not cols:
        raise RuntimeError("No interest-rate series could be downloaded")
    return pd.DataFrame(cols).sort_index().rename_axis("date")


def update_all() -> dict:
    """Download everything; returns a short status per file."""
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    status = {}
    for key in ASSETS:
        try:
            df = fetch_daily_yf(key)
            df.to_csv(daily_path(key), index=False)
            status[key] = f"{len(df)} days, last {df['open_time'].iloc[-1][:10]}"
        except Exception as exc:
            status[key] = f"FAILED: {exc}"
    try:
        rates = fetch_rates()
        rates.to_csv(rates_path())
        status["rates"] = f"{len(rates)} months, last {rates.index[-1]:%Y-%m}"
    except Exception as exc:
        status["rates"] = f"FAILED: {exc}"
    return status
