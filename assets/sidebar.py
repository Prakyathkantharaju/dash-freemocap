import dash_bootstrap_components as dbc
import dash_html_components as html

class sidebar:
    # the style arguments for the sidebar. We use position:fixed and a fixed width
    SIDEBAR_STYLE = {
        "position": "fixed",
        "top": 0,
        "left": 0,
        "bottom": 0,
        "width": "16rem",
        "padding": "2rem 1rem",
        "background-color": "#f8f9fa",
    }

    # the styles for the main content position it to the right of the sidebar and
    # add some padding.
    CONTENT_STYLE = {
        "margin-left": "18rem",
        "margin-right": "2rem",
        "padding": "2rem 1rem",
    }


    def html(self):
        slider_html_div = html.Div(
            [
                html.H2("Freemocap", className="display-4"),
                html.Hr(),
                html.P(
                    "visualization modes", className="lead"
                ),
                dbc.Nav(
                    [
                        dbc.NavLink("Home/3d", href="/", active="exact"),
                        dbc.NavLink("trajectories", href="/page-1", active="exact"),
                        dbc.NavLink("axis", href="/page-2", active="exact"),
                    ],
                    vertical=True,
                    pills=True,
                ),
            ],
            style=self.SIDEBAR_STYLE,
        )
        return slider_html_div
