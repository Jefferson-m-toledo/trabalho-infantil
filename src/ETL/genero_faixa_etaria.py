import pandas as pd
import numpy as np
from .database import cria_conexao
from secrets import *

def cria_tabela_genero_idade_atividade(tb:str='TrabalhoInfantil'):
    #cria conexão com banco
    con = cria_conexao(user=user, passwd=password, database='TrabalhoInfantil')
    # lê tabela
    df = pd.read_sql_table('tbpnadc', con=con)
    # aplica filtros e faz tratamento inicial
    df = df.astype({'Peso': float, 'Idade': int})
    df = df[(df['Ano'] == '2019') & (df['Trimestre'] == '4') & (df['Idade'] < 18) & (df['Idade'] >= 5)]
    df = df[(df['TrabDinheiro'] == '1') |
            (df['TrabNatura'] == '1') |
            (df['Bico'] == '1') |
            (df['TrabSemReceber'] == '1') |
            (df['TrabQueEstavaAfastado'] == '1') |
            (df['TrabDinheiro5a13'] == '1') |
            (df['TrabNatura5a13'] == '1') |
            (df['Bico5a13'] == '1') |
            (df['TrabSemReceber5a13'] == '1')]
    # altera sexo e grupo de idade
    df['Sexo'] = np.where(df['Sexo'] == '1', 'M', 'F')
    df['FaixaIdade'] = np.where(df['Idade'].between(5, 13, inclusive=True), '5 a 13',
                                '14 a 17')
    df['AtividadeGeral'] = np.where((df['CnaeDomiciliar'] < '10000') |
                                    (df['CnaeDomicilliar5a13'] < '10000'), 'Agricola', 'Nao Agricola')

    df['GrupamentoAtividade'] = np.where((df['CnaeDomiciliar'] < '10000') |
                                         (df['CnaeDomicilliar5a13'] < '10000'), 'Agricultura',
                                         np.where(
                                             ((df['CnaeDomiciliar'] >= '45000') & (df['CnaeDomiciliar'] < '49000')) |
                                             ((df['CnaeDomicilliar5a13'] >= '45000') & (
                                                         df['CnaeDomicilliar5a13'] < '49000')), 'Comercio',
                                             np.where((df['CnaeDomiciliar'] == '97000') |
                                                      (df['CnaeDomicilliar5a13'] == '97000'), 'Servicos Domesticos',
                                                      'Outros')))
    # agrupa por filtros
    df = df[['Peso', 'Sexo', 'FaixaIdade', 'AtividadeGeral', 'GrupamentoAtividade']]
    df_gr = df.groupby(['Sexo', 'FaixaIdade', 'AtividadeGeral', 'GrupamentoAtividade'], as_index=False).sum()
    df_gr = df_gr.rename(columns={'Peso': 'Trabalhadores'})
    try:
        df_gr.to_sql(name='tbsexoidadeatividade', con=con, if_exists='append', index=False)
    except ValueError:
        print('Falha ao carregar os dados')

