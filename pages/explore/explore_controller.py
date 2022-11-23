from app import app
import pandas as pd
from dash import callback_context
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from utils.constants import (
    OIL_COLOR,
    GAS_COLOR,
    CUSTOM_MODEBAR,
    OIL_UNITS,
    GAS_UNITS,
    WELL_COLOR,
)
from utils.functions import (
    scatter_commodity,
    log,
    generate_plot_title,
    generate_empty_plot,
)
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
        dm.L_OPERATOR,
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
                hovertemplate="<b>County: %{text}<br><extra></extra>",
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
            itemclick=False,
            itemdoubleclick=False,
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

    dm.df_oil_prod = None
    dm.df_gas_prod = None

    # Handle error
    if len(commodity) == 0:
        return generate_empty_plot()

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
        elif selection is not None and len(selection["points"]) == 0:
            lease_ids = []

    # Develop plot
    fig = make_subplots(
        rows=2,
        cols=max(1, len(commodity)),
        shared_xaxes=True,
        column_titles=[f"{commo} Leases" for commo in commodity],
        horizontal_spacing=0.13,
        vertical_spacing=0.02,
    )

    fig.update_layout(
        showlegend=False,
        title=generate_plot_title("Daily Production Rates and Well Data"),
        margin={"l": 25, "r": 25, "t": 50, "b": 50},
        modebar=CUSTOM_MODEBAR,
        hovermode="x",
        autosize=True,
    )

    # Add Traces
    for i, commo in enumerate(commodity):
        # Retrieve Data
        df = dm.get_production_from_ids(
            commo.lower(), lease_ids, county, operators, None, activity, get_rate=True
        )

        # Add watermark if Years chosen when no data is available
        if len(df) == 0:
            return generate_empty_plot()
        else:
            # Plot the two traces
            if commo == "Oil":
                color = OIL_COLOR
                units = OIL_UNITS
                dm.df_oil_prod = df
            elif commo == "Gas":
                color = GAS_COLOR
                units = GAS_UNITS
                dm.df_gas_prod = df
            else:
                raise ValueError(f"Unknown commodity: {commo}")

            fig.add_trace(
                go.Scatter(
                    x=df.index,
                    y=df[dm.CV_P_CAL_DAY_PROD].round(0),
                    line=dict(color=color),
                    name="",
                    hovertemplate="Daily Production: %{y}" + f" {units}<br>",
                ),
                row=1,
                col=i + 1,
            )
            fig.add_trace(
                go.Scatter(
                    x=df.index,
                    y=df[dm.P_WELLS].round(0),
                    line=dict(color=WELL_COLOR),
                    name="",
                    hovertemplate="Total Wells: %{y}<br>",
                ),
                row=2,
                col=i + 1,
            )

            xaxis_title = "Date"
            yaxis_title_prod = f"Production ({units})"
            yaxis_title_wells = "Well Count"
            fig.update_xaxes(title_text=xaxis_title, title_standoff=0, row=2, col=i + 1)
            fig.update_yaxes(
                title_text=yaxis_title_prod, title_standoff=0, row=1, col=i + 1
            )
            fig.update_yaxes(
                title_text=yaxis_title_wells, title_standoff=0, row=2, col=i + 1
            )

    return fig


@app.callback(
    Output("top-prod-counties", "figure"),
    Output("top-prod-operators", "figure"),
    Input("commodity", "value"),
    Input("year-slider", "value"),
    Input("county", "value"),
    Input("operators", "value"),
    Input("map", "selectedData"),
    prevent_initial_call=False,
)
def update_top_bargraphs(commodity, activity, county, operators, selection):
    # Handle error
    if len(commodity) == 0:
        return go.Figure(), go.Figure()

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
            county_opers = [x['customdata'] for x in selection["points"]]
            county = [pair[0] for pair in county_opers]
            operators = [pair[1] for pair in county_opers]
            lease_ids = [int(pt["text"]) for pt in selection["points"]]

    # Retrieve Data
    cols = [
        dm.L_LEASE_ID,
        dm.L_COUNTY,
        dm.L_OPERATOR,
        dm.L_PRODUCES,
        dm.P_PRODUCTION,
    ]
    commodity_l = [x.upper() for x in commodity]
    df = dm.get_lease_info(
        cols, lease_ids, county, operators, commodity_l, activity
    ).dropna()

    # Get top 5 counties
    df_counties = df[['PRODUCES','COUNTY','PRODUCTION']] \
                    .groupby(['PRODUCES','COUNTY']).sum()['PRODUCTION'] \
                    .reset_index() \
                    .sort_values(by='PRODUCTION', ascending=False) \
                    .groupby('PRODUCES') \
                    .head(5).round(0)
                    
    # Get top 5 Operators
    df_operators = df[['PRODUCES','OPERATOR','PRODUCTION']] \
                    .groupby(['PRODUCES','OPERATOR']).sum()['PRODUCTION'] \
                    .reset_index() \
                    .sort_values(by='PRODUCTION', ascending=False) \
                    .groupby('PRODUCES') \
                    .head(5).round(0)
    df_operators['TRUNCATED_NAME'] = df_operators['OPERATOR'].apply(lambda x: x[:6]+'...')
    
    # Develop plot
    fig_counties = make_subplots(
        rows=1,
        cols=max(1, len(commodity)),
        column_titles=[f"{commo} Leases" for commo in commodity],
        horizontal_spacing=0.05,
    )
    
    fig_operators = make_subplots(
        rows=1,
        cols=max(1, len(commodity)),
        column_titles=[f"{commo} Leases" for commo in commodity],
        horizontal_spacing=0.05,
    )
    
    for i, commo in enumerate(commodity):
        redgrad = ['rgb(203,24,29)', 'rgb(239,59,44)', 'rgb(251,106,74)', 'rgb(252,146,114)', 'rgb(252,187,161)']
        greengrad = ['rgb(35,139,69)', 'rgb(65,171,93)', 'rgb(116,196,118)', 'rgb(161,217,155)', 'rgb(199,233,192)']
        clrscle = redgrad if commo=='Gas' else greengrad
        
        # Add county traces
        traces_counties = px.bar(df_counties[df_counties['PRODUCES']==commo.upper()], 
                                x='PRODUCES',
                                y="PRODUCTION",
                                text='COUNTY',
                                color='COUNTY',
                                hover_data={'COUNTY':True,'PRODUCTION':True,'PRODUCES':False, 'PRODUCES':False},
                                barmode="overlay",
                                color_discrete_sequence=clrscle).data
        for trace in traces_counties:        
            fig_counties.add_trace(
                trace,
                row=1,
                col=i+1,
            )
            
        # Add operator traces
        traces_operators = px.bar(df_operators[df_operators['PRODUCES']==commo.upper()], 
                                x='PRODUCES',
                                y="PRODUCTION",
                                text='TRUNCATED_NAME',
                                hover_name='OPERATOR',
                                hover_data={'OPERATOR':True,'PRODUCTION':True,'TRUNCATED_NAME':False,'PRODUCES':False},
                                color='OPERATOR',
                                barmode="overlay",
                                color_discrete_sequence=clrscle).data
        for trace in traces_operators:
            fig_operators.add_trace(
                trace,
                row=1,
                col=i+1,
            )
        
        units = OIL_UNITS if commo == "Oil" else GAS_UNITS
        yaxis_title = f"Production ({units})"
        side = 'right' if i>0 else 'left'
        
        # Update County figure
        fig_counties.update_yaxes(
            title_text=yaxis_title, 
            side=side,
            title_standoff=1,
            gridcolor='grey',
            griddash='dash',
            gridwidth=0.1,
            showline=True,
            linewidth=2,
            linecolor='black',
            mirror=True,
            row=1, 
            col=i + 1,
        )
        fig_counties.update_xaxes(showline=True, linewidth=2, linecolor='black', mirror=True, gridwidth=0.5)
        
        # Update Operator figure
        fig_operators.update_yaxes(
            title_text=yaxis_title, 
            side=side,
            title_standoff=1,
            gridcolor='grey',
            griddash='dash',
            gridwidth=0.1,
            showline=True,
            linewidth=2,
            linecolor='black',
            mirror=True,
            row=1, 
            col=i + 1,
        )
        fig_operators.update_xaxes(showline=True, linewidth=2, linecolor='black', mirror=True, gridwidth=0.5)
        
    
    fig_counties.update_traces(textangle=0, textfont={'color':'black'})
    fig_operators.update_traces(textangle=0, textfont={'color':'black'})

    fig_counties.update_layout(
        #barmode='group',
        showlegend=False,
        #title=generate_plot_title("Top 5 Counties"),
        margin={"l": 35, "r": 35, "t": 25, "b": 5},
        modebar=CUSTOM_MODEBAR,
        autosize=True,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    fig_operators.update_layout(
        #barmode='group',
        showlegend=False,
        #title=generate_plot_title("Top 5 Counties"),
        margin={"l": 35, "r": 35, "t": 25, "b": 5},
        modebar=CUSTOM_MODEBAR,
        autosize=True,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig_counties, fig_operators


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


@app.callback(
    Output("operators", "options"),
    Input("county", "value"),
)
def update_operators_options(county):
    df_op = dm.get_lease_info([dm.L_OPERATOR])
    df_op = df_op.dropna()
    df_op = df_op.drop_duplicates()
    df_op = df_op.sort_values(by=[dm.L_OPERATOR])
    return ["All"] + [op for op in df_op[dm.L_OPERATOR]]
