from app import app
from dash import callback_context
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import pandas as pd
import plotly.graph_objects as go
from pages.explore.explore_model import dm
from components.forecaster import Forecaster
from utils.functions import log, generate_forecast_with_ci


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
            num_wells is None
            or well_months is None
            or num_wells == ""
            or well_months == ""
        ):
            return current_value
        else:
            return current_value + "\n" + f"{num_wells},{well_months}"


@app.callback(
    Output("predict-plot", "figure"),
    Input("forecast-execute-button", "n_clicks"),
    State("commodity-radio", "value"),
    State("forecast-well-input", "value"),
    # prevent_initial_call=False,
)
def update_predict_plot(n_clicks, commodity, forecast_input):

    # Convert input to DataFrame
    inputs = forecast_input.splitlines()
    header = ["wells", "months"]
    if len(inputs) > 1:
        vals = [[int(x.split(",")[0]), int(x.split(",")[1])] for x in inputs[1:]]
    else:
        vals = []
    df_user = pd.DataFrame(vals, columns=header)

    if n_clicks is None:
        raise PreventUpdate

    #############################################
    # TO REPLACE WITH FORECASTER IN THIS SECTION
    if commodity == "Oil":
        y = dm.df_oil_prod[dm.CV_P_CAL_DAY_PROD]
        X = dm.df_oil_prod[[dm.P_WELLS]]
    elif commodity == "Gas":
        y = dm.df_gas_prod[dm.CV_P_CAL_DAY_PROD]
        X = dm.df_gas_prod[[dm.P_WELLS]]
    else:
        return ValueError("Invalid commodity")

    # Set Defaults
    n_wells = 9000
    pred_period = 1 if n_clicks is None else 36
    wells_arr = pd.DataFrame([n_wells] * pred_period)

    # Override defaults with user inputs
    if len(df_user) > 0:
        pred_period = int(df_user["months"].sum())
        wells_arr = []
        for row in df_user.itertuples():
            wells_arr += [int(row.wells)] * int(row.months)
        wells_arr = pd.DataFrame(wells_arr)

    # Fit Forecaster
    fc = Forecaster(y, X)
    df_results = fc.fit_predict(pred_period, wells_arr)
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
    # Define sets and plot the figure
    x_train = pd.Series(y.index)
    x_forecast = pd.Series(df_results.index)
    y_train = y.round(0)
    y_forecast = df_results[fc.RES_FORECAST].round(0)
    y_upper = df_results[fc.RES_UPPER_INTERVAL].round(0)
    y_lower = df_results[fc.RES_LOWER_INTERVAL].round(0)
    well_train = pd.Series(X.iloc[:, 0])
    well_forecast = pd.Series(wells_arr.iloc[:, 0])

    fig = generate_forecast_with_ci(
        commodity,
        x_train,
        y_train,
        x_forecast,
        y_forecast,
        y_upper,
        y_lower,
        well_train,
        well_forecast,
    )

    return fig
