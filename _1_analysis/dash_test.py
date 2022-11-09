import dash
import dash_bootstrap_components as dbc
import numpy as np
import pandas as pd
import geopandas as gpd
import geojson
import json
import plotly.graph_objects as go
from dash import Input, Output, dcc, html
import plotly.express as px
from sqlalchemy import create_engine, MetaData, or_, and_
from sqlalchemy import select, func 
from db_schema import OIL_PROD_TABLE, GAS_PROD_TABLE, LEASE_TABLE, WELLS_TABLE, TOPS_TABLE
from shapely.geometry import Point

###################--- Helper Functions ---############################

def log(stuff):
    app.logger.info(stuff)

def draw_base_map():
    fig = go.Figure()
    midpoint = (38.48470, -98.38020) # (Lat,Lon)
    # Add Counties shaders
    fig.add_trace(
        go.Choroplethmapbox(geojson=kansas_geojson, locations=kansas_state["GEOID"], z=kansas_state["LSAD"],
                            marker_opacity=0.5, marker_line_width=0,
                            colorscale="gray", zmin=0, zmax=9, showscale=False,
                            text=kansas_state["NAME"],
                            hovertemplate=
                                        "<b>County</b><br>" +
                                        "%{text}<br>" +
                                        "<extra></extra>"
        )
    )
    # Add counties borders
    fig.update_layout(
        mapbox={
            "style": "open-street-map",
            "zoom": 6,
            "layers": [
                {
                    "source": kansas_geojson,
                    "below": "traces",
                    "type": "line",
                    "color": "purple",
                    "line": {"width": 1.5},
                }
            ],
            #"bounds" : {"west": -180, "east": -50, "south": 20, "north": 90},
            "center" : {"lat": midpoint[0], "lon": midpoint[1]}
        },
        margin={"l": 0, "r": 5, "t": 0, "b": 0},
        mapbox_style="open-street-map",#"white-bg",
        autosize = True,
        #height = 600,
        #dragmode='lasso',
        newselection=dict(line=dict(color="Crimson",
                                    width=2,
                                    dash="dash")),
                                    
        modebar = {
            'orientation': 'h',
            'bgcolor': 'rgba(255,255,255,0.7)',
            'color': 'rgb(255,0,0)',
            'activecolor': 'rgb(100,0,200)',
        },
    )

    fig.update_geos(fitbounds="locations", visible=False)
    fig['layout']['uirevision'] = 'base'
    return fig

def develop_cards():

    production_card = dbc.Card(
        [
            dbc.CardHeader("Production Type"),
            dbc.CardBody(
                [
                    dcc.Dropdown(
                        id="commodity",
                        options=["All","Oil","Gas"],
                        value="All",
                    ),
                ]
            ),
        ],
        body=True
    )

    active_card = dbc.Card(
        [
            dbc.CardHeader("Activity"),
            dbc.CardBody(
                [
                    dcc.Dropdown(
                        id="activity",
                        options=["All","Active","Inactive"],
                        value="All",
                    ),
                ]
            ),
        ],
        body=True
    )

    counties_card = dbc.Card(
        [
            dbc.CardHeader("County"),
            dbc.CardBody(
                [
                    dcc.Dropdown(
                        id="county",
                        options=['All']+counties,
                        value="All",
                    ),
                ]
            ),
        ], 
        body=True
    )

    map_type_card = dbc.Card(
        [
            dbc.CardHeader("Lease Visualizations"),
            dbc.CardBody(
                [
                    dcc.RadioItems(
                        id="map_type",
                        options=[
                                    {'label': 'Individual Leases', 'value': 'Scatter Plot'},
                                    {'label': 'Density', 'value': 'Heat Map'}
                                ],
                        value='None',
                        labelStyle={'display': 'block', 'margin-top':'-5%'},
                        inputStyle={"margin-right": "5%", 'margin-top':'6%'},
                    ),
                ]
            ),
        ], 
        body=True
    )

    map_controls_card = dbc.Card(
        [
            dbc.CardHeader("Map Controls"),
            dbc.CardBody(
                [
                    dbc.Button("Reset View", color="primary", className="mt-auto", id='reset_view'),
                ]
            ),
        ], 
        body=True
    )

    controls = html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(map_controls_card),
                    dbc.Col(map_type_card),
                    dbc.Col(counties_card),
                    dbc.Col(production_card),
                    dbc.Col(active_card),
                ], className="g-10",
            ),
        ]
    )

    return controls

########################################################################

###################--- SETUP ---############################

# Setup SQL Engine
engine = create_engine("sqlite:///../../kansas_oil_gas.db")
meta = MetaData()
meta.reflect(bind=engine)
oil_prod = meta.tables[OIL_PROD_TABLE]
gas_prod = meta.tables[GAS_PROD_TABLE]
lease = meta.tables[LEASE_TABLE]
wells = meta.tables[WELLS_TABLE]
tops = meta.tables[TOPS_TABLE]

# Setup required information
kansas_state = gpd.read_file("Shapefiles/cb_2018_us_county_500k.shp")
kansas_state = kansas_state[kansas_state["STATEFP"]=='20'].reset_index(drop=True)
kansas_state['LSAD'] = kansas_state['LSAD'].astype(int)
with open('kansas_counties.geojson') as f:
    kansas_geojson = geojson.load(f)

# Setup app config, layout, and tokens
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
mapbox_access_token = "pk.eyJ1IjoiZ2VldGFraW5nbGUiLCJhIjoiY2w5dmxxc3JmMHJ6azNva2JzOHNoMGhxayJ9.qEl0L0gXzDHVYSkF1uvoSg"
s = select(
        [
            func.distinct(lease.c.COUNTY)
        ]
)
counties = sorted(list(pd.read_sql(s, engine)["distinct_1"]))

########################################################################


###################--- APP LAYOUT ---##################################
map_config = {
                'displayModeBar': True,
                'displaylogo': False,
                'scrollZoom': True,
            }

app.layout = dbc.Container(
    [
        html.H1("Kansas Production Forecast"),
        html.Hr(),
        develop_cards(),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Graph(id="map", figure=draw_base_map(), config=map_config)
                    ],
                    className='mb-10',
                ),
                dbc.Col(
                    [
                        dcc.Graph(id="plot", figure=draw_base_map(), config=map_config)
                    ],
                    className='mb-10',
                ),
            ],
            style={'margin-top':'1%'},
            align="top", 
            className="g-10",
        ),
    ],
    fluid=True,
)
######################################################################


###################--- CALLBACKS ---##################################

@app.callback(
    [
        Output("map", "figure"),
        Output("map_type", "value"),
    ],
    [
        Input("map_type", "value"),
        Input("commodity", "value"),
        Input("activity", "value"),
        Input("county", "value"),
        Input("reset_view", "n_clicks"),
    ],
    prevent_initial_call=True
)
def drawn_polygon(map_type, commodity, active, county, reset_view):

    if commodity == None:
        commodity = 'All'
    if active == None:
        active = 'All'
    if county == None:
        county = 'All'
    if map_type == None:
        map_type = 'None'

    if dash.callback_context.triggered_id == 'reset_view':
        map_type = 'None'

    # Draw base map
    fig = draw_base_map()
        
    # Retrieve Data
    s = select(
            [
                lease.c.LEASE_KID,
                lease.c.LATITUDE,
                lease.c.LONGITUDE,
                lease.c.PRODUCES,
                lease.c.YEAR_STOP,
            ]
    )
    if commodity != 'All':
        s = s.where(lease.c.PRODUCES == commodity.upper())
    # else select all

    if county != 'All':
        s = s.where(lease.c.COUNTY == county)
    # else select all

    if active == 'Active':
        s = s.where(lease.c.YEAR_STOP == '2022')
    elif active == 'Inactive':
        s = s.where(lease.c.YEAR_STOP != '2022')
    # else do all
    
    df = pd.read_sql(s, engine)
    if map_type == "Heat Map":
        fig.add_trace(
            go.Densitymapbox(
                lat=df['LATITUDE'],
                lon=df['LONGITUDE'],
                radius=2,
                showscale=False,
            )
        )
    elif map_type == "Scatter Plot":
        df_oil = df[df['PRODUCES']=='OIL']
        df_gas = df[df['PRODUCES']=='GAS']
        
        if commodity=='All' or commodity=='Oil':
            fig.add_trace(
                go.Scattermapbox(
                    lat=df_oil['LATITUDE'],
                    lon=df_oil['LONGITUDE'],
                    mode='markers',
                    marker=go.scattermapbox.Marker(
                        size=5,
                        color='rgb(0,0,200)',
                        opacity=0.25,
                    ),
                    text=df_oil['LEASE_KID'],
                    customdata=kansas_state['NAME'],
                    showlegend=True,
                    legendgroup="scatter",
                    name="Oil Leases",
                    hovertemplate=
                        "<b>County</b><br>" +
                        "%{customdata}<br>" +
                        "<extra></extra>"
                )
            )

        if commodity=='All' or commodity=='Gas':
            fig.add_trace(
                go.Scattermapbox(
                    lat=df_gas['LATITUDE'],
                    lon=df_gas['LONGITUDE'],
                    mode='markers',
                    marker=go.scattermapbox.Marker(
                        size=5,
                        color='rgb(0,200,0)',
                        opacity=0.25,
                    ),
                    text=df_gas['LEASE_KID'],
                    customdata=kansas_state['NAME'],
                    showlegend=True,
                    legendgroup="scatter",
                    name="Gas Leases",
                    hovertemplate=
                        "<b>County</b><br>" +
                        "%{customdata}<br>" +
                        "<extra></extra>"
                )
            )
    # else select None map


    fig.update_layout(legend=dict(
        yanchor="top",
        y=0.99,
        xanchor="left",
        x=0.01
    ))

    fig['layout']['uirevision'] = 'base'
    
    return fig,map_type


# @app.callback(
#     Output('Coordinates', 'children'),
#     Input('Map', 'relayoutData'))
# def display_relayout_data(relayoutData):
#     try:
#         coords = relayoutData['mapbox._derived']['coordinates']
#         lon_min = coords[0][0]
#         lon_max = coords[1][0]
#         lat_min = coords[2][1]
#         lat_max = coords[1][1]
        
#         print(f'Min Lat: {lat_min}, Max Lat: {lat_max}, Min Lon:{lon_min}, Max Lon: {lon_max}')
#         return [lat_min, lat_max, lon_min, lon_max]
#     except:
#         return []     


######################################################################



###################--- START APP ---##################################
if __name__ == "__main__":
    app.run_server(debug=True, port=8888)