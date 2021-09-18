import pandas as pd
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import warnings
import datetime
import dash_table

header_color = '#C2B2AD'
card_color = '#BAA9C6'
bg_color = '#F5F5F5'


df = pd.read_csv('_ehir Tiyatrolar_nda Sahnelenen Oyunlar Verisi.csv')
df['PLAY_DATE'] = pd.to_datetime(df['PLAY_DATE'])
# csv'den okunan tarih degiskeni object olarak gorunebiliyor, buna engel olmak icin

tiyatrolar = df['THEATER_NAME'].value_counts()[df['THEATER_NAME'].value_counts() > 30].index
# 30'dan fazla oyun sahnelenmis tiyatro salonlarini Dropdownda listeyecegiz

REFRESH_INTERVAL = dcc.Interval(
    id='interval-component', interval=12*150005, n_intervals=0)
p1_layout = html.Div([
    dbc.CardBody(
        dbc.CardBody([
            html.H2('Istanbul Sehir Tiyatrolari - Sahnelenen Oyunlar',
                    style={'textAlign': 'center'}),
            html.H6('SistersLab Veri Gorsellestirme Serisi - Final',
                    style={'textAlign': 'center'})], style={'backgroundColor': header_color})),
    dbc.CardBody(
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    html.Hr(),
                    html.H5("Tiyatro Sec:"),
                    html.Div([dcc.Dropdown(
                        id='select-categorical',
                        options=[{"label": str(col), "value": str(col)}
                                 for col in tiyatrolar],
                        value='Fatih Reşat Nuri Sahnesi')], style={'padding-bottom': '15px'}),
                    html.Div([dbc.Button("Random Sec", id='random-secim',
                             color="primary", className="mr-1")], style={'padding-bottom': '15px'}),

                    html.Hr(),
                    html.H5("Tarih Araligi Sec: "),
                    dcc.DatePickerRange(
                        id='date-picker',
                        min_date_allowed=df['PLAY_DATE'].min(),
                        max_date_allowed=df['PLAY_DATE'].max(),
                        initial_visible_month=datetime.datetime(2019, 1, 1),
                        start_date=df['PLAY_DATE'].min(),
                        end_date=df['PLAY_DATE'].max(),
                    ),
                    html.Hr(),
                    html.H6("Sagdaki kenarda hangi grafik olsun?"),
                    html.Div([dbc.RadioItems(
                        id="choose-graph",
                        options=[
                            {"label": "Pie Chart", "value": 'pie'},
                            {"label": "Map", "value": 'map'},
                            {"label": "Histogram", "value": 'hist'}
                        ],
                        value='pie',
                    )], style={'padding-top': '15px'})
                ], width=2),
                dbc.Col([
                    dcc.Graph(id='first-one')
                ], width=6),
                dbc.Col([
                    dcc.Graph(id='second-one')
                ], width=4)
            ])
        ], style={'background-color': card_color})
    ),
    dbc.CardBody(
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    dcc.Graph(id='third-one')
                ], width=6),
                dbc.Col([
                    dash_table.DataTable(
                        id='data-table',
                        columns=[{"name": i, "id": i} for i in [
                            'PLAY_DATE', 'PLAY_NAME', 'PLAY_CATEGORY', 'PLAY_TYPE', 'NUMBER_OF_AUDIENCE']],
                        page_size=13,
                        style_header={
                            'backgroundColor': 'rgb(30, 30, 30)', 'fontWeight': 'bold'
                        },
                        style_cell={
                            'backgroundColor': 'rgb(60,60,60)',
                            'color': 'white',
                            'whiteSpace': 'normal'
                        }
                    )
                ], width=6)
            ])
        ], style={'background-color': card_color})),
    REFRESH_INTERVAL
], style={'background-color': bg_color})
