import html as html
from dash import html, dcc, callback, Dash
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc

# Cria data frame com o CSV
database = pd.read_csv('./dados.csv')

# Cria dataframe com UF, ESTADO e Região para o dropdown
database_dropdown = pd.DataFrame(database, columns=['UF', 'Estado', 'Regiao'])

# Importa CSV
df_idade_atividade = pd.read_csv('populacao_uf_idade.csv')

# Cria datafame a partir do CSV apenas com os dados de menores de idade (Idade <= 17)
dados_idade = df_idade_atividade.loc[df_idade_atividade.Idade <= 17, ['UF', 'Estado', 'AtividadeEconomica', 'Idade', 'Trabalhadores', 'Populacao']]

# criando um grid
grid = html.Div(
    [
        html.Div(
            [
                html.Div([
                    html.H5('Dashboard',
                            style={'margin-bottom': '10px', 'color': 'white', 'textAlign': 'center'}),
                    dbc.Row([
                        dbc.Col([
                            html.Div('Selecione a região', className='fix_label', style={'color': 'white'}),
                            dcc.Dropdown(id='regiao_dropdown',
                                         multi=False,
                                         searchable=True,
                                         value='Nordeste',
                                         placeholder='Selecione a Região',
                                         options=[{'label': c, 'value': c}
                                                  for c in (database['Regiao'].unique())], className='dcc_compon'),
                        ]),

                        dbc.Col([

                            html.Div('Selecione o estado', className='fix_label', style={'color': 'white'}),
                            dcc.Dropdown(id='estado_dropdown',
                                         multi=False,
                                         searchable=True,
                                         placeholder='Selecione o estado',
                                         options=[], className='dcc_compon'),
                        ])
                    ])


                ], className='create_container three columns')

            ], className='row flex-display'
        )
    ]
)

# inserindo a navbar
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Início", href="index"), id="index-link"),
        dbc.NavItem(dbc.NavLink("Mapa Interativo", href="mapa_inte"), id="mapa_inte-link"),
        dbc.NavItem(dbc.NavLink("Dashboard", href="mapa_regiao"), id="mapa-regiao-link"),
    ],
    brand="Mapa do Trabalho Infantil no Brasil",
    #brand="TESTE - Mapa do Trabalho Infantil no Brasil",
    brand_href="index",
    color="primary",
    #color="#800000",
    dark=True,
)

# montagem do layout
layout = html.Div(
    [
        html.Div(id='mapa_regiao-display-value'),
        # inserindo a navbar
        navbar,
        dbc.Container(
            [
                grid
            ]
        ),
        dbc.Container([
            dbc.Row([
                dbc.Col([
                    html.P(),
                    html.H4("Relação Idade x Atividade",style={'margin-bottom': '10px', 'color': 'white', 'textAlign': 'left'}),
                    dcc.Graph(id='idade_atividade', className='dcc_compon'),
                ])
            ]),
            dbc.Row([
                dbc.Col([
                    html.Div([

                        html.Div(id='dados'),

                    ])
                ], className='container'),
                dbc.Col([
                    html.H3("Gráfico 2", style={'margin-bottom': '10px', 'color': 'white', 'textAlign': 'center'}),
                    dcc.Graph(id='teste2', config={'displayModeBar': False}, className='dcc_compon',style={'margin-top': '20px', }),
                ])
            ]),

            html.H4("Gráfico 3", style={'margin-bottom': '10px', 'color': 'white', 'textAlign': 'center'}),
            dcc.Graph(id='teste3', config={'displayModeBar': False}, className='dcc_compon', style={'margin-top': '20px', }),
        ])

    ], id='mainContainer', style={'display': 'flex', 'flex-direction': 'column'}
)

#Callback dados do estado
@callback(
    Output('dados','children'),
    Input('estado_dropdown','value')
)

def update_output_div(estado_dropdown):
    df = dados_idade[(dados_idade['Estado'] == estado_dropdown)]
    totalPopulacao = df.Populacao.sum()
    totalOcupados = df.Trabalhadores.sum()
    percentual = ((totalOcupados / totalPopulacao)*100)
    fig = go.Figure(data=[go.Pie(labels=['População','Ocupados'], values=[totalPopulacao, totalOcupados],pull=[0, 0.2,])])
    fig.update_layout(margin = dict(t=0, l=0, r=0, b=0), autosize=True, paper_bgcolor='#272b30',plot_bgcolor='#272b30', font_color='white')


    return [
        html.Div([
        html.Div('Total da população entre 5 e 17 anos: {0:2.4f}'.format(totalPopulacao),style={'color': 'white',
                                                          'textAlign': 'left',
                                                          #'margin-top': '0px',
                                                          'fontSize':'20px'}),
        html.Div('Ocupados entre 5 e 17 anos: {0:2.4f}'.format(totalOcupados),style={'color': 'white',
                                                          'textAlign': 'left',
                                                          #'margin-top': '0px',
                                                          'fontSize':'20px'}),
        html.Div('Percentual ocupados em relação a população: {0:0.3f}%'.format(percentual),style={'color': 'white',
                                                          'textAlign': 'left',
                                                          #'margin-top': '0px',
                                                          'fontSize':'20px'}),
        html.Div(dcc.Graph(figure=fig,config={'displayModeBar': False})),
        ])

        #html.Span('Latitude: {0:.2f}'.format(lat), style=style),
        #html.Span('Altitude: {0:0.2f}'.format(alt), style=style)
    ]



# Callback Gráfico de barras Idade x Atividade
@callback(Output('idade_atividade', 'figure'),
          #[Input('regiao_dropdown', 'value')],
          [Input('estado_dropdown', 'value')])
def update_graph(estado_dropdown):
    df = dados_idade[(dados_idade['Estado'] == estado_dropdown)]
    fig = px.bar(df,
                  x='Idade',
                  y='Trabalhadores',
                  color='AtividadeEconomica',
                  hover_data=['AtividadeEconomica'],
                  barmode='stack',
                  )
    fig.update_layout(legend={
                     #'bgcolor':'#1f2c56',
                     'x': 0.01, 'y':.9,},
                    margin={'t':0, 'l':0, 'r':0, 'b':0},
                    paper_bgcolor='#272b30',
                    plot_bgcolor='#272b30',
                    font_color='white',
                    title='Idade x Atividade Econômica')

    return fig

# Fim da callback do gráfico de barras




# Callback Dropdown
@callback(Output('estado_dropdown', 'options'),
          [Input('regiao_dropdown', 'value')])
def update_country(regiao_dropdown):
    dados3 = database[database['Regiao'] == regiao_dropdown]
    return [{'label': i, 'value': i} for i in dados3['Estado'].unique()]


@callback(Output('estado_dropdown', 'value'),
          [Input('estado_dropdown', 'options')])
def update_country(estado_dropdown):
    return [k['value'] for k in estado_dropdown][0]


@callback(
    Output('mapa_regiao-display-value', 'children'),
    Input('nav-bar', 'href'))
def display_value(value):
    return f'You have selected {value}'
