
from dataclasses import dataclass, field, fields
import dataclasses
from typing import List
from connection_map import left_hand, right_hand, body, face

# numpy
import numpy as np


# load dash components
import numpy as np
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go

import plotly



# Sidebar
from assets.sidebar import sidebar





class freemocap_app(object):

    # general body objects
    left_hand = left_hand()
    right_hand = right_hand()
    body = body()
    face = face()

    def __init__(self):
        # css
        self.css_style_sheet = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
        self.app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP, self.css_style_sheet])
        self.sidebar =sidebar()
        self.content = html.Div(id="page-content", style=sidebar.CONTENT_STYLE)
        self._update_layout()
        self._add_callbacks()



    def _update_layout(self):
        self.app.layout = html.Div([dcc.Location(id="url"),
                                    self.sidebar.html(), self.content])

    def _add_callbacks(self):
        self.app.callback(Output("page-content", "children"),
                          [Input("url", "pathname")])(self._render_page_content)
        self.app.callback(Output('live-update-graph', 'figure'),
                          Input('interval-component', 'n_intervals'))(self._template_3d_plot)

    def _render_page_content(self,pathname):
        if pathname == "/":
            return self._render_3d_home()
        elif pathname == "/page-1":
            return html.P("This is the content of page 1. for specific marker trajectory!!!Future is great")
        elif pathname == "/page-2":
            return html.P("Oh cool, this is page 2!")
        # If the user tries to reach a different page, return a 404 message
        return dbc.Jumbotron(
            [
                html.H1("404: Not found", className="text-danger"),
                html.Hr(),
                html.P(f"The pathname {pathname} was not recognised..."),
            ]
        )

    def _render_3d_home(self):
        data = html.Div(
            html.Div([
                html.H4('3d feed feed'),
                html.Div(id='live-update-text'),
                dcc.Graph(id='live-update-graph',
                               figure={
                                'layout': plotly.graph_objs.Layout(
                                    xaxis =  {
                                        'showgrid': False
                                             },
                                    yaxis = {
                                        'showgrid': False
                                            })
                                        },
                          ),
                dcc.Interval(
                    id='interval-component',
                    interval=0.2*1000, # in milliseconds
                    n_intervals=0
                )
            ])
        )
        return data

    def _template_3d_plot(self,n):
        t = np.linspace(0, n, 10 * n)
        print(n)
        x, y, z = np.cos(t), np.sin(t), t

        fig = go.Figure(data=[go.Scatter3d(x=x, y=y, z=z,
                                           mode='markers')])
        return fig



if __name__ == "__main__":
        freemocap_app().app.run_server(port=8888, debug =True)
