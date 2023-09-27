from pages import *

if "user" not in st.session_state:
    initialize_session_state_variables()

# editing existing recipes:
if st.session_state.edit_recipe != "":
    pr_recipe = st.session_state.edit_recipe
    prev_name = pr_recipe.name
    prev_zutaten = pr_recipe.zutaten_to_str()
    prev_zubereitung = pr_recipe.zubereitung
    st.write(f'# "{pr_recipe.name}" bearbeiten')

# new recipes:
else:
    st.write("# Neues Rezept")
    prev_name, prev_zutaten, prev_zubereitung = "", "", ""

# Rezeptdaten eingeben / uebernehmen
autor = st.session_state.user
name = st.text_input("Name", prev_name)
bild = st.file_uploader("Bild hinzufuegen")
zutaten = st.text_area("Zutaten", prev_zutaten)
zubereitung = st.text_area("Zubereitung", prev_zubereitung)

vorschau = st.button("Rezept generieren")

if vorschau:
    # Zutaten input formatieren:
    zutaten = zutaten.replace("- ", "").split("\n")
    for i in range(len(zutaten)):
        zutaten[i] = Zutat.from_str(zutaten[i])
    # Rezept erstellen und anzeigen
    st.caption("[Vorschau]")
    st.session_state.r = Rezept(name, zutaten, 1, zubereitung, autor)
    st.markdown(st.session_state.r.to_docstring())

submit_recipe = st.button("Rezept erstellen/ aktualisieren")

if submit_recipe:
    st.session_state.dieses_kochbuch.append(st.session_state.r)
    st.balloons()
    st.toast('Your Rezipe was saved!', icon='😍')

# ---------------------- DEBUG -------------------------------------------------------------
st.write("## Debug")

st.json(json.dumps(st.session_state.dieses_kochbuch, default=lambda o: o.__dict__, sort_keys=False, indent=4))

st.write("### Session states:")
st.write(st.session_state)
