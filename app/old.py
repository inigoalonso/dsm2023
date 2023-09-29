
# Add a logo
# def add_logo():
#     # https://discuss.streamlit.io/t/put-logo-and-title-above-on-top-of-page-navigation-in-sidebar-of-multipage-app/28213/4
#     st.markdown(
#         """
#         <style>
#             [data-testid="stHeader"]::before {
#                 content: "Industry Sprint Workshop";
#                 margin-left: 20px;
#                 margin-top: 20px;
#                 font-size: 30px;
#                 position: relative;
#             }
#         </style>
#         """,
#         unsafe_allow_html=True,
#     )

# add_logo()

# from utils import set_bg
# set_bg('assets/background.png')

####################
# Sidebar          #

# st.sidebar.header("Navigation")

###############################################################################

import altair as alt

            # Compute x^2 + y^2 across a 2D grid
            x, y = np.meshgrid(
                range(1, len(product_elements)), range(1, len(product_elements))
            )
            distance = x**2 + y**2

            # Convert this grid to columnar data expected by Altair
            source = pd.DataFrame(
                {"x": x.ravel(), "y": y.ravel(), "z": distance.ravel()}
            )

            chart = alt.Chart(source).mark_rect().encode(x="x:O", y="y:O", color="z:Q")

            st.altair_chart(chart, theme="streamlit")

###############################################################################

            # tab_matrices_1, tab_matrices_2, tab_matrices_3 = st.tabs(
            #     [
            #         "DSM",
            #         "Distance matrix",
            #         "Risk matrix",
            #     ]
            # )

            # with tab_matrices_1:
            #     st.write("DSM")
            #     st.image("assets/dsm.png", width=600)
            # with tab_matrices_2:
            #     st.write("Distance matrix")
            #     st.image("assets/distance.png", width=600)
            # with tab_matrices_3:
            #     st.write("Risk matrix")
            #     st.image("assets/risk.png", width=600)

            # df_test = pd.DataFrame({"foo": [1, 2, 3], "bar": [4, 5, 6]})
            # styler = df_test.style.background_gradient(cmap=cm_g2r)
            # styler.set_table_styles([
            #     {"selector": "tr", "props": "line-height: 10px;"},
            #     {"selector": "td,th", "props": "line-height: inherit; padding: 0;"}
            # ])
            # html = styler.to_html()
            # st.write(html, unsafe_allow_html=True)

            # df_s1_dsm = pd.read_csv("data/s1_dsm.csv", sep=";", header=None, decimal=",").fillna(0)
            # df_s2_dsm = pd.read_csv("data/s2_dsm.csv", sep=";", header=None, decimal=",").fillna(0)
            # df_s3_dsm = pd.read_csv("data/s3_dsm.csv", sep=";", header=None, decimal=",").fillna(0)
            # df_s1_distances = pd.read_csv("data/s1_distances.csv", sep=";", header=None, decimal=",").fillna(0)
            # df_s2_distances = pd.read_csv("data/s2_distances.csv", sep=";", header=None, decimal=",").fillna(0)
            # df_s3_distances = pd.read_csv("data/s3_distances.csv", sep=";", header=None, decimal=",").fillna(0)

            # styler = df_s1_distances.style.background_gradient(cmap=cm_g2r)
            # styler.set_table_styles([
            #     {"selector": "tr", "props": "line-height: 12px;"},
            #     {"selector": "td,th", "props": "line-height: inherit; padding: 0;"}
            # ])
            # html = styler.to_html()

            # if system == "System 1 - Only front steering":
            #     st.write("System 1 - Only front steering")
            #     st.dataframe(df_s1_dsm)
            #     st.write(html, unsafe_allow_html=True)
            #     #st.dataframe(df_s1_distances.style.background_gradient(cmap=cm_r2g).format({2: '{:.2f}'}, na_rep='MISS', precision=2))
            # elif system == "System 2 - Front + Back steering (hydraulic)":
            #     st.write("System 2 - Front + Back steering (hydraulic)")
            #     st.dataframe(df_s2_dsm)
            #     st.dataframe(df_s2_distances.style.background_gradient(cmap=cm_r2g).format({2: '{:.2f}'}, na_rep='MISS', precision=2))
            # elif system == "System 3 - Front + Back steering (electric)":
            #     st.write("System 3 - Front + Back steering (electric)")
            #     st.dataframe(df_s3_dsm)
            #     st.dataframe(df_s3_distances.style.background_gradient(cmap=cm_r2g).format({2: '{:.2f}'}, na_rep='MISS', precision=2))
            # else:
            #     n = 10



