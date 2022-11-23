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
    predict_instructions_card,
    predict_forecast_time_card,
    predict_forecast_wells_card,
    predict_execute_card,
)

from pages.predict.predict_controller import (
    update_predict_plot,
)

sidebar = dbc.Row(
    [
        dbc.Col(predict_instructions_card, width=3),
        dbc.Col(production_radio_card, width=1),
        #dbc.Col(predict_forecast_time_card, width=1),
        dbc.Col(predict_forecast_wells_card, width='auto'),
        dbc.Col(
            [
                predict_execute_card,
                dbc.FormText("Try me!")
            ],
            width='auto'),
    ],
)


layout = [
    html.Br(),
    dbc.Row(
        [
            dbc.Col(
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
                width=9,
            ),
            dbc.Col(
                [
                    dbc.Row(
                        dbc.Toast(
                            [
                                html.P("This is the content of the toast", className="mb-0")
                            ],
                            id="simple-toast",
                            header="This is the header",
                            icon="primary",
                            dismissable=False,
                            is_open=True,
                        ),
                    ),
                    html.Br(),
                    dbc.Row(
                        dbc.Toast(
                            [
                                html.P("This is the content of the toast", className="mb-0")
                            ],
                            id="siadfa",
                            header="This is the header",
                            icon="primary",
                            dismissable=False,
                            is_open=True,
                        ),
                    ),
                    html.Br(),
                    dbc.Row(
                        dbc.Toast(
                            [
                                html.P("This is the content of the toast", className="mb-0")
                            ],
                            id="simadfast",
                            header="This is the header",
                            icon="primary",
                            dismissable=False,
                            is_open=True,
                        ),
                    ),
                ],
            )
        ]
    ),
]
