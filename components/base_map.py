import plotly.graph_objects as go

from utils.constants import (
    KANSAS_STATE,
    KANSAS_GEOJSON,
    DEFAULT_MIDPOINT,
    DEFAULT_ZOOM,
    COUNTIES,
    MAP_SELECTION_COLOR,
    MAP_MODEBAR_COLOR,
    MAP_MODEBAR_COLOR_ACTIVE,
    OIL_COLOR,
    GAS_COLOR,
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
                    "color": "gray",
                    "line": {"width": 1.5},
                }
            ],
            "center": {"lat": midpoint[0], "lon": midpoint[1]},
        },
        margin={"l": 0, "r": 0, "t": 0, "b": 0},
        autosize=True,
        newselection=dict(line=dict(color=MAP_SELECTION_COLOR, width=5, dash="solid")),
        modebar={
            "orientation": "h",
            "bgcolor": "rgba(255,255,255,0.7)",
            "color": MAP_MODEBAR_COLOR,
            "activecolor": MAP_MODEBAR_COLOR_ACTIVE,
        },
        selectionrevision=revision,
        uirevision=revision,
    )

    fig.update_geos(fitbounds="locations", visible=False)
    return fig
