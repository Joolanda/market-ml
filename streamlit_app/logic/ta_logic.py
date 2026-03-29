# streamlit_app/logic/ta_logic.py

from __future__ import annotations
from dataclasses import dataclass
from typing import Literal, Dict, List

Sentiment = Literal["bearish", "neutral", "bullish"]


@dataclass
class IndicatorResult:
    name: str
    sentiment: Sentiment
    status: str
    trend_support: str


def _classify_rsi(rsi: float) -> Sentiment:
    if rsi is None:
        return "neutral"
    if rsi > 60:
        return "bullish"
    if rsi < 40:
        return "bearish"
    return "neutral"


def _classify_macd(macd: float, macd_signal: float) -> Sentiment:
    if macd is None or macd_signal is None:
        return "neutral"
    if macd > macd_signal:
        return "bullish"
    if macd < macd_signal:
        return "bearish"
    return "neutral"


def _classify_sma(sma_20: float, sma_50: float) -> Sentiment:
    if sma_20 is None or sma_50 is None:
        return "neutral"
    if sma_20 > sma_50:
        return "bullish"
    if sma_20 < sma_50:
        return "bearish"
    return "neutral"


def _classify_bollinger(position: float) -> Sentiment:
    if position is None:
        return "neutral"
    if position > 0.8:
        return "bullish"
    if position < 0.2:
        return "bearish"
    return "neutral"


def _classify_volume(volume_ratio: float) -> Sentiment:
    if volume_ratio is None:
        return "neutral"
    if volume_ratio > 1.0:
        return "bullish"
    if volume_ratio < 0.8:
        return "bearish"
    return "neutral"


def _sentiment_score(sentiment: Sentiment) -> int:
    if sentiment == "bullish":
        return 1
    if sentiment == "bearish":
        return -1
    return 0


def aggregate_overall_sentiment(indicators: List[IndicatorResult]) -> Sentiment:
    score = sum(_sentiment_score(i.sentiment) for i in indicators)
    if score > 0:
        return "bullish"
    if score < 0:
        return "bearish"
    return "neutral"


def build_indicator_results(features: Dict) -> List[IndicatorResult]:
    # Veilig floats casten (None of NaN → None)
    def safe(v):
        try:
            if v is None:
                return None
            if isinstance(v, float) and pd.isna(v):
                return None
            return float(v)
        except:
            return None

    rsi = safe(features.get("rsi"))
    macd = safe(features.get("macd"))
    macd_signal = safe(features.get("macd_signal"))
    sma_20 = safe(features.get("sma_20"))
    sma_50 = safe(features.get("sma_50"))
    bb_position = safe(features.get("bb_position"))
    volume_ratio = safe(features.get("volume_ratio"))

    results: List[IndicatorResult] = []


    # RSI
    rsi_sent = _classify_rsi(rsi)
    rsi_status = (
        f"Overbought (RSI {rsi:.1f})" if rsi and rsi > 70
        else f"Bullish (RSI {rsi:.1f})" if rsi and rsi_sent == "bullish"
        else f"Bearish (RSI {rsi:.1f})" if rsi and rsi_sent == "bearish"
        else f"Sideways (RSI {rsi:.1f})" if rsi is not None
        else "No data"
    )
    rsi_trend = (
        "Supports uptrend" if rsi_sent == "bullish"
        else "Supports downtrend" if rsi_sent == "bearish"
        else "Neutral / mixed"
    )
    results.append(
        IndicatorResult(
            name="RSI",
            sentiment=rsi_sent,
            status=rsi_status,
            trend_support=rsi_trend,
        )
    )

    # MACD
    macd_sent = _classify_macd(macd, macd_signal)
    macd_status = (
        "Bullish crossover" if macd_sent == "bullish"
        else "Bearish crossover" if macd_sent == "bearish"
        else "Sideways (flat histogram)"
    )
    macd_trend = (
        "Supports uptrend" if macd_sent == "bullish"
        else "Supports downtrend" if macd_sent == "bearish"
        else "Neutral / mixed"
    )
    results.append(
        IndicatorResult(
            name="MACD",
            sentiment=macd_sent,
            status=macd_status,
            trend_support=macd_trend,
        )
    )

    # Moving averages (SMA20 vs SMA50)
    ma_sent = _classify_sma(sma_20, sma_50)
    ma_status = (
        "Bullish (SMA20 above SMA50)" if ma_sent == "bullish"
        else "Bearish (SMA20 below SMA50)" if ma_sent == "bearish"
        else "Sideways / flat"
    )
    ma_trend = (
        "Supports uptrend" if ma_sent == "bullish"
        else "Supports downtrend" if ma_sent == "bearish"
        else "Neutral / mixed"
    )
    results.append(
        IndicatorResult(
            name="Moving Averages",
            sentiment=ma_sent,
            status=ma_status,
            trend_support=ma_trend,
        )
    )

    # Bollinger Bands
    bb_sent = _classify_bollinger(bb_position)
    bb_status = (
        "High volatility (near upper band)" if bb_sent == "bullish"
        else "High volatility (near lower band)" if bb_sent == "bearish"
        else "Within bands"
    )
    bb_trend = "Neutral / mixed"
    results.append(
        IndicatorResult(
            name="Bollinger Bands",
            sentiment=bb_sent,
            status=bb_status,
            trend_support=bb_trend,
        )
    )

    # Volume
    vol_sent = _classify_volume(volume_ratio)
    vol_status = (
        "Above recent average" if vol_sent == "bullish"
        else "Below recent average" if vol_sent == "bearish"
        else "Around recent average"
    )
    vol_trend = "Neutral / mixed"
    results.append(
        IndicatorResult(
            name="Volume",
            sentiment=vol_sent,
            status=vol_status,
            trend_support=vol_trend,
        )
    )

    return results
