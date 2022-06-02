from dash import html, dcc, callback, Dash
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
import json


#Carregando Json do arquivo
geojson = json.load(open('./br_states.json'))

#Cria dataframe com os dados
database = pd.read_csv('./dados.csv')

#Criação do mapa cloroplético
fig = px.choropleth_mapbox(database, locations = 'UF',
                            geojson=geojson,
                            color='QUANTIDADE',
                            hover_name='Estado',
                            hover_data=['UF', 'Regiao', 'QUANTIDADE'],
                            title="Mapa Interativo",
                            mapbox_style = 'carto-darkmatter',
                            center={"lat":-14, "lon": -55},
                            zoom=3,
                            opacity=0.8,

)
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})


# Create dictionary of list
database_list = database[['Estado', 'latitude', 'longitude']]
dict_of_locations = database_list.set_index('Estado')[['latitude', 'longitude']].T.to_dict('dict')




# criando um grid
grid = html.Div(
    [
        html.Div([
            html.H3('Mapa Interativo', style={'margin-bottom': '10px', 'color':'white', 'textAlign':'center'}),
            html.Div('Selecione a região', className='fix_label', style={'color': 'white'}),
            dcc.Dropdown(id='w_countries',
                         multi=False,
                         searchable=True,
                         value='Nordeste',
                         placeholder='Selecione a Região',
                         options=[{'label': c, 'value': c}
                                  for c in (database['Regiao'].unique())], className='dcc_compon'),

            html.Div('Selecione o estado', className='fix_label', style={'color': 'white'}),
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
    #brand="TESTE - Mapa do Trabalho Infantil no Brasil",
    brand_href="index",
    color="primary",
    #color="Red",
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
                 dcc.Graph(id = 'mapa-interativo', figure=fig, config={'displayModeBar': False})

            ], className='create_container six columns' ),

            html.Div([
                 dcc.Graph(id = 'bar_chart', config={'displayModeBar': False})

            ], className='create_container six columns'),


        ], className='row flex-display')

        )

    ]
)


@callback(Output('w_countries1', 'options'),
          [Input('w_countries', 'value')])
def update_country(w_countries):
    dados3 = database[database['Regiao'] == w_countries]
    return [{'label': i, 'value': i} for i in dados3['Estado'].unique()]


@callback(Output('w_countries1', 'value'),
          [Input('w_countries1', 'options')])
def update_country(w_countries1):
    return [k['value'] for k in w_countries1][0]

#Início da callback do gráfico de barras

@callback(Output('bar_chart', 'figure'),
              [Input('w_countries','value')],
              [Input('w_countries1','value')])
def update_graph(w_countries, w_countries1):
    dados5 = database.groupby(['UF', 'Regiao', 'Estado'])[['QUANTIDADE']].sum().reset_index()
    dados6 = dados5[(dados5['Regiao'] == w_countries)]


    return {
         'data': [go.Bar(
                x=dados6['Estado'],
                y=dados6['QUANTIDADE'],
                text = dados6['QUANTIDADE'],
                texttemplate='%{text:,.0f}',
                textposition='auto',
                name='injured',
                marker=dict(color='#9C0C38'),
                hoverinfo='text',
                hovertext=
                '<b>UF</b>: ' + dados6['UF'].astype(str) + '<br>' +
                '<b>Estado</b>: ' + dados6['Estado'].astype(str) + '<br>' +
                '<b>Região</b>: ' + dados6['Regiao'].astype(str) + '<br>' +
                '<b>Quantidade</b>: ' + dados6['QUANTIDADE'].astype(str) + '<br>'

            ),

        ],


        'layout': go.Layout(
            barmode = 'stack',
            title={'text': 'Quantidade de registro por estado na região: ' + (w_countries) + ' ' + '<br>',
                   'y': 0.93,
                   'x': 0.5,
                   'xanchor': 'center',
                   'yanchor': 'top'},
            titlefont={'color': 'white',
                       'size': 20},
            font=dict(family='sans-serif',
                      color='white',
                      size=12),
            hovermode='closest',
            paper_bgcolor='#010915',
            plot_bgcolor='#010915',
            legend={'orientation': 'h',
                    'bgcolor': '#010915',
                    'xanchor': 'center', 'x': 0.5, 'y': -0.7},
            margin=dict(r=0),
            xaxis=dict(title='<b>Estados</b>',
                       tick0 = 0,
                       dtick = 1,
                       color = 'white',
                       #showline=True,
                       showgrid=True,
                       showticklabels=True,
                       linecolor='white',
                       linewidth=1,
                       ticks='outside',
                       tickfont=dict(
                           family='Aerial',
                           color='white',
                           size=12
                       )),
            yaxis=dict(title='<b>Quantidade</b>',
                       color='white',
                       showline=True,
                       showgrid=True,
                       showticklabels=True,
                       linecolor='white',
                       linewidth=1,
                       ticks='outside',
                       tickfont=dict(
                           family='Aerial',
                           color='white',
                           size=12
                       )
                       )


        )
    }

#Fim da callback do gráfico de barras


@callback(
    Output('mapa_inte-display-value', 'children'),
    Input('drop-down-mapa_inte', 'value'))
def display_value(value):
    return f'You have selected {value}'
