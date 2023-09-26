import streamlit as st
import pandas as pd
import json
from pint import UnitRegistry
from copy import deepcopy
from streamlit_extras.switch_page_button import switch_page


class Zutat:
    name: str
    menge: UnitRegistry.Quantity
    num: int
    list: list

    def __init__(self, name: str, menge: str, unit_reg: UnitRegistry):

        self.name = name
        self.menge = unit_reg(menge)

        self.list = []
        self.list.append(self.name)
        self.list.append(self.menge)

    def __str__(self):
        return str(self.menge) + " " + self.name

    def __dict__(self):  # for JSON dump
        # temp = {}
        # temp["name"] = self.name
        # temp["menge"] = str(self.menge)
        # return temp
        return

    def __iter__(self):
        self.num = 0
        return self

    def __next__(self):
        if self.num <= 1:
            self.num += 1
        else:
            raise StopIteration

        return self.list[self.num - 1]


class Rezept:
    name: str
    autor: str
    zutaten: str
    zubereitung: str

    def __init__(self, name: str, zutaten: str, zubereitung: str, autor="anonym"):  # warum wird dict angenommen?
        self.name = name
        self.autor = autor
        self.Zutaten = zutaten
        self.zubereitung = zubereitung

    def display(self):
        st.write(f"## {self.name}")
        st.caption(f"*von {self.autor}*")
        st.write("### Zutaten")
        st.write(f"{self.Zutaten}")
        st.write("### Zubereitung")
        st.write(f"{self.zubereitung}")


class Kochbuch:
    Rezepte: list

    def __init__(self, name: str):
        self.name = name
        self.Rezepte = {}

    def append(self, rezept: Rezept):
        self.Rezepte[rezept.name] = rezept


def initialize_session_state_variables():
    create_kochbuch(user=st.session_state.user)
    st.session_state.edit_recipe = ""


def create_kochbuch(user = None):
    zubereitung = '''
    1. Schritt: Wasser zum kochen bringen
    2. Schritt: Zwiebeln schälen und schneiden
    3. Schritt: 
    '''  # {Zutat 1} kann von str.format() nachgeschlagen werden.

    rezept = Rezept("Schinkenbrot", "- 100g Schinken \n- 100 g Brot", zubereitung, autor="Lukas")

    zubereitung = '''
    1. Schritt: Wasser zum kochen bringen
    2. Schritt: Zwiebeln schälen und schneiden
    '''

    rezept2 = Rezept("Käsebrot", "100g Käse", zubereitung)
    st.session_state.dieses_kochbuch = Kochbuch("Lukas' Kochbuch")
    "# Test"
    st.session_state.dieses_kochbuch.append(rezept)
    st.session_state.dieses_kochbuch.append(rezept2)
