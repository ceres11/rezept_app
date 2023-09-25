import streamlit as st
import numpy as np
import pandas as pd

st.set_page_config( page_title="Home")


"# Test"


a = st.text_input("Bitte eingeben")

st.write(a)

st.write("hello")


# dataframe = pd.DataFrame(
#     np.random.randn(10, 20),
#     columns=('col %d' % i for i in range(20)))
# st.dataframe(dataframe.style.highlight_max(axis=0))


# chart_data = pd.DataFrame(
#      np.random.randn(20, 3),
#      columns=['a', 'b', 'c'])

# st.line_chart(chart_data)

# x = st.slider('x')  # 👈 this is a widget
# st.write(x, 'squared is', x * x)




# # You can access the value at any point with:
# st.session_state.name

# map_data = pd.DataFrame(
#     np.random.randn(1000, 2) / [50, 50] + [48.75, 9.25],
#     columns=['lat', 'lon'])


# st.map(map_data)





# sidebar = st.sidebar.empty()

# st.write("""
# # Simple App


# | Tables        | Are           | Cool  |
# | ------------- |:-------------:| -----:|
# | col 3 is      | right-aligned | $1600 |
# | col 2 is      | centered      |   $12 |
# | zebra stripes | are neat      |    $1 |

# """)

# zutat = "Joghurt", 100, "g"



# st.write(f"Zutaten: {zutat[1]} {zutat[2]} {zutat[0]} ")
# st.table(zutat)


# Plotting
#----------------------------------------
# progress_bar = st.sidebar.progress(0)
# status_text = st.sidebar.empty()
# last_rows = np.random.randn(1, 1)
# chart = st.line_chart(last_rows)

# for i in range(1, 101):
#     new_rows = last_rows[-1, :] + np.random.randn(5, 1).cumsum(axis=0)
#     status_text.text("%i%% Complete" % i)
#     chart.add_rows(new_rows)
#     progress_bar.progress(i)
#     last_rows = new_rows
#     time.sleep(0.05)

# progress_bar.empty()

# # Streamlit widgets automatically run the script from top to bottom. Since
# # this button is not connected to any other logic, it just causes a plain
# # rerun.
# st.button("Re-run")


# multi select
# @st.cache_data
# def get_UN_data():
#     AWS_BUCKET_URL = "https://streamlit-demo-data.s3-us-west-2.amazonaws.com"
#     df = pd.read_csv(AWS_BUCKET_URL + "/agri.csv.gz")
#     return df.set_index("Region")

# try:
#     df = get_UN_data()
#     countries = st.multiselect(
#         "Choose countries", list(df.index), ["China", "United States of America"]
#     )
#     if not countries:
#         st.error("Please select at least one country.")
#     else:
#         data = df.loc[countries]
#         data /= 1000000.0
#         st.write("### Gross Agricultural Production ($B)", data.sort_index())

#         data = data.T.reset_index()
#         data = pd.melt(data, id_vars=["index"]).rename(
#             columns={"index": "year", "value": "Gross Agricultural Product ($B)"}
#         )
#         chart = (
#             alt.Chart(data)
#             .mark_area(opacity=0.3)
#             .encode(
#                 x="year:T",
#                 y=alt.Y("Gross Agricultural Product ($B):Q", stack=None),
#                 color="Region:N",
#             )
#         )
#         st.altair_chart(chart, use_container_width=True)
# except URLError as e:
#     st.error(
#         """
#         **This demo requires internet access.**
#         Connection error: %s
#     """
#         % e.reason
#     )