import streamlit as st
import pandas as pd
import json

from pint import UnitRegistry


# Todos
# - file read
# - file write

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


st.sidebar.markdown("# Rezepte 🍴")
st.write("## Rezepte 🍴")


st.button("Rezept erstellen")
st.button("Rezept bearbeiten")


rezept = Rezept( "Schinkenbrot", "Lukas", {
    "Zutat 1": Zutat("Schinken", 200, "g"),
    "Zutat 2": Zutat("Brot", 100, "g")
}, 4)



rezept.add_zubereitung('''Zubereitung:
1. Schritt: Wasser zum kochen bringen
2. Schritt: Zwiebeln schälen und schneiden
3. Schritt: {Zutat 1}
''') # {Zutat 1} kann von str.format() nachgeschlagen werden.

rezept2 = Rezept( "Käsebrot", "Lukas", {
    "Zutat 1": Zutat("Käse", 200, "g"),
    "Zutat 2": Zutat("Brot", 100, "g")
}, 4)

rezept2.add_zubereitung('''Zubereitung:
1. Schritt: Wasser zum kochen bringen
2. Schritt: Zwiebeln schälen und schneiden
3. Schritt: {Zutat 1}
''')

dieses_kochbuch = Kochbuch("Lukas' Kochbuch")
dieses_kochbuch.append(rezept)
dieses_kochbuch.append(rezept2)



# with st.expander("Alle Rezepte"):
radio_select = st.radio("Rezepte", dieses_kochbuch.Rezepte.keys())

#Using magic output
"## Rezept"
sel_recipe = dieses_kochbuch.Rezepte[radio_select]


col1 , col2, col3, col4 = st.columns([1,1,1,2])

with col1:
    "Portionen"

with col2:
    portionen = int(st.text_input("", value = "4", label_visibility='collapsed'))

with col3:
    st.button("Zurücksetzen")
    

sel_recipe.name
sel_recipe.autor

sel_recipe.portionieren(portionen)

st.table(pd.DataFrame(sel_recipe.Zutaten_portioniert, index = ["Zutat", "Menge"]).transpose())
st.write(sel_recipe.get_zubereitung())



unit_reg = get_unit_registry()



# ---------------------- DEBUG -------------------------------------------------------------
# st.write("## Debug")
# st.json(json.dumps(dieses_kochbuch, default=lambda o: o.__dict__, sort_keys=False, indent=4))