from pages import *

if "user" not in st.session_state:
    initialize_session_state_variables()

# for editing existing recipes:
if st.session_state.edit_recipe != "":
    pr_recipe = st.session_state.edit_recipe
    prev_name = pr_recipe.name
    prev_zutaten = pr_recipe.str_zutaten()
    prev_zubereitung = pr_recipe.zubereitung
    st.write(f'# "{pr_recipe.name}" bearbeiten')

# for creating new recipes:
else:
    st.write("# Neues Rezept")
    prev_name, prev_zutaten, prev_zubereitung = "", "", ""

# Rezeptdaten eingeben / uebernehmen
# Autor option
autor = st.session_state.user

# Rezeptname
name = st.text_input("Name", prev_name)

# Bild
bild = st.file_uploader("Bild hinzufuegen")

# Zutaten

zutaten = st.text_area("Zutaten", prev_zutaten)

# manuell Zutatenreihen (Menge, Einheit, Zutat) hinzufuegen:
# col1, col2, col3 = st.columns([1, 1, 3])
# list_zutaten = []
#
#
# def set_zutaten_rows():
#     m, e, z = "menge", "einheit", "zutat"
#
#     for i in range(st.session_state.n_zutaten):
#         l_m = col1.number_input(m + str(i), min_value=.1, max_value=1000., value=1., step=1., label_visibility="hidden", key=m+str(i))
#         l_e = col2.selectbox(e + str(i), Zutat.einheiten, label_visibility="hidden", key=e+str(i))
#         l_z = col3.text_input(z + str(i), label_visibility="hidden", key=z+str(i))
#         list_zutaten.append([l_m, l_e, l_z])
#
#     st.session_state.n_zutaten += 1

#
# st.button("Zutat hinzufuegen", on_click=set_zutaten_rows())

# Zubereitung
zubereitung = st.text_area("Zubereitung", prev_zubereitung)

vorschau = st.button("Rezept generieren")

if vorschau:
    st.caption("[Vorschau]")

    # Zutaten input formatieren:
    zutaten = zutaten.split("\n")
    for i in range(len(zutaten)):
        zutaten[i] = Zutat.from_str(zutaten[i])

    # Rezept erstellen und anzeigen
    r = Rezept(name, zutaten, 1, zubereitung, autor)
    st.markdown(r.to_docstring())

submit_recipe = st.button("Rezept erstellen/ aktualisieren")

if submit_recipe:
    st.session_state.dieses_kochbuch.append(Rezept(name, zutaten, 1, zubereitung, autor))
    st.balloons()
    st.toast('Your Rezipe was saved!', icon='😍')

# ---------------------- DEBUG -------------------------------------------------------------
st.write("## Debug")

st.json(json.dumps(st.session_state.dieses_kochbuch, default=lambda o: o.__dict__, sort_keys=False, indent=4))

st.write(st.session_state)