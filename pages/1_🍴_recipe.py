from rezept_pkg import *
import glob
import numpy as np
import io

st.set_page_config(layout="wide")


# ------------------------------------------------------------------
#           Set up Session variables
# ------------------------------------------------------------------

if 'selected_kochbuch' not in st.session_state:
    st.session_state.selected_kochbuch = 0

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
selected_kochbuch = st.session_state.selected_kochbuch


if 'next_radio_select' not in session:
    session.next_radio_select = 0




st.write("## Rezepte 🍴")

PATH_RECIPES = ".\\recipes\\"

selected_kochbuch = st.radio("Kochbuch", options=os.listdir(PATH_RECIPES), key="select_kochbuch", index=st.session_state.selected_kochbuch)
path_kochbuch = PATH_RECIPES + selected_kochbuch

sel_recipe = st.radio("Rezepte", options=os.listdir(path_kochbuch), key="radio_select", index=st.session_state.next_radio_select)
path_recipe = path_kochbuch + "\\" + sel_recipe


  
# -------------------------------------------------------------------------------------------------------------
#                        Rezept
# -------------------------------------------------------------------------------------------------------------
st.write("## " + sel_recipe)


# Todo:
# - Rezept-Upload
# - Zutaten-parser
# - Bildfindung verbessern

col1, col2 = st.columns([1, 1], gap="small")
with col1:
    try:
        st.image(path_recipe + "\\picture.jpg")
    except:
        print("tried opening picture type")
    try:
        st.image(path_recipe + "\\picture.png")
    except:
        print("tried opening picture type")

st.write(" ")
portionen = st.number_input("Portionen", key='portionen', step = 1, value = 4)



# ToDo:
# - Eingangs-Parser (Zutaten)
# - Rezept cache

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

    # Zutaten einlesen, skalieren
    df = pd.read_csv(io.StringIO(dict_text_absatz["Zutatenliste:"]), sep=",", names=["Name", "Zutat", "Menge", "Einheit"])
    
    rezept_portionen = int(dict_text_absatz["Portionen:"])
    rezept_skalierung = portionen / rezept_portionen
    df["Menge"] *= rezept_skalierung


    # Zutaten Dictionary zur Text-Formatierung
    dict_zutaten_output = {}
    for row in df.index:
        dict_zutaten_output[df["Name"][row]] = "`" + str(df["Menge"][row]) + df["Einheit"][row] + df["Zutat"][row] + "`"


    # Ausgabe:
    st.data_editor(df, hide_index=True)
    st.markdown(dict_text_absatz["Zubereitung:"].format(**dict_zutaten_output))


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