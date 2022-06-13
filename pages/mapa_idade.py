import html as html
from dash import html, dcc, callback, Dash
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc

# Cria data frame com o CSV
database = pd.read_csv('./dados_tratados/database.csv')

# Cria dataframe com UF, ESTADO e Região para o dropdown
database_dropdown = pd.DataFrame(database, columns=['UF', 'Estado', 'Regiao'])

# Importa CSV
df_idade_atividade = pd.read_csv('./dados_tratados/populacao_uf_idade.csv')

#Importa CSV Idade, Faixa etária e trabalho
df_faixa_etaria_atividade = pd.read_csv('./dados_tratados/trab_infantil_sexo_idade_atividade.csv')

# Cria datafame a partir do CSV apenas com os dados de menores de idade (Idade <= 17)
dados_idade = df_idade_atividade.loc[df_idade_atividade.Idade <= 17, ['UF', 'Estado', 'AtividadeEconomica', 'Idade', 'Trabalhadores', 'Populacao']]

# criando um grid
grid = html.Div(
    [
        html.Div(
            [
                html.Div([
                    html.H5('Análise por idade',
                            style={'margin-bottom': '10px', 'color': 'white', 'textAlign': 'center'}),
                    dbc.Row([
                        dbc.Col([
                            html.Div('Selecione a região', className='fix_label', style={'color': 'white'}),
                            dcc.Dropdown(id='regiao_dropdown',
                                         multi=False,
                                         searchable=True,
                                         value='Nordeste',
                                         placeholder='Selecione a Região',
                                         options=[{'label': c, 'value': c}
                                                  for c in (database['Regiao'].unique())], className='dcc_compon'),
                        ]),

                        dbc.Col([

                            html.Div('Selecione o estado', className='fix_label', style={'color': 'white'}),
                            dcc.Dropdown(id='estado_dropdown',
                                         multi=False,
                                         searchable=True,
                                         placeholder='Selecione o estado',
                                         options=[], className='dcc_compon'),
                        ])
                    ])


                ], className='create_container three columns')

            ], className='row flex-display'
        )
    ]
)

# inserindo a navbar
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Início", href="index"), id="index-link"),
        dbc.NavItem(dbc.NavLink("Saiba Mais", href="saiba_mais"), id="saiba_mais-link"),
        dbc.NavItem(dbc.NavLink("Mapa Interativo", href="mapa_inte"), id="mapa_inte-link"),
        dbc.NavItem(dbc.NavLink("Análise por Idade", href="mapa_idade"), id="mapa-idade-link"),
        dbc.NavItem(dbc.NavLink("Gênero e Trabalho", href="mapa_genero"), id="mapa-genero-link"),
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

# montagem do layout
layout = html.Div(
    [
        html.Div(id='mapa_regiao-display-value', style={'display': 'none'}),
        # inserindo a navbar
        navbar,
        dbc.Container(
            [
                grid
            ]
        ),
        dbc.Container([
            dbc.Row([
                dbc.Col([
                    html.H4("Relação Idade x Atividade",style={'margin-bottom': '10px', 'color': 'white', 'textAlign': 'left'}),
                    dcc.Graph(id='idade_atividade', className='dcc_compon', style={'marginBottom': '50px'}),
                ])
            ]),
            dbc.Row([
                dbc.Col([
                    html.Div([
                        html.Div(id='dados', style={'marginBottom': '50px'}),
                    ])
                ], className='container'),
                dbc.Col([
                    html.Div([
                        html.Div(id='idade_trabalho', style={'marginBottom': '50px'}),
                    ])
                ])
            ]),

        ])

    ], id='mainContainer', style={'display': 'flex', 'flex-direction': 'column'}
)

#Callback dados do estado
@callback(
    Output('dados','children'),
    Input('estado_dropdown','value')
)

def update_output_div(estado_dropdown):
    df = dados_idade[(dados_idade['Estado'] == estado_dropdown)]
    #estado = str(df.Estado.unique())
    totalPopulacao = df.Populacao.sum()
    totalOcupados = df.Trabalhadores.sum()
    percentual = ((totalOcupados / totalPopulacao)*100)
    titulo = ('Total da população entre 5 e 17 anos: ' + str(totalPopulacao) + ' ' + '<br>'+
        'Total de ocupados entre 5 e 17 anos: ' + str(totalOcupados) + ' ' + '<br>'
         'Percentual ocupados em relação a população: ' + str(percentual) + ' ' + '<br>')

    fig = go.Figure(data=[go.Pie(labels=['População','Ocupados'], values=[totalPopulacao, totalOcupados],pull=[0, 0.2,])])
    fig.update_layout(margin = dict(t=20, l=0, r=0, b=0),
                      autosize=True,
                      paper_bgcolor='#272b30',
                      #paper_bgcolor='#272b30',
                      plot_bgcolor='#272b30',
                      font_color='white',
                      title={'text':titulo,
                            #'x': 0.5,
                            'y': 0.1},
                            #'xanchor': 'left',
                            #'yanchor': 'bottom'},
                      titlefont={'color': 'white'},
                      #legend={'x': 1, 'y': -0.8})
                      )



    return [

         html.Div(dcc.Graph(figure=fig,config={'displayModeBar': False}))

     ]

#Callback Gráfico de barras
@callback(
    Output('idade_trabalho','children'),
    Input('estado_dropdown','value')
)

def update_output_div(estado_dropdown):
    filtro_estado = df_faixa_etaria_atividade[(df_faixa_etaria_atividade.NOUF == estado_dropdown)]
    faixa_idade = filtro_estado.groupby(['FaixaIdade'])[['Trabalhadores']].sum().reset_index()

    fig = px.bar(faixa_idade,
                 x='FaixaIdade',
                 y='Trabalhadores',
                 color='FaixaIdade',
                 #hover_data=['AtividadeEconomica'],
                 barmode='relative',
                 )
    fig.update_layout(margin=dict(t=20, l=0, r=0, b=0),
                      autosize=True,
                      paper_bgcolor='#272b30',
                      # paper_bgcolor='#272b30',
                      plot_bgcolor='#272b30',
                      font_color='white',
                      # title={'text': "Faixa Etária",
                      #        # 'x': 0.5,
                      #        'y': 0.1},
                      # 'xanchor': 'left',
                      # 'yanchor': 'bottom'},
                      titlefont={'color': 'white'},
                      # legend={'x': 1, 'y': -0.8})
                      )


    return [

         html.Div(dcc.Graph(figure=fig,config={'displayModeBar': False}))

     ]



# Callback Gráfico de barras Idade x Atividade
@callback(Output('idade_atividade', 'figure'),
          [Input('estado_dropdown', 'value')])
def update_graph(estado_dropdown):
    df = dados_idade[(dados_idade['Estado'] == estado_dropdown)]
    fig = px.histogram(df, x="Idade", y="Trabalhadores",
                       color='AtividadeEconomica', barmode='group',
                       )
    fig.update_layout(legend={
                     #'bgcolor':'#1f2c56',
                     'x': 0.01, 'y':.9,},
                    margin={'t':0, 'l':0, 'r':0, 'b':0},
                    paper_bgcolor='#272b30',
                    plot_bgcolor='#272b30',
                    font_color='white',
                    legend_title='Idade x Atividade Econômica')

    return fig
# Fim da callback do gráfico de barras




# Callback Dropdown
@callback(Output('estado_dropdown', 'options'),
          [Input('regiao_dropdown', 'value')])
def update_country(regiao_dropdown):
    dados3 = database[database['Regiao'] == regiao_dropdown]
    return [{'label': i, 'value': i} for i in dados3['Estado'].unique()]


@callback(Output('estado_dropdown', 'value'),
          [Input('estado_dropdown', 'options')])
def update_country(estado_dropdown):
    return [k['value'] for k in estado_dropdown][0]


@callback(
    Output('mapa_idade-display-value', 'children'),
    Input('nav-bar', 'href'))
def display_value(value):
    return f'You have selected {value}'
