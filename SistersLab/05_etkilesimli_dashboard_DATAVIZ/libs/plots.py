import plotly.express as px
import pandas as pd

plot_bg_color = '#E1ECFF'
plot_inner_color = '#F3F3F3'


def mark_on_map(df):
    fig = px.scatter_mapbox(df, lat='LATITUDE', lon='LONGITUDE', zoom=11, size='LONGITUDE',
                            #center = dict(lat = float(infos['Saat']), lon = float(infos['Enlem(N)'])),
                            #z = 'NUMBER_OF_AUDIENCE' ,
                            mapbox_style="stamen-terrain")
    fig.update_layout(
        title=f"{df.loc[0, 'THEATER_NAME']} Harita Uzerinde Konumu",
        showlegend=False,
        margin=dict(l=10, r=10, t=40, b=10),
        paper_bgcolor=plot_bg_color
    )
    fig.update_coloraxes(showscale=False)
    return fig


def bar_plot(df):
    first_15 = pd.DataFrame(df['PLAY_NAME'].value_counts()[:15])
    first_15['oyun'] = first_15.index

    fig = px.bar(first_15, x='oyun', y='PLAY_NAME', color='oyun')
    fig.update_layout(
        title=f"{df.loc[0, 'THEATER_NAME']} En Cok Izlenen Ilk {first_15.shape[0]} Oyun Seyirci Sayilari",
        showlegend=False,
        xaxis_title="Oyun Isimleri",
        yaxis_title="Toplam Izlenme Sayilari",
        margin=dict(l=10, r=10, t=40, b=10),
        plot_bgcolor=plot_inner_color,
        paper_bgcolor=plot_bg_color
    )
    return fig


def sunburst(df):
    fig = px.sunburst(df, path=['PLAY_CATEGORY', 'PLAY_TYPE', 'PLAY_NAME'],
                      color='PLAY_CATEGORY',
                      color_continuous_scale='RdBu',
                      values='NUMBER_OF_AUDIENCE')
    fig.update_layout(
        title=f"{df.loc[0, 'THEATER_NAME']} Kategorilere Gore Seyirci Sayilari",
        showlegend=False,
        paper_bgcolor=plot_bg_color
    )
    return fig


def hist_plot(df):
    fig = px.histogram(df['NUMBER_OF_AUDIENCE'], nbins=1000)
    fig.update_layout(
        title=f"{df.loc[0, 'THEATER_NAME']} Izleyici Sayilari Dagilimi",
        showlegend=False,
        xaxis_title="Izleyici Sayisi",
        yaxis_title="Frekans",
        plot_bgcolor=plot_inner_color,
        paper_bgcolor=plot_bg_color
    )
    return fig


def line_plot(df):
    df_grouped = df.groupby('PLAY_DATE')['NUMBER_OF_AUDIENCE'].sum()
    df.reset_index(drop=True, inplace=True)
    fig = px.line(x=df_grouped.index, y=df_grouped)
    fig.update_layout(
        title=f"{df.loc[0, 'THEATER_NAME']} Zamana Gore Izleyici Sayilari",
        showlegend=False,
        xaxis_title="Tarih (Secili Zaman Araliginda)",
        yaxis_title="Izleyici Sayisi",
        plot_bgcolor=plot_inner_color,
        paper_bgcolor=plot_bg_color
    )
    return fig
