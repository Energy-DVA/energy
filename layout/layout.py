from dash import dcc, html
import dash_bootstrap_components as dbc

from layout.tabs.tabs import tabs

content = html.Div(id="page-content")
sidebar = html.Div(id="sidebar")

title = html.H1("Kansas Production Forecast")

SIDEBAR_WIDTH = 3

sidebar_style = {"position": "fixed", "background-color": "#f8f9fa", "display": "block"}
content_style = {"display": "block"}

layout = html.Div(
    [
        title,
        html.Hr(),
        tabs,
        dbc.Container(
            [
                dbc.Row(
                    [
                        dbc.Col(sidebar, style=sidebar_style, className="mb-10"),
                        dbc.Col(content, style=content_style, className="mb-10"),
                    ],
                    className="g-0",
                ),
            ],
        ),
    ]
)
