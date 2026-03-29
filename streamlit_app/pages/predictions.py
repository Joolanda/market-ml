import streamlit as st

def render(current_price=None, price_change_24h=None):
    st.title("Predictions")

    st.markdown("### Model forecasts")
    st.caption("Short-, mid- and long-term directional predictions based on ML features.")

    cols = st.columns(3)

    with cols[0]:
        st.metric("1D Forecast", "Bullish", "78% confidence")
    with cols[1]:
        st.metric("1W Forecast", "Neutral", "55% confidence")
    with cols[2]:
        st.metric("1M Forecast", "Bearish", "32% confidence")

    st.markdown("---")

    st.markdown("### Current market snapshot")
    st.write("**Current price:**", current_price)
    st.write("**24h change:**", price_change_24h)

    st.markdown("---")

    st.markdown("### Technical rating")
    st.progress(0.72)
    st.caption("Overall technical bias based on combined indicators.")
