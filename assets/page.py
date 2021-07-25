

import abc

import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output


# making a super for the general information storing
class page(object):
    def __init__(self, name:str, url: str):
        self.name = name
        self.url = url
        self.loaded = False

    @abc.abstractmethod
    def content(self):
        pass

