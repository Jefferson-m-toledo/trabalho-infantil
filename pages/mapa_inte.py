from dash import html, dcc, callback
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
import dash_bootstrap_components as dbc

database = pd.read_csv('./dados.csv')

# Create dictionary of list
database_list = database[['Estado', 'latitude', 'longitude']]
dict_of_locations = database_list.set_index('Estado')[['latitude', 'longitude']].T.to_dict('dict')


# criando um grid
grid = html.Div(
    [
        html.Div([
            html.P('Selecione a Região', className='fix_label', style={'color': 'white'}),
            dcc.Dropdown(id='w_countries',
                         multi=False,
                         searchable=True,
                         value='Nordeste',
                         placeholder='Selecione a Região',
                         options=[{'label': c, 'value': c}
                                  for c in (database['Regiao'].unique())], className='dcc_compon'),

            html.P('Selecione o Estado', className='fix_label', style={'color': 'white'}),
            dcc.Dropdown(id='w_countries1',
                         multi=False,
                         searchable=True,
                         placeholder='Selecione o estado',
                         options=[], className='dcc_compon'),
        ], className='create_container three columns'),
    ]
)
# inserindo a navbar
navbar = dbc.NavbarSimple(
    children=[
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("Início", href="index", id='index-link'),
                dbc.DropdownMenuItem("Mapa Interativo", href="mapa_inte", id='mapa_inte-link'),
                dbc.DropdownMenuItem("Análise por Região", href="mapa_regiao", id='mapa-regiao-link'),
                dbc.DropdownMenuItem("Gênero e Tipo de trabalho", href="mapa_trabalho", id='mapa-trabalho-link'),
                dbc.DropdownMenuItem("Análise por período", href="mapa_periodo", id='mapa_periodo'),
            ],
            nav=True,
            in_navbar=True,
            label="Mais",
            id="drop-down-mapa_inte"
        ),
    ],
    brand="Mapa do Trabalho Infantil no Brasil",
    brand_href="index",
    color="primary",
    dark=True,
)

# montagem do layout
layout = html.Div(
    [
        html.Div(id='mapa_inte-display-value'),
        # inserindo a navbar
        navbar,
        dbc.Container(
            [
                grid
            ]
        ),
        html.Br(),
        dbc.Container(
        html.Div([
            html.Div([
                dcc.Graph(id='map_chart', config={'displayModeBar': 'hover'})

            ], className='create_container twelve columns')

        ], className='row flex-display'),)

    ]
)

@callback(Output('map_chart', 'figure'),
              [Input('w_countries','value')],
              [Input('w_countries1','value')])
def update_graph(w_countries, w_countries1):
    dados8 = database.groupby(['UF','Regiao', 'Estado','latitude', 'longitude'])[['QUANTIDADE']].sum().reset_index()
    dados9 = dados8[(dados8['Regiao'] == w_countries) &
                 (dados8['Estado'] == w_countries1)]

    if w_countries1:
        zoom=3
        zoom_lat = dict_of_locations[w_countries1]['latitude']
        zoom_long = dict_of_locations[w_countries1]['longitude']



    return {
        'data': [go.Scattermapbox(
            lon=dados9['longitude'],
            lat=dados9['latitude'],
            mode='markers',
            marker=go.scattermapbox.Marker(size=dados9['QUANTIDADE'],
                                           color=dados9['QUANTIDADE'],
                                           colorscale='HSV',
                                           showscale=False,
                                           sizemode='area',
                                           opacity=0.3),
            hoverinfo='text',
            hovertext=
            '<b>UF</b>: ' + dados9['UF'].astype(str) + '<br>' +
            '<b>Estado</b>: ' + dados9['Estado'].astype(str) + '<br>' +
            '<b>Região</b>: ' + dados9['Regiao'].astype(str) + '<br>' +
            '<b>Registros</b>: ' + dados9['QUANTIDADE'].astype(str) + '<br>'


        )],

        'layout': go.Layout(
            hovermode='x',
            paper_bgcolor='#010915',
            plot_bgcolor='#010915',
            margin=dict(r=0, l =0, b = 0, t = 0),
            mapbox=dict(
                accesstoken='pk.eyJ1IjoicXM2MjcyNTI3IiwiYSI6ImNraGRuYTF1azAxZmIycWs0cDB1NmY1ZjYifQ.I1VJ3KjeM-S613FLv3mtkw',
                center = go.layout.mapbox.Center(lat=zoom_lat, lon=zoom_long),
                style='dark',
                # style='open-street-map',
                zoom=zoom,
            ),
            autosize=True

        )
    }


@callback(Output('w_countries1', 'options'),
          [Input('w_countries', 'value')])
def update_country(w_countries):
    dados3 = database[database['Regiao'] == w_countries]
    return [{'label': i, 'value': i} for i in dados3['Estado'].unique()]


@callback(Output('w_countries1', 'value'),
          [Input('w_countries1', 'options')])
def update_country(w_countries1):
    return [k['value'] for k in w_countries1][0]


@callback(
    Output('mapa_inte-display-value', 'children'),
    Input('drop-down-mapa_inte', 'value'))
def display_value(value):
    return f'You have selected {value}'
