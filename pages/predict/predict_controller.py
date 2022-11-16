from app import app
from dash import callback_context
from dash.dependencies import Input, Output
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from utils.constants import (
    YEAR_START,
    YEAR_END,
    OIL_COLOR,
    GAS_COLOR,
    WATERMARK,
    CUSTOM_MODEBAR,
)
from utils.functions import (
    scatter_commodity,
    log,
    generate_plot_title,
    generate_empty_plot,
)
from pages.predict.predict_model import dm

from utils.functions import log, generate_forecast_with_ci


@app.callback(
    Output("predict-plot", "figure"),
    Input("commodity", "value"),
    prevent_initial_call=False,
)
def update_predict_plot(commodity):
    import pandas as pd
    import numpy as np

    # Read data
    df_train = pd.read_csv("pages/predict/xtrain.csv")
    df_valid = pd.read_csv("pages/predict/xvalid.csv")
    df_conf = pd.read_csv("pages/predict/confintx.csv")
    
    # If values go below 0, set it to 0
    df_conf["low"] = df_conf["low"].apply(lambda x: max(0, x))
    df_conf["high"] = df_conf["high"].apply(lambda x: max(0, x))

    # To ensure connectivity on graph, append last value from train to forecast
    df_train = pd.concat([df_train, df_valid.iloc[0:1]])
    
    # Define sets and plot the figure
    x_train = df_train["DATE"]
    y_train = df_train["MONTHLY_GAS_PROD"]
    x_forecast = df_valid["DATE"]
    y_forecast = df_valid["MONTHLY_GAS_PROD"]
    y_upper = df_conf["high"]
    y_lower = df_conf["low"]
    fig = generate_forecast_with_ci(
        x_train, y_train, x_forecast, y_forecast, y_upper, y_lower
    )
    
    return fig
