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
        dbc.Col(production_card,width=2),
        dbc.Col(counties_card,width=2),
        dbc.Col(operators_card,width=2),
        dbc.Col(active_card),
    ],
)


# Define page-content Layout

map_type_selection = dcc.Dropdown(
                        id="map_type",
                        options=[
                            {"label": "Counties Only", "value": "Counties"},
                            {"label": "Individual Leases", "value": "Scatter Plot"},
                            {"label": "Density", "value": "Heat Map"},
                        ],
                        value="Counties",
                    )

layout = dbc.Row(
    [
        dbc.Col(
            [   
                map_type_selection,
                dcc.Loading(
                    dcc.Graph(
                        id="map",
                        figure=draw_base_map(),
                        config=map_config,
                    ),
                    id="loading-1",
                    type="default",
                ),
            ]
        ),
        dbc.Col(
            dcc.Loading(
                dcc.Graph(
                    id="plot",
                    figure=go.Figure(),
                ),
                id="loading-1",
                type="default",
            )
        ),
    ]
)
