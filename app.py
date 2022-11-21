import dash
import dash_bootstrap_components as dbc

from layout.layout import layout


app = dash.Dash(
    __name__,
    suppress_callback_exceptions=True,
    external_stylesheets=[dbc.themes.COSMO],
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)

app.layout = layout

#COSMO, LUX, JOURNAL, FLATLY