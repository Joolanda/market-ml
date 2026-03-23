import streamlit as st
from pages import overview, predictions, historical, scenarios

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





st.title("Market-ML Dashboard")
st.write("Welcome to your personal ML lab for financial markets.")
st.set_page_config(
    page_title="Market ML Dashboard",
    page_icon="📈",
    layout="wide"
)
