from dash import dcc, html
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

from utils.constants import COUNTIES
from components.cards import (
    production_card,
    active_card,
    counties_card,
    operators_card,
    production_radio_card,
)

from pages.predict.predict_controller import update_predict_plot

sidebar = dbc.Row(
    [
        dbc.Col(production_radio_card, width=2),
        dbc.Col(counties_card, width=2),
        dbc.Col(operators_card, width=2),
        dbc.Col(active_card),
    ],
)


layout = [
    html.Br(),
    dbc.CardGroup(
        [
            dbc.Card(
                [
                    dbc.CardHeader("Production Forecasting"),
                    dbc.CardBody(
                        [
                            dbc.Row(
                                dcc.Loading(
                                    dcc.Graph(
                                        id="predict-plot",
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
        ]
    ),
]
