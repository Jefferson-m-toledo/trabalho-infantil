from dash import Dash, html, dcc, Input, Output, callback
import dash_bootstrap_components as dbc


# criando um grid
grid = html.Div(
    [
        dbc.Row(
            [
                html.Div([
                    html.P(),
                    html.H5('''     A erradicação do trabalho infantil é uma meta globalmente compartilhada.
                        Para isso, é necessário um somatório de atuações decisivas e articuladas entre
                        governos, organizações de trabalhadores e empregadores e a sociedade civil para
                        que possam avançar na sua prevenção e eliminação (OIT, 2021).
                        Para essas atuações se faz necessário ter informações atualizadas sobre o tema.
                        Quanto mais apresentáveis e facilitadas sejam essas informações, mais viável se torna
                        a possibilidade de apresentação de insights e planos de ação.'''),
                    html.H5('''O Mapa do Trabalho infantil é uma aplicação com dados infantis no Brasil com
                    informações atualizadas e consolidadas de forma iterativa ao usuário. A aplicação está
                    sendo construída com base nos dados abertos do IBGE que será previamente tratada e analisada.
                    A apresentação dos mapas será realizada por meio de módulos e painéis:'''),
                    html.H5('''- Mapa Interativo: Neste módulo serão apresentados a porcentagem de trabalho infantil
                        por região, onde será possível visualizar os valores totais e percentuais do trabalho
                        infantil por região selecionada.'''),
                    html.H5('''- Análise por região: Neste módulo será disponibilizado um filtro da região de interesse.
                        Para cada região selecionada serão apresentados Dashboards com detalhes e a possibilidade
                        do filtro das informações por estado de interesse em cada região.'''),
                    html.H5('''- Gênero e tipo de trabalho: O módulo será composto por Dashboards dos dados de trabalho
                        infantil a partir de um recorte de gênero e tipo de trabalho no qual também será possível
                        filtrar as informações por região.'''),
                    html.H5('''- Comparação entre períodos: Módulo no qual será possível realizar a comparação das
                        informações com filtro por período e região. Será apresentado o dashboards de análises
                        temporais dos dados ilustrando a evolução temporal do trabalho infantil do Brasil com
                        a possibilidade de drill down para outras agregações por região e setor econômico. ''')

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
                dbc.DropdownMenuItem("Análise por Região", href="mapa_regiao", id='mapa_regiao-link'),
                dbc.DropdownMenuItem("Gênero e Tipo de trabalho", href="mapa_trabalho", id='mapa_trabalho-link'),
                dbc.DropdownMenuItem("Análise por período", href="mapa_periodo", id='mapa_periodo'),
            ],
            nav=True,
            in_navbar=True,
            label="Início",
            id='drop-down-index'

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
        html.Div(id='index-display-value'),
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
    Output('index-display-value', 'children'),
    Input('drop-down-index', 'value'))
def display_value(value):
    return f'You have selected {value}'
