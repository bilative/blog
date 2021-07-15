
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

df=pd.read_csv("train.csv")
pie_options=[{'label': i.title(), 'value': i} for i in ["Heating","HeatingQC","CentralAir","Electrical"]]

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div([
    html.H6("DROPDWN BIR KATEGORIK DEGISKENI SECINIZ"),
    html.Div([dcc.Dropdown(id='dropdowndan-secilen-deger',
                            options=pie_options,
                            value="Heating")],
                            style={"width":"40%"}),
    html.Br(),
    html.Div(html.Div(dcc.Graph(id="grafik1"))),
])

@app.callback(Output("grafik1","figure"),
                Input("dropdowndan-secilen-deger","value"))

def graf3_pie(var):
    gruplanmis_df=df.groupby(var)["SalePrice"].mean()
    pie_chart = px.pie(gruplanmis_df,
                            values=gruplanmis_df,
                            names=gruplanmis_df.index,
                            labels=gruplanmis_df.index.values)
    return pie_chart

if __name__ == '__main__':
    app.run_server(debug=False)
