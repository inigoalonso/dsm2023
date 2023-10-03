
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

###############################################################################

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

###############################################################################

            # img = image_select(
            #     label="The following steps will be performed for the selected system. You can flip between the systems at any time.",
            #     images=[
            #         "assets/system1.png",
            #         "assets/system2.png",
            #         "assets/system3.png",
            #     ],
            #     captions=[
            #         "System 1 - Only front steering",
            #         "System 2 - Front + Back steering (hydraulic)",
            #         "System 3 - Front + Back steering (electric)",
            #     ],
            #     use_container_width=True,
            #     return_value="original",
            #     key="system_selection",
            # )
            # image_to_system = {
            #     "assets/system1.png": "System 1",
            #     "assets/system2.png": "System 2",
            #     "assets/system3.png": "System 3",
            # }
            # ss.system = image_to_system.get(img, "")


###############################################################################


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


###############################################################################


            config_risks_selectiopn = {
                "Selected": st.column_config.CheckboxColumn(
                    "Selected",
                    help="Select the risks you would like to mitigate.",
                    width="small",
                ),
                "ID": st.column_config.TextColumn(
                    "ID", help="Risk identification ID", width="small", disabled=True
                ),
                "Name": st.column_config.TextColumn(
                    "Name", help="Name", width="large", disabled=True
                ),
                "s1": None,
                "s2": None,
                "s3": None,
            }
            if ss.system == "System 1":
                questions_tab2_col1.multiselect(
                    label="Select the risks you would like to mitigate.",
                    options=ss.risks_selected_s1,
                    help="Select the risks you would like to mitigate.",
                )
                questions_tab2_col1.data_editor(
                    ss.df_risks_selected_s1,
                    key="risks_selected_s1",
                    height=400,
                    use_container_width=True,
                    hide_index=True,
                    num_rows="fixed",
                    column_config=config_risks_selectiopn,
                )
            elif ss.system == "System 2":
                questions_tab2_col1.data_editor(
                    ss.df_risks_selected_s2,
                    key="risks_selected_s2",
                    height=400,
                    use_container_width=True,
                    hide_index=True,
                    num_rows="fixed",
                    column_config=config_risks_selectiopn,
                )
            elif ss.system == "System 3":
                questions_tab2_col1.data_editor(
                    ss.df_risks_selected_s3,
                    key="risks_selected_s3",
                    height=400,
                    use_container_width=True,
                    hide_index=True,
                    num_rows="fixed",
                    column_config=config_risks_selectiopn,
                )
            else:
                st.warning("Please select a system to explore.")


###############################################################################


            # # editable_df = st.data_editor(
            # st.dataframe(
            #     ss["df_systems"],
            #     #key="systems_data_editor",
            #     #num_rows="dynamic",
            #     use_container_width=False,
            #     hide_index=True,
            #     #on_change=on_data_update(data="df test"),
            #     column_config={
            #         "name": st.column_config.TextColumn(
            #             "Name",
            #             help="Name of the alternative system",
            #             max_chars=50,
            #         ),
            #         "description": st.column_config.TextColumn(
            #             "Description",
            #             help="Description of the alternative system",
            #             max_chars=50,
            #         ),
            #         "min_R": st.column_config.NumberColumn(
            #             "Minimum Turning Radius",
            #             help="Turning radius distance in meters",
            #             min_value=0,
            #             max_value=50,
            #             step=0.1,
            #             format="%.1f m",
            #             disabled=True,
            #         ),
            #         "reliability": st.column_config.NumberColumn(
            #             "Reliability",
            #             help="Reliability of the system",
            #             min_value=0,
            #             max_value=1,
            #             step=0.01,
            #             format="%.2f",
            #             disabled=True,
            #         ),
            #         "price": st.column_config.NumberColumn(
            #             "Price",
            #             help="Price in kilo Euros",
            #             min_value=0,
            #             max_value=500,
            #             step=0.1,
            #             format="%.1f k€",
            #         ),
            #         "cost": st.column_config.NumberColumn(
            #             "Cost",
            #             help="Cost in kilo Euros",
            #             min_value=0,
            #             max_value=500,
            #             step=0.1,
            #             format="%.1f k€",
            #             disabled=True,
            #         ),
            #         "market_share_1": None,
            #         "market_share_2": None,
            #         "market_share_3": None,
            #         "market_units_1": None,
            #         "market_units_2": None,
            #         "market_units_3": None,
            #         "market_revenue_1": None,
            #         "market_revenue_2": None,
            #         "market_revenue_3": None,
            #         "market_profit_1": None,
            #         "market_profit_2": None,
            #         "market_profit_3": None,
            #         "total_units": None,
            #         "total_revenue": None,
            #         "total_profit": None,
            #     },
            # )


###############################################################################


df_risks_selected = df_risks[["ID", "Name", "s1", "s2", "s3"]].copy()
new_col_risks = ["False" for i in range(len(df_risks_selected))]
df_risks_selected.insert(loc=0, column="Selected", value=new_col_risks)


if (
    "df_risks_selected_s1" not in ss
    and "df_risks_selected_s2" not in ss
    and "df_risks_selected_s3" not in ss
):
    ss.df_risks_selected_s1 = df_risks[df_risks["s1"] == True].copy()
    ss.df_risks_selected_s2 = df_risks[df_risks["s2"] == True].copy()
    ss.df_risks_selected_s3 = df_risks[df_risks["s3"] == True].copy()


###############################################################################

                import numpy as np

                df_dsm = pd.DataFrame(
                    np.random.rand(n, n), columns=("col %d" % i for i in range(n))
                )

                for i in range(n):
                    df_dsm[f"col {i}"][i] = "nan"
                    # df_dsm.loc[:, (f'col {i}', i)] = 'nan'

                fig_dsm = px.imshow(
                    df_dsm,
                    labels=dict(x="", y=""),
                    x=product_elements,
                    y=product_elements,
                    color_continuous_scale=[
                        [0, "#D81B60"],
                        [0.5, "#FFB000"],
                        [1, "#004D40"],
                    ],
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
                risk_chart = st.plotly_chart(
                    fig_dsm,
                    use_container_width=True,
                    config={
                        "displaylogo": False,
                        "modeBarButtonsToRemove": [
                            "sendDataToCloud",
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
    
###############################################################################


            from streamlit_echarts import st_echarts

            if ss.system == "System 1":
                n = 16
            elif ss.system == "System 2":
                n = 18
            elif ss.system == "System 3":
                n = 25
            else:
                n = 10

            col_riskid_1, col_riskid_2 = st.columns([2, 1])

            with col_riskid_1:
                product_elements = [f"Element {i}" for i in range(1, n + 1)]

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
                st.write("The selected system is: ", ss.system)
                selected_points = []
                st.write("The selected points are: ", value)


###############################################################################


with col_system:
    st.write("")
    st.write("")
    selected_system_logo = st.empty()

# Timer and warning

# import asyncio

# start_conf = datetime.datetime(2023, 10, 4, 9, 45, 0)
# is_early = datetime.datetime.now() < start_conf

# holder = st.empty()
# countdown = holder.expander("Coundown", expanded=True)
# if is_early:
#     with countdown:
#         st.markdown(
#             """
#             <style>
#             .time {
#                 font-size: 60px !important;
#                 font-weight: 100 !important;
#                 color: rgb(125, 53, 59) !important;
#             }
#             </style>
#             """,
#             unsafe_allow_html=True,
#         )

#         async def watch(test):
#             while True:
#                 time_left = start_conf - datetime.datetime.now()
#                 test.markdown(
#                     f"""
#                     <p class="time">
#                         {str(time_left.days)} days, {str(time_left.seconds//3600)} hours, {str((time_left.seconds//60)%60)} minutes, {str(time_left.seconds%60)} seconds
#                     </p>
#                     """,
#                     unsafe_allow_html=True,
#                 )
#                 r = await asyncio.sleep(1)

#         test = st.empty()

#         st.markdown(
#             """
#             This website is meant to guide the participants of the Industry Sprint Workshop. It will be available on the day of the workshop, Wednesday October 4th.

#             Come back then for the full experience! Thank you :)

#             Meanwhile, you can check out some of these links for more information about the conference and DSMs:

#             - [The 25th International DSM Conference](https://www.dsm-conference.org/)
#             - [Conference Programme](https://dsm-conference.org/conference-programme/)
#             - [Conference Proceedings](https://dsm-conference.org/conference-proceedings-dsm-2023/)
#             - [Design Society](https://www.designsociety.org/)
#             - [dsmweb.org](https://DSMweb.org/)


#             If you still want a sneak peak and pinky swear not to cheat during the workshop, you can click on the "Info" section bellow to access the website.
#             """,
#         )

# Group and consent
# with st.expander("Info", expanded=not (is_early)):


###############################################################################
# Housekeeping
###############################################################################

# Show selected system logo in the top right corner
if ss.system == "System 1":
    selected_system_logo.image("assets/system1.png", width=115)
elif ss.system == "System 2":
    selected_system_logo.image("assets/system2.png", width=115)
elif ss.system == "System 3":
    selected_system_logo.image("assets/system3.png", width=115)
else:
    selected_system_logo.image("assets/system0.png", width=115)

# if not (is_ready):
#     asyncio.run(watch(test))
# else:
#     holder.empty()

###############################################################################


# fix echarts
st.markdown(
    """ <style>iframe[title="streamlit_echarts.st_echarts"]{ height: 600px !important } """,
    unsafe_allow_html=True,
)

###############################################################################

