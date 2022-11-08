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

    # fig = px.choropleth_mapbox(kansas_state, geojson=kansas_geojson, locations="GEOID", color="LSAD",
    #                             opacity=0.5, center={"lat": point[0], "lon": point[1]},
    #                             color_continuous_scale="gray", range_color=[0,8],
    #                             zoom = 6)
    # fig.update_layout(mapbox_style="light", mapbox_accesstoken=mapbox_access_token,
    #                 mapbox_zoom=3, mapbox_center = {"lat": 37.0902, "lon": -95.7129})
    # fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

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

    # fig = px.choropleth_mapbox(kansas_state, geojson=kansas_geojson, locations="GEOID", color="LSAD",
    #                             opacity=0.5, center={"lat": midpoint[0], "lon": midpoint[1]},
    #                             color_continuous_scale="gray", range_color=[0,8],
    #                             zoom = 6)

    # Add counties
    fig.update_layout(
        mapbox={
            "style": "open-street-map",
            "zoom": 6.25,
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
        margin={"l": 0, "r": 50, "t": 0, "b": 0},
        mapbox_style="open-street-map",#"white-bg",
        autosize = True,
        height = 600,
        dragmode='lasso',
        newselection=dict(line=dict(color="Crimson",
                                    width=2,
                                    dash="dash")),
    )

    fig.update_geos(fitbounds="locations", visible=False)
    
    return fig

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

production_card = dbc.Card(
    dbc.CardBody(
        [
            html.H5("Production Type", className="card-title"),
            dcc.Dropdown(
                id="commodity",
                options=["Oil","Gas"],
                value="Select",
            ),
        ]
    ), 
    body=True
)

active_card = dbc.Card(
    dbc.CardBody(
        [
            html.H5("Activity", className="card-title"),
            dcc.Dropdown(
                id="activity",
                options=["Active","Inactive"],
                value="Select",
            ),
        ]
    ), 
    body=True
)

counties_card = dbc.Card(
    dbc.CardBody(
        [
            html.H5("County", className="card-title"),
            dcc.Dropdown(
                id="county",
                options=['All']+counties,
                value="All",
            ),
        ]
    ), 
    body=True
)

controls = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(production_card, width=4),
                dbc.Col(active_card, width=4),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(counties_card, width=4),
            ]
        )
    ]
)

app.layout = dbc.Container(
    [
        html.H1("Kansas Production Forecast"),
        html.Hr(),
        dbc.Row(
            [
                dbc.Col(controls,md=4),
                dbc.Col(
                    [
                        dcc.RadioItems(
                            id="map_type",
                            options=['Scatter Plot', 'Heat Map'],
                            value='Heat Map'
                        ),
                        dcc.Graph(id="map", config=map_config)
                    ],
                md=8,
                ),
            ],
            align="top", 
            className="h-75",
        ),
    ],
    fluid=True,
)
######################################################################


###################--- CALLBACKS ---##################################

@app.callback(
    Output("map", "figure"),
    [
        Input("map_type", "value"),
        Input("commodity", "value"),
        Input("activity", "value"),
        Input("county", "value")
    ])
def drawn_polygon(map_type, commodity, active, county):
    # Draw basemap
    fig = draw_base_map()

    # Retrieve Data
    s = select(
            [
                lease.c.LEASE_KID,
                lease.c.LATITUDE,
                lease.c.LONGITUDE
            ]
    )
    if county != 'All':
        df = pd.read_sql(s.where(lease.c.COUNTY == county), engine)
    else:
        df = pd.read_sql(s, engine)
    
    if map_type == "Heat Map":
        fig.add_trace(
            go.Densitymapbox(
                lat=df['LATITUDE'],
                lon=df['LONGITUDE'],
                radius=2,
            )
        )

    elif map_type == "Scatter Plot":
        fig.add_trace(
            go.Scattermapbox(
                lat=df['LATITUDE'],
                lon=df['LONGITUDE'],
                mode='markers',
                marker=go.scattermapbox.Marker(
                    size=5
                ),
                showlegend=False,
                text=df['LEASE_KID'],
                customdata=kansas_state['NAME'],
                hovertemplate=
                    "<b>County</b><br>" +
                    "%{customdata}<br>" +
                    "<extra></extra>"
            )
        )


    return fig


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