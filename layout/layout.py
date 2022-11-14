from dash import dcc, html
import dash_bootstrap_components as dbc

from layout.tabs.tabs import tabs

content = html.Div(id="page-content")

title = html.H1("Kansas Production Forecast")

layout = html.Div([title, html.Hr(), tabs, content])
