import dash
import dash_core_components as dcc
import dash_bootstrap_components as bt

import plotly.express as px

from app import app
from helpers import build_counters
from helpers import create_card
from dataset import df
from dataset import countries_geojson


portals_by_country = (
    df.groupby(["country", "country_code"])
    ._id.count()
    .reset_index()
    .rename({"_id": "portals"}, axis=1)
)

ch_map = px.choropleth_mapbox(
    portals_by_country,
    geojson=countries_geojson,
    locations="country_code",
    color="portals",
    featureidkey="properties.iso_a2",
    color_continuous_scale="Viridis",
    opacity=0.5,
    hover_name="country",
    zoom=2,
    template=app.config.PLOTLY_THEME,
)
ch_map.update_layout(mapbox_style="light", mapbox_accesstoken=app.config.MB_TOKEN)
ch_map.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

countries_layout = bt.Container(
    [
        bt.Row(id="counters_row"),
        bt.Row(
            bt.Col(
                create_card(
                    dcc.Graph(figure=ch_map, id="ch_map"), title="Portals By Country"
                ),
            )
        ),
        bt.Row(
            [
                bt.Col(create_card(dcc.Graph(id="teams_pie_graph"), title="Teams",)),
                bt.Col(
                    create_card(
                        dcc.Graph(id="agents_bar_graph"), title="Top 10 Agents",
                    )
                ),
                bt.Col(
                    create_card(
                        dcc.Graph(id="cities_bar_graph"), title="Top 10 Cities",
                    )
                ),
            ]
        ),
    ],
    style={"height": "100%", "max-width": "90%"},
)


@app.callback(
    [
        dash.dependencies.Output("teams_pie_graph", "figure"),
        dash.dependencies.Output("agents_bar_graph", "figure"),
        dash.dependencies.Output("cities_bar_graph", "figure"),
        dash.dependencies.Output("counters_row", "children"),
    ],
    [dash.dependencies.Input("ch_map", "clickData")],
)
def country_selected(selected_country):
    trg = dash.callback_context.triggered
    trg_value = trg[0]["value"]
    zone_name = trg_value["points"][0]["location"] if trg_value else "RU"

    zone_df = df[df.country_code == zone_name]

    teams_df = (
        zone_df.team.value_counts()
        .reset_index()
        .rename({"index": "team", "team": "portals"}, axis=1)
    )
    teams_pie = px.pie(
        teams_df,
        values="portals",
        labels="team",
        names="team",
        color="team",
        color_discrete_map=app.config.TEAMS_COLORS,
        hole=0.3,
        template=app.config.PLOTLY_THEME,
    )
    teams_pie.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

    agents_df = (
        zone_df.agent.replace("unknown", None)
        .dropna()
        .value_counts()
        .sort_values(ascending=True)
        .tail(10)
        .reset_index()
        .rename({"index": "agent", "agent": "count"}, axis=1)
    )
    agents_bar = px.bar(
        agents_df,
        x="count",
        y="agent",
        orientation="h",
        template=app.config.PLOTLY_THEME,
    )
    agents_bar.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

    cvt_df = (
        zone_df.ct.dropna()
        .value_counts()
        .sort_values(ascending=True)
        .tail(10)
        .reset_index()
        .rename({"index": "City", "ct": "Count"}, axis=1)
    )

    cvt_bar = px.bar(
        cvt_df, x="Count", y="City", orientation="h", template=app.config.PLOTLY_THEME,
    )
    cvt_bar.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

    return teams_pie, agents_bar, cvt_bar, build_counters(country_code=zone_name)
