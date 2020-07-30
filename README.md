# Portals Dashboard

Interactive dashboard to explore geospatial data from [xgress.com](https://xgress.com). Try live version [here](https://portals-dashboard.herokuapp.com). A small sample of 1k records is provided for demonstration purposes.

This dashboard was built using `dash`, `plotly`, and `pandas`.

## Run Locally

This dashboard requires a free API token from [Mapbox](https://mapbox.com)

```
export MAPBOX_TOKEN=<get_free_token_from_mapbox>
```

Install requirements using pip
```
pip install -r requirements.txt
```

Run development server
```
python index.py
```

