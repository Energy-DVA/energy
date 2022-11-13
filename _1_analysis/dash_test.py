import dash
import dash_bootstrap_components as dbc
import numpy as np
import pandas as pd
import geopandas as gpd
import geojson
import json
import plotly.graph_objects as go
from dash import Input, Output, State, ClientsideFunction, dcc, html
import plotly.express as px
from sqlalchemy import create_engine, MetaData, or_, and_
from sqlalchemy import select, func 
from db_schema import OIL_PROD_TABLE, GAS_PROD_TABLE, LEASE_TABLE, WELLS_TABLE, TOPS_TABLE
from shapely.geometry import Point, Polygon

###################--- Helper Functions ---############################

def log(stuff):
    app.logger.info(stuff)

def calc_zoom(min_lat,max_lat,min_lng,max_lng):
    width_y = max_lat - min_lat
    width_x = max_lng - min_lng
    zoom_y = round(-1.446*np.log(width_y) + 7.2753,2)
    zoom_x = round(-1.415*np.log(width_x) + 8.7068,2)
    
    return min(zoom_y,zoom_x)

def draw_base_map(draw_counties=True, midpoint=(38.62470, -98.38020), zoom=6):
    fig = go.Figure()
    # Add Counties shaders
    # if draw_counties:
    #     trace = go.Choroplethmapbox(geojson=kansas_geojson, locations=kansas_state["GEOID"], z=kansas_state["LSAD"],
    #                             marker_opacity=0.5, marker_line_width=0,
    #                             colorscale="gray", zmin=0, zmax=9, showscale=False,
    #                             text=kansas_state["NAME"],
    #                             hovertemplate=
    #                                         "<b>County</b><br>" +
    #                                         "%{text}<br>" +
    #                                         "<extra></extra>"
    #             )
    # else:
    #     trace = go.Choroplethmapbox()
    
    trace = go.Choroplethmapbox()
    fig.add_trace(trace)
    
    # Set UI Revision
    revision = midpoint[0]+midpoint[1]+zoom

    # Add counties borders
    fig.update_layout(
        mapbox={
            "style": "open-street-map",
            "zoom": zoom,
            "layers": [
                {
                    "source": kansas_geojson,
                    "below": "traces",
                    "type": "line",
                    "color": "purple",
                    "line": {"width": 1.5},
                }
            ],
            "center" : {"lat": midpoint[0], "lon": midpoint[1]}
        },
        margin={"l": 0, "r": 5, "t": 0, "b": 0},
        autosize = True,
        newselection=dict(line=dict(color="Crimson",
                                    width=2,
                                    dash="dash")),
                                    
        modebar = {
            'orientation': 'h',
            'bgcolor': 'rgba(255,255,255,0.7)',
            'color': 'rgb(255,0,0)',
            'activecolor': 'rgb(100,0,200)',
        },
        selectionrevision  = revision,
        uirevision = revision,
    )

    fig.update_geos(fitbounds="locations", visible=False)
    return fig

def develop_cards():

    production_card = dbc.Card(
        [
            dbc.CardHeader("Production Type"),
            dbc.CardBody(
                [
                    dcc.RadioItems(
                        id="commodity",
                        options=["All","Oil","Gas"],
                        value="All",
                        labelStyle={'display': 'block', 'margin-top':'-5%'},
                        inputStyle={"margin-right": "5%", 'margin-top':'6%'},
                    ),
                ]
            ),
        ],
        body=True
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
                                    'Year from:',
                                    dbc.Input(type='number', min=1930, max=2022, id='activity-from', size='sm', value=1991, debounce=True),
                                ]
                            ),
                            dbc.Col(
                                [
                                    'Year to:',
                                    dbc.Input(type='number', min=1930, max=2022, id='activity-to', size='sm', value=2022, debounce=True),
                                ]
                            ),
                        ]
                    ),
                    html.Br(),
                    dcc.RangeSlider(
                        1930,
                        2022,
                        step=1,
                        id='year-slider',
                        value=[1991,2022],
                        marks={str(year): str(year) for year in range(1930,2022,15)},
                        tooltip={"placement": "bottom", "always_visible": True},
                        pushable=5,
                    ),
                ]
            )
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
                                    {'label': 'Counties Only', 'value': 'Counties'},
                                    {'label': 'Individual Leases', 'value': 'Scatter Plot'},
                                    {'label': 'Density', 'value': 'Heat Map'}
                                ],
                        value='Counties',
                        labelStyle={'display': 'block', 'margin-top':'-5%'},
                        inputStyle={"margin-right": "5%", 'margin-top':'6%'},
                    ),
                ]
            ),
        ], 
        body=True
    )

    # map_controls_card = dbc.Card(
    #     [
    #         dbc.CardHeader("Map Controls"),
    #         dbc.CardBody(
    #             [
    #                 dbc.Button("Reset View", color="primary", className="mt-auto", id='reset_view'),
    #             ]
    #         ),
    #     ], 
    #     body=True
    # )

    controls = html.Div(
        [
            dbc.Row(
                [
                    #dbc.Col(map_controls_card),
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
kansas_crs = kansas_state.crs
kansas_state = kansas_state[kansas_state["STATEFP"]=='20'].reset_index(drop=True)
kansas_state['LSAD'] = kansas_state['LSAD'].astype(int)
with open('kansas_counties.geojson') as f:
    kansas_geojson = geojson.load(f)

# Setup app config, layout, and tokens
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
#mapbox_access_token = "pk.eyJ1IjoiZ2VldGFraW5nbGUiLCJhIjoiY2w5dmxxc3JmMHJ6azNva2JzOHNoMGhxayJ9.qEl0L0gXzDHVYSkF1uvoSg"
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
                'modeBarButtonsToAdd':['select2d','lasso2d']
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
                        dcc.Graph(id="map", figure=draw_base_map(draw_counties=False), config=map_config)
                    ],
                    className='mb-10',
                ),
                dbc.Col(
                    [
                        dcc.Graph(id="plot", figure=draw_base_map(draw_counties=True), config=map_config)
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
    Output("year-slider", "value"),
    Output("activity-from", "value"),
    Output("activity-to", "value"),
    Input("year-slider", "value"),
    Input("activity-from", "value"),
    Input("activity-to", "value"),
    prevent_initial_call=False
)
def update_slider(slider, fro, to):
    trigger_id = dash.callback_context.triggered_id
    year_start = fro if trigger_id == "activity-from" else slider[0]
    year_end = to if trigger_id == "activity-to" else slider[1]
    slider_value = slider if trigger_id == "year-slider" else [year_start, year_end]

    # Adjust for inputs error (when year_start > year_end and vice versa)
    if (trigger_id == "activity-from" and year_start > year_end):
        year_end = year_start + 5
    elif (trigger_id == "activity-to" and year_start > year_end):
        year_start = year_end - 5
    return slider_value, year_start, year_end




# @app.callback(
#     Output("plot", "figure"),
#     Input("county", "value")
# )
# def draw_animation(county):
    # fig = draw_base_map(draw_counties=True)

    # s = select(
    #         [
    #             lease.c.LEASE_KID,
    #             lease.c.LATITUDE,
    #             lease.c.LONGITUDE,
    #             lease.c.YEAR_START,
    #             lease.c.YEAR_STOP,
    #         ]
    # )

    # # Read data from SQL
    # df = pd.read_sql(s, engine).dropna()

    # fig.add_trace(
    #     px.scatter_mapbox(df,
    #         lat="LATITUDE",
    #         lon="LONGITUDE",
    #         animation_frame = 'Date',
    #         animation_group = 'LEASE_KID', 
    #         color="Confirmed",
    #         size="Confirmed",
    #         color_continuous_scale=px.colors.cyclical.IceFire, 
    #         size_max=70,
    #         zoom=0.75,
    #         hover_name='Country', 
    #         hover_data = ['Confirmed', 'Deaths', 'Recovery'], 
    #         title = 'Visualizing spread of COVID from 22/1/2020 to 17/6/2020')
    # )
    # return fig


@app.callback(
    Output("map", "figure"),
    Input("map_type", "value"),
    Input("commodity", "value"),
    Input("year-slider", "value"),
    Input("county", "value"),
    prevent_initial_call=False
)
def drawn_polygon(map_type, commodity, activity, county):
    
    # Set flags to values
    if map_type == None:
        county = 'Counties'
    if commodity == None:
        commodity = 'All'
    if activity == None:
        activity = [1930,2022]
    if county == None:
        county = 'All'

    # If no map type is chosen, activate the counties Choropleth layer
    reset_view = True if map_type == 'Counties' else False

    # Draw base map
    fig = draw_base_map(draw_counties=reset_view)

    # Retrieve Data
    s = select(
            [
                lease.c.LEASE_KID,
                lease.c.LATITUDE,
                lease.c.LONGITUDE,
                lease.c.PRODUCES,
                lease.c.YEAR_START,
                lease.c.YEAR_STOP,
                lease.c.COUNTY,
            ]
    )
    if commodity != 'All':
        s = s.where(lease.c.PRODUCES == commodity.upper())
    # else select all

    if county != 'All':
        s = s.where(lease.c.COUNTY == county)
    # else select all


    # Filter on chosen years where leases are active using complement of the following two conditions
    # 
    # 1) Selection years are after the lease stops producing
    #               activity[0] |--------| activity[1]
    # YEAR_START |-------| YEAR_STOP
    # 
    # 2) Selection years are before the lease starts producing
    # activity[0] |--------| activity[1]
    #                     YEAR_START |-------| YEAR_STOP
    #     
    s = s.where(and_(lease.c.YEAR_STOP >= activity[0]), lease.c.YEAR_START <= activity[1])
    
    # Read data from SQL
    df = pd.read_sql(s, engine).dropna()
    
    if map_type == "Heat Map":
        fig.add_trace(
            go.Densitymapbox(
                lat=df['LATITUDE'],
                lon=df['LONGITUDE'],
                text=df['COUNTY'],
                radius=2,
                showscale=False,
                hovertemplate=
                    "<b>County</b><br>" +
                    "%{text}<br>" +
                    "<extra></extra>"
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
                        color='rgba(0,0,200,0.75)',
                        # opacity=0.66,
                    ),
                    text=df_oil['LEASE_KID'],
                    customdata=df_oil['COUNTY'],
                    showlegend=True,
                    legendgroup="scatter",
                    name="Oil Leases",
                    hovertemplate=
                        "<b>County</b><br>" +
                        "%{customdata}<br>" +
                        "%{text}<br>" +
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
                        color='rgba(0,200,0,0.75)',
                        # opacity=0.66,
                    ),
                    text=df_gas['LEASE_KID'],
                    customdata=df_gas['COUNTY'],
                    showlegend=True,
                    legendgroup="scatter",
                    name="Gas Leases",
                    hovertemplate=
                        "<b>County</b><br>" +
                        "%{customdata}<br>" +
                        "%{text}<br>" +
                        "<extra></extra>"
                )
            )
    # else Counties only and continue with basemap

    fig.update_layout(
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01,
            bgcolor="White",
            bordercolor="Black",
            borderwidth=1
        ),
        uirevision  = 'base',
        selectionrevision  = 'base',
    )
    
    return fig

#     if 'lassoPoints' in selection.keys():
#         poly = np.array(selection['lassoPoints']['mapbox'])
#         gdf = gpd.GeoDataFrame(index=[0],geometry=[Polygon(poly)])
#         gdf.set_crs(kansas_crs, inplace=True)
#         midpoint = (gdf.centroid[0].y , gdf.centroid[0].x)
#     else: # Rect range selected
#         poly = np.array(selection['range']['mapbox'])
#         midpoint = (np.mean(poly[:,1]) , np.mean(poly[:,0]))

#     zoom = calc_zoom(np.min(poly[:,1]),np.max(poly[:,1]),np.min(poly[:,0]),np.max(poly[:,0]))
#     log(midpoint)
#     log(zoom)
#     fig = draw_base_map(midpoint=midpoint, zoom=zoom)
#     return fig



# @app.callback(
#     Output("plot", "figure"), 
#     [
#         Input("commodity", "value"),
#         Input("county", "value"),
#     ]
# )
# def display_time_series(commodity, county):
#     if county == None or county == 'All' or commodity == 'All':
#         return px.line()
#     else:
#         table = oil_prod if commodity == 'Oil' else gas_prod
#         # Retrieve Data
#         s = select(
#                 [
#                     table.c.DATE,
#                     table.c.PRODUCTION
#                 ]
#         )
#         df = pd.read_sql(s, engine).dropna()
#         fig = px.line(df, x='DATE', y='PRODUCTION')
#         return fig

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