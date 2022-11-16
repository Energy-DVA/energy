from dash import dcc, html
import dash_bootstrap_components as dbc

from utils.constants import COUNTIES

# Declare cards for UI
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
                    inline=True
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
                                    1930,
                                    2022,
                                    step=1,
                                    id="year-slider",
                                    value=[1991, 2022],
                                    marks={str(year): str(year) for year in range(1930, 2022, 10)},
                                    tooltip={"placement": "bottom", "always_visible": True},
                                    pushable=5,
                                ),
                            ],
                        ),
                        dbc.Col(
                            [
                                dbc.Input(
                                    type="number",
                                    min=1930,
                                    max=2022,
                                    id="activity-from",
                                    size="sm",
                                    value=1991,
                                    debounce=True,
                                    minlength=4,
                                    maxlength=4,
                                ),
                                dbc.FormText("Year from"),
                            ],
                            width=2
                        ),
                        dbc.Col(
                            [
                                dbc.Input(
                                    type="number",
                                    min=1930,
                                    max=2022,
                                    id="activity-to",
                                    size="sm",
                                    value=2022,
                                    debounce=True,
                                    minlength=4,
                                    maxlength=4,
                                ),
                                dbc.FormText("Year from"),
                            ],
                            width=2
                        ),
                    ]
                )
            ],
            className='sidebar-card'
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
            className='sidebar-card'
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
            className='sidebar-card'
        ),
    ],
)
