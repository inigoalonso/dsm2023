"""
# DSM 2023 Workshop
This app helps the participants of the DSM Industry Sprint Workshop.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px


####################
# Formatting       #
####################

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

####################


with st.expander("Potential yearly market in the each region (trucks)"):
    markets =[10000,20000,100000]
    markets[0] = st.slider('Artic',   0, 200000, markets[0])
    markets[1] = st.slider('Desert',  0, 200000, markets[1])
    markets[2] = st.slider('Indoors', 0, 200000, markets[2])



df_designs_original = pd.DataFrame(
    [
        {"Name": "Only front steering",               "Min_R": 10.7, "FC": 6.5, "EC": 0.1, "Price": 100, "Cost": 90},
        {"Name": "Front + Back steering (hydraulic)", "Min_R": 7.6,  "FC": 3.5, "EC": 0.1, "Price": 100, "Cost": 90},
        {"Name": "Front + Back steering (electric)",  "Min_R": 7.6,  "FC": 0.1, "EC": 3.5, "Price": 105, "Cost": 95},
    ]
)

df_designs_edited = st.data_editor(
    df_designs_original,
    #num_rows="dynamic",
    )

market_shares_artic = []

for i in range(len(df_designs_edited)):
    market_shares_artic.append(0.25 * (
        1 / ( 1 + ((df_designs_edited["Min_R"][i]-10) * 0.5) ** 2) + 
        1 - (0.5)**(  2/df_designs_edited["FC"][i]) +
        1 - (0.5)**(0.5/df_designs_edited["EC"][i]) +
        1 - (0.5)**( 20/df_designs_edited["Price"][i])    
    ))
    # st.metric(label="Market", value=f"{100*market_shares[i]:.2f} %", delta="1.2 °F")

market_shares_desert = []

for i in range(len(df_designs_edited)):
    market_shares_desert.append(0.25 * (
        1 / ( 1 + ((df_designs_edited["Min_R"][i]-10) * 0.5) ** 2) + 
        1 - (0.5)**(  2/df_designs_edited["FC"][i]) +
        1 - (0.5)**(0.5/df_designs_edited["EC"][i]) +
        1 - (0.5)**( 20/df_designs_edited["Price"][i])    
    ))

market_shares_special = []

for i in range(len(df_designs_edited)):
    market_shares_special.append(0.25 * (
        1 - (0.5)**( 20/df_designs_edited["Min_R"][i]) + 
        1 - (0.5)**(  2/df_designs_edited["FC"][i]) +
        1 - (0.5)**(0.5/df_designs_edited["EC"][i]) +
        1 - (0.5)**( 20/df_designs_edited["Price"][i])    
    ))

import plotly.graph_objects as go

categories = ['Artic','Desert', 'Special', 'Artic']

from plotly.subplots import make_subplots

fig = make_subplots(
    rows=1, cols=2,
    specs=[[{"type": "polar"}, {"type": "bar"}]],
    subplot_titles=("Expected market shares", "Expected yearly revenue"),
)

fig.add_trace(go.Scatterpolar(
    r=[market_shares_artic[0], market_shares_desert[0], market_shares_special[0], market_shares_artic[0]],
    theta=categories,
    name='System 1',),
    row=1, col=1,
    )
fig.add_trace(go.Scatterpolar(
    r=[market_shares_artic[1], market_shares_desert[1], market_shares_special[1], market_shares_artic[1]],
    theta=categories,
    name='System 2'),
    row=1, col=1,)
fig.add_trace(go.Scatterpolar(
    r=[market_shares_artic[2], market_shares_desert[2], market_shares_special[2], market_shares_artic[2]],
    theta=categories,
    name='System 3'),
    row=1, col=1,)

fig.add_trace(go.Bar(
    name='Artic',
    y=[markets[0]*market_shares_artic[0], markets[0]*market_shares_artic[1], markets[0]*market_shares_artic[2]],
    x=['System 1', 'System 2', 'System 3'],),
    row=1, col=2)
fig.add_trace(go.Bar(
    name='Desert',
    y=[markets[1]*market_shares_desert[0], markets[1]*market_shares_desert[1], markets[1]*market_shares_desert[2]],
    x=['System 1', 'System 2', 'System 3'],),
    row=1, col=2)
fig.add_trace(go.Bar(
    name='Special',
    y=[markets[2]*market_shares_special[0], markets[2]*market_shares_special[1], markets[2]*market_shares_special[2]],
    x=['System 1', 'System 2', 'System 3'],),
    row=1, col=2)

fig.update_layout(
    polar=dict(
        radialaxis=dict(
            visible=True,
            range=[0, 1]
    )),
    showlegend=True
)



st.plotly_chart(fig, theme="streamlit", use_container_width=True)







####################
st.divider()

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
