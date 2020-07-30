from environs import Env
import dash_bootstrap_components as bt
from plotly.colors import DEFAULT_PLOTLY_COLORS

env = Env()
env.read_env()


# themes and colors
PLOTLY_THEME = "simple_white"
BOOTSTRAP_THEME = bt.themes.MINTY
TEAMS_COLORS = {
    "ALIENS": DEFAULT_PLOTLY_COLORS[2],
    "RESISTANCE": DEFAULT_PLOTLY_COLORS[0],
    "MISSING": DEFAULT_PLOTLY_COLORS[3],
    "NEUTRAL": DEFAULT_PLOTLY_COLORS[4],
}


# tokens
MB_TOKEN = env.str("MAPBOX_TOKEN")

# datasets
DATASET_PATH = env.str("DATASET_PATH", "data/portals_1k_addr_formatted.csv")
DATASET_DATES = env.list("DATASET_DATES", ["timestamp", "updated"])
COUNTRIES_GEOJSON_PATH = env.str("COUNTRIES_GEOJSON_PATH", "geojson/world_low_geo.json")

# graphs settings
TOP_LIMIT = 10
