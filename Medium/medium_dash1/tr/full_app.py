import numpy as np
import pandas as pd
import dash
import dash_table
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from plotly import graph_objects as go
import plotly.express as px
import warnings

renk1="#782525"
renk2="#052F5A"
renk3="#a5c5c7"
renk4="#672a2a"
renk5="#908c8c"

df=pd.read_csv("train.csv")

warnings.filterwarnings('ignore')

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
app.config.suppress_callback_exceptions = True

#-----------------------BURADAN ITIBAREN LAYOUT KISMI-----------------------
app.layout = html.Div([
        html.H2('DashBoard with plotly dash'),

    dbc.Card(
        dbc.CardBody([
            dbc.Row([
                dbc.Col(html.Div(dcc.Graph(id='graf1')),width=4),
                dbc.Col(dash_table.DataTable(id='table2',
                                             data=[{}], #callbackten gelen datalarla şekillenecek
                                             columns= [{'id': c, 'name': c} for c in 
                                             ["VARs",1870, 1880, 1890, 1900, 1910, 1920,1930, 1940, 1950, 1960, 1970,1980, 1990, 2000, 2010]],
                                            # #Görünmesini istediğimiz değişken başlıkları
                                              
                                            
                                            fixed_rows={ 'headers': True, 'data': 0},
                                            style_header={'backgroundColor': renk4},
                                            style_cell={
                                                'backgroundColor':renk5,
                                                'color': 'white',
                                                'whiteSpace': 'normal',
                                                'textOverflow': 'ellipsis',
                                                'height': 'auto',
                                                'overflow': 'hidden',
                                                'maxWidth': 0
                                                },
                                            virtualization=False,
                                            style_table={'height': 345},
                                            page_action='none', page_size=5
                                            ),width=8)
            ]),

        ], style={'background-color': renk1}) #Bulunulan row'un bg rengi
    ),

            dbc.Row([
                dbc.Col([
                    html.Div([
                        dcc.RadioItems(id='bar-type1', 
                                value="stack", #default olarak seçili gelecek seçenek
                                options=[{'value': x, 'label': x} for x in ["stack","group"]],
                                labelStyle={"float":"left","padding-right":"40px"}
                )])]),

                dbc.Col([
                    html.Div([
                         dcc.Dropdown(id='line-var1',
                                     options=[{'label': i.title(), 'value': i} for i in ['MSSubClass', 'LotFrontage','MasVnrArea',
                                                                            'BsmtFinSF2', 'BsmtUnfSF', 'TotalBsmtSF', '1stFlrSF', '2ndFlrSF',
                                                                            'LowQualFinSF', 'GrLivArea', 'BsmtFullBath', 'BsmtHalfBath', 'FullBath',
                                                                             'SalePrice']],
                                value=["MSSubClass","MasVnrArea","LotFrontage"],
                                multi=True) #False olduğu durumda dropdowndan tek değişken seçilebiliyor olucak
                    ],style={"margin-right":"40px",'width': '475px',"float":"right", 'display': 'inline-block'})
                ])]),
    
    dbc.Card(
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    html.Div([
                        dcc.Dropdown(id='pie-var1',
                                    options=[{'label': i.title(), 'value': i} for i in ["Heating","HeatingQC","CentralAir","Electrical"]],
                                    value="Heating",
                                    clearable=False)
                    ],style={'width': '80%', 'display': 'inline-block'}),
                    (html.Div(dcc.Graph(id="graf3")))],width=3),

                

                dbc.Col(html.Div(dcc.Graph(id='graf4')),width=4),
                dbc.Col(html.Div(dcc.Graph(id="graf5")),width=5)
            ])
        ], style={'background-color': renk1,"margin-top":"2px"})
    )
],style={'background-color':"#f9eded"})



#-----------------------BURADAN ITIBAREN CALLBACK KISMI-----------------------

@app.callback(Output("graf1","figure"), #return ile dönen grafik yukarıda "graf1" konumunda görünecek
                Input("bar-type1","value")) #yukarıda bar-type1 olarak belirlenen seçenek burada fonsiyonumuza girdi olarak gelecek
def graf1_barchart(typee): #bar-type1 ile gelen değer=typee
    son10=df[df["YearBuilt"]>2000].reset_index(drop=True)
    brr=px.bar(son10,x="YearBuilt",y="SalePrice",color="LotShape", barmode=typee)
    brr.update_layout(height=360,  title='2000 Sonrasında İnşa Edilen Evlerin Kümülatif Fiyatları', paper_bgcolor=renk3)
    return brr

@app.callback(Output("table2","data"),
                Input("pie-var1","value"))
def table2_df(variable):
    gr=df.groupby((df["YearBuilt"]//10)*10).mean()
    grT=gr.T
    grT.insert(0, 'VARs', grT.index) #Kolon isimleri ile yukarıda belirlediğimiz görünür kolon isimleri birebiraynı olmalı
    tble=np.round(grT,3).to_dict("records") #dashtable yapısı gereği girdi olarak dict formatında göndermemiz gerekiyor veriyi
    return tble


@app.callback(Output("graf3","figure"),
                Input("pie-var1","value"))
def graf3_pie(variable):
    print(variable)
    aa=df.groupby(variable)["SalePrice"].mean()

    fig = px.pie(df, values=aa,names=aa.index,labels=aa.index.values, color_discrete_sequence=px.colors.sequential.RdBu)
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(height=370,  title=str(variable)+" 'a Göre Ort Satış Bedelleri ve Dağılım ", paper_bgcolor=renk3)
    return fig



@app.callback([Output("graf5","figure"), #Bu şekilde tek fonksiyon/callbackten birden fazla çıktı almak da mümkün
                Output("graf4","figure")],
                Input("line-var1","value")) #
def graf4_5_multi(var):
    every_5=df.groupby((df["YearBuilt"]//5)*5).mean() #beşer yıllık ortalamaları alma
    every_5["ind"]=every_5.index 
    df_melt = every_5.melt(id_vars='ind', value_vars=var) #sağlıklı bir px.line plot için format değişikliği
    multi_line=px.line(df_melt, x='ind' , y='value' , color='variable')
    multi_line.update_layout(height=410,  title='Seçilen Değişkenlerin \n 5 Yıllık Ortalama Değerleri', paper_bgcolor=renk3)



    #CORR
    corrr=df[["SalePrice","OverallQual","GrLivArea","GarageCars", #Bunları rastgele atadım corr hesabı için
                  "GarageArea","GarageYrBlt","TotalBsmtSF","1stFlrSF","FullBath",
                  "TotRmsAbvGrd","YearBuilt","YearRemodAdd"]].corr()
    trace = go.Heatmap(z=corrr.values,
                  x=corrr.index.values,
                  y=corrr.columns.values,
                  type = 'heatmap',
                  colorscale = 'Cividis')
    
    data=[trace]
    corr=go.Figure(data)
    corr.update_layout(height=410,  title='Correlations', paper_bgcolor=renk3)
    return multi_line,corr


if __name__ == "__main__":
    app.run_server(debug=False)

