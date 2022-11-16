from dash import dcc, html
import dash_bootstrap_components as dbc

from layout.tabs.tabs import tabs

SIDEBAR_WIDTH = 4


title = html.H1("Kansas Production Forecast", id='website-title')
sidebar = html.Div(id="sidebar")
content = html.Div(id="page-content")


# sidebar_style = {'display': 'inline-block', "position": "fixed", "background-color": "#f8f9fa"}
# content_style = {'display': 'inline-block', 'vertical-align': 'top', 'margin-left': f'{OFFSET_VW}vw'}

layout = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(title, width='auto'),
                dbc.Col(tabs),
            ],
            id='header'
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
