from dash import dcc, html
import dash_bootstrap_components as dbc

from layout.tabs.tabs import tabs

SIDEBAR_WIDTH = 4


title = html.H1("Kansas Production Forecast")
sidebar = html.Div(id="sidebar")
content = html.Div(id="page-content")


# sidebar_style = {'display': 'inline-block', "position": "fixed", "background-color": "#f8f9fa"}
# content_style = {'display': 'inline-block', 'vertical-align': 'top', 'margin-left': f'{OFFSET_VW}vw'}

layout = html.Div(
    [
        title,
        html.Hr(),
        tabs,
        dbc.Container(
            [
                dbc.Col(sidebar, className='sidebar-layout'),
                dbc.Col(content, className='content-layout'),
            ],
            fluid=True
        ),
    ]
)
