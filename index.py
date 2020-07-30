import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as bt

from app import app

from pages import activity_layout
from pages import countries_layout
from pages import communities_layout


page_content = html.Div(id="page_content", style={"width": "100%", "height": "100%"})
location_url = dcc.Location(id="url", refresh=False)

navigation = bt.NavbarSimple(
    children=[
        bt.NavItem(bt.NavLink("Activity", href="/activity")),
        bt.NavItem(bt.NavLink("Countries", href="/countries")),
        bt.NavItem(bt.NavLink("Communities", href="/communities")),
    ],
    brand="Portals",
    brand_href="#",
    color="primary",
    dark=True,
)


app.layout = html.Div(
    [location_url, navigation, page_content], style={"height": "100%", "width": "100%"}
)

app.validation_layout = html.Div(
    [
        location_url,
        navigation,
        page_content,
        activity_layout,
        countries_layout,
        communities_layout,
    ]
)


@app.callback(
    dash.dependencies.Output("page_content", "children"),
    [dash.dependencies.Input("url", "pathname")],
)
def display_page(pathname):
    if pathname == "/activity":
        return activity_layout
    elif pathname == "/countries":
        return countries_layout
    elif pathname == "/communities":
        return communities_layout


server = app.server


if __name__ == "__main__":
    app.run_server(host="0.0.0.0", debug=True)
