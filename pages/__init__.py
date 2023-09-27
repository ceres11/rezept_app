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
    menge: float
    einheit: str
    name: str
    i: int
    
    def __init__(self, menge: float, einheit: str, name: str):
        self.name = str(name)
        self.menge = float(menge)
        self.einheit = str(einheit)

    @staticmethod
    def construct_from_str(input_str: str):
        rows = input_str.split("\n")
        for i, row in enumerate(rows):
            rows[i] = row.replace("- ", "").split(" ")
            rows[i] = Zutat(rows[i][0], rows[i][1], rows[i][2])
        return rows

    def __repr__(self):
        return str(self.menge) + " " + self.einheit + " " + self.name
    
    def __dict__(self): # for JSON dump
        # temp = {}
        # temp["name"] = self.name
        # temp["menge"] = str(self.menge)
        # return temp
        return
    
    def __iter__(self):
        self.i = 0
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

    Zutaten: list
    zubereitung: str
    portionen: int # die Standard-Portionszahl
    Zutaten_portioniert: dict

    def __init__(self, name: str,  zutaten: list, portionen: int, zubereitung: str, autor="anonym"):
        self.name = name
        self.Zutaten = zutaten
        self.portionen = portionen
        self.zubereitung = zubereitung
        self.autor = autor
        # self.Zutaten_portioniert = {}
        #
        # for key in self.Zutaten:
        #     z = self.Zutaten[key]
        #     self.Zutaten_portioniert[key] = Zutat(z.name, z.menge, z.einheit)

    def str_zutaten(self):
        zutaten_string = "- " + "\n- ".join([str(zutat) for zutat in self.Zutaten])
        return zutaten_string

    def to_docstring(self):
        return f"""## {self.name}\n*von {self.autor}*\n### Zutaten\n{self.str_zutaten()}\n### Zubereitung\n{self.zubereitung}"""

    def __str__(self):
        return f'''
        Rezept: {self.name}
        Autor: {self.autor}
        '''


    # def add_zubereitung(self, beschreibung: str):
    #     self.beschreibung = beschreibung # Zutaten werden rein formatiert

    # def portionieren(self, portionen: int):
    #     for key in self.Zutaten_portioniert:
    #         self.Zutaten_portioniert[key].menge *= portionen
    #     return

        # self.Zutaten_portioniert = copy.deepcopy(self.Zutaten)
        # print("Zutaten")
        # print(self.Zutaten)
        # print("portioniert")
        # print(self.Zutaten_portioniert)

    # def get_zubereitung(self):
    #     return self.beschreibung.format(**self.Zutaten_portioniert)


class Kochbuch:
    Rezepte: dict

    def __init__(self, name: str):
        self.name = name
        self.Rezepte = {}

    def append(self, rezept: Rezept):
        self.Rezepte[rezept.name] = rezept


def initialize_session_state_variables(user="anonym"):
    st.session_state.user = user
    st.session_state.edit_recipe = ""
    st.session_state.dieses_kochbuch = create_kochbuch()


def create_kochbuch():
    zubereitung = '''
    1. Schritt: Wasser zum kochen bringen
    2. Schritt: Zwiebeln schälen und schneiden
    3. Schritt: 
    '''
    rezept = Rezept("Schinkenbrot", [Zutat(100, "g", "Schinken"), Zutat(500, "g", "Brot")], 2, zubereitung, autor="Lukas")
    zubereitung2 = '''
        1. Schritt: Wasser zum kochen bringen
        2. Schritt: Zwiebeln schälen und schneiden
        '''
    rezept2 = Rezept("Kaesebrot", [Zutat(100, "g", "Kaese"), Zutat(500, "g", "Brot")], 2, zubereitung2, autor="Lukas")

    kb = Kochbuch("Lukas' Kochbuch")
    kb.append(rezept)
    kb.append(rezept2)
    return kb


