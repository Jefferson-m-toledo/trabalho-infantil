from dash import html, dcc, callback, Dash
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
import json

# Carregando Json do arquivo
geojson = json.load(open('./geoBrasil.json'))

database = pd.read_csv('./dados_tratados/database.csv')

options_region = [{'label': 'Todas', 'value': 'Todas', 'label': c, 'value': c} for c in (database['Regiao'].unique())]
options_region.append({'label': 'Todas', 'value': 'Todas'})

# Importa CSV
df_idade_atividade = pd.read_csv('./dados_tratados/populacao_uf_idade.csv')

#Importa CSV Idade, Faixa etária e trabalho
df_faixa_etaria_atividade = pd.read_csv('./dados_tratados/trab_infantil_sexo_idade_atividade.csv')

# Cria datafame a partir do CSV apenas com os dados de menores de idade (Idade <= 17)
dados_idade = df_idade_atividade.loc[df_idade_atividade.Idade <= 17, ['UF', 'Estado', 'AtividadeEconomica', 'Idade', 'Trabalhadores', 'Populacao']]


fig = px.choropleth_mapbox()

# Create dictionary of list
database_list = database[['Estado', 'latitude', 'longitude']]
dict_of_locations = database_list.set_index('Estado')[['latitude', 'longitude']].T.to_dict('dict')

# criando um grid
grid = html.Div(
    [
        html.Div([
            html.H3('Mapa Interativo', style={'margin-bottom': '10px', 'color': 'white', 'textAlign': 'center'}),
                dbc.Row([
                    dbc.Col([
                        html.Div('Selecione a região', className='fix_label', style={'color': 'white'}),
                        dcc.Dropdown(id='w_countries',
                                     multi=False,
                                     searchable=True,
                                     value='Todas',
                                     placeholder='Selecione a Região',
                                     options=options_region, className='dcc_compon'),
                    ]),

                    dbc.Col([
                        html.Div('Selecione o estado', className='fix_label', style={'color': 'white'}),
                        dcc.Dropdown(id='w_countries1',
                                     multi=False,
                                     searchable=True,
                                     # value='',
                                     placeholder='Selecione o estado',
                                     options=[], className='dcc_compon'),
                        ])
                    ])
        ], className='create_container three columns'),
    ]
)
# inserindo a navbar
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Início", href="index"), id="index-link"),
        dbc.NavItem(dbc.NavLink("Saiba Mais", href="saiba_mais"), id="saiba_mais-link"),
        dbc.NavItem(dbc.NavLink("Mapa Interativo", href="mapa_inte"), id="mapa_inte-link"),
        dbc.NavItem(dbc.NavLink("Análise por Idade", href="mapa_idade"), id="mapa-idade-link"),
        dbc.NavItem(dbc.NavLink("Gênero e Trabalho", href="mapa_genero"), id="mapa-genero-link"),
    ],
    brand="Mapa do Trabalho Infantil",
    brand_href="index",
    color="primary",
    dark=True,
    id="nav-bar",
    style={'background': 'linear-gradient(145deg, #375ee3 0%, #6543e0 80%)',
           'boxShadow': '0 1px 2px rgb(0 0 0 / 30%)',
            'color': 'rgba(255, 255, 255, 0.7)',
            'fontSize': '16px',
            'fontWeight': '400'}
)

# montagem do layout
layout = html.Div(
    [
        html.Div(id='mapa_inte-display-value', style={'display': 'none'}),
        navbar,
        dbc.Container(
            [
                grid
            ]
        ),
        html.Br(),
        dbc.Container(
            html.Div([
                    dcc.Graph(id='mapa-interativo', figure=fig, config={'displayModeBar': False}, style={'marginTop': '15px'}),
                    dcc.Graph(id='bar_chart', config={'displayModeBar': False}, style={'margin': '50px 0'})
            ], className='row flex-display')

        ),
        html.Div(id='modal')

    ]
)


## TESTE MAPA CLOROPLÉTICO
@callback(Output('mapa-interativo', 'figure'),
          [Input('w_countries1', 'value')])
def display_choropleth(w_countries1):
    df = database.groupby(['UF', 'Regiao', 'Estado'])[['QUANTIDADE']].sum().reset_index()
    if w_countries1:
        zoom = 5
        zoom_lat = dict_of_locations[w_countries1]['latitude']
        zoom_long = dict_of_locations[w_countries1]['longitude']
        fig = px.choropleth_mapbox(df, locations='UF',
                                   geojson=geojson,
                                   color='QUANTIDADE',
                                   #featureidkey="feature.id",
                                   hover_name='Estado',
                                   hover_data=['UF', 'Regiao', 'QUANTIDADE'],
                                   title="Mapa Interativo",
                                   mapbox_style='white-bg',
                                   center={"lat":zoom_lat,"lon": zoom_long},
                                   zoom=zoom,
                                   opacity=0.8,
                                   )
        fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

    else:
        fig = px.choropleth_mapbox(df, locations='UF',
                                   geojson=geojson,
                                   color='QUANTIDADE',
                                   # featureidkey="feature.id",
                                   hover_name='Estado',
                                   hover_data=['UF', 'Regiao', 'QUANTIDADE'],
                                   title="Mapa Interativo",
                                   mapbox_style='white-bg',
                                   center={"lat": -14, "lon": -55},
                                   zoom=3,
                                   opacity=0.8,
                                   )
        fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

    return fig




@callback(Output('w_countries1', 'options'),
          [Input('w_countries', 'value')])
def update_country(w_countries):
    if w_countries == 'Todas':
        dados1 = database.groupby(['UF', 'Regiao', 'Estado'])[['QUANTIDADE']].sum().reset_index()
        return [{'label': 'Selecione e região', 'value': 'Selecione e região'}]
        # return [{'label': i, 'value': i} for i in dados1['Estado'].unique()]
    else:
        dados2 = database[database['Regiao'] == w_countries]
        return [{'label': i, 'value': i} for i in dados2['Estado'].unique()]


@callback(Output('w_countries1', 'value'),
          [Input('w_countries1', 'options')])
def update_country(w_countries1):
    if 'w_countries' == 'Todas':
        dados3 = database.groupby(['UF', 'Regiao', 'Estado'])[['QUANTIDADE']].sum().reset_index()
        return [{'label': i, 'value': i} for i in dados3['Estado'].unique()]
    else:
        # dados3 = database[database['Regiao'] == w_countries]
        return [k['value'] for k in w_countries1]


# Início da callback do gráfico de barras

@callback(Output('bar_chart', 'figure'),
          [Input('w_countries', 'value')],
          [Input('w_countries1', 'value')])
def update_graph(w_countries, w_countries1):
    if w_countries == 'Todas':
        dados6 = database.groupby(['UF', 'Regiao', 'Estado'])[['QUANTIDADE']].sum().reset_index()

    else:
        dados5 = database.groupby(['UF', 'Regiao', 'Estado'])[['QUANTIDADE']].sum().reset_index()
        dados6 = dados5[(dados5['Regiao'] == w_countries)]

    return {
        'data': [go.Bar(
            x=dados6['UF'],
            y=dados6['QUANTIDADE'],
            text=dados6['QUANTIDADE'],
            texttemplate='%{text:,.0f}',
            textposition='auto',
            name='injured',
            marker=dict(color='#1da6f0'),
            hoverinfo='text',
            hovertext=
            '<b>UF</b>: ' + dados6['UF'].astype(str) + '<br>' +
            '<b>Estado</b>: ' + dados6['Estado'].astype(str) + '<br>' +
            '<b>Região</b>: ' + dados6['Regiao'].astype(str) + '<br>' +
            '<b>Quantidade</b>: ' + dados6['QUANTIDADE'].astype(str) + '<br>'

        ),

        ],

        'layout': go.Layout(
            barmode='stack',
            title={'text': 'Quantidade de registro por estado/região:' + '<br>',
                   'y': 0.93,
                   'x': 0.5,
                   'xanchor': 'center',
                   'yanchor': 'top'},
            titlefont={'color': 'black',
                       'size': 20},
            font=dict(family='sans-serif',
                      color='black',
                      size=12),
            hovermode='closest',
            #paper_bgcolor='#272b30',
            #plot_bgcolor='#272b30',
            legend={'orientation': 'h',
                    'bgcolor': 'white',
                    'xanchor': 'center', 'x': 0.5, 'y': -0.7},
            margin=dict(r=0),
            xaxis=dict(title='<b>Estados</b>',
                       tick0=0,
                       dtick=1,
                       color='black',
                       showline=True,
                       showgrid=True,
                       showticklabels=True,
                       linecolor='black',
                       linewidth=1,
                       ticks='outside',
                       tickfont=dict(
                           family='Aerial',
                           color='black',
                           size=12
                       )),
            yaxis=dict(title='<b>Quantidade</b>',
                       color='black',
                       showline=True,
                       showgrid=True,
                       showticklabels=True,
                       linecolor='black',
                       linewidth=1,
                       ticks='outside',
                       tickfont=dict(
                           family='Aerial',
                           color='black',
                           size=12
                       )
                       )

        )
    }
# Fim da callback do gráfico de barras

#Callback Pop-up
@callback(
    Output('modal', 'children'),
    [Input('mapa-interativo', 'clickData')])
def display_click_data(clickData):



    if clickData:
        uf = clickData['points'][0]['location']
        df = dados_idade[(dados_idade['UF'] == uf)]
        totalPopulacao = df.Populacao.sum()
        text_totalPopulacao = f'{totalPopulacao:_.2f}'
        text_totalPopulacao = text_totalPopulacao.replace('.', ',').replace('_', '.')

        totalOcupados = df.Trabalhadores.sum()
        text_totalOcupados = f'{totalOcupados:_.2f}'
        text_totalOcupados = text_totalOcupados.replace('.', ',').replace('_', '.')

        percentual = (totalOcupados / totalPopulacao)
        fig = go.Figure(data=[go.Pie(labels=df.AtividadeEconomica, values=df.Trabalhadores)])

        #print(estado)

        return [
            html.Div(
                dbc.Modal([
                    dbc.ModalHeader("Detalhes do Estado"),
                    dbc.ModalBody(
                        html.Div([
                            dbc.Row([
                                html.Div([
                                    html.H2(df.Estado.unique(),style={'textAlign': 'center'}),
                                    html.H6('Total da população entre 5 e 17 anos: ' + str(text_totalPopulacao)),
                                    html.H6('Total de ocupados entre 5 e 17 anos: ' + str(text_totalOcupados)),
                                    html.H6('Percentual ocupados em relação a população: ' + str(f'{percentual:.3%}')),
                                ], className='pretty_container one columns'),
                            ]),
                            dbc.Row([
                                html.Div([
                                    dcc.Graph(figure=fig)

                                ], className='pretty_container one columns')
                            ])
                        ])),
                    #dbc.ModalFooter(dbc.Button("Close", id="close"))
                ], is_open=True, size='xl')
            )
        ]



@callback(
    Output('mapa_inte-display-value', 'children'),
    Input('nav-bar', 'href'))
    #Input('drop-down-mapa_inte', 'value'))
def display_value(value):
    return f'You have selected {value}'
