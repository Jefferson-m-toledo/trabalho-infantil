from dash import Dash, html, dcc, Input, Output, callback
import dash_bootstrap_components as dbc
import pandas as pd


# Cria data frame com o CSV
database = pd.read_csv('./dados_tratados/database.csv')

# Cria dataframe com UF, ESTADO e Região para o dropdown
database_dropdown = pd.DataFrame(database, columns=['UF', 'Estado', 'Regiao'])


# criando um grid
# criando um grid
grid = html.Div(
    [
        html.Div(
            [
                html.Div([
                    html.H5('Análise por idade',
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
        dbc.NavItem(dbc.NavLink("Saiba Mais", href="saiba_mais"), id="saiba_mais-link"),
        dbc.NavItem(dbc.NavLink("Mapa Interativo", href="mapa_inte"), id="mapa_inte-link"),
        dbc.NavItem(dbc.NavLink("Análise por Idade", href="mapa_idade"), id="mapa-idade-link"),
        dbc.NavItem(dbc.NavLink("Gênero e Trabalho", href="mapa_genero"), id="mapa-genero-link"),
        dbc.NavItem(dbc.NavLink("Comparação entre Períodos", href="mapa_periodo"), id="mapa-periodo-link"),
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
        html.Div(id='mapa_periodo-display-value'),
        # inserindo a navbar
        navbar,
        dbc.Container(
            [
                grid
            ]
        )
    ]
)


@callback(
    Output('mapa_periodo-display-value', 'children'),
    Input('drop-down-mapa_periodo', 'value'))
def display_value(value):
    return f'You have selected {value}'
