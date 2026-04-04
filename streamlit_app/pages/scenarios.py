import streamlit as st
import sys
import os

ROOT = os.path.dirname(os.path.dirname(__file__))
sys.path.append(ROOT)


def render(current_price=None, price_change_24h=None):
    st.write("Current price:", current_price)
    st.write("24h change:", price_change_24h)
