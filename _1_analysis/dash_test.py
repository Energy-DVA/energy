import dash
import dash_bootstrap_components as dbc
import numpy as np
import pandas as pd
import geopandas as gpd
import geojson
import plotly.graph_objects as go
from dash import Input, Output, dcc, html
import plotly.express as px
from sqlalchemy import create_engine, MetaData, or_, and_
from sqlalchemy import select, func 
from db_schema import OIL_PROD_TABLE, GAS_PROD_TABLE, LEASE_TABLE, WELLS_TABLE, TOPS_TABLE
from shapely.geometry import Point

# Setup SQL Engine
engine = create_engine("sqlite:///../../kansas_oil_gas.db")
meta = MetaData()
meta.reflect(bind=engine)
oil_prod = meta.tables[OIL_PROD_TABLE]
gas_prod = meta.tables[GAS_PROD_TABLE]
lease = meta.tables[LEASE_TABLE]
wells = meta.tables[WELLS_TABLE]
tops = meta.tables[TOPS_TABLE]

# Setup app config, layout, and tokens
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
mapbox_access_token = "pk.eyJ1IjoiZ2VldGFraW5nbGUiLCJhIjoiY2w5dmxxc3JmMHJ6azNva2JzOHNoMGhxayJ9.qEl0L0gXzDHVYSkF1uvoSg"
controls = dbc.Card(
    [
        html.Div(
            [
                dbc.Label("Choose Production Type"),
                dcc.Dropdown(
                    id="commodity",
                    options=["Oil","Gas"],
                    value="Select",
                ),
            ]
        ),
        html.Div(
            [
                dbc.Label("Active"),
                dcc.Dropdown(
                    id="active",
                    options=["Active","Inactive"],
                    value="Select",
                ),
            ]
        ),
    ],
    body=True,
)
map_config = {
                'displayModeBar': True,
                'displaylogo': False,
                'scrollZoom': True,
            }


# Import informations
kansas_state = gpd.read_file("Shapefiles/cb_2018_us_county_500k.shp")
kansas_state = kansas_state[kansas_state["STATEFP"]=='20'].reset_index(drop=True)
kansas_state['LSAD'] = kansas_state['LSAD'].astype(int)
with open('kansas_counties.geojson') as f:
    kansas_geojson = geojson.load(f)




# Define App Layout
app.layout = dbc.Container(
    [
        html.H1("Kansas Production Forecast"),
        html.Hr(),
        dbc.Row(
            [
                dbc.Col(controls, md=4),
                dbc.Col(dcc.Graph(id="map", config=map_config), md=8)
            ],
            align="top", 
            className="h-75",
        ),
    ],
    fluid=True,
)

@app.callback(
    Output("map", "figure"),
    [
        Input("commodity", "value"),
        Input("active", "value")
    ])
def drawn_polygon(commodity, active):

    # fig = go.Figure(data=go.Choroplethmapbox(
    #                     geojson=kansas_geojson,
    #                     locations=kansas_state.index,
    #                     z=kansas_state.NAME,
    #                     colorscale = "reds",
    #                     colorbar_title = "Millions USD")
    # )

    # fig.update_geos(fitbounds="locations")

    # fig.update_layout(mapbox_style="light", mapbox_accesstoken=mapbox_access_token,
    #                 mapbox_zoom=3, mapbox_center = {"lat": 37.0902, "lon": -95.7129})
    # fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

    # fig.update_layout(
    #     title_text = '2011 US Agriculture Exports by State',
    #     dragmode='drawclosedpath',
    #     newshape=dict(line_color='red',
    #                 fillcolor='grey',
    #                 opacity=0.5)
    # )


    #fig = go.Figure()
    
    # Add counties
    fig = px.choropleth_mapbox(kansas_state, geojson=kansas_geojson, locations="GEOID", color="LSAD",
                                opacity=0.5, center={"lat": 38.48470, "lon": -98.38020},
                                color_continuous_scale="gray", range_color=[0,8],
                                zoom = 6)

    fig.update_layout(
        # mapbox_layers=[
        #     {
        #         "source": kansas_geojson,
        #         "below": "traces",
        #         "type": "line",
        #         "color": "black",
        #         "line": {"width": 0.5},
        #     },
        # ],
        # mapbox_bounds = {"west": -180, "east": -50, "south": 20, "north": 90},
        mapbox_style="white-bg",
        autosize = True,
        height = 625
    )
    
    fig.update_geos(fitbounds="locations", visible=False)
    
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



# Start App
if __name__ == "__main__":
    app.run_server(debug=True, port=8888)