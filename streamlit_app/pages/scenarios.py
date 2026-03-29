import streamlit as st

def render(current_price=None, price_change_24h=None):
    st.write("Current price:", current_price)
    st.write("24h change:", price_change_24h)
