from dash import dcc, html
import dash_bootstrap_components as dbc

tabs = html.Div(
    [
        dcc.Tabs(
            parent_className="custom-tabs",
            className="custom-tabs-container",
            id="tabs-container",
            value="page_explore",
            children=[
                dcc.Tab(
                    label='EXPLORE',
                    value="page_explore",
                    id="page-explore",
                    className="custom-tab",
                    selected_className="custom-tab--selected",
                ),
                dcc.Tab(
                    label="PREDICT",
                    value="page_predict",
                    id="page-predict",
                    className="custom-tab",
                    selected_className="custom-tab--selected",
                ),
            ],
        ),
        dbc.Tooltip(
            [
                html.I(className="bi bi-exclamation-octagon-fill"), 
                "\tEnsure all figures have finished loading before proceeding! This ensures all data has been loaded successfully"
            ],
            id="predict-tooltip",
            target="page-predict",
            trigger='hover',
            placement='left',
        )
    ]
)
