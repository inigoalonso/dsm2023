"""
# DSM 2023 Workshop
This app helps the participants of the DSM Industry Sprint Workshop.
"""

####################
# Imports          #
####################

from __future__ import annotations

import datetime
import json
import numpy as np
import pandas as pd
import streamlit as st
from streamlit import runtime
from streamlit.runtime.scriptrunner import get_script_run_ctx
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from google.cloud import firestore
from google.oauth2 import service_account
from streamlit_echarts import st_echarts


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


# Authenticate to Firestore
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


def get_session_id() -> str:
    """Get the Session ID for the current session."""
    try:
        ctx = get_script_run_ctx()
        if ctx is None:
            return None
        session_info = runtime.get_instance().get_client(ctx.session_id)
        if session_info is None:
            return None
    except Exception as e:
        return None
    return session_info._session_id


def calculate_ms(new_df: pd.DataFrame | None = None):
    if new_df is not None:
        if new_df.equals(st.session_state["df_designs"]):
            return
        st.session_state["df_designs"] = new_df

    df_designs = st.session_state["df_designs"]
    df_designs["market_share_1"] = df_designs["price"] * 2
    df_designs["market_share_2"] = df_designs["price"] * 3
    df_designs["market_share_3"] = df_designs["price"] * 4
    df_designs["market_units_1"] = df_designs["market_share_1"] * market_sizes[0]
    df_designs["market_units_2"] = df_designs["market_share_2"] * market_sizes[1]
    df_designs["market_units_3"] = df_designs["market_share_3"] * market_sizes[2]
    df_designs["market_revenue_1"] = df_designs["price"] * df_designs["market_units_1"]
    df_designs["market_revenue_2"] = df_designs["price"] * df_designs["market_units_2"]
    df_designs["market_revenue_3"] = df_designs["price"] * df_designs["market_units_3"]
    df_designs["market_profit_1"] = (
        df_designs["price"] - df_designs["cost"]
    ) * df_designs["market_units_1"]
    df_designs["market_profit_2"] = (
        df_designs["price"] - df_designs["cost"]
    ) * df_designs["market_units_2"]
    df_designs["market_profit_3"] = (
        df_designs["price"] - df_designs["cost"]
    ) * df_designs["market_units_3"]
    df_designs["total_units"] = (
        df_designs["market_units_1"]
        + df_designs["market_units_2"]
        + df_designs["market_units_3"]
    )
    df_designs["total_revenue"] = (
        df_designs["market_revenue_1"]
        + df_designs["market_revenue_2"]
        + df_designs["market_revenue_3"]
    )
    df_designs["total_profit"] = (
        df_designs["market_profit_1"]
        + df_designs["market_profit_2"]
        + df_designs["market_profit_3"]
    )
    st.session_state["df_designs"] = df_designs
    st.experimental_rerun()


####################
# Head             #
####################

# Logo and title
col_logo, col_title = st.columns([0.2, 1])
with col_logo:
    st.write("")
    st.write("")
    st.image("assets/logo_large.png", width=60)

with col_title:
    st.title("Industry Sprint Workshop 2023")
    st.caption("**Workshop Facilitator** for _The 25th International DSM Conference_")
    # st.subheader("Workshop Facilitator")
    # st.markdown('The DSM 2023 Industry Sprint Workshop is brought to you in collaboration with Volvo Group.')


with st.expander("Info", expanded=True):
    st.markdown(
        """
            Please fill in the following information to start the workshop.
            """
    )

    group = st.selectbox(
        label="Workshop group",
        help="Select your assigned group here.",
        options=(
            "Select",
            "1",
            "2",
            "3",
            "4",
            "5",
            "6",
            "7",
            "8",
            "9",
            "10",
            "11",
            "12",
        ),
        index=0,
    )
    consent = st.checkbox(
        label="I consent to the use of my data for research purposes.",
        help="Please check this box to consent to the use of your data for research purposes.",
    )

    if not ((group != "Select") and consent):
        warning = st.warning(
            body="Please make sure to enter your role, experience, and group correctly.",
            icon="⚠️",
        )
    else:
        # Creating a NEW document for each participant
        session_id = get_session_id()
        session_ref = db.collection("sessions").document(session_id)
        # And then uploading the data to that reference
        session_ref.set(
            {"session_id": session_id, "timestamp": timestamp, "group": group}
        )
        st.success(
            body="You are ready to go! Click on the top right arrow to minimize this section. The tabs bellow will guide you through the workshop.",
            icon="👍",
        )

# Colors
systems_colors = ["#264653", "#E9C46A", "#E76F51"]
markets_colors = ["#3A86FF", "#FF006E", "#8338EC"]


# Market shares
@st.cache_data
def market_shares_inputs():
    market_sizes = [10000, 20000, 40000]
    return market_sizes


market_sizes = market_shares_inputs()


# Original designs
if "df_designs" not in st.session_state:
    st.session_state.df_designs = pd.DataFrame(
        [
            {
                "name": "System 1",
                "description": "Only front steering",
                "min_R": 10.7,
                "reliability": 0.92,
                "price": 100,
                "cost": 90,
                "market_share_1": 0,
                "market_share_2": 0,
                "market_share_3": 0,
                "market_units_1": 0,
                "market_units_2": 0,
                "market_units_3": 0,
                "market_revenue_1": 0,
                "market_revenue_2": 0,
                "market_revenue_3": 0,
                "market_profit_1": 0,
                "market_profit_2": 0,
                "market_profit_3": 0,
                "total_units": 0,
                "total_revenue": 0,
                "total_profit": 0,
            },
            {
                "name": "System 2",
                "description": "Front + Back steering (hydraulic)",
                "min_R": 8.0,
                "reliability": 0.8,
                "price": 110,
                "cost": 100,
                "market_share_1": 0,
                "market_share_2": 0,
                "market_share_3": 0,
                "market_units_1": 0,
                "market_units_2": 0,
                "market_units_3": 0,
                "market_revenue_1": 0,
                "market_revenue_2": 0,
                "market_revenue_3": 0,
                "market_profit_1": 0,
                "market_profit_2": 0,
                "market_profit_3": 0,
                "total_units": 0,
                "total_revenue": 0,
                "total_profit": 0,
            },
            {
                "name": "System 3",
                "description": "Front + Back steering (electric)",
                "min_R": 7.6,
                "reliability": 0.9,
                "price": 110,
                "cost": 100,
                "market_share_1": 0,
                "market_share_2": 0,
                "market_share_3": 0,
                "market_units_1": 0,
                "market_units_2": 0,
                "market_units_3": 0,
                "market_revenue_1": 0,
                "market_revenue_2": 0,
                "market_revenue_3": 0,
                "market_profit_1": 0,
                "market_profit_2": 0,
                "market_profit_3": 0,
                "total_units": 0,
                "total_revenue": 0,
                "total_profit": 0,
            },
        ]
    )
    calculate_ms()

risks = [
    "R01 - Wheel front axle failure",
    "R02 - Hub front axle failure",
    "R03 - Steering knuckle front axle failure",
    "R04 - Knuckle arm front axle failure",
    "R05 - Frame front axle failure",
    "R06 - Tie rod front axle failure",
    "R07 - Angle sensor front axle failure",
    "R08 - Speedometer failure",
    "R09 - ECU failure",
    "R10 - Engine failure",
    "R11 - Hydraulic oil reservoir failure",
    "R12 - Steering actuation cylinder front axle failure",
    "R13 - Servo valve front axle failure",
    "R14 - Pump front axle failure",
    "R15 - Filter front axle failure",
    "R16 - Cooler front axle failure",
    "R17 - Steering actuation cylinder second axle failure",
    "R18 - Servo valve second axle failure",
    "R19 - Pump second axle failure",
    "R20 - Filter second axle failure",
    "R21 - Cooler second axle failure",
    "R22 - Wheel second axle failure",
    "R23 - Hub second axle failure",
    "R24 - Steering knuckle second axle failure",
    "R25 - Knuckle arm second axle failure",
    "R26 - Frame second axle failure",
    "R27 - Tie rod second axle failure",
    "R28 - Angle sensor second axle failure",
    "R29 - Electric steering motor front axle failure",
    "R30 - Electric steering motor second axle failure",
    "R31 - Battery Box failure",
]

# If the user has filled in the intro form correctly
if (group != "Select") and consent:
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
        [
            "Inputs",
            "1. Analyze Value",
            "2. Identify Risks",
            "3. Mitigate Risks",
            "Questionnaire",
            "Help",
        ]
    )

    ####################
    # Tab 1            #
    ####################

    with tab1:
        st.subheader("Inputs")
        with st.expander("Markets", expanded=False):
            st.markdown(
                """**Potential yearly market for each application (# of trucks)**"""
            )
            market_sizes[0] = st.slider("Artic", 0, 200000, market_sizes[0])
            market_sizes[1] = st.slider("Desert", 0, 200000, market_sizes[1])
            market_sizes[2] = st.slider("Special", 0, 200000, market_sizes[2])

        with st.expander("Systems", expanded=True):
            st.markdown("""**Systems under consideration**""")
            editable_df = st.data_editor(
                st.session_state["df_designs"],
                key="data",
                num_rows="dynamic",
                use_container_width=False,
                hide_index=True,
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
                    "market_share_1": st.column_config.NumberColumn(
                        "MS1",
                        help="Market share in %",
                        min_value=0,
                        max_value=100,
                        step=0.01,
                        format="%.2f",
                        disabled=True,
                    ),
                    "market_share_2": st.column_config.NumberColumn(
                        "MS2",
                        help="Market share in %",
                        min_value=0,
                        max_value=100,
                        step=0.01,
                        format="%.2f",
                        disabled=True,
                    ),
                    "market_share_3": st.column_config.NumberColumn(
                        "MS3",
                        help="Market share in %",
                        min_value=0,
                        max_value=100,
                        step=0.01,
                        format="%.2f",
                        disabled=True,
                    ),
                    "market_units_1": None,
                    "market_units_2": None,
                    "market_units_3": None,
                    "market_revenue_1": None,
                    "market_revenue_2": None,
                    "market_revenue_3": None,
                    "market_profit_1": None,
                    "market_profit_2": None,
                    "market_profit_3": None,
                },
            )

            calculate_ms(editable_df)

            market_shares_artic = []
            market_shares_desert = []
            market_shares_special = []

            for i in range(len(editable_df)):
                a = 1 / (1 + ((editable_df["min_R"][i] - 10) * 0.5) ** 2) - 0.5
                d = 1 - (0.5) ** (50 / editable_df["price"][i]) - 0.3
                e = 1 - (0.5) ** (1 / editable_df["reliability"][i])
                market_share = 0.2 * (a + d + e)
                market_shares_artic.append(market_share)
                print(i, a, d, e, market_shares_artic)

            for i in range(len(editable_df)):
                a = 1 / (1 + ((editable_df["min_R"][i] - 10) * 0.5) ** 2) - 0.5
                d = 1 - (0.5) ** (50 / editable_df["price"][i]) - 0.3
                e = 1 - (0.5) ** (1 / editable_df["reliability"][i])
                market_share = 0.2 * (a + d + e)
                market_shares_desert.append(market_share)
                print(i, a, d, e, market_shares_desert)

            for i in range(len(editable_df)):
                a = 1 - (0.5) ** (50 / editable_df["min_R"][i]) - 0.3
                d = 1 - (0.5) ** (500 / editable_df["price"][i]) - 0.3
                e = 1 - (0.5) ** (1 / editable_df["reliability"][i])
                market_share = 0.2 * (a + d + e)
                market_shares_special.append(market_share)
                print(i, a, d, e, market_shares_special)

            categories = ["Artic", "Desert", "Special", "Artic"]

            units_artic = [
                editable_df["market_units_1"][0],
                editable_df["market_units_1"][1],
                editable_df["market_units_1"][2],
            ]
            units_desert = [
                editable_df["market_units_2"][0],
                editable_df["market_units_2"][1],
                editable_df["market_units_2"][2],
            ]
            units_special = [
                editable_df["market_units_3"][0],
                editable_df["market_units_3"][1],
                editable_df["market_units_3"][2],
            ]
            revenue_artic = [
                editable_df["market_revenue_1"][0],
                editable_df["market_revenue_1"][1],
                editable_df["market_revenue_1"][2],
            ]
            revenue_desert = [
                editable_df["market_revenue_2"][0],
                editable_df["market_revenue_2"][1],
                editable_df["market_revenue_2"][2],
            ]
            revenue_special = [
                editable_df["market_revenue_3"][0],
                editable_df["market_revenue_3"][1],
                editable_df["market_revenue_3"][2],
            ]
            profit_artic = [
                editable_df["market_profit_1"][0],
                editable_df["market_profit_1"][1],
                editable_df["market_profit_1"][2],
            ]
            profit_desert = [
                editable_df["market_profit_2"][0],
                editable_df["market_profit_2"][1],
                editable_df["market_profit_2"][2],
            ]
            profit_special = [
                editable_df["market_profit_3"][0],
                editable_df["market_profit_3"][1],
                editable_df["market_profit_3"][2],
            ]

            markets_df = pd.DataFrame(
                [
                    {
                        "market": "Artic",
                        "share_system_1": market_shares_artic[0],
                        "share_system_2": market_shares_artic[1],
                        "share_system_3": market_shares_artic[2],
                        "units_system_1": editable_df["market_units_1"][0],
                        "units_system_2": editable_df["market_units_1"][1],
                        "units_system_3": editable_df["market_units_1"][2],
                        "revenue_system_1": editable_df["market_revenue_1"][0],
                        "revenue_system_2": editable_df["market_revenue_1"][1],
                        "revenue_system_3": editable_df["market_revenue_1"][2],
                        "profit_system_1": editable_df["market_profit_1"][0],
                        "profit_system_2": editable_df["market_profit_1"][1],
                        "profit_system_3": editable_df["market_profit_1"][2],
                    },
                    {
                        "market": "Desert",
                        "share_system_1": market_shares_desert[0],
                        "share_system_2": market_shares_desert[1],
                        "share_system_3": market_shares_desert[2],
                        "units_system_1": editable_df["market_units_2"][0],
                        "units_system_2": editable_df["market_units_2"][1],
                        "units_system_3": editable_df["market_units_2"][2],
                        "revenue_system_1": editable_df["market_revenue_2"][0],
                        "revenue_system_2": editable_df["market_revenue_2"][1],
                        "revenue_system_3": editable_df["market_revenue_2"][2],
                        "profit_system_1": editable_df["market_profit_2"][0],
                        "profit_system_2": editable_df["market_profit_2"][1],
                        "profit_system_3": editable_df["market_profit_2"][2],
                    },
                    {
                        "market": "Special",
                        "share_system_1": market_shares_special[0],
                        "share_system_2": market_shares_special[1],
                        "share_system_3": market_shares_special[2],
                        "units_system_1": editable_df["market_units_3"][0],
                        "units_system_2": editable_df["market_units_3"][1],
                        "units_system_3": editable_df["market_units_3"][2],
                        "revenue_system_1": editable_df["market_revenue_3"][0],
                        "revenue_system_2": editable_df["market_revenue_3"][1],
                        "revenue_system_3": editable_df["market_revenue_3"][2],
                        "profit_system_1": editable_df["market_profit_3"][0],
                        "profit_system_2": editable_df["market_profit_3"][1],
                        "profit_system_3": editable_df["market_profit_3"][2],
                    },
                ]
            )

        questions_tab1 = st.expander("Questions", expanded=False)

    ####################
    # Tab 2            #
    ####################

    with tab2:
        st.subheader("1. Analyze Value")
        with st.expander("Market share", expanded=True):
            markets_col1, markets_col2 = st.columns(2)

            with markets_col1:
                # Plotly group bars plot of market share per system
                st.plotly_chart(
                    px.bar(
                        markets_df,
                        x="market",
                        y=["share_system_1", "share_system_2", "share_system_3"],
                        barmode="group",
                        color_discrete_sequence=systems_colors,
                        labels={
                            "value": "Market share",
                            "variable": "System",
                            "market": "Market",
                        },
                        height=400,
                    ),
                    use_container_width=True,
                )

            # with markets_col2:
            #     market_table = st.dataframe(
            #         markets_df[
            #             [
            #                 "market",
            #                 "share_system_1",
            #                 "share_system_2",
            #                 "share_system_3",
            #             ]
            #         ],
            #         hide_index=True,
            #         column_config={
            #             "market": st.column_config.TextColumn(
            #                 "Market", help="Name of the market"
            #             ),
            #             "share_system_1": st.column_config.NumberColumn(
            #                 "System 1",
            #                 format="%.2f",
            #             ),
            #             "share_system_2": st.column_config.NumberColumn(
            #                 "System 2",
            #                 format="%.2f",
            #             ),
            #             "share_system_3": st.column_config.NumberColumn(
            #                 "System 3",
            #                 format="%.2f",
            #             ),
            #         },
            #     )

        with st.expander("Profits", expanded=True):
            col_profits_1, col_profits_2, col_profits_3 = st.columns(3)

            with col_profits_1:
                st.metric(
                    label="System 1",
                    value=f"{editable_df['total_profit'][0]/1000000:.3f} M€",
                    delta="",
                )

            with col_profits_2:
                st.metric(
                    label="System 2",
                    value=f"{editable_df['total_profit'][1]/1000000:.3f} M€",
                    delta="",
                )

            with col_profits_3:
                st.metric(
                    label="System 3",
                    value=f"{editable_df['total_profit'][2]/1000000:.3f} M€",
                    delta="",
                )

        questions_tab2 = st.expander("Questions", expanded=False)

    ####################
    # Tab 3            #
    ####################

    with tab3:
        st.subheader("2. Identify Risks")

        with st.expander("Technical risk registry", expanded=True):
            df_risks = pd.DataFrame(
                [
                    {"name": "Risk 1", "description": "Risk 1 description"},
                    {"name": "Risk 2", "description": "Risk 2 description"},
                ]
            )
            st.write(df_risks)

        with st.expander("Risk location", expanded=True):
            # Select system to plot
            system = st.selectbox(
                label="System",
                help="Select the system you would like to plot.",
                options=("System 1", "System 2", "System 3"),
                index=0,
            )

            if system == "System 1":
                n = 16
            elif system == "System 2":
                n = 18
            elif system == "System 3":
                n = 25
            else:
                n = 10

            col_riskid_1, col_riskid_2 = st.columns([2, 1])

            with col_riskid_1:
                product_elements = [f"Element {i}" for i in range(1, n+1)]

                # df_dsm = pd.DataFrame(
                #     np.random.rand(n, n), columns=("col %d" % i for i in range(n))
                # )

                # for i in range(n):
                #     df_dsm[f"col {i}"][i] = "nan"
                #     # df_dsm.loc[:, (f'col {i}', i)] = 'nan'

                # fig_dsm = px.imshow(
                #     df_dsm,
                #     labels=dict(x="", y=""),
                #     x=product_elements,
                #     y=product_elements,
                #     color_continuous_scale=[
                #         [0, "#D81B60"],
                #         [0.5, "#FFB000"],
                #         [1, "#004D40"],
                #     ],
                #     # title='Combined Risk Matrix',
                #     width=900,
                #     height=900,
                #     text_auto=".2f",
                #     aspect="equal",
                # )
                # fig_dsm.update_layout(
                #     xaxis={"side": "top"},
                #     yaxis={"side": "left"},
                # )
                # risk_chart = st.plotly_chart(
                #     fig_dsm,
                #     use_container_width=True,
                #     config={
                #         "displaylogo": False,
                #         "modeBarButtonsToRemove": [
                #             "sendDataToCloud",
                #             "lasso2d",
                #             "zoomIn2d",
                #             "zoomOut2d",
                #             "autoScale2d",
                #             "resetScale2d",
                #             "hoverClosestCartesian",
                #             "hoverCompareCartesian",
                #             "toggleSpikelines",
                #         ],
                #     },
                # )

                #
                x = [f"Element {i}" for i in range(1, n+1)]
                y = [f"Element {i}" for i in range(1, n+1)]

                data = [
                    [0, 0, 5],
                    [0, 1, 1],
                    [0, 2, 0],
                    [0, 3, 0],
                    [0, 4, 0],
                    [0, 5, 0],
                    [0, 6, 0],
                    [0, 7, 0],
                    [0, 8, 0],
                    [0, 9, 0],
                    [0, 10, 0],
                    [0, 11, 2],
                    [0, 12, 4],
                    [0, 13, 1],
                    [0, 14, 1],
                    [0, 15, 3],
                    [0, 16, 4],
                    [0, 17, 6],
                    [0, 18, 4],
                    [0, 19, 4],
                    [0, 20, 3],
                    [0, 21, 3],
                    [0, 22, 2],
                    [0, 23, 5],
                    [1, 0, 7],
                    [1, 1, 0],
                    [1, 2, 0],
                    [1, 3, 0],
                    [1, 4, 0],
                    [1, 5, 0],
                    [1, 6, 0],
                    [1, 7, 0],
                    [1, 8, 0],
                    [1, 9, 0],
                    [1, 10, 5],
                    [1, 11, 2],
                    [1, 12, 2],
                    [1, 13, 6],
                    [1, 14, 9],
                    [1, 15, 11],
                    [1, 16, 6],
                    [1, 17, 7],
                    [1, 18, 8],
                    [1, 19, 12],
                    [1, 20, 5],
                    [1, 21, 5],
                    [1, 22, 7],
                    [1, 23, 2],
                    [2, 0, 1],
                    [2, 1, 1],
                    [2, 2, 0],
                    [2, 3, 0],
                    [2, 4, 0],
                    [2, 5, 0],
                    [2, 6, 0],
                    [2, 7, 0],
                    [2, 8, 0],
                    [2, 9, 0],
                    [2, 10, 3],
                    [2, 11, 2],
                    [2, 12, 1],
                    [2, 13, 9],
                    [2, 14, 8],
                    [2, 15, 10],
                    [2, 16, 6],
                    [2, 17, 5],
                    [2, 18, 5],
                    [2, 19, 5],
                    [2, 20, 7],
                    [2, 21, 4],
                    [2, 22, 2],
                    [2, 23, 4],
                    [3, 0, 7],
                    [3, 1, 3],
                    [3, 2, 0],
                    [3, 3, 0],
                    [3, 4, 0],
                    [3, 5, 0],
                    [3, 6, 0],
                    [3, 7, 0],
                    [3, 8, 1],
                    [3, 9, 0],
                    [3, 10, 5],
                    [3, 11, 4],
                    [3, 12, 7],
                    [3, 13, 14],
                    [3, 14, 13],
                    [3, 15, 12],
                    [3, 16, 9],
                    [3, 17, 5],
                    [3, 18, 5],
                    [3, 19, 10],
                    [3, 20, 6],
                    [3, 21, 4],
                    [3, 22, 4],
                    [3, 23, 1],
                    [4, 0, 1],
                    [4, 1, 3],
                    [4, 2, 0],
                    [4, 3, 0],
                    [4, 4, 0],
                    [4, 5, 1],
                    [4, 6, 0],
                    [4, 7, 0],
                    [4, 8, 0],
                    [4, 9, 2],
                    [4, 10, 4],
                    [4, 11, 4],
                    [4, 12, 2],
                    [4, 13, 4],
                    [4, 14, 4],
                    [4, 15, 14],
                    [4, 16, 12],
                    [4, 17, 1],
                    [4, 18, 8],
                    [4, 19, 5],
                    [4, 20, 3],
                    [4, 21, 7],
                    [4, 22, 3],
                    [4, 23, 0],
                    [5, 0, 2],
                    [5, 1, 1],
                    [5, 2, 0],
                    [5, 3, 3],
                    [5, 4, 0],
                    [5, 5, 0],
                    [5, 6, 0],
                    [5, 7, 0],
                    [5, 8, 2],
                    [5, 9, 0],
                    [5, 10, 4],
                    [5, 11, 1],
                    [5, 12, 5],
                    [5, 13, 10],
                    [5, 14, 5],
                    [5, 15, 7],
                    [5, 16, 11],
                    [5, 17, 6],
                    [5, 18, 0],
                    [5, 19, 5],
                    [5, 20, 3],
                    [5, 21, 4],
                    [5, 22, 2],
                    [5, 23, 0],
                    [6, 0, 1],
                    [6, 1, 0],
                    [6, 2, 0],
                    [6, 3, 0],
                    [6, 4, 0],
                    [6, 5, 0],
                    [6, 6, 0],
                    [6, 7, 0],
                    [6, 8, 0],
                    [6, 9, 0],
                    [6, 10, 1],
                    [6, 11, 0],
                    [6, 12, 2],
                    [6, 13, 1],
                    [6, 14, 3],
                    [6, 15, 4],
                    [6, 16, 0],
                    [6, 17, 0],
                    [6, 18, 0],
                    [6, 19, 0],
                    [6, 20, 1],
                    [6, 21, 2],
                    [6, 22, 2],
                    [6, 23, 6],
                ]
                data = [[d[1], d[0], d[2] if d[2] != 0 else "-"] for d in data]

                option = {
                    "tooltip": {"position": "top"},
                    "grid": {"height": "50%", "top": "10%"},
                    "xAxis": {"type": "category", "data": x, "splitArea": {"show": True}},
                    "yAxis": {"type": "category", "data": y, "splitArea": {"show": True}},
                    "visualMap": {
                        "min": 0,
                        "max": 10,
                        "calculable": True,
                        "orient": "horizontal",
                        "left": "center",
                        "bottom": "15%",
                    },
                    "series": [
                        {
                            "name": "Interfaces",
                            "type": "heatmap",
                            "data": data,
                            "label": {"show": True},
                            "emphasis": {
                                "itemStyle": {"shadowBlur": 10, "shadowColor": "rgba(0, 0, 0, 0.5)"}
                            },
                        }
                    ],
                }
                value = st_echarts(
                    option, 
                    height="500px",
                    key="echarts",
                    events={"click": "function(params) { console.log(params.name); return params.name }"},
                    )

            
            with col_riskid_2:
                st.write("The selected system is: ", system)
                selected_points = []
                st.write("The selected points are: ", value)

        questions_tab3 = st.expander("Questions", expanded=False)


    ####################
    # Tab 4            #
    ####################

    with tab4:
        st.subheader("3. Mitigate Risks")

        mitigations = [
            "M01 - EMI Filter",
            "M02 - Cable shielding ",
            "M03 - Heat-resistant bearing",
            "M04 - Regular inspection of hub alignment and torque values",
            "M05 - Regular lubribation of moving parts",
            "M06 - Temperature sensors or thermal monitoring devices",
            "M07 - Heat sinks ",
            "M08 - Hydraulic reservoir shutdown mechanism ",
            "M09 - Cable shielding ",
            "M10 - EMI Filter",
            "M11 - Optical isolators",
            "M12 - EMI shielded housing",
            "M13 - Redundant angle sensor ",
            "M14 - Load sensors",
            "M15 - Motor Force Control and Feedback System",
            "M16 - Load cells",
            "M17 - Load cells",
            "M18 - Load cells",
            "M19 - Ventilation mechanism",
            "M20 - Dampening mechanism ",
            "M21 - Elastomeric mount ",
            "M22 - Electromagnetic Shielding",
            "M23 - Electric motor housing with conductive materials",
            "M24 - Heat-resistant material",
            "M25 - Ventilation system",
        ]

        with st.form(key="risk_mitigation_form"):
            st.markdown(
                """**Please select the mitigation you would like to add to the risk mitigation registry.**"""
            )
            st.caption(
                "Please select mitigation you would like to add to the risk mitigation registry."
            )
            # multiple selection
            mitigation = st.multiselect(
                "Mitigation",
                mitigations,
                help="Select the mitigation you would like to add to the risk mitigation registry.",
            )
            # Submit button
            submit_button = st.form_submit_button(
                label="Submit", help="Click here to submit your answers."
            )

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
            st.caption(
                "Please rate the following options from 0 (not at all) to 5 (very much)."
            )
            q1 = st.slider(
                "My previous experience",
                key="q1",
                min_value=0.0,
                max_value=5.0,
                value=2.5,
                step=0.1,
            )
            st.divider()
            q2 = st.slider(
                "Discussion with my colleagues",
                key="q2",
                min_value=0.0,
                max_value=5.0,
                value=2.5,
                step=0.1,
            )
            st.divider()
            q3 = st.slider(
                "Risk registry",
                key="q3",
                min_value=0.0,
                max_value=5.0,
                value=2.5,
                step=0.1,
            )
            st.divider()
            q4 = st.slider(
                "Value analysis models",
                key="q4",
                min_value=0.0,
                max_value=5.0,
                value=2.5,
                step=0.1,
            )
            st.divider()
            q5 = st.slider(
                "Binary DSMs",
                key="q5",
                min_value=0.0,
                max_value=5.0,
                value=2.5,
                step=0.1,
            )
            st.divider()
            q6 = st.slider(
                "Numerical (Spatial) DSMs",
                key="q6",
                min_value=0.0,
                max_value=5.0,
                value=2.5,
                step=0.1,
            )
            st.divider()
            q7 = st.slider(
                "Risk propagation matrices",
                key="q7",
                min_value=0.0,
                max_value=5.0,
                value=2.5,
                step=0.1,
            )
            st.divider()
            q8 = st.slider(
                "Risk mitigations registry",
                key="q8",
                min_value=0.0,
                max_value=5.0,
                value=2.5,
                step=0.1,
            )
            st.divider()
            st.markdown("""**Demographic information**""")
            st.caption(
                "Please fill in the following information. It will be used for research purposes only."
            )
            person_col1, person_col2 = st.columns(2)

            role = person_col1.text_input(
                label="Professional role",
                help="Enter your professional role here.",
            )
            experience = person_col2.number_input(
                label="Professional experience (years)",
                help="Enter your years of professional experience here.",
                min_value=0,
                max_value=100,
            )
            st.divider()
            # Submit button
            submit_button = st.form_submit_button(
                label="Submit", help="Click here to submit your answers."
            )
            if submit_button:
                #
                session_id = get_session_id()
                response_ref = db.collection("responses").document(session_id)
                # And then uploading the data to that reference
                response_ref.set(
                    {
                        "session_id": session_id,
                        "timestamp": timestamp,
                        "group": group,
                        "role": role,
                        "experience": experience,
                        "q1": q1,
                        "q2": q2,
                        "q3": q3,
                        "q4": q4,
                        "q5": q5,
                        "q6": q6,
                        "q7": q7,
                        "q8": q8,
                        "consent": consent,
                        "session_state": st.session_state["data"],
                    }
                )
                st.success(
                    body="Your answers have been submitted. Thank you for participating!",
                    icon="👍",
                )

        questions_tab5 = st.expander("Questions", expanded=False)

    ####################
    # Tab 6            #
    ####################

    with tab6:
        st.subheader("Help")
        with st.expander("How to use this webapp?", expanded=True):
            st.markdown(
                """
            **Inputs**: In this tab, you can change the market sizes and the characteristics of the systems under consideration.

            **Value Analysis**: In this tab, you can see the market shares, revenues, and profits of the systems under consideration.

            **Risk Identification**: In this tab, you can see the risk matrix of the systems under consideration.

            **Risk Mitigation**: In this tab, you can see the risk registry of the systems under consideration.

            **Questionnaire**: In this tab, you can answer the questionnaire.

            **Help**: In this tab, you can find help on how to use the app.

            For additional information, please contact the workshop in-person facilitators.
            """
            )
        with st.expander("Contact", expanded=False):
            st.markdown(
                """
            **Facilitators**: 
            - Massimo Panarotto
            - Iñigo Alonso Fernandez
            - ...
            """
            )
        with st.expander("References", expanded=False):
            st.markdown(
                """
            **Value Analysis**:
            - ...

            **Risk Identification**:
            - ...

            **Risk Mitigation**:
            - ...
            """
            )
        with st.expander("Acknowledgements", expanded=False):
            st.markdown(
                """
            **Acknowledgements**:
            - Volvo Trucks
            - VINNOVA
            - Design Society
            - Chalmers University of Technology
            - DSM Conference
            """
            )

    questions_tab1.write("What is the minimum turning radius of a truck?")
    questions_tab2.write("what do you thiunk?")
    questions_tab3.selectbox(
                "Risk",
                risks,
                help="Select the risk you would like to add to the risk mitigation registry.",
            )

print("Here's the session state:")
print([key for key in st.session_state.keys()])
# ic(st.session_state["data_editor"])

try:
    sessions_ref = db.collection("session_states").document(participants_id)
    # And then uploading the data to that reference
    sessions_ref.set({"role": role, "group": group})
except:
    pass
