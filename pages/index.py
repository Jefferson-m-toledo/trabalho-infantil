from dash import Dash, html, dcc, Input, Output, callback
import dash_bootstrap_components as dbc
import base64
from pages import navbar

app = Dash(__name__)

# criando um grid
grid = html.Div(
    [

        dbc.Row(
            [
                html.Div([
                    html.H3('Apresentação', style={'margin': '30px 10px', 'textAlign': 'center'}),
                    html.P('''A erradicação do trabalho infantil é uma meta globalmente compartilhada.
                        Para isso, é necessário um somatório de atuações decisivas e articuladas entre
                        governos, organizações de trabalhadores e empregadores e a sociedade civil para
                        que possam avançar na sua prevenção e eliminação (OIT, 2021).
                        Para essas atuações se faz necessário ter informações atualizadas sobre o tema.
                        Quanto mais apresentáveis e facilitadas sejam essas informações, mais viável se torna
                        a possibilidade de apresentação de insights e planos de ação.'''),
                    html.P(['''O Mapa do Trabalho Infantil é uma aplicação com dados infantis no Brasil, com
                        informações atualizadas e consolidadas de forma interativa ao usuário.''',
                        html.A("Saiba mais",
                               href='saiba_mais',
                               style={'padding': '0 10px', 'text-decoration': 'none'})
                        ]),

                ], className='col-6', style={'textAlign': 'justify', 'fontSize': '18px', 'padding': '50px 0'}),
                html.Div([
                    html.Img(src=app.get_asset_url('bg.svg'), style={'maxWidth': '400px'})
                ], className='col-6', style={'textAlign': 'center', 'padding': '50px 0'})

                # dbc.Col(dcc.Graph(), md=4),
                # dbc.Col(dcc.Graph(), md=8)
            ], className='align-items-center'
        )
    ]
)

# inserindo a navbar
# navbar = dbc.NavbarSimple(
#     children=[
#         dbc.NavItem(dbc.NavLink("Início", href="index"), id="index-link"),
#         dbc.NavItem(dbc.NavLink("Saiba Mais", href="saiba_mais"), id="saiba_mais-link"),
#         dbc.NavItem(dbc.NavLink("Mapa Interativo", href="mapa_inte"), id="mapa_inte-link"),
#         dbc.NavItem(dbc.NavLink("Análise por Idade", href="mapa_idade"), id="mapa-idade-link"),
#         dbc.NavItem(dbc.NavLink("Gênero e Trabalho", href="mapa_genero"), id="mapa-genero-link"),
#         dbc.NavItem(dbc.NavLink("Comparação entre Períodos", href="mapa_periodo"), id="mapa-periodo-link"),
#     ],
#     brand="Mapa do Trabalho Infantil",
#     brand_href="index",
#     color="primary",
#     dark=True,
#     id="nav-bar",
#     style={'background': 'linear-gradient(145deg, #375ee3 0%, #6543e0 80%)',
#            'boxShadow': '0 1px 2px rgb(0 0 0 / 30%)',
#             'color': 'rgba(255, 255, 255, 0.7)',
#             'fontSize': '16px',
#             'fontWeight': '400'}
# )

# montagem do layout
layout = html.Div(
    [
        html.Div(id='index-display-value', style={'display': 'none'}),
        # inserindo a navbar
        navbar.navbar,
        dbc.Container(
            [
                grid
            ]
        )
    ]
)


@callback(
    Output('index-display-value', 'children'),
    Input('nav-bar', 'href'))
def display_value(value):
    return f'You have selected {value}'
