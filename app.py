from dash import Dash, dcc, html, Input, Output, callback
from pages import index, saiba_mais, mapa_inte, mapa_idade, mapa_genero, mapa_periodo
import dash_bootstrap_components as dbc

app = Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.ZEPHYR])
server = app.server
app.title = "Mapa do Trabalho Infantil"




app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


@callback(Output('page-content', 'children'),
          Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/index':
        return index.layout
    elif pathname == '/saiba_mais':
        return saiba_mais.layout
    elif pathname == '/mapa_inte':
        return mapa_inte.layout
    elif pathname == '/mapa_idade':
        return mapa_idade.layout
    elif pathname == '/mapa_genero':
        return mapa_genero.layout
    elif pathname == '/mapa_periodo':
        return mapa_periodo.layout
    else:
        # return '404'
        return index.layout


if __name__ == '__main__':
    app.run_server(debug=True)
