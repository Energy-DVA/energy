from dash import dcc, html
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

from utils.constants import COUNTIES
from components.base_map import draw_base_map
from components.cards import (
    production_card,
    active_card,
    counties_card,
    operators_card,
)

from pages.explore.explore_controller import (
    update_map,
    update_plot,
    update_slider_values,
    filter_based_on_input,
)


# Define Map Configuration
map_config = {
    "displayModeBar": True,
    "displaylogo": False,
    "scrollZoom": True,
    "modeBarButtonsToAdd": ["select2d", "lasso2d"],
}

# Define sidebar layout
sidebar = dbc.Row(
    [
        dbc.Col(production_card, width=2),
        dbc.Col(counties_card, width=2),
        dbc.Col(operators_card, width=2),
        dbc.Col(active_card),
    ],
)


# Define page-content Layout

map_type_selection = dcc.Dropdown(
    id="map_type",
    options=[
        {"label": "Kansas Counties Outlines", "value": "Counties"},
        {"label": "Scatter Plot of Individual Leases", "value": "Scatter Plot"},
        {"label": "Density Heatmap of Leases", "value": "Heat Map"},
    ],
    value="Counties",
)


layout = [
    html.Br(),
    dbc.CardGroup(
        [
            dbc.Card(
                [
                    dbc.CardHeader("Kansas State Map"),
                    dbc.CardBody(
                        [
                            dbc.Row(
                                [
                                    dbc.Col(
                                        "Select Chart Type:",
                                        width="auto",
                                        style={
                                            "padding-top": "0.5%",
                                            "padding-right": "0.5%",
                                        },
                                    ),
                                    dbc.Col(map_type_selection, width=5),
                                ]
                            ),
                            dbc.Row(
                                dcc.Loading(
                                    dcc.Graph(
                                        id="map",
                                        figure=draw_base_map(),
                                        config=map_config,
                                        style={"padding-top": "1%"},
                                    ),
                                    id="loading-1",
                                    type="default",
                                )
                            ),
                        ]
                    ),
                ]
            ),
            dbc.Card(
                [
                    dbc.CardHeader("Historical Production Plots"),
                    dbc.CardBody(
                        dcc.Loading(
                            dcc.Graph(
                                id="plot",
                                figure=go.Figure(),
                                style={"padding-top": "3%"},
                            ),
                            id="loading-1",
                            type="default",
                        ),
                    ),
                ],
            ),
        ]
    ),
    html.Br(),
    dbc.CardGroup(
        [
            dbc.Card(
                [
                    dbc.CardHeader("Kansas State Map"),
                    dbc.CardBody(
                        [
                            dbc.Row(
                                dcc.Loading(
                                    dcc.Graph(
                                        id="dfadfadfadf",
                                        figure=draw_base_map(),
                                        config=map_config,
                                        style={"padding-top": "1%"},
                                    ),
                                    id="loading-1",
                                    type="default",
                                )
                            ),
                        ]
                    ),
                ]
            ),
            dbc.Card(
                [
                    dbc.CardHeader("Historical Production Plots"),
                    dbc.CardBody(
                        dcc.Loading(
                            dcc.Graph(
                                id="yutitusdsdf",
                                figure=go.Figure(),
                                style={"padding-top": "3%"},
                            ),
                            id="loading-1",
                            type="default",
                        ),
                    ),
                ],
            ),
        ]
    ),
]
