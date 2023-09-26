import streamlit as st
import pandas as pd
import json
from pint import UnitRegistry
from copy import deepcopy
from streamlit_extras.switch_page_button import switch_page


@st.cache_resource
def get_unit_registry():
    return UnitRegistry(fmt_locale='de_DE') # slow!


class Zutat:
    # class variables
    einheiten = ["g", "kg", "l", "ml"]

    # instance variables
    name: str
    menge: int
    einheit: str
    i: int
    
    def __init__(self, name: str, menge: int, einheit: str):

        self.name = name
        self.menge = menge
        self.einheit = einheit


    def __str__(self):
        return str(self.menge) + " " + self.einheit + " " + self.name
    
    def __dict__(self): # for JSON dump
        # temp = {}
        # temp["name"] = self.name
        # temp["menge"] = str(self.menge)
        # return temp
        return
    
    def __iter__(self):
        self.i  = 0
        return self
    
    def __next__(self):

        self.i += 1

        match self.i:
            case 1: return self.name
            case 2: return str(self.menge) + " " + self.einheit
            case 3: raise StopIteration

class Rezept:
    name: str
    autor: str

    Zutaten: dict

    portionen: int # die Standard-Portionszahl
    Zutaten_portioniert: dict

    def __init__(self, name: str, autor: str,  zutaten: dict, portionen: int):
        self.name = name
        self.autor = autor
        self.Zutaten  = zutaten
        self.portionen = portionen

        self.Zutaten_portioniert = {}

        for key in self.Zutaten:
            z = self.Zutaten[key]
            self.Zutaten_portioniert[key] = Zutat(z.name, z.menge, z.einheit)

    def display(self):
        st.write(f'''{self.name}''')
        st.write(f"## ")
        st.caption(f"*von {self.autor}*")
        st.write("### Zutaten")
        st.write(f"{self.Zutaten}")
        st.write("### Zubereitung")
        st.write(f"{self.zubereitung}")

    def add_zubereitung(self, beschreibung: str):
        self.beschreibung = beschreibung # Zutaten werden rein formatiert

    def portionieren(self, portionen: int):
        for key in self.Zutaten_portioniert:
            self.Zutaten_portioniert[key].menge *= portionen
        return
    

        # self.Zutaten_portioniert = copy.deepcopy(self.Zutaten)
        # print("Zutaten")
        # print(self.Zutaten)
        # print("portioniert")
        # print(self.Zutaten_portioniert)


    def get_zubereitung(self):
        return self.beschreibung.format(**self.Zutaten_portioniert)




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
