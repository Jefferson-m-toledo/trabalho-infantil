from dash import Dash, html, dcc, Input, Output, callback
import dash_bootstrap_components as dbc
from pages import navbar

app = Dash(__name__)

# criando um grid
grid = html.Div(
    [

        dbc.Row(
            [
                html.Div([
                    html.H3('O Mapa do Trabalho Infantil', style={'margin': '30px 10px', 'textAlign': 'center'}),
                    html.P('''Somos uma aplicação com dados infantis no Brasil com
                        informações atualizadas e consolidadas de forma interativa ao usuário. A aplicação 
                        está sendo construída com base nos dados abertos do IBGE que será previamente tratada 
                        e analisada. A apresentação dos mapas será realizada por meio de módulos e painéis:'''),
                    html.P([
                        html.B('Mapa Interativo: '),
                        '''Neste módulo serão apresentados a porcentagem de trabalho infantil
                        por região, onde será possível visualizar os valores totais e percentuais do trabalho
                        infantil por região selecionada.''']),
                    html.P([
                        html.B('Análise por região: '),
                        '''Neste módulo será disponibilizado um filtro da região de interesse.
                        Para cada região selecionada serão apresentados Dashboards com detalhes e a possibilidade
                        do filtro das informações por estado de interesse em cada região.''']),
                    html.P([
                        html.B('Sexo e tipo de trabalho: '),
                        '''O módulo será composto por Dashboards dos dados de trabalho
                        infantil a partir de um recorte de sexo e tipo de trabalho no qual também será possível
                        filtrar as informações por região.''']),
                    html.P([
                        html.B('Comparação entre períodos: '),
                        '''Módulo no qual será possível realizar a comparação das
                        informações com filtro por período e região. Será apresentado o dashboards de análises
                        temporais dos dados ilustrando a evolução temporal do trabalho infantil do Brasil com
                        a possibilidade de drill down para outras agregações por região e setor econômico.'''])
                ], className='col-6', style={'textAlign': 'justify', 'fontSize': '18px', 'padding': '50px 0'}),
                html.Div([
                    html.Img(src=app.get_asset_url('bg.svg'), style={'maxWidth': '400px'})
                ], className='col-6', style={'textAlign': 'center', 'padding': '50px 0'})

                # dbc.Col(dcc.Graph(), md=4),
                # dbc.Col(dcc.Graph(), md=8)
            ]
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
#     brand_href="saiba_mais",
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
        html.Div(id='saiba-mais-display-value', style={'display': 'none'}),
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
    Output('saiba-mais-display-value', 'children'),
    Input('nav-bar', 'href'))
def display_value(value):
    return f'You have selected {value}'
