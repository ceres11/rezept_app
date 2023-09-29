import streamlit as st
import pandas as pd
import json
from pint import UnitRegistry
from streamlit_extras.switch_page_button import switch_page
import os



# def initialize_session_state_variables(user="anonym"):
#     st.session_state.user = user
#     st.session_state.edit_recipe = ""


# @ todo: cache recipe load?
# e.g.: data = read.json(*alle rezepte*)


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

    # @staticmethod
    # def from_str(input_str: str):
    #     """
    #     :param input_str: mit dem Format: "Menge Einheit Zutat"
    #     :return: Zutat instanz
    #     """
    #     split_s = input_str.split(" ")
    #     return Zutat(split_s[0], split_s[1], split_s[2])

    def __repr__(self):
        # return [str(self.menge) , self.einheit , self.name]
        return str(self.menge) + " " + self.einheit + " " + self.name

    def __str__(self) -> str:
        return str(self.menge) + " " + self.einheit + " " + self.name
    
    def __dict__(self) -> dict: # for JSON dump
        # temp = {}
        # temp["name"] = self.name
        # temp["menge"] = str(self.menge)
        # return temp
        return {"menge": self.menge , "einheit": self.einheit , "name": self.name}
        # return self.__str__()
    
    
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

    Zutaten: dict
    zubereitung: str
    portionen: int # die Standard-Portionszahl
    Zutaten_portioniert: dict
    # @todo: attribut "in kochbuch" hinzufuegen um Rezepte zu kochbuechern zuordnen zu koennen?

    def __init__(self, name: str,  zutaten: dict = {}, portionen: int = 4, zubereitung: str = "Bitte Zubereitung eingeben", autor="anonym"):
        self.name = name
        self.Zutaten = zutaten

        if portionen == 0: self.portionen = 4
        else: self.portionen = portionen

        self.zubereitung = zubereitung
        self.autor = autor
        self.Zutaten_portioniert = {}

        for key in self.Zutaten:
            z = self.Zutaten[key]
            self.Zutaten_portioniert[key] = Zutat(z.menge, z.einheit, z.name)

    def zutaten_to_str(self):
        # Helpermethode fuer to_docstring()
        zutaten_string = "- " + "\n- ".join([str(zutat) for zutat in self.Zutaten])
        return zutaten_string

    def to_docstring(self):
        return f"""## {self.name}\n*von {self.autor}*\n### Zutaten\n{self.zutaten_to_str()}\n### Zubereitung\n{self.zubereitung}"""

    def __str__(self):
        return f'''
        Rezept: {self.name}
        Autor: {self.autor}
        '''

    def add_zubereitung(self, beschreibung: str):
        self.zubereitung = beschreibung # Zutaten werden rein formatiert

    def portionieren(self, portionen: int):
        for key in self.Zutaten_portioniert:
            self.Zutaten_portioniert[key].menge = (portionen / self.portionen) * self.Zutaten[key].menge
        return

    def get_zubereitung(self):
        return self.zubereitung.format(**self.Zutaten_portioniert)


class Kochbuch:
    Rezepte: dict

    def __init__(self, name: str):
        self.name = name
        self.Rezepte = {}

    def append(self, rezept: Rezept):
        self.Rezepte[rezept.name] = rezept


def create_kochbuch():
    zubereitung = '''
    1. Schritt: Wasser zum kochen bringen
    2. Schritt: Zwiebeln schälen und schneiden
    3. Schritt: Die {Zutat 1} würfeln
    '''
    rezept = Rezept("Schinkenbrot", {"Zutat 1": Zutat(100, "g", "Schinken"), "Zutat 2": Zutat(500, "g", "Brot")}, 2, zubereitung, autor="Lukas")


    zubereitung2 = '''
        1. Schritt: Wasser zum kochen bringen
        2. Schritt: Zwiebeln schälen und schneiden
        '''
    rezept2 = Rezept("Kaesebrot", {"Zutat 1": Zutat(100, "g", "Kaese"), "Zutat 2": Zutat(500, "g", "Brot")}, 2, zubereitung2, autor="Lukas")

    kb = Kochbuch("Lukas' Kochbuch")
    kb.append(rezept)
    kb.append(rezept2)
    return kb


def save_all():
    pass  # @todo: write to json

def json_encoder(o):
    # if(type(o) == Zutat): return str(o)
    if(type(o) == Zutat): return o.__dict__()
    return o.__dict__
