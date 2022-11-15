import plotly.graph_objects as go

from utils.constants import (
    KANSAS_STATE,
    KANSAS_GEOJSON,
    DEFAULT_MIDPOINT,
    DEFAULT_ZOOM,
    COUNTIES,
)


def draw_base_map(midpoint=DEFAULT_MIDPOINT, zoom=DEFAULT_ZOOM):
    # Develop Figure to draw the base map on
    fig = go.Figure(go.Choroplethmapbox())

    # Set UI Revision
    revision = midpoint[0] + midpoint[1] + zoom

    # Add counties borders
    fig.update_layout(
        mapbox={
            "style": "open-street-map",
            "zoom": zoom,
            "layers": [
                {
                    "source": KANSAS_GEOJSON,
                    "below": "traces",
                    "type": "line",
                    "color": "purple",
                    "line": {"width": 1.5},
                }
            ],
            "center": {"lat": midpoint[0], "lon": midpoint[1]},
        },
        margin={"l": 0, "r": 0, "t": 0, "b": 0},
        autosize=True,
        newselection=dict(line=dict(color="Crimson", width=2, dash="dash")),
        modebar={
            "orientation": "h",
            "bgcolor": "rgba(255,255,255,0.7)",
            "color": "rgb(255,0,0)",
            "activecolor": "rgb(100,0,200)",
        },
        selectionrevision=revision,
        uirevision=revision,
    )

    fig.update_geos(fitbounds="locations", visible=False)
    return fig
