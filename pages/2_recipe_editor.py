import streamlit as st
import pandas as pd
import json


# Rezeptdaten eingeben
st.write("# Neues Rezept")

with st.form("my_form"):
    ## Rezeptname
    st.text_input("Name")

    ## Bild
    st.file_uploader("Bild hinzufuegen")

    ## Zutaten
    st.text_area("Zutaten")
    # if st.button("Zutat hinzufuegen"):
    #     col1, col2, col3 = st.columns(3)
    #     with col1:
    #         col1 = st.number_input("Anzahl")
    #     with col2:
    #         col2 = st.selectbox("Einheit", ["g", "kg", "l"])
    #     with col3:
    #         col3 = st.text_input("Zutat", placeholder="Mehl")

    ## Zubereitung
    st.text_area("Zubereitung")
    # Every form must have a submit button.
    submitted = st.form_submit_button("Rezept ersellen")
    # if submitted:
    #     st.write("slider", slider_val, "checkbox", checkbox_val)

st.write("Outside the form")