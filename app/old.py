
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