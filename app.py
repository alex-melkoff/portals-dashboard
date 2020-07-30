import dash
import flask
import dash_bootstrap_components as bt


app = dash.Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width"}],
    external_stylesheets=[bt.themes.MINTY],
)

tmp_app = flask.Flask(__name__)
tmp_app.config.from_object("settings")
app.config.update(tmp_app.config.items())
