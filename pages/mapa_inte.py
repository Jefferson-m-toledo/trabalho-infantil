from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import json
import plotly.graph_objects as go

app = Dash(__name__, external_stylesheets=[dbc.themes.MATERIA])

geojson = json.load(open('../br_states.json'))
database = pd.read_csv('../database.csv')

estados_opcoes = list(database['UF'].unique())
regiao_opcoes = list(database['Regiao'].unique())
estados_opcoes.append("Todos")
regiao_opcoes.append("Todas")
uf_selecionada = ''
regiao_selecionada = ''
df_estado = database[database['UF'] == uf_selecionada]
df_regiao = database[database['Regiao'] == regiao_selecionada]

fig = px.choropleth(database, geojson=geojson,
                    locations='UF',
                    color='QUANTIDADE',
                    hover_data=['UF'],
                    scope='south america',
                    width=600,
                    height=600
                    )

fig2 = go.Figure(data=[go.Table(
    header=dict(values=list(df_estado.columns), ),
    cells=dict(
        values=[df_estado.UF, df_estado.Estado, df_estado.Regiao, df_estado.QUANTIDADE], )
)])

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
        dbc.NavItem(dbc.NavLink("Início", href="index")),
        dbc.NavItem(dbc.NavLink("Mapa Interativo", href="mapa_inte")),
        dbc.NavItem(dbc.NavLink("Análise por Região", href="#")),
        dbc.NavItem(dbc.NavLink("Gênero e Tipo de trabalho", href="#")),
        dbc.NavItem(dbc.NavLink("Análise por período", href="#")),
        # dbc.DropdownMenu(
        #     children=[
        #         dbc.DropdownMenuItem("More pages", header=True),
        #         dbc.DropdownMenuItem("Page 2", href="#"),
        #         dbc.DropdownMenuItem("Page 3", href="#"),
        #     ],
        #     nav=True,
        #     in_navbar=True,
        #     label="More",
        # ),
    ],
    brand="Mapa do Trabalho Infantil no Brasil",
    brand_href="#",
    color="primary",
    dark=True,
)

# montagem do layout
app.layout = html.Div(
    [
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


if __name__ == '__main__':
    app.run(debug=True)
