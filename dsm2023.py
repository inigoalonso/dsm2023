"""
# DSM 2023 Workshop
This app helps the participants of the DSM Industry Sprint Workshop.
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Set wide display, if not done before
try:
    st.set_page_config(
        layout="wide",
        page_title="Industry Sprint Workshop 2023 - The 25th International DSM Conference",
        # page_icon="🚚",
        page_icon="favicon.jpg",
        # initial_sidebar_state="expanded",
        )
except:
    pass

# Hide the menu and the footer
hide_st_style = """<style>#MainMenu {visibility: hidden;} footer {visibility: hidden;}</style>"""
st.markdown(hide_st_style, unsafe_allow_html=True)

def add_logo():
    # https://discuss.streamlit.io/t/put-logo-and-title-above-on-top-of-page-navigation-in-sidebar-of-multipage-app/28213/4
    st.markdown(
        """
        <style>
            [data-testid="stHeader"]::before {
                content: "Industry Sprint Workshop";
                margin-left: 20px;
                margin-top: 20px;
                font-size: 30px;
                position: relative;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )
add_logo()


# st.header('Industry Sprint Workshop 2023')

st.markdown('The DSM 2023 Industry Sprint Workshop is brought to you in collaboration with Volvo Group.')

# with st.sidebar:
#     # Upload files
#     st.header('Sidebar')


# Display the session state
# st.write('Session state: ',st.session_state)

df = pd.DataFrame(
    [
        {"name": "Element 1", "x": 4, "y": 3, "z": 2},
        {"name": "Element 2", "x": 5, "y": 3, "z": 2},
        {"name": "Element 3", "x": 4, "y": 3, "z": 2},
        {"name": "Element 1", "x": 4, "y": 3, "z": 2},
        {"name": "Element 2", "x": 5, "y": 3, "z": 2},
        {"name": "Element 3", "x": 4, "y": 3, "z": 2},
        {"name": "Element 1", "x": 4, "y": 3, "z": 2},
        {"name": "Element 2", "x": 5, "y": 3, "z": 2},
        {"name": "Element 3", "x": 4, "y": 3, "z": 2},
        {"name": "Element 1", "x": 4, "y": 3, "z": 2},
        {"name": "Element 2", "x": 5, "y": 3, "z": 2},
        {"name": "Element 3", "x": 4, "y": 3, "z": 2},
        {"name": "Element 1", "x": 4, "y": 3, "z": 2},
        {"name": "Element 2", "x": 5, "y": 3, "z": 2},
        {"name": "Element 3", "x": 4, "y": 3, "z": 2},
        {"name": "Element 1", "x": 4, "y": 3, "z": 2},
        {"name": "Element 2", "x": 5, "y": 3, "z": 2},
        {"name": "Element 3", "x": 4, "y": 3, "z": 2},
        {"name": "Element 1", "x": 4, "y": 3, "z": 2},
        {"name": "Element 2", "x": 5, "y": 3, "z": 2},
        {"name": "Element 3", "x": 4, "y": 3, "z": 2},
        {"name": "Element 1", "x": 4, "y": 3, "z": 2},
        {"name": "Element 2", "x": 5, "y": 3, "z": 2},
        {"name": "Element 3", "x": 4, "y": 3, "z": 2},
        {"name": "Element 1", "x": 4, "y": 3, "z": 2},
        {"name": "Element 2", "x": 5, "y": 3, "z": 2},
        {"name": "Element 3", "x": 4, "y": 3, "z": 2},
        {"name": "Element 1", "x": 4, "y": 3, "z": 2},
        {"name": "Element 2", "x": 5, "y": 3, "z": 2},
        {"name": "Element 3", "x": 4, "y": 3, "z": 2},
    ]
)
edited_df = st.data_editor(
    df,
    num_rows="dynamic",
    )

favorite_element = edited_df.loc[edited_df["x"].idxmax()]["name"]
st.markdown(f"Your favorite element is **{favorite_element}** 🎈")

st.divider()

df = pd.DataFrame(
    np.random.rand(30, 30),
    columns=('col %d' % i for i in range(30)))

for i in range(30):
    df[f'col {i}'][i] = 'nan'

product_elements = [f"Element {i}" for i in range(1, 31)]

fig = px.imshow(
    df,
    labels=dict(x="", y=""),
    x=product_elements,
    y=product_elements,
    color_continuous_scale=[[0, '#D81B60'],
                    [0.5, '#FFB000'],
                    [1, '#004D40']],
    #title='Combined Risk Matrix',
    width=900,
    height=900,
    text_auto='.2f',
    aspect='equal',

)
fig.update_layout(
    xaxis={"side": "top"},
    yaxis={'side': 'left'},
)
st.plotly_chart(
    fig, 
    use_container_width=True,
    config={
        'displaylogo': False,
        'modeBarButtonsToRemove': ['sendDataToCloud', 'select2d', 'lasso2d', 'zoomIn2d', 'zoomOut2d', 'autoScale2d', 'resetScale2d', 'hoverClosestCartesian', 'hoverCompareCartesian', 'toggleSpikelines']
    }
)
