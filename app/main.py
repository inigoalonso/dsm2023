"""
# DSM 2023 Workshop
This app helps the participants of the DSM Industry Sprint Workshop.
"""

####################
# Imports          #
####################

import datetime
import json
import altair as alt
import numpy as np
import pandas as pd
import streamlit as st
#from icecream import ic
#from vega_datasets import data
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from google.cloud import firestore
from google.oauth2 import service_account

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

# Hide the top decoration menu, footer, and top padding
hide_streamlit_style = """
                <style>
                div[data-testid="stDecoration"] {
                visibility: hidden;
                height: 0%;
                position: fixed;
                }
                #MainMenu {
                visibility: hidden;
                height: 0%;
                }
                footer {
                visibility: hidden;
                height: 0%;
                }
                #root > div:nth-child(1) > div > div > div > div > section > div {padding-top: 0rem;}
                </style>
                """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

####################
# Setup            #
####################

# Authenticate to Firestore with the JSON account key.
@st.cache_resource
def authenticate_to_firestore():
    key_dict = json.loads(st.secrets["textkey"])
    creds = service_account.Credentials.from_service_account_info(key_dict)
    db = firestore.Client(credentials=creds, project="dsm2023isw")
    return db
db = authenticate_to_firestore()

# Timestamp string
now = datetime.datetime.now()
timestamp = now.strftime("%Y-%m-%d %H:%M:%S")

# Disable SettingWithCopyWarning from pandas
# https://stackoverflow.com/questions/20625582/how-to-deal-with-settingwithcopywarning-in-pandas
pd.options.mode.chained_assignment = None  # default='warn'

####################
# Functions        #
####################

def on_data_update(data):
    print("Data updated:", data)


####################
# Head             #
####################

st.title('Industry Sprint Workshop 2023')
st.caption('**Workshop Facilitator** for _The 25th International DSM Conference_')
#st.subheader("Workshop Facilitator")
#st.markdown('The DSM 2023 Industry Sprint Workshop is brought to you in collaboration with Volvo Group.')

with st.expander("Info", expanded=True):

    st.markdown(
            """
            Please fill in the following information to start the workshop.
            """
        )

    info_col1, info_col2, info_col3 = st.columns(3)

    role = info_col1.text_input(
        label="Professional role",
        help="Enter your professional role here.",
        )
    experience = info_col2.number_input(
        label="Professional experience (years)",
        help="Enter your years of professional experience here.",
        min_value=0,
        max_value=100,
        )
    group = info_col3.selectbox(
        label='Workshop group',
        help="Select your assigned group here.",
        options=('Select', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12'),
        index=0,
        )
    consent = st.checkbox(
        label="I consent to the use of my data for research purposes.",
        help="Please check this box to consent to the use of your data for research purposes.",
        )

    if not (role and experience and (group != "Select") and consent):
        warning = st.warning(
            body="Please make sure to enter your role, experience, and group correctly.",
            icon="⚠️",
            )
    else:
        # Creating a NEW document for each participant
        participants_id = timestamp+"_"+role
        participants_ref = db.collection("participants").document(participants_id)
        # And then uploading the data to that reference
        participants_ref.set({
            "role": role,
            "group": group,
            "experience": experience
        })
        st.success(
            body="You are ready to go! Click on the top right arrow to minimize this section. The tabs bellow will guide you through the workshop.",
            icon="👍",
            )


# Market shares
@st.cache_data
def market_shares_inputs():
    markets = [10000, 20000, 40000]
    return markets
markets = market_shares_inputs()

# Original designs
@st.cache_data
def designs_original():
    df_designs_original = pd.DataFrame(
        [
            {
                "name": "System 1",
                "description": "Only front steering",
                "min_R": 10.7,
                "FC": 0.3,
                "EC": 0.5,
                "reliability": 0.92,
                "price": 100,
                "cost": 90,
                "market_share_1": 0,
                "market_share_2": 0,
                "market_share_3": 0,
            },
            {
                "name": "System 2",
                "description": "Front + Back steering (hydraulic)",
                "min_R": 7.6,
                "FC": 0.35,
                "EC": 0.5,
                "reliability": 0.8,
                "price": 110,
                "cost": 100,
                "market_share_1": 0,
                "market_share_2": 0,
                "market_share_3": 0,
            },
            {
                "name": "System 3",
                "description": "Front + Back steering (electric)",
                "min_R": 7.6,
                "FC": 0.25,
                "EC": 1.5,
                "reliability": 0.9,
                "price": 110,
                "cost": 100,
                "market_share_1": 0,
                "market_share_2": 0,
                "market_share_3": 0,
            },
        ]
    )
    return df_designs_original
df_designs_original = designs_original()

# If the user has filled in the intro form correctly
if (role and experience and (group != "Select") and consent):

    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "Inputs", 
        "Value Analysis", 
        "Risk Identification", 
        "Risk Mitigation", 
        "Questionnaire", 
        "Help"
    ])

    ####################
    # Tab 1            #
    ####################

    with tab1:
        st.subheader("Inputs")
        with st.expander("Markets", expanded=False):
            st.markdown(
                """**Potential yearly market for each application (# of trucks)**"""
            )
            markets[0] = st.slider("Artic", 0, 200000, markets[0])
            markets[1] = st.slider("Desert", 0, 200000, markets[1])
            markets[2] = st.slider("Special", 0, 200000, markets[2])
        
        with st.expander("Systems", expanded=True):
            st.markdown(
                """**Systems under consideration**"""
            )
            df_designs_edited = st.data_editor(
                df_designs_original,
                num_rows="dynamic",
                use_container_width=False,
                hide_index=True,
                key="data_editor",
                on_change=on_data_update(data="df test"),
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
                        disabled=True,
                    ),
                    "FC": st.column_config.NumberColumn(
                        "Fuel Cons.",
                        help="Fuel consumption in L/km",
                        min_value=0,
                        max_value=50,
                        step=0.01,
                        format="%.2f L/km",
                        disabled=True,
                    ),
                    "EC": st.column_config.NumberColumn(
                        "Electricity Cons.",
                        help="Electricity consumption in kWh",
                        min_value=0,
                        max_value=50,
                        step=0.1,
                        format="%.1f kWh",
                        disabled=True,
                    ),
                    "reliability": st.column_config.NumberColumn(
                        "Reliability",
                        help="Reliability of the system",
                        min_value=0,
                        max_value=1,
                        step=0.01,
                        format="%.2f",
                        disabled=True,
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
                        disabled=True,
                    ),
                    "market_share_1": None,
                    "market_share_2": None,
                    "market_share_3": None,
                },
            )

            market_shares_artic = []
            market_shares_desert = []
            market_shares_special = []

            for i in range(len(df_designs_edited)):
                a = (1 / (1 + ((df_designs_edited["min_R"][i] - 10) * 0.5) ** 2) - 0.5)
                b = (1 - (0.5) ** (0.1 / df_designs_edited["FC"][i]) - 0.3)
                c = (1 - (0.5) ** (1 / df_designs_edited["EC"][i]) - 0.3)
                d = (1 - (0.5) ** (50 / df_designs_edited["price"][i]) - 0.3)
                e = 1 - (0.5) ** (1 / df_designs_edited["reliability"][i])
                market_share = 0.2 * (a + b + c + d + e)
                market_shares_artic.append(market_share)
                print(i, a, b, c, d, e, market_shares_artic)

            for i in range(len(df_designs_edited)):
                a = (1 / (1 + ((df_designs_edited["min_R"][i] - 10) * 0.5) ** 2) - 0.5)
                b = (1 - (0.5) ** (0.5 / df_designs_edited["FC"][i]) - 0.3)
                c = (1 - (0.5) ** (0.5 / df_designs_edited["EC"][i]) - 0.3)
                d = (1 - (0.5) ** (50 / df_designs_edited["price"][i]) - 0.3)
                e = 1 - (0.5) ** (1 / df_designs_edited["reliability"][i])
                market_share = 0.2 * (a + b + c + d + e)
                market_shares_desert.append(market_share)
                print(i, a, b, c, d, e, market_shares_desert)

            for i in range(len(df_designs_edited)):
                a = (1 - (0.5) ** (50 / df_designs_edited["min_R"][i]) - 0.3)
                b = (1 - (0.5) ** (2 / df_designs_edited["FC"][i]) - 0.3)
                c = (1 - (0.5) ** (2 / df_designs_edited["EC"][i]) - 0.3)
                d = (1 - (0.5) ** (500 / df_designs_edited["price"][i]) - 0.3)
                e = 1 - (0.5) ** (1 / df_designs_edited["reliability"][i])
                market_share = 0.2 * (a + b + c + d + e)
                market_shares_special.append(market_share)
                print(i, a, b, c, d, e, market_shares_special)

            categories = ["Artic", "Desert", "Special", "Artic"]

            units_artic = [
                markets[0] * market_shares_artic[0],
                markets[0] * market_shares_artic[1],
                markets[0] * market_shares_artic[2],
            ]
            units_desert = [
                markets[1] * market_shares_desert[0],
                markets[1] * market_shares_desert[1],
                markets[1] * market_shares_desert[2],
            ]
            units_special = [
                markets[2] * market_shares_special[0],
                markets[2] * market_shares_special[1],
                markets[2] * market_shares_special[2],
            ]

            revenue_artic = [
                df_designs_edited["price"][0] * units_artic[0],
                df_designs_edited["price"][1] * units_artic[1],
                df_designs_edited["price"][2] * units_artic[2],
            ]
            revenue_desert = [
                df_designs_edited["price"][0] * units_desert[0],
                df_designs_edited["price"][1] * units_desert[1],
                df_designs_edited["price"][2] * units_desert[2],
            ]
            revenue_special = [
                df_designs_edited["price"][0] * units_special[0],
                df_designs_edited["price"][1] * units_special[1],
                df_designs_edited["price"][2] * units_special[2],
            ]

            unit_profit_system_1 = df_designs_edited["price"][0] - df_designs_edited["cost"][0]
            unit_profit_system_2 = df_designs_edited["price"][1] - df_designs_edited["cost"][1]
            unit_profit_system_3 = df_designs_edited["price"][2] - df_designs_edited["cost"][2]

            profit_artic = [
                unit_profit_system_1 * units_artic[0],
                unit_profit_system_2 * units_artic[1],
                unit_profit_system_3 * units_artic[2],
            ]

            profit_desert = [
                unit_profit_system_1 * units_desert[0],
                unit_profit_system_2 * units_desert[1],
                unit_profit_system_3 * units_desert[2],
            ]

            profit_special = [
                unit_profit_system_1 * units_special[0],
                unit_profit_system_2 * units_special[1],
                unit_profit_system_3 * units_special[2],
            ]

            revenue_system_1 = revenue_artic[0] + revenue_desert[0] + revenue_special[0]
            revenue_system_2 = revenue_artic[1] + revenue_desert[1] + revenue_special[1]
            revenue_system_3 = revenue_artic[2] + revenue_desert[2] + revenue_special[2]

            profit_system_1 = profit_artic[0] + profit_desert[0] + profit_special[0]
            profit_system_2 = profit_artic[1] + profit_desert[1] + profit_special[1]
            profit_system_3 = profit_artic[2] + profit_desert[2] + profit_special[2]

        questions_tab1 = st.expander("Questions", expanded=False)

    ####################
    # Tab 2            #
    ####################

    with tab2:

        fig_polar = go.Figure()

        fig_bar = go.Figure()

        fig = make_subplots(
            rows=1,
            cols=2,
            specs=[[{"type": "polar"}, {"type": "bar"}]],
            subplot_titles=("Expected market shares", "Expected yearly revenue"),
        )

        fig_polar.add_trace(
            go.Scatterpolar(
                r=[
                    market_shares_artic[0],
                    market_shares_desert[0],
                    market_shares_special[0],
                    market_shares_artic[0],
                ],
                theta=categories,
                name="System 1",
            ),
        )
        fig_polar.add_trace(
            go.Scatterpolar(
                r=[
                    market_shares_artic[1],
                    market_shares_desert[1],
                    market_shares_special[1],
                    market_shares_artic[1],
                ],
                theta=categories,
                name="System 2",
            ),
        )
        fig_polar.add_trace(
            go.Scatterpolar(
                r=[
                    market_shares_artic[2],
                    market_shares_desert[2],
                    market_shares_special[2],
                    market_shares_artic[2],
                ],
                theta=categories,
                name="System 3",
            ),
        )



        fig_bar.add_trace(
            go.Bar(
                name="Artic",
                y=revenue_artic,
                x=["System 1", "System 2", "System 3"],
            ),
        )
        fig_bar.add_trace(
            go.Bar(
                name="Desert",
                y=revenue_desert,
                x=["System 1", "System 2", "System 3"],
            ),
        )
        fig_bar.add_trace(
            go.Bar(
                name="Special",
                y=revenue_special,
                x=["System 1", "System 2", "System 3"],
            ),
        )

        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 1])), showlegend=True
        )

        st.subheader("Market share")
        
        source = pd.DataFrame({
            'market': ['Artic', 'Desert', 'Special'],
            'system1': [market_shares_artic[0], market_shares_artic[1], market_shares_artic[2]],
            'system2': [market_shares_desert[0], market_shares_desert[1], market_shares_desert[2]],
            'system3': [market_shares_special[0], market_shares_special[1], market_shares_special[2]],
        })
        chart_markets = alt.Chart(source, width=500).transform_window(
            index='count()'
        ).transform_fold(
            ['Artic', 'Desert', 'Special']
        ).mark_line().encode(
            x='market:N',
            y='share:Q',
            color='system:N',
            opacity=alt.value(0.5)
        )
        #st.altair_chart(chart_markets, theme="streamlit")

        col_market_1, col_market_2 = st.columns(2)
        with col_market_1:
            st.plotly_chart(fig_polar, theme="streamlit", use_container_width=True)
        with col_market_2:
            st.text("Market share of each system in each application")

        st.subheader("Revenues")

        col_revenues_1, col_revenues_2 = st.columns(2)

        with col_revenues_1:
            st.plotly_chart(fig_bar, theme="streamlit", use_container_width=True)

        with col_revenues_2:
            st.metric(
                label="System 1", value=f"{revenue_system_1/1000000:.3f} M€", delta=""
            )
            st.metric(
                label="System 2", value=f"{revenue_system_2/1000000:.3f} M€", delta=""
            )
            st.metric(
                label="System 3", value=f"{revenue_system_3/1000000:.3f} M€", delta=""
            )

        st.subheader("Profits")

        col_profits_1, col_profits_2, col_profits_3 = st.columns(3)

        with col_profits_1:
            st.metric(label="System 1", value=f"{profit_system_1/1000000:.3f} M€", delta="")

        with col_profits_2:
            st.metric(label="System 2", value=f"{profit_system_2/1000000:.3f} M€", delta="")

        with col_profits_3:
            st.metric(label="System 3", value=f"{profit_system_3/1000000:.3f} M€", delta="")


        questions_tab2 = st.expander("Questions", expanded=False)

    ####################
    # Tab 3            #
    ####################

    with tab3:
        st.subheader("Risk Identification")

        with st.expander("Risk location", expanded=True):
            df_dsm = pd.DataFrame(
                np.random.rand(31, 31), columns=("col %d" % i for i in range(31))
            )

            for i in range(31):
                df_dsm[f"col {i}"][i] = "nan"
                # df_dsm.loc[:, (f'col {i}', i)] = 'nan'

            product_elements = [f"Element {i}" for i in range(1, 32)]

            fig_dsm = px.imshow(
                df_dsm,
                labels=dict(x="", y=""),
                x=product_elements,
                y=product_elements,
                color_continuous_scale=[[0, "#D81B60"], [0.5, "#FFB000"], [1, "#004D40"]],
                # title='Combined Risk Matrix',
                width=900,
                height=900,
                text_auto=".2f",
                aspect="equal",
            )
            fig_dsm.update_layout(
                xaxis={"side": "top"},
                yaxis={"side": "left"},
            )
            st.plotly_chart(
                fig_dsm,
                use_container_width=True,
                config={
                    "displaylogo": False,
                    "modeBarButtonsToRemove": [
                        "sendDataToCloud",
                        "select2d",
                        "lasso2d",
                        "zoomIn2d",
                        "zoomOut2d",
                        "autoScale2d",
                        "resetScale2d",
                        "hoverClosestCartesian",
                        "hoverCompareCartesian",
                        "toggleSpikelines",
                    ],
                },
            )
            # Compute x^2 + y^2 across a 2D grid
            x, y = np.meshgrid(range(1, len(product_elements)), range(1, len(product_elements)))
            distance = x ** 2 + y ** 2

            # Convert this grid to columnar data expected by Altair
            source = pd.DataFrame({ 'x': x.ravel(),
                                    'y': y.ravel(),
                                    'z': distance.ravel()})

            chart = alt.Chart(source).mark_rect().encode(
                x='x:O',
                y='y:O',
                color='z:Q'
            )

            st.altair_chart(chart, theme="streamlit")

        questions_tab3 = st.expander("Questions", expanded=False)

    ####################
    # Tab 4            #
    ####################

    with tab4:
        st.subheader("Risk Mitigation")

        with st.expander("Risk registry", expanded=False):
            source = data.barley()
            st.write(source)
            chart = alt.Chart(source).mark_bar().encode(
                x='year:O',
                y='sum(yield):Q',
                color='year:N',
                column='site:N'
            )
            st.altair_chart(chart, theme="streamlit")

        questions_tab4 = st.expander("Questions", expanded=False)

    ####################
    # Tab 5            #
    ####################

    with tab5:
        st.subheader("Questionnaire")
        with st.form(key="questionnaire_form"):
            st.markdown(
                """**To develop my solution to the challenge, I based my reasoning on...**"""
            )
            st.caption("Please rate the following options from 0 (not at all) to 5 (very much).")
            q1 = st.slider("My previous experience", key="q1", min_value=0.0, max_value=5.0, value=2.5, step=0.1)
            q2 = st.slider("Discussion with my colleagues", key="q2", min_value=0.0, max_value=5.0, value=2.5, step=0.1)
            q3 = st.slider("Risk registry", key="q3", min_value=0.0, max_value=5.0, value=2.5, step=0.1)
            q4 = st.slider("Value analysis models", key="q4", min_value=0.0, max_value=5.0, value=2.5, step=0.1)
            q5 = st.slider("Binary DSMs", key="q5", min_value=0.0, max_value=5.0, value=2.5, step=0.1)
            q6 = st.slider("Numerical (Spatial) DSMs", key="q6", min_value=0.0, max_value=5.0, value=2.5, step=0.1)
            q7 = st.slider("Risk propagation matrices", key="q7", min_value=0.0, max_value=5.0, value=2.5, step=0.1)
            q8 = st.slider("Risk mitigations registry", key="q8", min_value=0.0, max_value=5.0, value=2.5, step=0.1)
            # Submit button
            submit_button = st.form_submit_button(label="Submit", help="Click here to submit your answers.")

        questions_tab5 = st.expander("Questions", expanded=False)

    ####################
    # Tab 6            #
    ####################

    with tab6:
        st.subheader("Help")
        st.markdown(
            """
            This app helps the participants of the DSM Industry Sprint Workshop.
            """
        )

    questions_tab1.write("What is the minimum turning radius of a truck?")

print("Here's the session state:")
print([key for key in st.session_state.keys()])
#ic(st.session_state["data_editor"])

try:
    sessions_ref = db.collection("session_states").document(participants_id)
    # And then uploading the data to that reference
    sessions_ref.set({
        "role": role,
        "group": group
    })
except:
    pass