import streamlit as st
import pandas as pd
import json

from pint import UnitRegistry
from copy import deepcopy


# Todos
# - file read
# - file write


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
    
    def __dict__(self): # for JSON dump
        # temp = {}
        # temp["name"] = self.name
        # temp["menge"] = str(self.menge)
        # return temp
        return
    
    def __iter__(self):
        self.num  = 0
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
    Zutaten: dict

    portionen: int # die Standard-Portionszahl

    unit_reg: UnitRegistry


    def __init__(self, name: str, autor: str,  zutaten: dict, portionen: int, unit_registry: UnitRegistry): # warum wird dict angenommen?
        self.name = name
        self.autor = autor
        self.Zutaten  = zutaten
        self.portionen = portionen
        self.unit_reg = unit_registry

    def add_zubereitung(self, beschreibung: str):
        self.beschreibung = beschreibung # Zutaten werden rein formatiert
    
    def get_zubereitung(self, portionen = 0):
        if portionen == 0: 
            portionen = self.portionen
            #Todo: Zutaten * menge

        temp_Zutaten = {}
        for Zutat in self.Zutaten:
            temp_Zutaten[Zutat.name] = str(Zutat.menge), self.unit_reg

        return self.beschreibung.format(**temp_Zutaten)


class Kochbuch:
    Rezepte: list

    def __init__(self, name: str):  
        self.name = name
        self.Rezepte = {}

    def append(self, rezept: Rezept):
        self.Rezepte[rezept.name] = rezept



st.sidebar.markdown("# Rezepte 🍴")
st.write("## Rezepte 🍴")


# --------------- Units -------------------------------
unit_reg = UnitRegistry()
Q = unit_reg.Quantity
Q("200g").to("kg")

st.write('Variable =  {:P}'.format(Q("10 m/s^2"))) # Markdown
st.latex('Variable =  {:L}'.format(Q("10 m/s^2"))) # LaTex
st.write('Variable =  {:H}'.format(Q("10 m/s^2"))) # html

# zutat1 = Zutat("Salz", 100, "gram", unit_reg)
# print(zutat1.menge.to("kg"))
# zutat1.menge

# st.balloons()
# st.toast('Your Rezipe was saved!', icon='😍')

unit_reg = UnitRegistry(fmt_locale='de_DE')



rezept = Rezept( "Schinkenbrot", "Lukas", {
    "Zutat 1": Zutat("Schinken", "100 g", unit_reg),
    "Zutat 2": Zutat("Brot", "100 g", unit_reg)
}, 4, unit_reg)


rezept.add_zubereitung('''Zubereitung:
1. Schritt: Wasser zum kochen bringen
2. Schritt: Zwiebeln schälen und schneiden
3. Schritt: {Zutat 1}
''') # {Zutat 1} kann von str.format() nachgeschlagen werden.

rezept2 = Rezept( "Käsebrot", "Lukas", {
    "Zutat 1": [100, "g", "Käse"]
}, 4, unit_reg)

rezept2.add_zubereitung('''Zubereitung:
1. Schritt: Wasser zum kochen bringen
2. Schritt: Zwiebeln schälen und schneiden
3. Schritt: {Zutat 1[0]}
''')

dieses_kochbuch = Kochbuch("Lukas' Kochbuch")
dieses_kochbuch.append(rezept)
dieses_kochbuch.append(rezept2)



# with st.expander("Alle Rezepte"):
radio_select = st.radio("Rezepte", dieses_kochbuch.Rezepte.keys())

#Using magic output
"## Rezept"
sel_recipe = dieses_kochbuch.Rezepte[radio_select]


sel_recipe.name
sel_recipe.autor

st.table(pd.DataFrame(sel_recipe.Zutaten, index = ["Zutat", "Menge"]).transpose())


portionen = 4
st.write(sel_recipe.get_zubereitung(portionen))






    # st.write(dieses_kochbuch.Rezepte[key])

# st.text_input("Portionen", key="n")
# Zutaten_output = pd.DataFrame(rezept.Zutaten, index = ["Menge", "Einheit", "Zutat"]).transpose()


# st.dataframe(Zutaten_output)  


# ---------------------- DEBUG -------------------------------------------------------------
st.write("## Debug")
st.json(json.dumps(dieses_kochbuch, default=lambda o: o.__dict__, sort_keys=False, indent=4))