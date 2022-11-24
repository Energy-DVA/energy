from dash import dcc, html
import dash_bootstrap_components as dbc

from utils.constants import COUNTIES, YEARS_RANGE

# Declare cards for UI
logo_card = dbc.Card(
    [
        dbc.CardImg(src="/assets/dva_team_logo.png", top=True),
    ],
    style={
        "height": "10vh",
        "padding-top": "10%",
        "padding-left": "10%",
        "border": "0",
    },
)

instructions = [
    html.P("Use 'Explore' tab to make selections of data"),
    html.P("Fill forecast inputs required on the right"),
]
predict_instructions_card = dbc.Card(
    [
        dbc.CardHeader("Instructions"),
        dbc.CardBody(html.Ol([html.Li(i) for i in instructions])),
    ],
)


production_radio_card = dbc.Card(
    [
        dbc.CardHeader("Pick:"),
        dbc.CardBody(
            [
                dcc.RadioItems(
                    id="commodity-radio",
                    options=["Oil", "Gas"],
                    value=None,
                    labelClassName="card-labels",
                    inputClassName="card-inputs",
                    inline=False,
                ),
            ],
        ),
    ],
)

predict_forecast_time_card = dbc.Card(
    [
        dbc.CardHeader("Input:"),
        dbc.CardBody(
            [
                dbc.Input(
                    type="number",
                    min=0,
                    id="predict-months",
                    size="sm",
                    value=None,
                    debounce=True,
                ),
                dbc.FormText("Months to Forecast"),
            ],
        ),
    ],
)

predict_forecast_wells_card = dbc.Card(
    [
        dbc.CardHeader(
            [
                "Construct Wells Array:", 
                html.I(className="bi bi-info-circle-fill",
                       id="tooltip-forecast-button",
                       style={'margin-left':'0.5vw'})
            ]
        ),
        dbc.CardBody(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                dbc.Input(
                                    type="number",
                                    min=0,
                                    id="predict-wells",
                                    size="sm",
                                    value=None,
                                    debounce=True,
                                ),
                                dbc.FormText("Input num. of wells..."),
                            ],
                            width=3,
                        ),
                        dbc.Col(
                            [
                                dbc.Input(
                                    type="number",
                                    min=0,
                                    id="predict-wells-month",
                                    size="sm",
                                    value=None,
                                    debounce=True,
                                ),
                                dbc.FormText("for a period (months) of..."),
                            ],
                            width=3,
                        ),
                        dbc.Col(
                            [
                                dbc.Button(
                                    id="wells-submit-button",
                                    n_clicks=0,
                                    children="Append \u21a6",
                                    size="sm",
                                    color="secondary",
                                ),
                                html.Br(),
                                dbc.FormText("and append..."),
                            ],
                            width="auto",
                        ),
                        dbc.Col(
                            [
                                dbc.Textarea(
                                    id="forecast-well-input",
                                    value="Number of Wells, Months",
                                    disabled=True,
                                    className="text-area",
                                    style={
                                        "padding-left": "0.75vw",
                                    },
                                ),
                                dbc.FormText("to create array of input pairs"),
                            ],
                        ),
                        dbc.Col(
                            [
                                dbc.Button(
                                    id="clear-input-button",
                                    n_clicks=0,
                                    children="\u21a4 Clear",
                                    size="sm",
                                    color="secondary",
                                ),
                            ],
                            width="auto",
                        ),
                    ]
                ),
            ],
        ),
    ],
)

predict_execute_card = dbc.Card(
    [
        dbc.CardHeader("Execute:"),
        dbc.CardBody(
            [
                dbc.Button(
                    id="forecast-execute-button",
                    n_clicks=None,
                    children="FORECAST",
                    size="sm",
                    color="primary",
                )
            ],
        ),
    ],
)


production_card = dbc.Card(
    [
        dbc.CardHeader("Production Type"),
        dbc.CardBody(
            [
                dcc.Checklist(
                    id="commodity",
                    options=["Oil", "Gas"],
                    value=[],
                    labelClassName="card-labels",
                    inputClassName="card-inputs",
                    inline=True,
                ),
            ],
        ),
    ],
)

active_card = dbc.Card(
    [
        dbc.CardHeader("Select Years of Activity"),
        dbc.CardBody(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                dcc.RangeSlider(
                                    YEARS_RANGE[0],
                                    YEARS_RANGE[1],
                                    step=1,
                                    id="year-slider",
                                    value=[1991, YEARS_RANGE[1]],
                                    marks={
                                        str(year): str(year)
                                        for year in range(
                                            YEARS_RANGE[0], YEARS_RANGE[1], 10
                                        )
                                    },
                                    tooltip={
                                        "placement": "bottom",
                                        "always_visible": True,
                                    },
                                    pushable=1,
                                ),
                            ],
                        ),
                        dbc.Col(
                            [
                                dbc.Input(
                                    type="number",
                                    min=YEARS_RANGE[0],
                                    max=YEARS_RANGE[1],
                                    id="activity-from",
                                    size="sm",
                                    value=1991,
                                    debounce=True,
                                    minlength=4,
                                    maxlength=4,
                                ),
                                dbc.FormText("Year from"),
                            ],
                            width=2,
                        ),
                        dbc.Col(
                            [
                                dbc.Input(
                                    type="number",
                                    min=YEARS_RANGE[0],
                                    max=YEARS_RANGE[1],
                                    id="activity-to",
                                    size="sm",
                                    value=YEARS_RANGE[1],
                                    debounce=True,
                                    minlength=4,
                                    maxlength=4,
                                ),
                                dbc.FormText("Year from"),
                            ],
                            width=2,
                        ),
                    ]
                )
            ],
            className="sidebar-card",
        ),
    ],
)

counties_card = dbc.Card(
    [
        dbc.CardHeader("County"),
        dbc.CardBody(
            [
                dcc.Dropdown(
                    id="county",
                    options=["All"] + COUNTIES,
                    value=["All"],
                    multi=True,
                    searchable=True,
                ),
            ],
            className="sidebar-card",
        ),
    ],
)

operators_card = dbc.Card(
    [
        dbc.CardHeader("Operators"),
        dbc.CardBody(
            [
                dcc.Dropdown(
                    id="operators",
                    options=["All", "X", "Y", "Z"],
                    value=["All"],
                    multi=True,
                    searchable=True,
                ),
            ],
            className="sidebar-card",
        ),
    ],
)
