from app import app
from dash.dependencies import Input, Output
import plotly.graph_objects as go
from utils.constants import YEAR_START, YEAR_END
from utils.functions import scatter_commodity
from pages.explore.explore_model import dm
from components.base_map import draw_base_map


@app.callback(
    Output("map", "figure"),
    Input("map_type", "value"),
    Input("commodity", "value"),
    Input("year-slider", "value"),
    Input("county", "value"),
    Input("operators", "value"),
    prevent_initial_call=False,
)
def update_map(map_type, commodity, activity, county, operators):

    # Draw base map
    fig = draw_base_map()

    # Retrieve Data
    cols = [
        dm.L_LEASE_ID,
        dm.L_LATITUDE,
        dm.L_LONGITUDE,
        dm.L_PRODUCES,
        dm.L_YEAR_START,
        dm.L_YEAR_STOP,
        dm.L_COUNTY,
    ]
    commodity_l = [x.upper() for x in commodity]
    df = dm.get_lease_info(
        cols, None, county, operators, commodity_l, activity
    ).dropna()

    if map_type == "Heat Map":
        fig.add_trace(
            go.Densitymapbox(
                lat=df[dm.L_LATITUDE],
                lon=df[dm.L_LONGITUDE],
                text=df[dm.L_COUNTY],
                radius=2,
                showscale=False,
                hovertemplate="<b>County</b><br>" + "%{text}<br>" + "<extra></extra>",
            )
        )
    elif map_type == "Scatter Plot":
        df_oil = df[df[dm.L_PRODUCES] == dm.L_PRODUCES_OIL]
        df_gas = df[df[dm.L_PRODUCES] == dm.L_PRODUCES_GAS]
        print(df_oil)

        if "Oil" in commodity:
            fig.add_trace(
                scatter_commodity(df_oil, dm, "rgba(0,200,0,0.75)", "Oil Leases")
            )

        if "Gas" in commodity:
            fig.add_trace(
                scatter_commodity(df_gas, dm, "rgba(200,0,0,0.75)", "Gas Leases")
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
            borderwidth=1,
        ),
        uirevision="base",
        selectionrevision="base",
    )

    return fig
