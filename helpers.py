import dash_html_components as html
import dash_bootstrap_components as bt

from dataset import df


def create_card(content, title=None, description=None):
    children = []
    if title:
        children.append(html.H2(title))
    children.append(content)
    if description:
        children.append(html.P(description))
    return html.Div(
        children,
        className="withShadow",
        style={
            "padding": "15px",
            "margin-top": "15px",
            "margin-bottom": "15px",
            "border-radius": "5px",
            "z-index": "1",
            "background": "white",
        },
    )


def build_counters(country_code=None, input_df=None):
    country_name = None
    counters_df = df if input_df is None else input_df

    if country_code:
        counters_df = counters_df[counters_df.country_code == country_code]
        country_name = counters_df.country.iloc[0]

    n_portals = counters_df._id.count()
    n_agents = counters_df.agent.dropna().nunique()
    n_cities = counters_df.ct.dropna().nunique()
    n_countries = (
        counters_df.country.dropna().nunique() if not country_code else country_name
    )
    countries_desc = "Countries" if not country_code else "Country"

    return [
        bt.Col(create_card(None, title=n_countries, description=countries_desc)),
        bt.Col(create_card(None, title=n_cities, description="Cities")),
        bt.Col(create_card(None, title=n_portals, description="Portals")),
        bt.Col(create_card(None, title=n_agents, description="Agents")),
    ]
