from dash import Dash, html, dcc, Input, Output, callback
import dash_bootstrap_components as dbc


# criando um grid
grid = html.Div(
    [
        dbc.Row(
            [
                html.Div([
                    html.P(),
                    html.H2('EM CONSTRUÇÃO'),

                ], style={'textAlign': 'justify'})

                # dbc.Col(dcc.Graph(), md=4),
                # dbc.Col(dcc.Graph(), md=8)
            ]
        )
    ]
)

# inserindo a navbar
navbar = dbc.NavbarSimple(
    children=[
        # dbc.NavItem(dbc.NavLink("Início", href="index"), id="index-link"),
        # dbc.NavItem(dbc.NavLink("Mapa Interativo", href="mapa_inte"), id="mapa_inte-link"),
        # dbc.NavItem(dbc.NavLink("Análise por Região", href="#"), id="mapa-regiao-link"),
        # dbc.NavItem(dbc.NavLink("Gênero e Tipo de trabalho", href="#"), id="mapa-tipo-link"),
        # dbc.NavItem(dbc.NavLink("Análise por período", href="#"), id="mapa-periodo-link"),
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("Início", href="index", id='index-link'),
                dbc.DropdownMenuItem("Mapa Interativo", href="mapa_inte", id='mapa_inte-link'),
                dbc.DropdownMenuItem("Análise por Região", href="mapa_regiao", id='mapa-regiao-link'),
                dbc.DropdownMenuItem("Gênero e Tipo de trabalho", href="mapa_trabalho", id='mapa_trabalho-link'),
                dbc.DropdownMenuItem("Análise por período", href="mapa_periodo", id='mapa_periodo'),
            ],
            nav=True,
            in_navbar=True,
            label="Início",
            id='drop-down-mapa_periodo'

        ),
    ],
    brand="Mapa do Trabalho Infantil no Brasil",
    brand_href="index",
    color="primary",
    dark=True,
    id="nav-bar"
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
    Output('mapa_trabalho-display-value', 'children'),
    Input('drop-down-mapa_periodo', 'value'))
def display_value(value):
    return f'You have selected {value}'
