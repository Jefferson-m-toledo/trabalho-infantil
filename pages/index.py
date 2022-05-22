from dash import Dash, html, dcc, Input, Output, callback
import dash_bootstrap_components as dbc

app = Dash(__name__, external_stylesheets=[dbc.themes.MATERIA])

# criando um grid
grid = html.Div(
    [
        dbc.Row(
            [
                html.H5('''A erradicação do trabalho infantil é uma meta globalmente compartilhada.
                        Para isso, é necessário um somatório de atuações decisivas e articuladas entre
                        governos, organizações de trabalhadores e empregadores e a sociedade civil para
                        que possam avançar na sua prevenção e eliminação (OIT, 2021).
                        Para essas atuações se faz necessário ter informações atualizadas sobre o tema.
                        Quanto mais apresentáveis e facilitadas sejam essas informações, mais viável se torna
                        a possibilidade de apresentação de insights e planos de ação.

                        O Mapa do Trabalho infantil é aplicação com dados sobre o trabalho infantil no Brasil
                        com informações atualizadas e consolidadas de forma iterativa ao usuário. A aplicação
                        está sendo construída com base nos dados abertos do IBGE que serão previamente tratados
                        e analisados. A apresentação será através de mapas iterativos e dashboards do trabalho
                        infantil no Brasil através dos dados coletados que serão apresentados nos seguintes
                        módulos:
                        - Mapa Interativo: Neste módulo serão apresentados a porcentagem de trabalho infantil
                        por região, onde será possível visualizar os valores totais e percentuais do trabalho
                        infantil por região selecionada.
                        - Análise por região: Neste módulo será disponibilizado um filtro da região de interesse.
                        Para cada região selecionada serão apresentados Dashboards com detalhes e a possibilidade
                        do filtro das informações por estado de interesse em cada região.
                        - Gênero e tipo de trabalho: O módulo será composto por Dashboards dos dados de trabalho
                        infantil a partir de um recorte de gênero e tipo de trabalho no qual também será possível
                        filtrar as informações por região.
                        - Comparação entre períodos: Módulo no qual será possível realizar a comparação das
                        informações com filtro por período e região. Será apresentado o dashboards de análises
                        temporais dos dados ilustrando a evolução temporal do trabalho infantil do Brasil com
                        a possibilidade de drill down para outras agregações por região e setor econômico. '''

                        )
                # dbc.Col(dcc.Graph(), md=4),
                # dbc.Col(dcc.Graph(), md=8)
            ]
        )
    ]
)

# inserindo a navbar
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Início", href="/index")),
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

if __name__ == '__main__':
    app.run(debug=True)
