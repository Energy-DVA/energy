import dash
import dash_bootstrap_components as dbc

# from utils.external_assets import FONT_AWSOME, CUSTOM_STYLE
from layout.layout import layout


app = dash.Dash(
    __name__,
    suppress_callback_exceptions=False,
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        # Add more sheets and place in utils.external_assets
    ],
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)

app.layout = layout
