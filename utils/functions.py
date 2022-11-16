from app import app
import plotly.graph_objects as go
import pandas as pd
from components.data_manager import DataManager
from utils.constants import WATERMARK


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
        customdata=df[dm.L_COUNTY],
        showlegend=True,
        legendgroup="scatter" + title,
        name=title,
        hovertemplate="<b>County</b><br>"
        + "%{customdata}<br>"
        + "%{text}<br>"
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
    x_train, y_train, x_forecast, y_forecast, y_upper, y_lower
):

    # Define Colors
    train_color = "rgb(31, 119, 180)"
    forecast_color = "rgb(200, 0, 0)"
    ci_line_color = "rgb(100,100,100)"
    ci_fill_color = "rgba(68, 68, 68, 0.33)"

    # Generate figure
    fig = go.Figure(
        [
            go.Scatter(
                name="Measurement",
                x=x_train,
                y=y_train,
                mode="lines",
                line=dict(color=train_color),
            ),
            go.Scatter(
                name="Measurement",
                x=x_forecast,
                y=y_forecast,
                mode="lines",
                line=dict(color=forecast_color),
            ),
            go.Scatter(
                name="Upper Bound",
                x=x_forecast,
                y=y_upper,
                mode="lines",
                marker=dict(color=ci_line_color),
                line=dict(width=1),
                showlegend=False,
            ),
            go.Scatter(
                name="Lower Bound",
                x=x_forecast,
                y=y_lower,
                marker=dict(color=ci_line_color),
                line=dict(width=1),
                mode="lines",
                fillcolor=ci_fill_color,
                fill="tonexty",
                showlegend=False,
            ),
        ]
    )

    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Commodity Forecast",
        title="Continuous, variable value error bars",
        hovermode="x",
    )

    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(zeroline=True,
                     zerolinecolor='black',
                     zerolinewidth=1
    )


    return fig
