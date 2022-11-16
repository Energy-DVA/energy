from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

from app import app

from pages.explore import explore_view
from pages.predict import predict_view


@app.callback(
    Output("sidebar", "children"),
    Output("page-content", "children"),
    Input("tabs-container", "value"),
)
def render_page_content(tabvalue):
    if tabvalue == "page_explore":
        return (
            explore_view.sidebar,
            explore_view.layout,
        )
    elif tabvalue == "page_predict":
        return (
            predict_view.sidebar,
            predict_view.layout,
        )
    # elif tabvalue == 'page_compare':
    #     return iris.layout
    else:
        return "adfadfadfadfadfadfadf", "ERROR"
