from rezept_pkg import *
import glob

st.set_page_config(layout="wide")

@st.cache_resource
def get_unit_registry():
    return UnitRegistry(fmt_locale='de_DE') # slow --> cache

# @st.cache_resource
# def read_recipes_from_filesystem():
    


if 'dieses_kochbuch' not in st.session_state:
    st.session_state.dieses_kochbuch = create_kochbuch()

if 'rezept_erstellt_' not in st.session_state:
    st.session_state.rezept_erstellt_ = False

if 'rezept_erstellt_fehlschlag' not in st.session_state:
    st.session_state.rezept_erstellt_fehlschlag = False

if st.session_state.rezept_erstellt_:
    st.success("Rezept erstellt!", icon="✨")
    st.session_state.rezept_erstellt_ = False

if st.session_state.rezept_erstellt_fehlschlag:
    st.error("Rezept konnte nicht erstellt werden.", icon="❌")
    st.session_state.rezept_erstellt_fehlschlag = False

if 'portionen' not in st.session_state:
    st.session_state.portionen = 4

session = st.session_state

if 'next_radio_select' not in session:
    session.next_radio_select = 0

# if 'radio_select' not in st.session_state:
#     st.session_state.radio_select = 0


st.write("## Rezepte 🍴")


dieses_kochbuch = st.session_state.dieses_kochbuch

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
st.write(os.listdir(".\\recipes\\Kochbuch_Lukas\\Brot\\"))


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


col1, col2 = st.columns([1, 1], gap="small")
with col1:
    st.image(".\\recipes\\Kochbuch_Lukas\\Brot\\013.JPG", )

st.write(" ")
portionen = st.number_input("Portionen", key='portionen', step = 1)


    
# Using magic output
sel_recipe.portionieren(portionen)
st.table(pd.DataFrame(sel_recipe.Zutaten_portioniert, index = ["Zutat", "Menge"]).transpose())
st.write(sel_recipe.get_zubereitung())


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


unit_reg = get_unit_registry()
# --------------- Units -------------------------------
Q = unit_reg.Quantity
Q("200g").to("kg")
