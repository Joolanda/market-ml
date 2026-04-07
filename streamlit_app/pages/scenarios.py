import os
import sys
import streamlit as st

ROOT = os.path.dirname(os.path.dirname(__file__))
if ROOT not in sys.path:
    sys.path.append(ROOT)


def render(current_price=None, price_change_24h=None):
    st.title("Scenario Analysis")

    st.markdown("### Market snapshot")
    st.write("**Current price:**", current_price)
    st.write("**24h change:**", price_change_24h)

    st.markdown("---")

    st.markdown("### Bullish scenario")
    st.write("Describe the conditions under which BTC may move higher.")

    st.markdown("---")

    st.markdown("### Bearish scenario")
    st.write("Describe the conditions under which BTC may move lower.")

    st.markdown("---")

    st.markdown("### Neutral / consolidation scenario")
    st.write("Describe sideways movement or low‑volatility regimes.")
