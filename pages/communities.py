import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as bt
import plotly.express as px

from app import app
from helpers import create_card
from dataset import df


cities_df = (
    df.groupby(["country", "ct"])
    ._id.count()
    .reset_index()
    .sort_values("_id", ascending=False)
    .rename({"_id": "portals"}, axis=1)
)


cutoff_marks = {i: str(i) for i in range(101)}
communities_layout = bt.Container(
    [
        bt.Row(
            [
                bt.Col(
                    create_card(
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.Span(id="cutoff_slider_label"),
                                        dcc.Slider(
                                            id="cutoff_slider",
                                            min=1,
                                            max=50,
                                            marks=cutoff_marks,
                                            step=1,
                                            value=1,
                                        ),
                                    ],
                                    className="filterBlock",
                                ),
                                dcc.Graph(id="cities_sunburst_graph"),
                            ]
                        ),
                        title="Countries & Cities",
                    ),
                ),
            ]
        ),
    ],
    style={"height": "100%", "max-width": "90%"},
)


@app.callback(
    dash.dependencies.Output("cities_sunburst_graph", "figure"),
    [dash.dependencies.Input("cutoff_slider", "value")],
)
def cutoff_updated(cutoff_value):
    cutoff_df = cities_df[cities_df.portals >= cutoff_value]
    cities_fig = px.sunburst(
        cutoff_df,
        path=["country", "ct"],
        values="portals",
        template=app.config.PLOTLY_THEME,
        color="portals",
        color_continuous_scale="viridis",
        height=1000,
    )
    cities_fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return cities_fig
