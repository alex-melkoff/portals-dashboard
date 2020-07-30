import json

import pandas as pd
from app import app


df = pd.read_csv(app.config.DATASET_PATH, parse_dates=app.config.DATASET_DATES)
with open(app.config.COUNTRIES_GEOJSON_PATH, "r", encoding="utf-8") as f:
    countries_geojson = json.load(f)
