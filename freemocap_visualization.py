
from dataclasses import dataclass, field, fields
import dataclasses
from typing import List, Any
from assets.connection_map import left_hand, right_hand, body, face, main_data_class

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

# filter
from scipy.signal import savgol_filter




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
        # html layout
        self._update_layout()
        # setup callback
        self._add_callbacks()

        # if you have more body ports create a database of connection and add here
        self.body_parts = [self.face, self.body, self.left_hand, self.right_hand]

        # start frame
        self.frame_counter = 100

        # free mocap data file.
        self.open_pose_file_path = 'freemocap/DataArrays/openPoseSkel_3d.npy'
        self._load_free_mocap_data()

        # self._plot_3d_frame_data(i)




    def _update_layout(self):
        """update the layout for the app
        """
        self.app.layout = html.Div([dcc.Location(id="url"),
                                    self.sidebar.html(), self.content])

    def _add_callbacks(self) -> None:
        """add the callback function for the updating the figure
        """
        self.app.callback(Output("page-content", "children"),
                          [Input("url", "pathname")])(self._render_page_content)
        self.app.callback(Output('live-update-graph', 'figure'),
                          Input('interval-component', 'n_intervals'))(self._plot_3d_frame_data)

    def _render_page_content(self,pathname:str) -> dbc.Jumbotron:
        """Render the page content based on the html path

        Args:
            pathname (str): html path

        Returns:
            dbc.Jumbotron: [html content]
        """
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

    def _render_3d_home(self) -> html.Div:
        """Render the 3d animation in the homepage

        Returns:
            html.Div: html division containing all the information
        """
        data = html.Div(
            html.Div([
                html.H4('3d feed feed'),
                html.Div(id='live-update-text'),
                dcc.Graph(id='live-update-graph'),
                dcc.Interval(
                    id='interval-component',
                    interval=0.2*1000, # in milliseconds
                    n_intervals=0
                )
            ])
        )
        return data

    def _load_free_mocap_data(self):
        """Load the data from the self.open_pose_file_path
        """
        skel_fr_mar_dim = np.load(self.open_pose_file_path)
        # smotthing similar to freemocap

        for mm in np.arange(0, skel_fr_mar_dim.shape[1]):
            if mm > 24 and mm < 67: #don't smooth the hands, or they disappear! :O
                pass
            else:
                for dim in range(skel_fr_mar_dim.shape[2]):
                    skel_fr_mar_dim[:,mm,dim] = savgol_filter(skel_fr_mar_dim[:,mm,dim], 5, 3)

        self.openpose_3d_data = skel_fr_mar_dim


    def _template_3d_plot(self,n: int) -> go.Figure:
        """Test 3d plot

        Args:
            n (int): number of callback generated automatically based on the timer set in the callback

        Returns:
            go.Figure: Figure instance containing all the information
        """
        t = np.linspace(0, n, 10 * n)
        print(n)
        x, y, z = np.cos(t), np.sin(t), t

        fig = go.Figure(data=[go.Scatter3d(x=x, y=y, z=z,
                                           mode='markers')])
        fig.update_layout(
            scene = dict(
                    xaxis = dict(nticks=4, range=[-500,200],),
                    yaxis = dict(nticks=4, range=[-900,1600],),
                    zaxis = dict(nticks=4, range=[-800,300],)))
        return fig


    def _plot_3d_frame_data(self,n: int) -> go.Figure:
        """plot 3d skeleton data based on the frame count

        Args:
            n (int): number of the callback generated automatically based on the timer set in the callback

        Returns:
            go.Figure: Figure instance containing all the information
        """
        # print(self.frame_counter)
        self.frame_counter += 1
        if  self.frame_counter > len(self.openpose_3d_data[:,1,1]):
            self.frame_counter = 0
        fig = self._plot_frame(self.frame_counter)
        fig = go.Figure(data=fig)
        fig.update_layout(
            scene = dict(
                    xaxis = dict(nticks=4, range=[-500,500],),
                    yaxis = dict(nticks=4, range=[-900,1600],),
                    zaxis = dict(nticks=4, range=[-800,500],)),
            # change this based on the browser
            width = 2000,
            height = 1000,
            # camera = dict(eye=dict(x=0., y=2.5, z=0.))
        )
        return fig


    def _plot_frame(self,frame_id: int) -> List:
        """Plot all the bodies in the frame

        Args:
            frame_id (int): frame number to plot

        Returns:
            List: list of the all the scatter3d instance
        """
        fig_instance = []
        for body_part in self.body_parts:
            print(body_part.get_name())
            fig_instance.append(self._plot_data_points(frame_id, body_part))
            # go.Figure(fig_instance).show()
        return fig_instance


    def _plot_data_points(self, frame_id:int, body_part:int, mode:str = 'lines+markers') -> go.Scatter3d:
        """plot data points for each body

        Args:
            frame_id (int): frame number
            body_part (main_data_class): body path dataclass 
            mode (str, optional): type of graph for only markers use 'markers'. Defaults to 'lines+markers'.

        Returns:
            go.Scatter3d: instance of the Scatter3d plot
        """

        # I will go step by step for clear understanding, but can be oprtimized
        mark_pose = body_part.get_values()
        marker_data = self.openpose_3d_data[frame_id,mark_pose,:]
        x_data = marker_data[:,0]
        y_data = marker_data[:,1]
        z_data = marker_data[:,2]

        # deal with nan value or else scatter is not plotting anything
        x_data = x_data[~np.isnan(x_data)]
        y_data = y_data[~np.isnan(y_data)]
        z_data = z_data[~np.isnan(z_data)]

        # x_data, y_data, z_data needs to be rotated
        # TODO: add a method to handle the 3d rotation.
        fig_instance = go.Scatter3d(x=x_data, y=z_data,
                                    z=y_data * -1, mode=mode, name = body_part.get_name())
        print(x_data, y_data, z_data)
        return fig_instance





if __name__ == "__main__":
    freemocap_app().app.run_server(port=8888, debug =True)
    # freemocap_app()
