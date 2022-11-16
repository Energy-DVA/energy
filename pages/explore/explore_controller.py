from app import app
from dash import callback_context
from dash.dependencies import Input, Output
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from utils.constants import YEAR_START, YEAR_END, OIL_COLOR, GAS_COLOR
from utils.functions import scatter_commodity, log, generate_plot_title
from pages.explore.explore_model import dm
from components.base_map import draw_base_map


from utils.functions import log


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

    # Handle error
    if len(commodity) == 0:
        return draw_base_map()

    # Set flags
    if county == [] or county == ["All"]:
        county = None

    if operators == [] or operators == ["All"]:
        operators = None

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

        if "Oil" in commodity:
            fig.add_trace(scatter_commodity(df_oil, dm, OIL_COLOR, "Oil Leases"))

        if "Gas" in commodity:
            fig.add_trace(scatter_commodity(df_gas, dm, GAS_COLOR, "Gas Leases"))
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


@app.callback(
    Output("plot", "figure"),
    Input("commodity", "value"),
    Input("year-slider", "value"),
    Input("county", "value"),
    Input("operators", "value"),
    Input("map", "selectedData"),
    prevent_initial_call=False,
)
def update_plot(commodity, activity, county, operators, selection):

    # Handle error
    if len(commodity) == 0:
        return go.Figure(
            layout={
                "title": generate_plot_title(
                    "Select appropriate inputs and/or Click-Drag Select on Map"
                )
            }
        )

    # Set flags
    if county == [] or county == ["All"]:
        county = None
    if operators == [] or operators == ["All"]:
        operators = None

    # Check if map selection triggered callback
    # If yes, retrieve selection leases
    # If selection is empty, do nothing and return original figure
    lease_ids = None
    if callback_context.triggered_id == "map":
        if selection is not None and len(selection["points"]) > 0:
            lease_ids = [int(pt["text"]) for pt in selection["points"]]

    subplot_titles = [None, None]
    for commo in commodity:
        subplot_titles.append(f"Number of Wells of Selected {commo} Leases")

    # Develop plot
    fig = make_subplots(
        rows=2,
        cols=max(1, len(commodity)),
        shared_xaxes=True,
        vertical_spacing=0.1,
        column_titles=[
            f"Monthly Production of Selected {commo} Leases" for commo in commodity
        ],
        subplot_titles=subplot_titles,
    )

    fig.update_layout(
        showlegend=False,
        title=generate_plot_title("Selected Data Production"),
        margin = {"l": 0, "r": 0, "t": 50, "b": 0},
    )

    # Add Traces
    for i, commo in enumerate(commodity):
        # Retrieve Data
        df = dm.get_production_from_ids(
            commo.lower(), lease_ids, county, operators, None, activity, get_rate=True
        )
        # Plot the two traces
        color = OIL_COLOR if commo == "Oil" else GAS_COLOR
        fig.add_trace(
            go.Scatter(x=df.index, y=df["PRODUCTION"], line=dict(color=color)),
            row=1,
            col=i + 1,
        )
        fig.add_trace(
            go.Scatter(x=df.index, y=df["WELLS"], line=dict(color=color)),
            row=2,
            col=i + 1,
        )

    return fig


@app.callback(
    Output("year-slider", "value"),
    Output("activity-from", "value"),
    Output("activity-to", "value"),
    Input("year-slider", "value"),
    Input("activity-from", "value"),
    Input("activity-to", "value"),
    prevent_initial_call=False,
)
def update_slider_values(slider, fro, to):
    trigger_id = callback_context.triggered_id
    year_start = fro if trigger_id == "activity-from" else slider[0]
    year_end = to if trigger_id == "activity-to" else slider[1]
    slider_value = slider if trigger_id == "year-slider" else [year_start, year_end]

    # Adjust for inputs error (when year_start > year_end and vice versa)
    if trigger_id == "activity-from" and year_start > year_end:
        year_end = year_start + 5
    elif trigger_id == "activity-to" and year_start > year_end:
        year_start = year_end - 5
    return slider_value, year_start, year_end


@app.callback(
    Output("county", "value"),
    Output("operators", "value"),
    Input("county", "value"),
    Input("operators", "value"),
    prevent_initial_call=False,
)
def filter_based_on_input(county, operators):
    # This function filters the inputs and sets the same outputs
    # If input has "All" and any other value, it removes "All"
    # If "All" is added, all other inputs are removed

    if len("county") > 1 and "All" in county:
        if county[-1] == "All":  # If All was selected at the end
            county = ["All"]
        else:  # Remove All from list
            county = [i for i in county if i != "All"]

    if len("operators") > 1 and "All" in operators:
        if operators[-1] == "All":  # If All was selected at the end
            operators = ["All"]
        else:  # Remove All from list
            operators = [i for i in operators if i != "All"]

    return county, operators
