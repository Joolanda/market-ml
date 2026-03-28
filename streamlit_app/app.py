import streamlit as st
from streamlit_app.pages import overview, predictions, historical, scenarios
from pathlib import Path

# voorbeeld data
# current_price = 67420.55
# price_change_24h = 2.14

# overview.render(current_price, price_change_24h)


def load_css(file_path: str):
    css_path = Path(file_path)
    if css_path.exists():
        with open(css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css("streamlit_app/assets/style.css")

st.set_page_config(
    page_title="Market ML Dashboard",
    page_icon="📈",
    layout="wide"
)

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
    page.render()

if __name__ == "__main__":
    main()