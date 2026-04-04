import streamlit as st
import pandas as pd

def placeholder_chart():
    st.line_chart(pd.DataFrame({"value": [1, 2, 3, 2, 4]}))
