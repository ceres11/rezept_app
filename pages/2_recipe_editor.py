from pages import *

for i in st.session_state.items():
    i
prev_name, prev_zutaten, prev_zubereitung = "", "", ""

st.write(st.session_state.dieses_kochbuch.Rezepte.keys())

if st.session_state.edit_recipe != "":
    pr_recipe = st.session_state.edit_recipe
    prev_name = pr_recipe.name
    prev_zutaten = pr_recipe.Zutaten
    prev_zubereitung = pr_recipe.zubereitung
    st.write(f'# "{pr_recipe.name}" bearbeiten')
else:
    st.write("# Neues Rezept")

# Rezeptdaten eingeben / uebernehmen
with st.form("my_form"):
    # Autor option
    autor = "anonym"
    # Rezeptname
    name = st.text_input("Name", prev_name)
    # Bild
    bild = st.file_uploader("Bild hinzufuegen")
    # Zutaten
    zutaten = st.text_area("Zutaten", prev_zutaten)
    # Zubereitung
    zubereitung = st.text_area("Zubereitung", prev_zubereitung)

    vorschau = st.form_submit_button("Rezept generieren")

if vorschau:
    st.caption("[Vorschau]")
    r = Rezept(name, zutaten, zubereitung)
    r.display()

submit_recipe = st.button("Rezept erstellen/ aktualisieren")

if submit_recipe:
    st.session_state.dieses_kochbuch = st.session_state.dieses_kochbuch.append(Rezept(name, zutaten, zubereitung))
    st.balloons()
    st.toast('Your Rezipe was saved!', icon='😍')

