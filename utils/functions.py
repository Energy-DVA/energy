from app import app
import plotly.graph_objects as go
import numpy as np
import pandas as pd
from plotly.subplots import make_subplots

from utils.constants import (
    WATERMARK,
    OIL_UNITS,
    GAS_UNITS,
    OIL_COLOR,
    GAS_COLOR,
    WELL_COLOR,
    CUSTOM_MODEBAR,
)
from components.data_manager import DataManager


# Debugging function to log input to Console
def log(stuff):
    app.logger.info(stuff)


def scatter_commodity(df: pd.DataFrame, dm: DataManager, color: str, title: str):
    return go.Scattermapbox(
        lat=df[dm.L_LATITUDE],
        lon=df[dm.L_LONGITUDE],
        mode="markers",
        marker=go.scattermapbox.Marker(
            size=5,
            color=color,
            opacity=0.6,
        ),
        text=df[dm.L_LEASE_ID],
        customdata= np.stack([df[dm.L_COUNTY], df[dm.L_OPERATOR]], axis=-1),
        showlegend=True,
        legendgroup="scatter" + title,
        name=title,
        hovertemplate="<b>County: %{customdata[0]}<br>"
        + "<b> Lease ID: #%{text}<br>"
        + "<b> Operator: %{customdata[1]}<br>"
        + "<extra></extra>",
    )


def generate_empty_plot():
    fig = go.Figure(
        layout={
            "title": generate_plot_title(
                "Select Commodities and other Inputs. Click-Drag Select on Map to filter"
            )
        }
    )
    fig.add_layout_image(
        dict(
            source=WATERMARK,
            xref="paper",
            yref="paper",
            x=0.5,
            y=0.24,
            sizex=0.5,
            sizey=0.6,
            xanchor="center",
            yanchor="bottom",
            sizing="contain",
            opacity=0.5,
            layer="below",
        )
    )
    return fig


def generate_plot_title(text):
    return {"text": text, "y": 0.99, "x": 0.5, "xanchor": "center", "yanchor": "top"}


def generate_forecast_with_ci(
    commodity,
    x_train,
    y_train,
    well_train,
    x_forecast=None,
    y_forecast=None,
    y_upper=None,
    y_lower=None,
    well_forecast=None,
):

    # Define Colors and units
    units = OIL_UNITS if commodity == "Oil" else GAS_UNITS
    train_color = OIL_COLOR if commodity == "Oil" else GAS_COLOR
    forecast_color = "blue"
    ci_line_color = "rgb(100,100,100)"
    ci_fill_color = "rgba(68, 68, 68, 0.33)"

    # Make 2 subplots. Top for production data, bottom for wells
    fig = make_subplots(
        rows=2,
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.01,
    )

    # Generate figure
    fig.add_trace(
        go.Scatter(
            x=x_train,
            y=y_train,
            mode="lines",
            line=dict(color=train_color),
            name="",
            hovertemplate="Historical Production: %{y}" + f"{units}<br>",
        ),
        row=1,
        col=1,
    )

    if x_forecast is not None:
        fig.add_trace(
            go.Scatter(
                x=x_forecast,
                y=y_forecast,
                mode="lines",
                line=dict(color=forecast_color),
                name="",
                hovertemplate="Forecasted Production: %{y}" + f"{units}<br>",
            ),
            row=1,
            col=1,
        )

        fig.add_trace(
            go.Scatter(
                x=x_forecast,
                y=y_upper,
                mode="lines",
                marker=dict(color=ci_line_color),
                line=dict(width=1),
                showlegend=False,
                name="",
                hovertemplate="Forecast Upper Bound: %{y}" + f"{units}<br>",
            ),
            row=1,
            col=1,
        )

        fig.add_trace(
            go.Scatter(
                x=x_forecast,
                y=y_lower,
                marker=dict(color=ci_line_color),
                line=dict(width=1),
                mode="lines",
                fillcolor=ci_fill_color,
                fill="tonexty",
                showlegend=False,
                name="",
                hovertemplate="Forecast Lower Bound: %{y}" + f"{units}<br>",
            ),
            row=1,
            col=1,
        )

        fig.add_trace(
            go.Scatter(
                x=x_train,
                y=well_train,
                mode="lines",
                line=dict(color=WELL_COLOR),
                name="",
                hovertemplate="Historical Well Count: %{y}<br>",
            ),
            row=2,
            col=1,
        )

        fig.add_trace(
            go.Scatter(
                x=x_forecast,
                y=well_forecast,
                mode="lines",
                line=dict(color=forecast_color),
                name="",
                hovertemplate="Forecasted Well Count: %{y}<br>",
            ),
            row=2,
            col=1,
        )

        # Add Vertical Lines
        fig.add_vline(
            x=x_forecast.iloc[0],
            line_width=2,
            line_dash="dot",
            line_color="black",
            row=1,
            col=1,
        )
        fig.add_vline(
            x=x_forecast.iloc[0],
            line_width=2,
            line_dash="dot",
            line_color="black",
            row=2,
            col=1,
        )

    fig.update_layout(
        yaxis_title=f"{commodity} Production ({units})",
        title=generate_plot_title("Commodity Production Forecast and Well Data "),
        hovermode="x",
        margin={"l": 25, "r": 25, "t": 50, "b": 50},
        modebar=CUSTOM_MODEBAR,
        showlegend=False,
    )

    # Update X-axes
    fig.update_xaxes(showgrid=False, row=1, col=1)
    fig.update_xaxes(title_text="Date", title_standoff=0, row=2, col=1, showgrid=False)
    # Update all y axes
    fig.update_yaxes(zeroline=True, zerolinecolor="black", zerolinewidth=1)
    # Update top Y axis
    fig.update_yaxes(title_text=f"Production ({units})", title_standoff=0, row=1, col=1)
    # Update bottom Y axis
    fig.update_yaxes(title_text="Well Count", title_standoff=0, row=2, col=1)

    return fig
