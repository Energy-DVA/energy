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
                    value=["Oil", "Gas"],
                    labelClassName='card-labels',
                    inputClassName='card-inputs',
                ),
            ]
        ),
    ],
    body=True,
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
                                "Year from:",
                                dbc.Input(
                                    type="number",
                                    min=1930,
                                    max=2022,
                                    id="activity-from",
                                    size="sm",
                                    value=1991,
                                    debounce=True,
                                ),
                            ]
                        ),
                        dbc.Col(
                            [
                                "Year to:",
                                dbc.Input(
                                    type="number",
                                    min=1930,
                                    max=2022,
                                    id="activity-to",
                                    size="sm",
                                    value=2022,
                                    debounce=True,
                                ),
                            ]
                        ),
                    ]
                ),
                html.Br(),
                dcc.RangeSlider(
                    1930,
                    2022,
                    step=1,
                    id="year-slider",
                    value=[1991, 2022],
                    marks={str(year): str(year) for year in range(1930, 2022, 15)},
                    tooltip={"placement": "bottom", "always_visible": True},
                    pushable=5,
                ),
            ]
        ),
    ],
    body=True,
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
            ]
        ),
    ],
    body=True,
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
            ]
        ),
    ],
    body=True,
)

map_type_card = dbc.Card(
    [
        dbc.CardHeader("Lease Visualizations"),
        dbc.CardBody(
            [
                dcc.RadioItems(
                    id="map_type",
                    options=[
                        {"label": "Counties Only", "value": "Counties"},
                        {"label": "Individual Leases", "value": "Scatter Plot"},
                        {"label": "Density", "value": "Heat Map"},
                    ],
                    value="Counties",
                    labelClassName='card-labels',
                    inputClassName='card-inputs',
                ),
            ]
        ),
    ],
    body=True,
)
