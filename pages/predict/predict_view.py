from dash import dcc, html
import dash_bootstrap_components as dbc

from utils.constants import COUNTIES
from components.cards import (
    production_radio_card,
    predict_instructions_card,
    predict_forecast_wells_card,
    predict_execute_card,
)

from pages.predict.predict_controller import (
    update_predict_plot,
    update_user_input_to_textbox,
)

sidebar = dbc.Row(
    [
        dbc.Col(predict_instructions_card, width=3),
        dbc.Col(production_radio_card, width=1),
        dbc.Col(predict_forecast_wells_card),
        dbc.Col([predict_execute_card, dbc.FormText("Try me!")], width="auto"),
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
                            children="No Selection Made",
                            id="toast-hist-prod",
                            header="Cumulative Historical Production",
                            icon="primary",
                            dismissable=False,
                            is_open=True,
                            class_name="toast-body",
                            header_class_name="toast-header",
                        ),
                    ),
                    html.Br(),
                    dbc.Row(
                        dbc.Toast(
                            children="No Selection Made",
                            id="toast-hist-wells",
                            header="Average Historical Well Count",
                            icon="dark",
                            dismissable=False,
                            is_open=True,
                            class_name="toast-body",
                            header_class_name="toast-header",
                        ),
                    ),
                    html.Br(),
                    dbc.Row(
                        dbc.Toast(
                            children="No Selection Made",
                            id="toast-fore-prod",
                            header="Cumulative Forecast Production",
                            icon="primary",
                            dismissable=False,
                            is_open=True,
                            class_name="toast-body",
                            header_class_name="toast-header",
                        ),
                    ),
                    html.Br(),
                    dbc.Row(
                        dbc.Toast(
                            children="No Selection Made",
                            id="toast-fore-wells",
                            header="Average Forecast Well Count",
                            icon="secondary",
                            dismissable=False,
                            is_open=True,
                            class_name="toast-body",
                            header_class_name="toast-header",
                        ),
                    ),
                ],
                width="auto",
            ),
        ]
    ),
    dbc.Tooltip(
        [
            html.P("HOW IT WORKS"),
            html.Hr(), 
            html.P("You can configure the number of wells and how long you want to forecast production from those wells. By constructing the array, you can control how you want the forecast to be done."),
            html.P("For example: If the array is [(wells, months),(1000,12),(500,4)], the forecaster will forecast production from 1000 wells for 12 months, following with 500 wells for another 4 months."),
            html.P("Construct the array by iteratively inputting number of wells and time period (months) and appending to the array. View the array in the textbox"),
            html.P("You can reset the array by using the Clear button")
        ],
        id="hovertip-forecast",
        target="tooltip-forecast-button",
        trigger='hover',
        placement='left',
    )
]
