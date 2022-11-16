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

    df_train = pd.read_csv("pages/predict/xtrain.csv")
    df_valid = pd.read_csv("pages/predict/xvalid.csv")
    df_conf = pd.read_csv("pages/predict/confintx.csv")
    df_conf["low"] = df_conf["low"].apply(lambda x: max(0, x))
    df_conf["high"] = df_conf["high"].apply(lambda x: max(0, x))

    df_hist = pd.concat([df_train, df_valid])
    df_hist["DATE"] = pd.to_datetime(df_hist["DATE"], infer_datetime_format=True)
    df_conf["DATE"] = pd.to_datetime(df_conf["DATE"], infer_datetime_format=True)
    df_hist = pd.merge(df_hist, df_conf, on="DATE", how="left")
    df_hist["low"] = df_hist["low"].fillna(df_hist["MONTHLY_GAS_PROD"])
    df_hist["high"] = df_hist["high"].fillna(df_hist["MONTHLY_GAS_PROD"])

    x_train = df_hist["DATE"]
    y_train = df_hist["MONTHLY_GAS_PROD"]
    x_forecast = df_valid["DATE"]
    y_forecast = df_valid["MONTHLY_GAS_PROD"]
    y_upper = df_conf["high"]
    y_lower = df_conf["low"]

    return generate_forecast_with_ci(
        x_train, y_train, x_forecast, y_forecast, y_upper, y_lower
    )
