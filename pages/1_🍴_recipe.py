from rezept_pkg import *
import glob

st.set_page_config(layout="wide")


# ToDo:
# - Rezepte aus Ordner lesen
#

# ------------------------------------------------------------------
#           Set up Session variables
# ------------------------------------------------------------------

if 'dieses_kochbuch' not in st.session_state:
    st.session_state.dieses_kochbuch = create_kochbuch()

if 'rezept_erstellt_' not in st.session_state:
    st.session_state.rezept_erstellt_ = False

if 'rezept_erstellt_fehlschlag' not in st.session_state:
    st.session_state.rezept_erstellt_fehlschlag = False

if 'portionen' not in st.session_state:
    st.session_state.portionen = 4



# Popup messages
if st.session_state.rezept_erstellt_:
    st.success("Rezept erstellt!", icon="✨")
    st.session_state.rezept_erstellt_ = False

if st.session_state.rezept_erstellt_fehlschlag:
    st.error("Rezept konnte nicht erstellt werden.", icon="❌")
    st.session_state.rezept_erstellt_fehlschlag = False


# load session variables
session = st.session_state
dieses_kochbuch = st.session_state.dieses_kochbuch


if 'next_radio_select' not in session:
    session.next_radio_select = 0




st.write("## Rezepte 🍴")




radio_select = st.radio("rezepte", options=dieses_kochbuch.Rezepte.keys(), label_visibility="collapsed", key="radio_select", index=st.session_state.next_radio_select)

sel_recipe = dieses_kochbuch.Rezepte[radio_select]

col1, col2, col3, col4 = st.columns([1, 1, 1, 2], gap="small")

with col1:
    rezeptname = st.text_input("rezeptname", "rezeptname", label_visibility="collapsed")

with col2:
    if st.button("Neues Rezept"):
        if rezeptname != "" and rezeptname != "rezeptname" and rezeptname not in dieses_kochbuch.Rezepte.keys():
            dieses_kochbuch.append(Rezept(rezeptname))
            st.session_state.next_radio_select = dieses_kochbuch.Rezepte.__len__() - 1
            st.session_state.rezept_erstellt_ = True
            st.rerun()
        else:
            st.session_state.rezept_erstellt_fehlschlag = True
            st.rerun()


recipe_images = []
st.write(os.listdir(".\\recipes\\Kochbuch_Lukas"))


# def create_kochbuch():
#     zubereitung = '''
#     1. Schritt: Wasser zum kochen bringen
#     2. Schritt: Zwiebeln schälen und schneiden
#     3. Schritt: Die {Zutat 1} würfeln
#     '''
#     rezept = Rezept("Schinkenbrot", {"Zutat 1": Zutat(100, "g", "Schinken"), "Zutat 2": Zutat(500, "g", "Brot")}, 2, zubereitung, autor="Lukas")


#     zubereitung2 = '''
#         1. Schritt: Wasser zum kochen bringen
#         2. Schritt: Zwiebeln schälen und schneiden
#         '''
#     rezept2 = Rezept("Kaesebrot", {"Zutat 1": Zutat(100, "g", "Kaese"), "Zutat 2": Zutat(500, "g", "Brot")}, 2, zubereitung2, autor="Lukas")

    
#     kb.append(rezept)
#     kb.append(rezept2)
#     return kb



all_recipes = {}
level = 0
top = '.\\recipes'
startinglevel = top.count(os.sep)

  
# -------------------------------------------------------------------------------------------------------------
#                        Rezept
# -------------------------------------------------------------------------------------------------------------

col1, col2 = st.columns([1, 1], gap="small")
with col1:
    st.image(".\\recipes\\Kochbuch_Lukas\\Schinkenbrot\\013.JPG", )

st.write(" ")
portionen = st.number_input("Portionen", key='portionen', step = 1, value = 4)

# Using magic output
# sel_recipe.portionieren(portionen)
# st.table(pd.DataFrame(sel_recipe.Zutaten_portioniert, index = ["Zutat", "Menge"]).transpose())
# st.write(sel_recipe.get_zubereitung())

with open(".\\recipes\\Kochbuch_Lukas\\Schinkenbrot\\zubereitung.md", mode="r", encoding="utf-8") as my_file:
    
    text = my_file.read()

    # Absätze aufteilen
    text_segmented = text.split("# ")
    dict_text_absatz = {}

    for absatz in text_segmented:
        titel = absatz.split("\n")[0]
        try:
            dict_text_absatz[titel] = absatz.split(titel)[1].strip()
        except ValueError:
            print("absatz verworfen")

    rezept_portionen = int(dict_text_absatz["Portionen:"])
    rezept_skalierung = portionen / rezept_portionen


    # Zutaten einlesen
    zutaten = dict_text_absatz["Zutatenliste:"].split("\n") # Textteil "Zutatenliste" in Zeilen aufspalten
    dict_zutaten = {}

    for i in range (0, len(zutaten)):
        zutaten[i] = zutaten[i].split(",")
        for j in range (0, len(zutaten[i])):
            try:
                zutaten[i][j] = zutaten[i][j].strip()
                dict_zutaten[zutaten[i][0][1:-1]] = "`" + str(rezept_skalierung * int(zutaten[i][2].split(" ")[0])) + " " + zutaten[i][2].split(" ")[1] + " " + zutaten[i][1] + "`"
            except (IndexError, ValueError):
                print("line " + str(i) + " removed.")


    output = dict_text_absatz["Zubereitung:"].format(**dict_zutaten)
    st.markdown(output)


# ---------------------- DEBUG -------------------------------------------------------------
st.write("## Debug")
st.json(json.dumps(dieses_kochbuch, default=json_encoder, sort_keys=False, indent=4))



level = 0

top = '.\\recipes'
startinglevel = top.count(os.sep)
  
st.write("## File structure")
for (root, dirs, files) in os.walk(".\\recipes"):
    level = root.count(os.sep) - startinglevel
    st.write(level) 
    st.write(root)
    st.write(dirs)
    st.write(files)
    st.markdown("---")


    
st.write("## File structure")
for (root, dirs, files) in os.walk(".\\recipes"):
    level = root.count(os.sep) - startinglevel

    st.write(root)
    st.write(level)
    
    match level:
        case 0:
            for kochbuch in dirs:
                all_recipes[kochbuch] = Kochbuch(kochbuch)
        case 1:
            for recipe in dirs:
                all_recipes[root.split("\\")[-1]].append(Rezept(recipe))

        case 2:
            for file in files:
                (filename, file_extension) = os.path.splitext(file)
                if file_extension == ".json":
                    with open(root + "\\" + file, 'r') as json_file:
                        st.write(json.load(json_file))

        


                # json.loads()
                # i = 1

# for recipe in all_recipes:
st.json(json.dumps(all_recipes, default=json_encoder, sort_keys=False, indent=4))