from app import app
from dash import callback_context
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from pages.explore.explore_model import dm
from pages.predict.predict_model import fc
from utils.functions import generate_forecast_with_ci
from utils.constants import (
    OIL_UNITS,
    GAS_UNITS,
)


@app.callback(
    Output("forecast-well-input", "value"),
    Input("wells-submit-button", "n_clicks"),
    Input("clear-input-button", "n_clicks"),
    State("predict-wells-month", "value"),
    State("predict-wells", "value"),
    State("forecast-well-input", "value"),
    prevent_initial_call=False,
)
def update_user_input_to_textbox(
    submit_click, clear_click, well_months, num_wells, current_value
):
    if callback_context.triggered_id == "clear-input-button":
        return "Number of Wells, Months"
    else:
        if (
            num_wells == None
            or well_months == None
            or num_wells == ""
            or well_months == ""
        ):
            return current_value
        else:
            return current_value + "\n" + f"{num_wells},{well_months}"


@app.callback(
    Output("predict-wells", "value"),
    Output("predict-wells-month", "value"),
    Output("commodity-radio", "options"),
    Output("commodity-radio", "value"),
    Output("toast-hist-prod", "children"),
    Output("toast-hist-prod", "icon"),
    Output("toast-hist-wells", "children"),
    Output("toast-fore-prod", "children"),
    Output("toast-fore-wells", "children"),
    Output("predict-plot", "figure"),
    Input("toast-hist-prod", "icon"),
    Input("forecast-execute-button", "n_clicks"),
    State("commodity-radio", "value"),
    State("forecast-well-input", "value"),
    # prevent_initial_call=False,
)
def update_predict_plot(toast_icon, n_clicks, commodity, forecast_input: str):

    # Convert input to DataFrame
    inputs = forecast_input.splitlines()
    header = ["wells", "months"]
    if len(inputs) > 1:
        vals = [[int(x.split(",")[0]), int(x.split(",")[1])] for x in inputs[1:]]
    else:
        vals = []
    df_user = pd.DataFrame(vals, columns=header)

    com_radio = []
    if dm.df_oil_prod is not None:
        com_radio.append("Oil")
    if dm.df_gas_prod is not None:
        com_radio.append("Gas")

    # Retrieve data from data_manager
    if commodity == "Oil":
        y = dm.df_oil_prod[dm.CV_P_CAL_DAY_PROD]
        X = dm.df_oil_prod[[dm.P_WELLS]]
    elif commodity == "Gas":
        y = dm.df_gas_prod[dm.CV_P_CAL_DAY_PROD]
        X = dm.df_gas_prod[[dm.P_WELLS]]
    else:
        if dm.df_oil_prod is not None:
            y = dm.df_oil_prod[dm.CV_P_CAL_DAY_PROD]
            X = dm.df_oil_prod[[dm.P_WELLS]]
            commodity = "Oil"
        elif dm.df_gas_prod is not None:
            y = dm.df_gas_prod[dm.CV_P_CAL_DAY_PROD]
            X = dm.df_gas_prod[[dm.P_WELLS]]
            commodity = "Gas"
        else:
            return ValueError("No commodity selected")

    # Prepare train data
    x_train = pd.Series(y.index)
    y_train = y.round(0)
    well_train = pd.Series(X.iloc[:, 0])

    # Set Defaults
    n_wells = X.iloc[-1, 0]
    DEFAULT_MONTHS = 36
    pred_period = 1 if n_clicks is None else DEFAULT_MONTHS
    wells_arr = pd.DataFrame([n_wells] * pred_period)

    # Populate Toast elements (summation cards)
    units = OIL_UNITS if commodity == "Oil" else GAS_UNITS
    toast_hist_prod = str(np.mean(y_train).round(0)) + " " + units
    toast_hist_wells = str(int(np.mean(well_train))) + " wells"
    toast_fore_prod = "N/A"
    toast_fore_wells = "N/A"
    toast_hist_prod_icon = "success" if commodity == "Oil" else "danger"

    if n_clicks is None:
        fig = generate_forecast_with_ci(
            commodity,
            x_train,
            y_train,
            well_train,
        )

        return (
            n_wells,
            DEFAULT_MONTHS,
            com_radio,
            commodity,
            toast_hist_prod,
            toast_hist_prod_icon,
            toast_hist_wells,
            toast_fore_prod,
            toast_fore_wells,
            fig,
        )

    # Override defaults with user inputs
    if len(df_user) > 0:
        pred_period = int(df_user["months"].sum())
        wells_arr = []
        for row in df_user.itertuples():
            wells_arr += [int(row.wells)] * int(row.months)
        wells_arr = pd.DataFrame(wells_arr)

    # Fit Forecaster
    fc.y = y
    fc.X = X

    refit = (toast_icon == "success" and commodity == "Gas") or (
        toast_icon == "danger" and commodity == "Oil"
    )

    if n_clicks == 1 or refit:
        # Fit model
        df_results = fc.fit()

    # Predict
    df_results = fc.predict(pred_period, wells_arr)

    #########################################

    # If values go below 0, set it to 0
    df_results[fc.RES_LOWER_INTERVAL] = df_results[fc.RES_LOWER_INTERVAL].apply(
        lambda x: max(0, x)
    )
    df_results[fc.RES_UPPER_INTERVAL] = df_results[fc.RES_UPPER_INTERVAL].apply(
        lambda x: max(0, x)
    )

    # To ensure connectivity on graph, append last value from train to forecast
    y = pd.concat([y, df_results[fc.RES_FORECAST].iloc[0:1]])
    X.loc[df_results.index[0], dm.P_WELLS] = wells_arr.iloc[0, 0]

    # Prepare train data (replicated to handle First load case)
    x_train = pd.Series(y.index)
    y_train = y.round(0)
    well_train = pd.Series(X.iloc[:, 0])

    # Define sets and plot the figure
    x_forecast = pd.Series(df_results.index)
    y_forecast = df_results[fc.RES_FORECAST].round(0)
    y_upper = df_results[fc.RES_UPPER_INTERVAL].round(0)
    y_lower = df_results[fc.RES_LOWER_INTERVAL].round(0)
    well_forecast = pd.Series(wells_arr.iloc[:, 0])

    # Populate Toast elements (summation cards)
    toast_fore_prod = str(y_forecast.mean().round(0)) + " " + units
    toast_fore_wells = str(int(np.mean(well_forecast))) + " wells"

    fig = generate_forecast_with_ci(
        commodity,
        x_train,
        y_train,
        well_train,
        x_forecast,
        y_forecast,
        y_upper,
        y_lower,
        well_forecast,
    )

    return (
        None,
        None,
        com_radio,
        commodity,
        toast_hist_prod,
        toast_hist_prod_icon,
        toast_hist_wells,
        toast_fore_prod,
        toast_fore_wells,
        fig,
    )
