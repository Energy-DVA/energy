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
    fig = go.Figure(layout={
        "title": generate_plot_title(
            "Select Commodities and other Inputs. Click-Drag Select on Map to filter"
        )
    })
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
