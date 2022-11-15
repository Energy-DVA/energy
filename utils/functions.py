from app import app
import plotly.graph_objects as go
import pandas as pd
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
            # opacity=0.66,
        ),
        text=df[dm.L_LEASE_ID],
        customdata=df[dm.L_COUNTY],
        showlegend=True,
        legendgroup="scatter"+title,
        name=title,
        hovertemplate="<b>County</b><br>"
        + "%{customdata}<br>"
        + "%{text}<br>"
        + "<extra></extra>",
    )
