from dash import dcc, html
import dash_bootstrap_components as dbc

from layout.tabs.tabs import tabs
from components.cards import logo_card

title = html.H1("Kansas Production Forecast")
sidebar = html.Div(id="sidebar")
content = html.Div(id="page-content")

layout = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(logo_card, width=1),
                dbc.Col(title, width="auto", className="website-title"),
                dbc.Col(tabs),
            ],
        ),
        dbc.Container(
            [
                dbc.Row(sidebar, className="sidebar-layout"),
                dbc.Row(content, className="content-layout"),
            ],
            id="page-body",
            fluid=True,
        ),
    ],
    className="dbc",
)
