from pages import *


if "user" not in st.session_state:
    print("run initialize")
    initialize_session_state_variables()

st.write("## Rezepte 🍴")


# --------------- Units -------------------------------
unit_reg = UnitRegistry()
Q = unit_reg.Quantity
Q("200g").to("kg")
unit_reg = UnitRegistry(fmt_locale='de_DE')

radio_select = st.radio("rezepte", options=st.session_state.dieses_kochbuch.Rezepte.keys(), label_visibility="hidden")

col1, col2, _ = st.columns([1, 1, 2], gap="small")

with col1:
    if st.button("Rezept bearbeiten"):
        st.session_state.edit_recipe = st.session_state.dieses_kochbuch.Rezepte[radio_select]
        switch_page("recipe_editor")

with col2:
    if st.button("Neues Rezept"):
        switch_page("recipe_editor")

# Using magic output
sel_recipe = st.session_state.dieses_kochbuch.Rezepte[radio_select]
st.markdown(sel_recipe.to_docstring())

# ---------------------- DEBUG -------------------------------------------------------------
st.write("## Debug")

st.json(json.dumps(st.session_state.dieses_kochbuch, default=lambda o: o.__dict__, sort_keys=False, indent=4))

st.write(st.session_state)

unit_reg = get_unit_registry()
