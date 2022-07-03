import html as html
from dash import html, dcc, callback, Dash
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
from plotly.subplots import make_subplots
from pages import navbar

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

#Dropdown Gênero
genero = ["Todos", "Feminino", "Masculino"]

# criando um grid
grid = html.Div(
    [
        html.Div(
            [
                html.Div([
                    html.H5('Gênero',
                            style={'margin-bottom': '10px', 'color': 'white', 'textAlign': 'center'}),
                    dbc.Row([
                        dbc.Col([
                            html.Div('Selecione a região', className='fix_label'),
                            dcc.Dropdown(id='regiao_dropdown',
                                         multi=False,
                                         searchable=True,
                                         value='Nordeste',
                                         placeholder='Selecione a Região',
                                         options=[{'label': c, 'value': c}
                                                  for c in (database['Regiao'].unique())], className='dcc_compon'),
                        ]),

                        dbc.Col([

                            html.Div('Selecione o estado', className='fix_label'),
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


# montagem do layout
layout = html.Div(
    [
        html.Div(id='mapa_genero-display-value'),
        # inserindo a navbar
        navbar.navbar,
        dbc.Container(
            [
                grid
            ]
        ),
        dbc.Container([
            dbc.Row([
                dbc.Col([
                    html.P(),
                    #html.H4("Relação Idade x Atividade",style={'margin-bottom': '10px', 'color': 'white', 'textAlign': 'left'}),
                    html.Div(id='genero-atividade'),
                ]),
                dbc.Col([
                    html.Div([
                    html.Div(id='genero_grupo_atividade'),

                ])
            ]),
            dbc.Row([
                dbc.Col([
                            html.Div('Selecione o gênero', className='fix_label'),
                            dcc.Dropdown(id='genero_dropdown',
                                         multi=False,
                                         searchable=True,
                                         value='F',
                                         placeholder='Selecione o gênero',
                                         options=[{'label': 'Feminino', 'value': 'F'},
                                                  {'label': 'Masculino', 'value': 'M'}], className='dcc_compon'),
                        #html.H5('Estado: ' + (dados_idade['Estado'].loc[dados_idade.Estado == 'estado_dropdown'].unique())),
                        #dcc.Graph(id='teste', config={'displayModeBar': False}, className='dcc_compon'),
                    ])
                ],),
                dbc.Col([
                    html.Div([
                        html.Div(id='genero_trabalho'),
                        # html.H5('Estado: ' + (dados_idade['Estado'].loc[dados_idade.Estado == 'estado_dropdown'].unique())),
                        # dcc.Graph(id='teste', config={'displayModeBar': False}, className='dcc_compon'),
                    ])
                ]),
                dbc.Col([
                    html.Div([
                        html.Div(id='genero_grupo'),
                        # html.H5('Estado: ' + (dados_idade['Estado'].loc[dados_idade.Estado == 'estado_dropdown'].unique())),
                        # dcc.Graph(id='teste', config={'displayModeBar': False}, className='dcc_compon'),
                    ])
                ]),

            ]),

            #html.H4("Gráfico 3", style={'margin-bottom': '10px', 'color': 'white', 'textAlign': 'center'}),
            #dcc.Graph(id='teste3', config={'displayModeBar': False}, className='dcc_compon', style={'margin-top': '20px', }),
        ])

    ], id='mainContainer', style={'display': 'flex', 'flex-direction': 'column'}
)



#Callback genero Grupo atividade (Agrícoloa / Não Agrícola)
@callback(
    Output('genero-atividade','children'),
    Input('estado_dropdown','value')
)

def update_output_div(estado_dropdown):
    filtro_estado = df_faixa_etaria_atividade[(df_faixa_etaria_atividade['NOUF'] == estado_dropdown)]  # Dropdown
    ativ_geral = filtro_estado.groupby(['Sexo', 'AtividadeGeral'])[['Trabalhadores']].sum().reset_index()
    df_feminino = ativ_geral.loc[ativ_geral.Sexo == 'F', ['Sexo', 'AtividadeGeral', 'Trabalhadores']]
    df_masculino = ativ_geral.loc[ativ_geral.Sexo == 'M', ['Sexo', 'AtividadeGeral', 'Trabalhadores']]

    fig = make_subplots(1, 2, specs=[[{'type': 'domain'}, {'type': 'domain'},]],
                        subplot_titles=['Feminino', 'Masculino'])
    fig.add_trace(go.Pie(labels=df_feminino.AtividadeGeral, values=df_feminino.Trabalhadores,
                         name="Feminino"), 1,1)
    fig.add_trace(go.Pie(labels=df_masculino.AtividadeGeral, values=df_masculino.Trabalhadores,
                         name="Masculino"), 1,2)
    fig.update_layout(title_text='Pessoas de 5 a 17 anos ocupadas por atividade',
                      #autosize=True,
                      #paper_bgcolor='#272b30',
                      #font_color='white',

                      )
    return [

         html.Div(dcc.Graph(figure=fig,config={'displayModeBar': False}))

     ]

# #Callback genero grupo atividade
@callback(
    Output('genero_grupo_atividade','children'),
    Input('estado_dropdown','value'),

)

def update_output_div(estado_dropdown):
    filtro_estado = df_faixa_etaria_atividade[(df_faixa_etaria_atividade['NOUF'] == estado_dropdown)]  # Dropdown
    ativ_grupo = filtro_estado.groupby(['Sexo', 'GrupamentoAtividade'])[['Trabalhadores']].sum().reset_index()

    fig = px.histogram(ativ_grupo, x="GrupamentoAtividade", y="Trabalhadores",
                       color='Sexo', barmode='group',
                       )

    fig.update_layout(title_text='Por grupo de atividade',
                      autosize=True,
                      # paper_bgcolor='#272b30',
                      # plot_bgcolor='#272b30',
                      # font_color='white'
                      yaxis=dict(title='Nº de Trabalhadores(as)'),
                      xaxis=dict(title='Grupo da atividade')
                      )


    return [

         html.Div(dcc.Graph(figure=fig,config={'displayModeBar': False}))

     ]


#Callback Grupo atividade (Agrícoloa / Não Agrícola) POR GÊNERO
@callback(
    Output('genero_trabalho','children'),
    Input('estado_dropdown','value'),
    Input('genero_dropdown','value')
)

def update_output_div(estado_dropdown, genero_dropdown):
    filtro_estado = df_faixa_etaria_atividade[(df_faixa_etaria_atividade['NOUF'] == estado_dropdown)]  # Dropdown
    ativ_geral = filtro_estado.groupby(['Sexo','FaixaIdade', 'AtividadeGeral','GrupamentoAtividade'])[['Trabalhadores']].sum().reset_index()

    #Incluir IF para alterar o Sexo
    df_sexo = ativ_geral.loc[ativ_geral.Sexo == genero_dropdown, ['Sexo', 'FaixaIdade', 'AtividadeGeral','GrupamentoAtividade', 'Trabalhadores']]
    df_5_13 = df_sexo.loc[df_sexo.FaixaIdade == "5 a 13", ['Sexo', 'FaixaIdade', 'AtividadeGeral', 'Trabalhadores']]
    df_14_17 = df_sexo.loc[df_sexo.FaixaIdade == "14 a 17", ['Sexo', 'FaixaIdade', 'AtividadeGeral', 'Trabalhadores']]

    fig = make_subplots(1, 2, specs=[[{'type': 'domain'}, {'type': 'domain'}]],
                        subplot_titles=['5 a 13', '14 a 17'])
    fig.add_trace(go.Pie(labels=df_5_13.AtividadeGeral, values=df_5_13.Trabalhadores,
                         name="5 a 13"), 1, 1)
    fig.add_trace(go.Pie(labels=df_14_17.AtividadeGeral, values=df_14_17.Trabalhadores,
                         name="14 a 17"), 1, 2)

    fig.update_layout(title_text='Pessoas ocupadas por atividade e faixa etária',
                      autosize=True,
                      # paper_bgcolor='#272b30',
                      # font_color='white',
                      )


    return [

         html.Div(dcc.Graph(figure=fig,config={'displayModeBar': False}))

     ]

# #Callback grupo atividade POR GÊNERO
@callback(
    Output('genero_grupo','children'),
    Input('estado_dropdown','value'),
    Input('genero_dropdown', 'value')

)

def update_output_div(estado_dropdown, genero_dropdown):
    filtro_estado = df_faixa_etaria_atividade[(df_faixa_etaria_atividade['NOUF'] == estado_dropdown)]  # Dropdown
    ativ_geral = filtro_estado.groupby(['Sexo','FaixaIdade','AtividadeGeral','GrupamentoAtividade'])[['Trabalhadores']].sum().reset_index()
    df_sexo = ativ_geral.loc[ativ_geral.Sexo == genero_dropdown, ['Sexo', 'FaixaIdade', 'AtividadeGeral','GrupamentoAtividade', 'Trabalhadores']]

    fig = px.histogram(df_sexo, x="GrupamentoAtividade", y="Trabalhadores",
                       color='FaixaIdade', barmode='group',
                       )

    fig.update_layout(title_text='Por grupo de atividade',
                      autosize=True,
                      # paper_bgcolor='#272b30',
                      # plot_bgcolor='#272b30',
                      # font_color='white'
                      yaxis=dict(title='Nº de Trabalhadores(as)'),
                      xaxis=dict(title='Grupo da atividade'),
                      legend=dict(title='Faixa Etária')
                      )


    return [

         html.Div(dcc.Graph(figure=fig,config={'displayModeBar': False}))

     ]


@callback(
    Output('mapa_genero-display-value', 'children'),
    #Input('drop-down-mapa_regiao', 'value'))
    Input('nav-bar', 'href'))
def display_value(value):
    return f'You have selected {value}'
