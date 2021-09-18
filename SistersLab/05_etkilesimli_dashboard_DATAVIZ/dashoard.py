# -*- coding: utf-8 -*-\

import plotly.graph_objects as go
import pandas as pd
import dash
import dash_bootstrap_components as dbc
from dash_bootstrap_components._components.CardBody import CardBody
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from dash_html_components.P import P
from numpy.lib.function_base import select
import plotly.express as px
import warnings
import datetime
import dash_table
import random
from libs.plots import *
from libs.helpy import BUTTON
from libs.helpy import time_filter
from libs.views.page1 import p1_layout


df = pd.read_csv('_ehir Tiyatrolar_nda Sahnelenen Oyunlar Verisi.csv')
print(df.shape)
button = BUTTON(0)


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
app.layout = p1_layout

@app.callback([Output("first-one", "figure"),
               Output("second-one", "figure"),
               Output("third-one", "figure"),
              Output("data-table", "data")],
              [Input('date-picker', 'start_date'),
              Input('date-picker', 'end_date'),
              Input("select-categorical", "value"),
              Input('choose-graph', 'value'),
              Input('random-secim', 'n_clicks')])
def toggle_active_links(start_date_, end_date_, category, graph_type, clicky):
    df['PLAY_DATE'] = pd.to_datetime(df['PLAY_DATE'])

    is_it_new = button.isNew(clicky)
    if is_it_new:
        # eger butona tiklandi ise random THEATER_NAME secimi yapar
        unique_theaters = list(set(df['THEATER_NAME']))
        random_selected = random.choice(unique_theaters)
        selected = df[df['THEATER_NAME'] == random_selected]
    else:
        # Dropdown'dan secilen tiyatroya gore dataseti filtreler
        selected = df[df['THEATER_NAME'] == str(category)]

    selected = time_filter(selected, start_date_, end_date_)
    #selected = selected[selected['THEATER_NAME'] == str(category)]
    selected = selected.sort_values(by='PLAY_DATE')

    line_plot_ = line_plot(selected)

    bars_ = bar_plot(selected)

    if graph_type == 'map':
        plot_selected = mark_on_map(selected)
    elif graph_type == 'pie':
        plot_selected = sunburst(selected)
    else:
        plot_selected = hist_plot(selected)

    selected.sort_values(by='NUMBER_OF_AUDIENCE', ascending=False, inplace=True)
    selected['PLAY_DATE'] = selected['PLAY_DATE'].astype(str)

    return line_plot_, plot_selected, bars_, selected.to_dict('records')


if __name__ == '__main__':
    app.run_server(debug=False, port=8050)
