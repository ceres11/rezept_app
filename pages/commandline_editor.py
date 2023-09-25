import streamlit as st
import numpy as np
import pandas as pd

# Commandline commander

import streamlit as st

st.markdown("# Page 2 ❄️")
st.sidebar.markdown("# Page 2 ❄️")

st.sidebar.empty()

df = pd.DataFrame({
    'first column': ["CCE4100_flashprogrammer", "AP_Asic pinout tool"],
    'second column': [10, 20]
    })



left_column, middle_column, right_column =  st.columns(3)

with left_column:
    option = st.selectbox(
    'command',
     df['first column'])

with middle_column:
    st.text_input("Arguments", key="n")