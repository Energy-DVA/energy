from dash import dcc, html


tabs = html.Div(
    dcc.Tabs(
        parent_className="custom-tabs",
        className="custom-tabs-container",
        id="tabs-container",
        value="page_explore",
        children=[
            dcc.Tab(
                label="EXPLORE",
                value="page_explore",
                id="page-explore",
                className="custom-tab",
                selected_className="custom-tab--selected",
            ),
            dcc.Tab(
                label="PREDICT",
                value="page_predict",
                id="page-predict",
                className="custom-tab",
                selected_className="custom-tab--selected",
            ),
        ],
    )
)
