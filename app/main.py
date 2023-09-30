"""
# DSM 2023 Workshop
This app helps the participants of the DSM Industry Sprint Workshop.
"""

###############################################################################
# Imports
###############################################################################

from __future__ import annotations

import datetime
import json
import pandas as pd
import streamlit as st
from streamlit import runtime
from streamlit.runtime.scriptrunner import get_script_run_ctx
from streamlit import session_state as ss
import plotly.express as px
from plotly.subplots import make_subplots
from google.cloud import firestore
from google.oauth2 import service_account
import seaborn as sns
from streamlit_echarts import st_echarts
from ragraph.graph import Graph
from ragraph.node import Node
from ragraph.edge import Edge
from ragraph import plot
from ragraph.colors import (
    get_diverging_redblue,
)

###############################################################################
# Formatting
###############################################################################

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
                header {
                background: rgba(250,250,250, 0) !important;
                }
                footer {
                visibility: hidden;
                height: 0%;
                }
                #root > div:nth-child(1) > div > div > div > div > section > div {padding-top: 0rem;}
                .modebar-group {
                background-color: rgba(0, 0, 0, 0.1) !important;
                }
                </style>
                """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# increase the size of the expander titles (class streamlit-expanderHeader)
expander_titles_style = """
                <style>
                .streamlit-expanderHeader {font-size: 3rem;}
                </style>
                """
st.markdown(expander_titles_style, unsafe_allow_html=True)


# fix echarts
st.markdown(
    """ <style>iframe[title="streamlit_echarts.st_echarts"]{ height: 600px !important } """,
    unsafe_allow_html=True,
)

###############################################################################
# Setup
###############################################################################


# Authenticate to Firestore
@st.cache_resource
def authenticate_to_firestore():
    """Authenticates to Firestore and returns a client."""
    key_dict = json.loads(st.secrets["textkey"])
    creds = service_account.Credentials.from_service_account_info(key_dict)
    db = firestore.Client(credentials=creds, project="dsm2023isw")
    return db


db = authenticate_to_firestore()


# Disable SettingWithCopyWarning from pandas
# https://stackoverflow.com/questions/20625582/how-to-deal-with-settingwithcopywarning-in-pandas
pd.options.mode.chained_assignment = None  # default='warn'



# Colors
systems_colors = ["#264653", "#E9C46A", "#E76F51"]
markets_colors = ["#3A86FF", "#FF006E", "#8338EC"]

# dataframe colors
cm_g2r = sns.diverging_palette(130, 12, as_cmap=True)
cm_r2g = sns.diverging_palette(12, 130, as_cmap=True)


###############################################################################
# Functions
###############################################################################


# Timestamp string
def get_timestamp():
    """Returns a timestamp string"""
    now = datetime.datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
    return timestamp


def on_data_update(data):
    """Callback function when data is updated."""
    # print("Data updated (not uploaded):", data)
    pass


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
    """Calculate market shares and update the dataframe."""
    if new_df is not None:
        if new_df.equals(ss["df_systems"]):
            return
        ss["df_systems"] = new_df

    df_systems = ss["df_systems"]
    df_systems["market_share_1"] = df_systems["price"] * 2
    df_systems["market_share_2"] = df_systems["price"] * 3
    df_systems["market_share_3"] = df_systems["price"] * 4
    df_systems["market_units_1"] = df_systems["market_share_1"] * ss.market_sizes[0]
    df_systems["market_units_2"] = df_systems["market_share_2"] * ss.market_sizes[1]
    df_systems["market_units_3"] = df_systems["market_share_3"] * ss.market_sizes[2]
    df_systems["market_revenue_1"] = df_systems["price"] * df_systems["market_units_1"]
    df_systems["market_revenue_2"] = df_systems["price"] * df_systems["market_units_2"]
    df_systems["market_revenue_3"] = df_systems["price"] * df_systems["market_units_3"]
    df_systems["market_profit_1"] = (
        df_systems["price"] - df_systems["cost"]
    ) * df_systems["market_units_1"]
    df_systems["market_profit_2"] = (
        df_systems["price"] - df_systems["cost"]
    ) * df_systems["market_units_2"]
    df_systems["market_profit_3"] = (
        df_systems["price"] - df_systems["cost"]
    ) * df_systems["market_units_3"]
    df_systems["total_units"] = (
        df_systems["market_units_1"]
        + df_systems["market_units_2"]
        + df_systems["market_units_3"]
    )
    df_systems["total_revenue"] = (
        df_systems["market_revenue_1"]
        + df_systems["market_revenue_2"]
        + df_systems["market_revenue_3"]
    )
    df_systems["total_profit"] = (
        df_systems["market_profit_1"]
        + df_systems["market_profit_2"]
        + df_systems["market_profit_3"]
    )
    ss["df_systems"] = df_systems
    # st.rerun()


###############################################################################
# Head
###############################################################################

# Logo and title
col_logo, col_title = st.columns([0.2, 1])
with col_logo:
    st.write("")
    st.write("")
    st.image("assets/logo_large.png", width=60)

with col_title:
    st.title("Industry Sprint Workshop 2023")
    st.caption("**Workshop Facilitator** for _The 25th International DSM Conference_")

# Group and consent
with st.expander("Info", expanded=True):
    st.markdown(
        """
            Please fill in the following information to start the workshop.
            """
    )

    group = st.radio(
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
        ),
        horizontal=True,
    )
    consent = st.checkbox(
        label="I consent to the use of my data for research purposes.",
        help="Please check this box to consent to the use of your data for research purposes.",
    )

    if not ((group != "Select") and consent):
        warning = st.warning(
            body="Please make sure to enter your group correctly.",
            icon="⚠️",
        )
    else:
        # Creating a NEW document for each participant
        session_id = get_session_id()
        session_ref = db.collection("sessions").document(session_id)
        # And then uploading the data to that reference
        session_ref.set(
            {"session_id": session_id, "timestamp": get_timestamp(), "group": group}
        )
        st.success(
            body="You are ready to go! Click on the top right arrow to minimize this section. The tabs bellow will guide you through the workshop.",
            icon="👍",
        )

# Market shares
if "market_sizes" not in ss:
    ss.market_sizes = [10000, 20000, 40000]

# Import data from data/TechRisks.csv into dataframe
df_risks = pd.read_csv("data/TechRisks.csv")

# Import data from data/Mitigations.csv into dataframe
df_mitigations = pd.read_csv("data/Mitigations.csv")

# Import data from data/Components.csv into dataframe
df_components = pd.read_csv("data/Components.csv", sep=";", decimal=",")
# Compomnets per system
df_components_s1 = df_components[df_components["s1"] == True]
df_components_s2 = df_components[df_components["s2"] == True]
df_components_s3 = df_components[df_components["s3"] == True]


# Original designs
if "df_systems" not in ss:
    ss.df_systems = pd.DataFrame(
        [
            {
                "name": "System 1",
                "description": "Only front steering",
                "min_R": 10.7,
                "reliability": 0.82,
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
                "reliability": 0.75,
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
        ]
    )
    calculate_ms()



# If the user has filled in the intro form correctly
if (group != "Select") and consent:
    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        [
            "(1) Analyze Value",
            "(2) Identify Risks",
            "(3) Mitigate Risks",
            "Questionnaire",
            "Help",
        ]
    )

    ###############################################################################
    # Tab 1
    ###############################################################################

    with tab1:
        st.subheader("📋 Inputs")
        with st.expander("**Markets**", expanded=False):
            st.markdown(
                """**Potential yearly market for each application (# of trucks)**"""
            )
            ss.market_sizes[0] = st.slider("Artic", 0, 200000, ss.market_sizes[0])
            ss.market_sizes[1] = st.slider("Desert", 0, 200000, ss.market_sizes[1])
            ss.market_sizes[2] = st.slider("Special", 0, 200000, ss.market_sizes[2])

        with st.expander("**Systems under consideration**", expanded=True):
            editable_df = st.data_editor(
                ss["df_systems"],
                key="systems_data_editor",
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
                # print(i, a, d, e, market_shares_artic)

            for i in range(len(editable_df)):
                a = 1 / (1 + ((editable_df["min_R"][i] - 10) * 0.5) ** 2) - 0.5
                d = 1 - (0.5) ** (50 / editable_df["price"][i]) - 0.3
                e = 1 - (0.5) ** (1 / editable_df["reliability"][i])
                market_share = 0.2 * (a + d + e)
                market_shares_desert.append(market_share)
                # print(i, a, d, e, market_shares_desert)

            for i in range(len(editable_df)):
                a = 1 - (0.5) ** (50 / editable_df["min_R"][i]) - 0.3
                d = 1 - (0.5) ** (500 / editable_df["price"][i]) - 0.3
                e = 1 - (0.5) ** (1 / editable_df["reliability"][i])
                market_share = 0.2 * (a + d + e)
                market_shares_special.append(market_share)
                # print(i, a, d, e, market_shares_special)

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

        st.subheader("🔍 1. Analyze Value")

        with st.expander("**Profits**", expanded=True):
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

        with st.expander("**Market share**", expanded=True):
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

        questions_tab1 = st.expander("**Questions**", expanded=True)

    ###############################################################################
    # Tab 2
    ###############################################################################

    with tab2:
        st.subheader("🗹 2. Identify Risks")

        with st.expander("**Select system**", expanded=True):
            # Select system to display
            system = st.selectbox(
                label="System",
                help="Select the system you would like to display.",
                options=(
                    "System 1 - Only front steering",
                    "System 2 - Front + Back steering (hydraulic)",
                    "System 3 - Front + Back steering (electric)",
                ),
                index=0,
            )

        with st.expander("**Technical risk registry**", expanded=True):
            df_risks_table = st.dataframe(
                df_risks.style.background_gradient(cmap=cm_g2r).format(
                    {2: "{:.2f}"}, na_rep="MISS", precision=2
                ),
                height=400,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "ID": st.column_config.TextColumn("Risk ID", help="Risk ID"),
                    "Name": st.column_config.TextColumn(
                        "Risk name", help="Risk description"
                    ),
                    "Mechanical": st.column_config.NumberColumn(
                        "Mechanical",
                        help="Mechanical risk",
                        format="%.2f",
                    ),
                    "Electromagnetic": st.column_config.NumberColumn(
                        "Electromagnetic",
                        help="Electromagnetic risk",
                        format="%.2f",
                    ),
                    "Thermal": st.column_config.NumberColumn(
                        "Thermal",
                        help="Thermal risk",
                        format="%.2f",
                    ),
                    "Comments": None,
                    "id2": None,
                    "x": None,
                    "y": None,
                    "z": None,
                    "force_e2": None,
                    "force_t": None,
                    "force_r": None,
                    "electro_e2": None,
                    "electro_t": None,
                    "electro_r": None,
                    "thermo_e2": None,
                    "thermo_t": None,
                    "thermo_r": None,
                },
            )

        with st.expander("**Matrices**", expanded=True):
            matrix = st.radio(
                "Select the matrix to display",
                ["Binary DSM", "Distance DSM", "Risk DSM [TODO]"],
                captions=[
                    "Interfaces between components",
                    "Distances between components",
                    "Propagation of risks between components",
                ],
                horizontal=True,
            )

            df_components = pd.read_csv("data/components.csv", sep=";", decimal=",")
            df_dsm = pd.read_csv(
                "data/dsm.csv", sep=";", header=None, decimal=","
            ).fillna(0)
            df_distances = pd.read_csv(
                "data/distances.csv", sep=";", header=None, decimal=","
            ).fillna(0)

            kinds = {
                "M": "mechanical",
                "E": "electrical",
                "I": "information",
                "H": "hydraulic",
            }

            g = Graph()

            for component in df_components.iterrows():
                # print(f'id: {component[1]["id"]} name:{component[1]["name"]}')
                labels = [s for s in ["s2", "s2", "s3"] if component[1][s] == True]
                fancy_node = Node(
                    name=component[1]["name"],
                    kind="component",
                    labels=labels,
                    weights={
                        "x": component[1]["x"],
                        "y": component[1]["y"],
                        "z": component[1]["z"],
                        "force_e": component[1]["force_e"],
                        "force_t": component[1]["force_t"],
                        "force_r": component[1]["force_r"],
                        "electro_e": component[1]["electro_e"],
                        "electro_t": component[1]["electro_t"],
                        "electro_r": component[1]["electro_r"],
                        "thermo_e": component[1]["thermo_e"],
                        "thermo_t": component[1]["thermo_t"],
                        "thermo_r": component[1]["thermo_r"],
                    },
                    annotations={
                        "id": component[1]["id"],
                    },
                )
                g.add_node(fancy_node)

            for i, row in df_dsm.iterrows():
                for j, value in enumerate(row):
                    # print(i, j, value)
                    # print()
                    if i == j:
                        continue
                    if value in kinds.keys():
                        kind = kinds[value]
                    else:
                        kind = None
                    g.add_edge(
                        Edge(
                            source=g.nodes[i],
                            target=g.nodes[j],
                            name=f'{g.nodes[i].annotations["id"]}_{g.nodes[j].annotations["id"]}',
                            kind=kind,
                            labels=[],
                            weights={
                                "distance": df_distances.iloc[i, j],
                            },
                            annotations={},
                        )
                    )

            if matrix == "Binary DSM":
                fig = plot.mdm(
                    leafs=g.leafs,
                    edges=g.edges,
                    style=plot.Style(
                        piemap=dict(
                            fields=[
                                "mechanical",
                                "electrical",
                                "information",
                                "hydraulic",
                            ],
                        ),
                        palettes=dict(
                            fields={
                                "mechanical": {"categorical": "#de9c38"},
                                "electrical": {"categorical": "#a64747"},
                                "information": {"categorical": "#545a8e"},
                                "hydraulic": {"categorical": "#389dfc"},
                            }
                        ),
                    ),
                )
            elif matrix == "Distance DSM":
                fig = plot.mdm(
                    leafs=g.leafs,
                    edges=g.edges,
                    style=plot.Style(
                        piemap=dict(
                            display="weights",
                            fields=[
                                "distance",
                            ],
                            mode="relative",
                        ),
                        palettes=dict(
                            fields={
                                "distance": {"continuous": get_diverging_redblue()},
                            }
                        ),
                    ),
                )
            elif matrix == "Risk DSM [TODO]":
                fig = plot.mdm(
                    leafs=g.leafs,
                    edges=g.edges,
                    style=plot.Style(
                        piemap=dict(
                            fields=[
                                "force_e",
                                "force_t",
                                "force_r",
                                "electro_e",
                                "electro_t",
                                "electro_r",
                                "thermo_e",
                                "thermo_t",
                                "thermo_r",
                            ],
                        ),
                        palettes=dict(
                            fields={
                                "force_e": {"categorical": "#de9c38"},
                                "force_t": {"categorical": "#de9c38"},
                                "force_r": {"categorical": "#de9c38"},
                                "electro_e": {"categorical": "#a64747"},
                                "electro_t": {"categorical": "#a64747"},
                                "electro_r": {"categorical": "#a64747"},
                                "thermo_e": {"categorical": "#545a8e"},
                                "thermo_t": {"categorical": "#545a8e"},
                                "thermo_r": {"categorical": "#545a8e"},
                            }
                        ),
                    ),
                )

            fig.update_layout(
                {
                    "plot_bgcolor": "rgba(0, 0, 0, 0)",
                    "paper_bgcolor": "rgba(0, 0, 0, 0)",
                    "xaxis": {"fixedrange": True},
                    "yaxis": {"fixedrange": True},
                }
            )

            st.plotly_chart(
                fig,
                use_container_width=True,
                config={
                    "displayModeBar": False,
                    "displaylogo": False,
                    "modeBarButtonsToRemove": [
                        "zoom2d",
                        "zoomIn2d",
                        "zoomOut2d",
                        "resetScale2d",
                        "toggleSpikelines",
                        "pan2d",
                        "lasso2d",
                        "select2d",
                        "autoScale2d",
                        "hoverClosestCartesian",
                        "hoverCompareCartesian",
                    ],
                },
            )

        questions_tab2 = st.expander("**Questions**", expanded=True)

        with questions_tab2:
            questions_tab2_col1, questions_tab2_col2 = st.columns(2)

    ###############################################################################
    # Tab 3
    ###############################################################################

    with tab3:
        st.subheader("🛡️ 3. Mitigate Risks")

        with st.expander("**Where to place mitigations? TODO**", expanded=True):
            if system == "System 1 - Only front steering":
                n = 16
            elif system == "System 2 - Front + Back steering (hydraulic)":
                n = 18
            elif system == "System 3 - Front + Back steering (electric)":
                n = 25
            else:
                n = 10

            col_riskid_1, col_riskid_2 = st.columns([2, 1])

            with col_riskid_1:
                product_elements = [f"Element {i}" for i in range(1, n + 1)]

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
                x = [f"Element {i}" for i in range(1, n + 1)]
                y = [f"Element {i}" for i in range(1, n + 1)]

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
                    "tooltip": {
                        "position": "top",
                        "formatter": "Origin:<br />{b}<br />Destination:<br />{c}",
                        "valueFormatter": "(value) => '$'",
                    },
                    "grid": {"height": "50%", "top": "10%"},
                    "xAxis": {
                        "type": "category",
                        "data": x,
                        "splitArea": {"show": True},
                    },
                    "yAxis": {
                        "type": "category",
                        "data": y,
                        "splitArea": {"show": True},
                    },
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
                                "itemStyle": {
                                    "shadowBlur": 10,
                                    "shadowColor": "rgba(0, 0, 0, 0.5)",
                                }
                            },
                        }
                    ],
                }
                value = st_echarts(
                    option,
                    height="600px",
                    key="echarts",
                    events={
                        "click": "function(params) { console.log(params.name); return params.name }"
                    },
                )

            with col_riskid_2:
                st.write("The selected system is: ", system)
                selected_points = []
                st.write("The selected points are: ", value)

        with st.expander("**List of Mitigation Elements**", expanded=True):
            st.dataframe(
                df_mitigations.style.background_gradient(
                    cmap=cm_g2r, subset=["Cost (k€)"]
                ).format({3: "{:.2f}", 4: "{:.2f}"}, na_rep="MISS", precision=2),
                height=400,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "ID": st.column_config.TextColumn(
                        "Mitigation ID", help="Mitigation ID"
                    ),
                    "Risk Mitigation element": st.column_config.TextColumn(
                        "Risk Mitigation element", help="Risk Mitigation element"
                    ),
                    "Placed at the interface between ": st.column_config.TextColumn(
                        "Placed at the interface between ",
                        help="Placed at the interface between ",
                    ),
                    "Cost (k€)": st.column_config.NumberColumn(
                        "Cost (k€)",
                        help="Cost (k€)",
                        format="%.2f",
                    ),
                    "Reliability gain": st.column_config.NumberColumn(
                        "Reliability gain",
                        help="Reliability gain",
                        format="%.3f",
                    ),
                    "Mechanical": st.column_config.CheckboxColumn(
                        "Mechanical", help="Mechanical"
                    ),
                    "Electromagnetic": st.column_config.CheckboxColumn(
                        "Electromagnetic", help="Electromagnetic"
                    ),
                    "Thermal": st.column_config.CheckboxColumn(
                        "Thermal", help="Thermal"
                    ),
                    "id2": None,
                    "x": None,
                    "y": None,
                    "z": None,
                    "force_e2": None,
                    "force_t": None,
                    "force_r": None,
                    "electro_e2": None,
                    "electro_t": None,
                    "electro_r": None,
                    "thermo_e2": None,
                    "thermo_t": None,
                    "thermo_r": None,
                },
            )
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

        questions_tab3 = st.expander("**Questions**", expanded=True)

    ###############################################################################
    # Tab 4
    ###############################################################################

    with tab4:
        # show text if time is over 3pm onn October 4
        start = datetime.datetime(2023, 10, 4, 15, 0, 0)
        if datetime.datetime.now() > start:
            st.error(
                "  This questionnaire is not available yet. Please come back after 15:00. Thank you!",
                icon="🕒",
            )
        else:
            st.subheader("❔ Questionnaire")
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
                person_col1, person_col2, person_col3 = st.columns(3)

                roles = [
                    "Student",
                    "Engineering Manager",
                    "Systems Architect",
                    "Platform Architect",
                    "Product Manager",
                    "Project Manager",
                    "Program Manager",
                    "Design Engineer",
                    "Manufacturing Engineer",
                    "Quality Engineer",
                    "Reliability Engineer",
                    "Software Engineer",
                    "Data Scientist",
                    "Research Scientist",
                    "Systems Analyst",
                    "Business Analyst",
                    "Executive (CEO, COO, CFO, etc.)",
                    "Consultant",
                    "Professor",
                    "Vendor",
                    "Other",
                ]

                sectors = [
                    "Aerospace",
                    "Automotive",
                    "Biomedical",
                    "Chemical",
                    "Civil",
                    "Construction",
                    "Consumer Products",
                    "Defense",
                    "Education",
                    "Electrical",
                    "Electronics",
                    "Energy",
                    "Entertainment",
                    "Food",
                    "Healthcare",
                    "Information Technology",
                    "Manufacturing",
                    "Marine",
                    "Materials",
                    "Mechanical",
                    "Packaging",
                    "Pharmaceutical",
                    "Robotics",
                    "Software",
                    "Telecommunications",
                    "Transportation",
                    "Other",
                ]

                role = person_col1.selectbox(
                    label="Professional role",
                    options=roles,
                    index=None,
                    help="Select your professional role here.",
                )
                # role_other = person_col1.text_input(
                #     label="Other professional role",
                #     help="Enter your professional role here if not on the list above.",
                # )
                sector = person_col2.selectbox(
                    label="Professional sector",
                    options=sectors,
                    index=None,
                    help="Select your professional sector here.",
                )
                # sector_other = person_col2.text_input(
                #     label="Other professional sector",
                #     help="Enter your professional sector here if not on the list above.",
                # )
                experience = person_col3.number_input(
                    label="Professional experience (years)",
                    help="Enter your years of professional experience here.",
                    value=None,
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
                            "timestamp": get_timestamp(),
                            "group": group,
                            "consent": consent,
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
                            "session_state": ss,
                        }
                    )
                    st.success(
                        body="Your answers have been submitted. Thank you for participating!",
                        icon="👍",
                    )

        questions_tab4 = st.expander("**Questions**", expanded=True)

    ###############################################################################
    # Tab 5
    ###############################################################################

    with tab5:
        st.subheader("ℹ️ Help")
        with st.expander("**How to use this webapp?**", expanded=True):
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
        with st.expander("**Contact**", expanded=False):
            st.markdown(
                """
            **Facilitators**: 
            - Massimo Panarotto
            - Iñigo Alonso Fernandez
            - ...
            """
            )
        with st.expander("**References**", expanded=False):
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
        with st.expander("**Acknowledgements**", expanded=False):
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

    ###############################################################################
    # Questions
    ###############################################################################

    # Questions Tab 1
    questions_tab1.write(
        "I think that the most valuable systems for each of the markets are..."
    )
    questions_tab1.caption(
        "Please rate from 1 to 10, where 1 means low potential and 10 high potential."
    )
    cont_market_artic = questions_tab1.container()
    with cont_market_artic:
        st.write("Artic Market")
        col_cont_artic_1, col_cont_artic_2, col_cont_artic_3 = st.columns(3)
        with col_cont_artic_1:
            artic_s1 = st.slider("System 1 in Artic Market", 1, 10, 5)
        with col_cont_artic_2:
            artic_s2 = st.slider("System 2 in Artic Market", 1, 10, 5)
        with col_cont_artic_3:
            artic_s3 = st.slider("System 3 in Artic Market", 1, 10, 5)

    cont_market_desert = questions_tab1.container()
    with cont_market_desert:
        st.write("Desert Market")
        col_cont_desert_1, col_cont_desert_2, col_cont_desert_3 = st.columns(3)
        with col_cont_desert_1:
            desert_s1 = st.slider("System 1 in Desert Market", 1, 10, 5)
        with col_cont_desert_2:
            desert_s2 = st.slider("System 2 in Desert Market", 1, 10, 5)
        with col_cont_desert_3:
            desert_s3 = st.slider("System 3 in Desert Market", 1, 10, 5)

    cont_market_special = questions_tab1.container()
    with cont_market_special:
        st.write("Special Market")
        col_cont_special_1, col_cont_special_2, col_cont_special_3 = st.columns(3)
        with col_cont_special_1:
            special_s1 = st.slider("System 1 in Special Market", 1, 10, 5)
        with col_cont_special_2:
            special_s2 = st.slider("System 2 in Special Market", 1, 10, 5)
        with col_cont_special_3:
            special_s3 = st.slider("System 3 in Special Market", 1, 10, 5)

    # Questions Tab 2
    questions_tab2_col1.radio(
        "Which of the risks would you select for mitigation?",
        df_risks["Name"].tolist(),
        help="Select the risk you would like to mitigate.",
    )

    # Questions Tab 3
    questions_tab3.write(
        "Please reasses the potential of the new design with mitigations compared with the baseline designs:"
    )
    questions_tab3.caption(
        "Please rate form 1 to 10, where 1 means low potential and 10 high potential."
    )
    questions_tab3.table(
        [
            ["Market", "System 1", "System 2", "System 3", "My design"],
            ["Artic", "5", "5", "5", "5"],
            ["Desert", "5", "5", "5", "5"],
            ["Special", "5", "5", "5", "5"],
        ]
    )


###############################################################################
# Session state
###############################################################################

# print("Here's the session state:")
# print([key for key in ss.keys()])
# print(ss)

try:
    session_state_ref = db.collection("session_states").document(get_session_id())
    # And then uploading the data to that reference
    session_state_ref.set(
        {
            "session_id": get_session_id(), 
            "role": role, 
            "group": group,
            "session_state": ss,
        }
    )
except:
    pass

###############################################################################
# Footer
###############################################################################

# footer = st.expander(
#     "Links",
#     expanded=True
# )

# col_footer1, col_footer2, col_footer3, col_footer4, col_footer5 = footer.columns(5)

# col_footer2.link_button(
#     "Conference Homepage",
#     url="https://dsm-conference.org/",
#     help="Go to DSM Conference 2023 website",
# )
# col_footer3.link_button(
#     "Conference Programme",
#     url="https://dsm-conference.org/conference-programme/",
#     help="Go to DSM Conference 2023 programme",
# )
# col_footer4.link_button(
#     "Conference Proceedings",
#     url="https://dsm-conference.org/conference-proceedings-dsm-2023/",
#     help="Go to DSM Conference 2023 proceedings",
# )
# col_footer5.link_button(
#     "Design Society",
#     url="https://www.designsociety.org/",
#     help="Go to Design Society website",
# )
# col_footer1.link_button(
#     "dsmweb.org",
#     url="https://DSMweb.org/",
#     help="Go to DSMweb.org website",
# )

# footer.markdown(
#     """
#         Made with ❤️ by the DSM Conference 2021 team.
#     """
# )
