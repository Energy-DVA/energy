from dash import dcc, html
import dash_bootstrap_components as dbc

from layout.tabs.tabs import tabs

title = html.H1("Kansas Production Forecast")
sidebar = html.Div(id="sidebar")
content = html.Div(id="page-content")

layout = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(title, width='auto', className='website-title'),
                dbc.Col(tabs),
            ],
        ),
        dbc.Container(
            [
                dbc.Row(sidebar, className="sidebar-layout"),
                dbc.Row(content, className="content-layout"),
            ],
            id='page-body',
            fluid=True,
        ),
    ],
    className="dbc"
)
