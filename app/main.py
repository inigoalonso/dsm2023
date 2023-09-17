"""
# DSM 2023 Workshop
This app helps the participants of the DSM Industry Sprint Workshop.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from utils import set_bg

####################
# Formatting       #
####################

# Set wide display, if not done before
try:
    st.set_page_config(
        layout="wide",
        page_title="Industry Sprint Workshop 2023 - The 25th International DSM Conference",
        page_icon="assets/favicon.jpg",
        )
except:
    pass

# Hide the menu and the footer
hide_st_style = """<style>#MainMenu {visibility: hidden;} footer {visibility: hidden;} </style>"""
st.markdown(hide_st_style, unsafe_allow_html=True)

# Add a logo
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

#set_bg('assets/background.png')

# st.header('Industry Sprint Workshop 2023')
# st.markdown('The DSM 2023 Industry Sprint Workshop is brought to you in collaboration with Volvo Group.')

####################

markets =[10000,20000,40000]

if False:
    col1, col2 = st.columns(2)

    with col1:
        with st.expander("Help"):
            st.markdown("""
            This app helps the participants of the DSM Industry Sprint Workshop.
            """)

    with col2:
        with st.expander("Inputs"):
            st.markdown("""
                        **Potential yearly market for each application (# of trucks)**
                        """)
            markets[0] = st.slider('Artic',   0, 200000, markets[0])
            markets[1] = st.slider('Desert',  0, 200000, markets[1])
            markets[2] = st.slider('Special', 0, 200000, markets[2])


df_designs_original = pd.DataFrame(
    [
        {"name": "System 1", "description": "Only front steering",               "min_R": 10.7, "FC": 6.5, "EC": 0.5, "price": 100, "cost": 90},
        {"name": "System 2", "description": "Front + Back steering (hydraulic)", "min_R": 7.6,  "FC": 3.5, "EC": 0.5, "price": 110, "cost": 100},
        {"name": "System 3", "description": "Front + Back steering (electric)",  "min_R": 7.6,  "FC": 0.1, "EC": 3.5, "price": 110, "cost": 100},
    ]
)

with st.expander("Designs", expanded=True):
    df_designs_edited = st.data_editor(
        df_designs_original,
        #num_rows="dynamic",
        use_container_width=False,
        hide_index=True,
        column_config={
            "name": st.column_config.TextColumn(
                "Name",
                help="Name of the alternative system",
                max_chars=50,
            ),
            "description": st.column_config.TextColumn(
                "Description",
                help="Description of the alternative system",
                max_chars=50,
            ),
            "min_R": st.column_config.NumberColumn(
                "Minimum Turning Radius",
                help="Turning radius distance in meters",
                min_value=0,
                max_value=50,
                step=0.1,
                format="%.1f m",
            ),
            "FC": st.column_config.NumberColumn(
                "Fuel Cons.",
                help="Fuel consumption in km/L",
                min_value=0,
                max_value=50,
                step=0.1,
                format="%.1f km/L",
            ),
            "EC": st.column_config.NumberColumn(
                "Electricity Cons.",
                help="Electricity consumption in kWh",
                min_value=0,
                max_value=50,
                step=0.1,
                format="%.1f kWh",
            ),
            "price": st.column_config.NumberColumn(
                "Price",
                help="Price in kilo Euros",
                min_value=0,
                max_value=500,
                step=0.1,
                format="%.1f k€",
            ),
            "cost": st.column_config.NumberColumn(
                "Cost",
                help="Cost in kilo Euros",
                min_value=0,
                max_value=500,
                step=0.1,
                format="%.1f k€",
            ),
        },
        )


market_shares_artic = []

for i in range(len(df_designs_edited)):
    a = 1 / ( 1 + ((df_designs_edited["min_R"][i]-10) * 0.5) ** 2)
    b = 1 - (0.5)**(  1/df_designs_edited["FC"][i])
    c = 1 - (0.5)**(  1/df_designs_edited["EC"][i])
    d = 1 - (0.5)**( 20/df_designs_edited["price"][i])
    market_shares_artic.append(0.25 * (
        a+b+c+d
    ))

market_shares_desert = []

for i in range(len(df_designs_edited)):
    market_shares_desert.append(0.25 * (
        1 / ( 1 + ((df_designs_edited["min_R"][i]-10) * 0.5) ** 2) + 
        1 - (0.5)**(  2/df_designs_edited["FC"][i]) +
        1 - (0.5)**(0.5/df_designs_edited["EC"][i]) +
        1 - (0.5)**( 20/df_designs_edited["price"][i])    
    ))

market_shares_special = []

for i in range(len(df_designs_edited)):
    market_shares_special.append(0.25 * (
        1 - (0.5)**( 20/df_designs_edited["min_R"][i]) + 
        1 - (0.5)**(  2/df_designs_edited["FC"][i]) +
        1 - (0.5)**(0.5/df_designs_edited["EC"][i]) +
        1 - (0.5)**( 20/df_designs_edited["price"][i])    
    ))


categories = ['Artic','Desert', 'Special', 'Artic']

fig_polar = go.Figure()

fig_bar = go.Figure()

fig = make_subplots(
    rows=1, cols=2,
    specs=[[{"type": "polar"}, {"type": "bar"}]],
    subplot_titles=("Expected market shares", "Expected yearly revenue"),
)

fig_polar.add_trace(go.Scatterpolar(
    r=[market_shares_artic[0], market_shares_desert[0], market_shares_special[0], market_shares_artic[0]],
    theta=categories,
    name='System 1',),)
fig_polar.add_trace(go.Scatterpolar(
    r=[market_shares_artic[1], market_shares_desert[1], market_shares_special[1], market_shares_artic[1]],
    theta=categories,
    name='System 2'),)
fig_polar.add_trace(go.Scatterpolar(
    r=[market_shares_artic[2], market_shares_desert[2], market_shares_special[2], market_shares_artic[2]],
    theta=categories,
    name='System 3'),)


units_artic          = [markets[0]*market_shares_artic[0],   markets[0]*market_shares_artic[1],   markets[0]*market_shares_artic[2]]
units_desert         = [markets[1]*market_shares_desert[0],  markets[1]*market_shares_desert[1],  markets[1]*market_shares_desert[2]]
units_special        = [markets[2]*market_shares_special[0], markets[2]*market_shares_special[1], markets[2]*market_shares_special[2]]

revenue_artic        = [df_designs_edited["price"][0]*units_artic[0],   df_designs_edited["price"][1]*units_artic[1],   df_designs_edited["price"][2]*units_artic[2]]
revenue_desert       = [df_designs_edited["price"][0]*units_desert[0],  df_designs_edited["price"][1]*units_desert[1],  df_designs_edited["price"][2]*units_desert[2]]
revenue_special      = [df_designs_edited["price"][0]*units_special[0], df_designs_edited["price"][1]*units_special[1], df_designs_edited["price"][2]*units_special[2]]

unit_profit_system_1 = df_designs_edited["price"][0] - df_designs_edited["cost"][0]
unit_profit_system_2 = df_designs_edited["price"][1] - df_designs_edited["cost"][1]
unit_profit_system_3 = df_designs_edited["price"][2] - df_designs_edited["cost"][2]

profit_artic         = [unit_profit_system_1*  units_artic[0], 
                        unit_profit_system_2*  units_artic[1], 
                        unit_profit_system_3*  units_artic[2]]

profit_desert        = [unit_profit_system_1* units_desert[0], 
                        unit_profit_system_2* units_desert[1], 
                        unit_profit_system_3* units_desert[2]]

profit_special       = [unit_profit_system_1*units_special[0], 
                        unit_profit_system_2*units_special[1], 
                        unit_profit_system_3*units_special[2]]

revenue_system_1 = revenue_artic[0] + revenue_desert[0] + revenue_special[0]
revenue_system_2 = revenue_artic[1] + revenue_desert[1] + revenue_special[1]
revenue_system_3 = revenue_artic[2] + revenue_desert[2] + revenue_special[2]

profit_system_1  = profit_artic[0] + profit_desert[0] + profit_special[0]
profit_system_2  = profit_artic[1] + profit_desert[1] + profit_special[1]
profit_system_3  = profit_artic[2] + profit_desert[2] + profit_special[2]

fig_bar.add_trace(go.Bar(
    name='Artic',
    y=revenue_artic,
    x=['System 1', 'System 2', 'System 3'],
    ),)
fig_bar.add_trace(go.Bar(
    name='Desert',
    y=revenue_desert,
    x=['System 1', 'System 2', 'System 3'],),)
fig_bar.add_trace(go.Bar(
    name='Special',
    y=revenue_special,
    x=['System 1', 'System 2', 'System 3'],),)

fig.update_layout(
    polar=dict(
        radialaxis=dict(
            visible=True,
            range=[0, 1]
    )),
    showlegend=True
)

with st.expander("Results", expanded=True):

    col_plot_1, col_plot_2 = st.columns(2)

    with col_plot_1:
        st.header('Market share')
        st.plotly_chart(fig_polar, theme="streamlit", use_container_width=True)

    with col_plot_2:
        st.header('Revenues')
        st.plotly_chart(fig_bar, theme="streamlit", use_container_width=True)


    st.header('Revenue totals')

    col_revenues_1, col_revenues_2, col_revenues_3 = st.columns(3)

    with col_revenues_1:
        st.metric(label="System 1", value=f"{revenue_system_1/1000000:.3f} M€", delta="")

    with col_revenues_2:
        st.metric(label="System 2", value=f"{revenue_system_2/1000000:.3f} M€", delta="")

    with col_revenues_3:
        st.metric(label="System 3", value=f"{revenue_system_3/1000000:.3f} M€", delta="")

    st.header('Profit totals')

    col_profits_1, col_profits_2, col_profits_3 = st.columns(3)

    with col_profits_1:
        st.metric(label="System 1", value=f"{profit_system_1/1000000:.3f} M€", delta="")

    with col_profits_2:
        st.metric(label="System 2", value=f"{profit_system_2/1000000:.3f} M€", delta="")

    with col_profits_3:
        st.metric(label="System 3", value=f"{profit_system_3/1000000:.3f} M€", delta="")

if False:

    ####################
    st.divider()
    ####################

    with st.expander("Other stuff"):

        df_dsm = pd.DataFrame(
            np.random.rand(30, 30),
            columns=('col %d' % i for i in range(30)))

        for i in range(30):
            df_dsm[f'col {i}'][i] = 'nan'
            #df_dsm.loc[:, (f'col {i}', i)] = 'nan'

        product_elements = [f"Element {i}" for i in range(1, 31)]

        fig_dsm = px.imshow(
            df_dsm,
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
        fig_dsm.update_layout(
            xaxis={"side": "top"},
            yaxis={'side': 'left'},
        )
        st.plotly_chart(
            fig_dsm, 
            use_container_width=True,
            config={
                'displaylogo': False,
                'modeBarButtonsToRemove': ['sendDataToCloud', 'select2d', 'lasso2d', 'zoomIn2d', 'zoomOut2d', 'autoScale2d', 'resetScale2d', 'hoverClosestCartesian', 'hoverCompareCartesian', 'toggleSpikelines']
            }
        )


