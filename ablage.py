

class test:

    var1 = 1
    var2 = 2
    var3 = 3

    def __init__(self):
        self.var1 = 4
        self.var2 = 5

    

test1 = test()

a = 2

# --------------- Units -------------------------------
# unit_reg = UnitRegistry()
# Q = unit_reg.Quantity
# Q("200g").to("kg")

# st.write('Variable =  {:P}'.format(Q("10 m/s^2"))) # Markdown
# st.latex('Variable =  {:L}'.format(Q("10 m/s^2"))) # LaTex
# st.write('Variable =  {:H}'.format(Q("10 m/s^2"))) # html

# zutat1 = Zutat("Salz", 100, "gram", unit_reg)
# print(zutat1.menge.to("kg"))
# zutat1.menge

# st.balloons()
# st.toast('Your Rezipe was saved!', icon='😍')