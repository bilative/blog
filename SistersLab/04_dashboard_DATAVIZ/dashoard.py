# -*- coding: utf-8 -*-\

from dash_core_components.Dropdown import Dropdown
import plotly.graph_objects as go
import plotly.express as px
from dash.dependencies import Input, Output
import dash
import dash_html_components as html
import dash_core_components as dcc
import pandas as pd
import dash_bootstrap_components as dbc
import dash_table

from libs.helpy import preprocess

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


df = pd.read_csv('bodyfat.csv')
df = preprocess(df)


def bosGun():
    v1 = 5
    v3 = 6
    fig = go.Figure(go.Indicator(
        mode="number+delta",
        value=v1,
        delta={"reference": 808, "valueformat": ".0f"},
        title={"text": "NULLTABLE"},
        domain={'y': [0, 1], 'x': [0.25, 0.75]}))
    fig.add_trace(go.Scatter(
        y=[v3, v3, v3, v3, v3, v3, v3, v3, v3, v3, v3, v3, v3, v3, v3]))
    bosGun = fig
    return bosGun



app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
    dbc.Card([
        dbc.CardBody([html.H2('Kaggle BodyFat Verisi Ozet Bilgileri', style={'textAlign': 'center'})],style={'backgroundColor':'#FDDBC4'}),
        html.Hr(),
        dbc.CardBody([
            html.H3("BMI Skoru Ile Karsilastirmak Istediginiz Degiskeni Seciniz!"),
            dcc.Dropdown(id='dropdown-1',
                                value = 'BodyFat',
                                options=[
                                    {'label': 'BodyFat','value': 'BodyFat'},
                                    {'label': 'Age', 'value': 'Age'},
                                    {'label': 'Abdomen', 'value': 'Abdomen'},
                                    {'label': 'Ankle', 'value': 'Ankle'},
                                    {'label': 'Biceps', 'value': 'Biceps'}
                                ], style={'width' : '50%'}),
            dbc.Row([
                dbc.Col(
                    dcc.Graph(id='first-one')
                ),
                dbc.Col([
                    html.H4("Bazi Gozlem Bilgileri"),
                    dash_table.DataTable(
                        id='df-table',
                        columns=[{"name": i, "id": i} for i in ['BodyFat', 'Age', 'Weight', 'Height', 'Neck', 'Chest', 'Abdomen', 'Biceps', 'bmi', 'bmi_sonuc']],
                        page_size=10,
                        style_header={
                            'backgroundColor': 'rgb(30, 30, 30)', 'fontWeight': 'bold'
                        },
                        style_cell={
                            'backgroundColor': 'rgb(50,50,50)',
                            'color':'white',
                            'whiteSpace':'normal'
                        }
                    )])
            ]),
            html.Hr(),
            dbc.Row([
                dbc.Col(
                    dcc.Graph(id='third-one')
                ),
                dbc.Col(
                    dcc.Graph(id='fourth-one')
                )
            ])
        ],style={'backgroundColor':'#FCF5C7'})
    ])
])


@app.callback([Output('first-one', 'figure'),
                Output('df-table', 'data'),
                Output('third-one', 'figure'),
                Output('fourth-one', 'figure')],
              Input('dropdown-1', 'value'))
def deneme(dropdown_value):
    scatter_plot = px.scatter(df, x='bmi', y=dropdown_value , title= f'BMI Skoru ve {dropdown_value} Korelasyonu')
    scatter_plot.update_layout(
                plot_bgcolor = "#e6f0ff",
                paper_bgcolor = "#cce0ff")

    gBy = df.groupby('bmi_sonuc')[dropdown_value].mean()
    bar_plot = px.bar(gBy, title= f'BMI Grubuna Gore {dropdown_value} Ortalamalari')
    bar_plot.update_layout(
                plot_bgcolor = "#e6f0ff",
                paper_bgcolor = "#cce0ff")

    pie_chart = px.pie(df,
             values = 'counts',
             names = 'bmi_sonuc',
             title = 'BMI Gruplarina Gore Yuzdesel Dagilim')
    pie_chart.update_traces(textinfo = 'percent+label')

    data = df.to_dict('records')
    return scatter_plot, data, bar_plot, pie_chart


if __name__ == '__main__':
    app.run_server(debug=False)
