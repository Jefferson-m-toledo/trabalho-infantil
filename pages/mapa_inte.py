from dash import Dash, html, dcc, Input, Output, callback
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import json
import plotly.graph_objects as go

geojson = json.load(open('br_states.json'))
database = pd.read_csv('database.csv')


estados_opcoes = list(database['UF'].unique())
estados_opcoes.append("Todos")
uf_selecionada = 'Todos'

regiao_opcoes = list(database['Regiao'].unique())
regiao_opcoes.append("Todas")
regiao_selecionada = 'Todas'


df_estado = database[database['UF'] == uf_selecionada]
df_regiao = database[database['Regiao'] == regiao_selecionada]

fig = px.choropleth(database, geojson=geojson,
                    locations='UF',
                    color='QUANTIDADE',
                    hover_data=['UF'],
                    scope='south america',
                    width=600,
                    height=600,
                    )


fig2 = go.Figure(data=[go.Table(
    header=dict(values=list(database.columns), ),
    cells=dict(values=[database.UF, database.Estado, database.Regiao, database.QUANTIDADE], )
)])


# fig2 = go.Figure(data=[go.Table(
#     header=dict(values=list(df_estado.columns), ),
#     cells=dict(values=[df_estado.UF, df_estado.Estado, df_estado.Regiao, df_estado.QUANTIDADE], )
# )])

# criando um grid
grid = html.Div(
    [
        html.H5('Selecione o estado'),
        dcc.Dropdown(estados_opcoes, value='Todos', id='drop_estados'),
        html.H5('Selecione a Região'),
        dcc.Dropdown(regiao_opcoes, value='Todas', id='drop_regiao'),
        dbc.Row(
            [
                dbc.Col(dcc.Graph(id='mapa-interativo', figure=fig), md=6),
                dbc.Col(dcc.Graph(id='tabela', figure=fig2), md=6)
            ]
        )
    ]
)

# inserindo a navbar
navbar = dbc.NavbarSimple(
    children=[
        # dbc.NavItem(dbc.NavLink("Início", href="index")),
        # dbc.NavItem(dbc.NavLink("Mapa Interativo", href="mapa_inte")),
        # dbc.NavItem(dbc.NavLink("Análise por Região", href="#")),
        # dbc.NavItem(dbc.NavLink("Gênero e Tipo de trabalho", href="#")),
        # dbc.NavItem(dbc.NavLink("Análise por período", href="#")),
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
    brand_href="#",
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
        )
    ]
)

# app.layout = html.Div(children=[
#     html.H1(children='Mapa Interativo do Trabalho Infantil'),
#     html.H2(children='Soma dos registro de trabalho infantil por estado'),
#     html.Div(children=''''Teste'''),
#
#     dcc.Dropdown(estados_opcoes, value='Todos', id='drop_estados'),
#     dcc.Graph(
#         id='mapa-interativo',
#         figure=fig
#
#     ),
#
#     dcc.Graph(
#         id='tabela',
#         figure=fig2
#     )
#
# ])


# @app.callback(
#     Output('tabela', 'figure'),
#     Input('drop_estados','value')
#
# )
# def update_output(value):
#     if value == 'Todos':
#         fig2 = go.Figure(data=[go.Table(
#             header=dict(values=list(database.columns), ),
#             cells=dict(
#                 values=[database.UF, database.Estado, database.Regiao, database.QUANTIDADE], )
#         )])
#     else:
#         fig2 = go.Figure(data=[go.Table(
#             header=dict(values=list(df_estado.columns), ),
#             cells=dict(
#                 values=[df_estado.UF, df_estado.Estado, df_estado.Regiao, df_estado.QUANTIDADE], )
#         )])
#     return fig2

@callback(
    Output('mapa_inte-display-value', 'children'),
    Input('drop-down-mapa_inte', 'value'))
def display_value(value):
    return f'You have selected {value}'

