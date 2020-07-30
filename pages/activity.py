import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as bt
import plotly.express as px

from app import app
from helpers import build_counters
from helpers import create_card
from dataset import df


min_date = df.updated.min()
max_date = df.updated.max()


activity_layout = bt.Container(
    [
        bt.Row(id="activity_counters_row"),
        bt.Row(
            [
                bt.Col(
                    [
                        create_card(
                            html.Div(
                                [
                                    html.Div(
                                        [
                                            html.Span("Date Range"),
                                            dcc.DatePickerRange(
                                                id="date_range_filter",
                                                min_date_allowed=min_date,
                                                max_date_allowed=max_date,
                                                start_date=min_date,
                                                end_date=max_date,
                                            ),
                                        ],
                                        className="widgetBlock",
                                    ),
                                    html.Div(
                                        [
                                            html.Span("Teams"),
                                            dcc.Checklist(
                                                options=[
                                                    {
                                                        "label": "Aliens",
                                                        "value": "ALIENS",
                                                    },
                                                    {
                                                        "label": "Missing",
                                                        "value": "MISSING",
                                                    },
                                                    {
                                                        "label": "Resistance",
                                                        "value": "RESISTANCE",
                                                    },
                                                    {
                                                        "label": "Neutral",
                                                        "value": "NEUTRAL",
                                                    },
                                                ],
                                                value=[
                                                    "ALIENS",
                                                    "MISSING",
                                                    "RESISTANCE",
                                                    "NEUTRAL",
                                                ],
                                                labelStyle={"display": "block"},
                                                id="teams_filter",
                                            ),
                                        ],
                                        className="widgetBlock",
                                    ),
                                ]
                            ),
                            title="Filters",
                        ),
                    ],
                    width=3,
                ),
                bt.Col(
                    create_card(
                        dcc.Graph(id="portals_map_graph"), title="Portals Map",
                    ),
                ),
            ]
        ),
        bt.Row(
            [
                bt.Col(
                    create_card(
                        dcc.Graph(id="portals_hist_graph"), title="Updated Portals",
                    )
                ),
            ]
        ),
    ],
    style={"height": "100%", "max-width": "90%"},
)


@app.callback(
    [
        dash.dependencies.Output("portals_map_graph", "figure"),
        dash.dependencies.Output("portals_hist_graph", "figure"),
        dash.dependencies.Output("activity_counters_row", "children"),
    ],
    [
        dash.dependencies.Input("date_range_filter", "start_date"),
        dash.dependencies.Input("date_range_filter", "end_date"),
        dash.dependencies.Input("teams_filter", "value"),
    ],
)
def filters_updated(start_date, end_date, checkbox_value):
    filtered_df = df[df.updated >= start_date]
    filtered_df = filtered_df[filtered_df.updated <= end_date]
    filtered_df = filtered_df[filtered_df.team.isin(checkbox_value)]

    portals_map = px.scatter_mapbox(
        filtered_df,
        lat="lat",
        lon="lon",
        color="team",
        color_discrete_map=app.config.TEAMS_COLORS,
        hover_data=["country", "ct", "name", "description"],
        zoom=2,
        template=app.config.PLOTLY_THEME,
    )
    portals_map.update_layout(
        mapbox_style="light", mapbox_accesstoken=app.config.MB_TOKEN
    )
    portals_map.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

    hist = px.histogram(
        filtered_df,
        x="updated",
        marginal="violin",
        histnorm="probability density",
        template=app.config.PLOTLY_THEME,
    )
    hist.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return portals_map, hist, build_counters(input_df=filtered_df)
