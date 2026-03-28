import streamlit as st
from pathlib import Path

from streamlit_app.pages import overview, predictions, historical, scenarios
from streamlit_app.data.loaders import get_live_price


def load_css(file_path: str):
    css_path = Path(file_path)
    if css_path.exists():
        with open(css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


st.set_page_config(
    page_title="Market ML Dashboard",
    page_icon="📈",
    layout="wide"
)

load_css("streamlit_app/assets/style.css")



PAGES = {
    "📊 Overview": overview,
    "🤖 Predictions": predictions,
    "📜 Historical Analysis": historical,
    "🧠 Scenario AI": scenarios,
}


def main():
    st.sidebar.title("Navigation")
    selection = st.sidebar.radio("Go to", list(PAGES.keys()))
    page = PAGES[selection]

    # Load live data once per page render
    current_price, price_change_24h = get_live_price("BTC")

    # Pass data into the page renderer
    page.render(current_price, price_change_24h)


if __name__ == "__main__":
    main()
