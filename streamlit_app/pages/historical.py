import streamlit as st
import pandas as pd

def render(current_price=None, price_change_24h=None):
    st.title("Historical Analysis")

    st.markdown("### Price history")
    st.caption("Long-term trend view based on historical BTC data.")

    try:
        df = pd.read_csv("data/processed/btc_1d_features.csv")
        st.line_chart(df["close"])
    except Exception:
        st.info("Historical price data not found. Add your CSV to data/processed/.")

    st.markdown("---")

    st.markdown("### Moving averages")
    st.write("SMA20 vs SMA50 trend direction")

    try:
        st.line_chart(df[["sma_20", "sma_50"]])
    except Exception:
        pass

    st.markdown("---")

    st.markdown("### Volatility overview")
    st.write("Standard deviation of returns (proxy for volatility)")

    try:
        df["returns"] = df["close"].pct_change()
        st.line_chart(df["returns"].rolling(20).std())
    except Exception:
        pass
