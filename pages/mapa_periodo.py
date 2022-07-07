from dash import html, dcc, callback, Dash, State
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
import json
from pages import navbar


# Carregando Json do arquivo
geojson = json.load(open('./geoBrasil.json'))

series_temporais = pd.read_csv('dados_tratados/series_temporais.csv')

options_region = [{'label': 'Todas', 'value': 'Todas', 'label': c, 'value': c} for c in (series_temporais['Regiao'].unique())]
options_region.append({'label': 'Todas', 'value': 'Todas'})

options_ano = [{'label': c, 'value': c} for c in (series_temporais['Ano'].unique())]





fig = px.choropleth_mapbox()



# criando um grid
grid = html.Div(
    [
        html.Div([
            html.H3('Mapa Interativo por Período', style={'margin-bottom': '10px', 'color': 'white', 'textAlign': 'center'}),
                dbc.Row([
                    dbc.Col([
                        html.Div('Selecione a região', className='fix_label'),
                        dcc.Dropdown(id='drop_regiao_periodo',
                                     multi=False,
                                     searchable=True,
                                     value='Todas',
                                     placeholder='Selecione a Região',
                                     options=options_region, className='dcc_compon'),
                    ]),
                    dbc.Col([
                        html.Div('Selecione o ano', className='fix_label'),
                        dcc.Dropdown(id='ano_dropdown',
                                         multi=False,
                                         searchable=True,
                                         value=options_ano[0]['label'],
                                         placeholder='Selecione o ano',
                                         options=options_ano, className='dcc_compon'),


                    ]),
                    ])
        ], className='create_container three columns'),
    ]
)


# montagem do layout
layout = html.Div(
    [
        html.Div(id='mapa_periodo-display-value', style={'display': 'none'}),
        navbar.navbar,
        dbc.Container(
            [
                grid
            ]
        ),
        html.Br(),
        dbc.Container(

                html.Div([
                        dcc.Graph(id='mapa-periodo', figure=fig, config={'displayModeBar': False}, style={'marginTop': '15px'}),
                        dcc.Graph(id='line_chart', config={'displayModeBar': False}, style={'margin': '50px 0'})
                ], className='row flex-display')

        ),
        html.Div(id='modal_periodo')

    ]
)


## TESTE MAPA CLOROPLÉTICO
@callback(Output('mapa-periodo', 'figure'),
          [Input('drop_regiao_periodo', 'value')])
def display_choropleth(drop_regiao_periodo):
    df = series_temporais.groupby(['Ano','UF', 'NOUF', 'Regiao'])[['Trabalhadores']].sum().reset_index()

    fig = px.choropleth_mapbox(df, locations='UF',
                               geojson=geojson,
                               color='Trabalhadores',
                               # featureidkey="feature.id",
                               hover_name='NOUF',
                               hover_data=['UF', 'Trabalhadores'],
                               animation_frame='Ano',
                               #title="Análise por período",
                               mapbox_style='white-bg',
                               center={"lat": -14, "lon": -55},
                               zoom=2.3,
                               opacity=0.8,
                               )
    fig.update_layout(margin={"r": 0, "t": 30, "l": 0, "b": 30})

    return fig


# Início da callback do gráfico de linhas
@callback(Output('line_chart', 'figure'),
          [Input('drop_regiao_periodo', 'value')],
          [Input('ano_dropdown', 'value')])
def update_graph(drop_regiao_periodo, ano_dropdown):

    df_ANO = series_temporais.loc[series_temporais.Ano == ano_dropdown, ['FaixaIdade', 'Ano', 'Trimestre', 'Trabalhadores', 'UF', 'NOUF','Regiao']]

    if drop_regiao_periodo == 'Todas':
        df_ANO2 = df_ANO.groupby(['Ano','UF', 'NOUF', 'Trimestre', 'Regiao'])[['Trabalhadores']].sum().reset_index()

    else:
        df_ANO2 = df_ANO.groupby(['Ano','UF', 'NOUF', 'Trimestre','Regiao'])[['Trabalhadores']].sum().reset_index()
        df_ANO2 = df_ANO2[(df_ANO2['Regiao'] == drop_regiao_periodo)]

    fig2 = px.line(df_ANO2, x='Trimestre', y='Trabalhadores', color='NOUF', markers=True, title=ano_dropdown)

    return fig2
# Fim da callback do gráfico de linhas

#Callback Pop-up
@callback(
    Output('modal_periodo', 'children'),
    [State('ano_dropdown','value')],
    [Input('mapa-periodo', 'clickData')],
    prevent_initial_call=True)


def display_click_data(ano_dropdown,clickData):


    if clickData:
        uf = clickData['points'][0]['location']
        df_Estado = series_temporais.loc[series_temporais.UF == uf, ['FaixaIdade','Ano','Trimestre','Trabalhadores','UF','NOUF']]
        df_Estado_group = df_Estado.groupby(['Ano', 'UF', 'NOUF', 'Trimestre'])[['Trabalhadores']].sum().reset_index()
        df_Estado_Ano = df_Estado.loc[
        df_Estado.Ano == ano_dropdown, ['FaixaIdade', 'Ano', 'Trimestre', 'Trabalhadores', 'UF', 'NOUF']]

        fig3 = px.line(df_Estado_group, x='Trimestre', y='Trabalhadores', color='Ano', markers=True, title=df_Estado_group.NOUF[1])


        fig3.update_layout(title={
                           'y': 0.93,
                            'x': 0.5,
                            'xanchor': 'center',
                            'yanchor': 'top'},
                            titlefont={'color': 'black',
                            'size': 20},

        )


        fig4 = px.histogram(df_Estado_Ano, x="Trimestre", y="Trabalhadores",
                            color='FaixaIdade', barmode='group', title=ano_dropdown
                            # range_x=[5,17],
                            # nbins=13
                            )

        fig4.update_layout(title={
            'y': 0.93,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'},
            titlefont={'color': 'black',
                       'size': 20},

        )

        # df_Estado_Ano2 = df_Estado.loc[df_Estado.Ano == 2019, ['FaixaIdade', 'Ano', 'Trimestre', 'Trabalhadores', 'UF', 'NOUF']]
        # fig5 = px.histogram(df_Estado_Ano2, x="Trimestre", y="Trabalhadores",
        #                     color='FaixaIdade', barmode='group', title='2019'
        #                     # range_x=[5,17],
        #                     # nbins=13
        #                     )

        # totalPopulacao = df.Populacao.sum()
        # text_totalPopulacao = f'{totalPopulacao:_.2f}'
        # text_totalPopulacao = text_totalPopulacao.replace('.', ',').replace('_', '.')
        #
        # totalOcupados = df.Trabalhadores.sum()
        # text_totalOcupados = f'{totalOcupados:_.2f}'
        # text_totalOcupados = text_totalOcupados.replace('.', ',').replace('_', '.')
        #
        # percentual = ((totalOcupados / totalPopulacao))
        # fig = go.Figure(data=[go.Pie(labels=df.AtividadeEconomica, values=df.Trabalhadores)])

        #print(estado)

        return [
            html.Div(
                dbc.Modal([
                    dbc.ModalHeader("Detalhes do Estado"),
                    dbc.ModalBody(
                        html.Div([
                            dbc.Row([
                                dbc.Col([

                                    dcc.Graph(figure=fig3, config={'displayModeBar': False})
                                    #html.Div([
                                        #html.H2(df.Estado.unique(),style={'textAlign': 'center'}),
                                        #html.H6('Total da população entre 5 e 17 anos: ' + str(text_totalPopulacao)),
                                        #html.H6('Total de ocupados entre 5 e 17 anos: ' + str(text_totalOcupados)),
                                        #html.H6('Percentual ocupados em relação a população: ' + str(f'{percentual:.2%}')),
                                    #], className='row flex-display'),
                                ]),
                            ]),
                            dbc.Row([
                                dbc.Col([
                                    #html.Div([
                                        dcc.Graph(figure=fig4, config={'displayModeBar': False})

                                    #], className='row flex-display')
                                ])
                            ]),
                            # dbc.Row([
                            #     dbc.Col([
                            #         # html.Div([
                            #         dcc.Graph(figure=fig5)
                            #
                            #         # ], className='row flex-display')
                            #     ])
                            # ])

                        ], className='row flex-display')),
                    #dbc.ModalFooter(dbc.Button("Close", id="close"))
                ], is_open=True, size='xl', scrollable=True)
            )
        ]



@callback(
    Output('mapa_periodo-display-value', 'children'),
    Input('nav-bar', 'href'))
    #Input('drop-down-mapa_inte', 'value'))
def display_value(value):
    return f'You have selected {value}'
