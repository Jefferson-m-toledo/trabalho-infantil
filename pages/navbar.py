import dash_bootstrap_components as dbc


navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Início", href="index"), id="index-link"),
        dbc.NavItem(dbc.NavLink("Saiba Mais", href="saiba_mais"), id="saiba_mais-link"),
        dbc.DropdownMenu(
            [
                dbc.DropdownMenuItem("Mapa Interativo", href="mapa_inte", id="mapa_inte-link"),
                dbc.DropdownMenuItem("Análise por Idade", href="mapa_idade", id="mapa-idade-link"),
                dbc.DropdownMenuItem("Sexo e Tipo de Trabalho", href="mapa_genero", id="mapa-genero-link"),
                dbc.DropdownMenuItem("Comparação entre Períodos", href="mapa_periodo", id="mapa-periodo-link"),
            ],
            label="Dados",
            nav=True,
        ),
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