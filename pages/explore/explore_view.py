from dash import dcc, html
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

from utils.constants import COUNTIES
from components.base_map import draw_base_map
from components.cards import production_card, active_card, counties_card, operators_card, map_type_card

# Define Map Configuration
map_config = {
    "displayModeBar": True,
    "displaylogo": False,
    "scrollZoom": True,
    "modeBarButtonsToAdd": ["select2d", "lasso2d"],
}

# Define sidebar layout
sidebar = [
    dbc.Row(
        [
            dbc.Col(production_card),
            dbc.Col(map_type_card),
        ]
    ),
    dbc.Row(
        [
            dbc.Col(counties_card),
            dbc.Col(operators_card),
        ]
    ),
    dbc.Row(active_card),
]


# Define page-content Layout
layout = [
    dcc.Loading(
        dcc.Graph(
            id="map",
            figure=draw_base_map(),
            config=map_config,
        ),
        id="loading-1",
        type="default",
    ),
    dcc.Loading(
        dcc.Graph(
            id="plot",
            figure=go.Figure(),
        ),
        id="loading-1",
        type="default",
    ),
]
