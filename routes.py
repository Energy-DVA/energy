from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

from app import app


from pages.explore import explore_view

# from pages.gdp import gdp
# from pages.iris import iris


@app.callback(Output("page-content", "children"), [Input("tabs-container", "value")])
def render_page_content(tabvalue):
    if tabvalue == "page_explore":
        return explore_view.layout
    # elif tabvalue == 'page_predict':
    #     return gdp.layout
    # elif tabvalue == 'page_compare':
    #     return iris.layout
    else:
        return "ERROR"
