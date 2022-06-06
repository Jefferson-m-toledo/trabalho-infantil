import pandas as pd
import numpy as np
from .database import cria_conexao
from .secrets import *

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
    df = df[['Peso', 'CDUF', 'Sexo', 'FaixaIdade', 'AtividadeGeral', 'GrupamentoAtividade']]
    df_gr = df.groupby(['CDUF','Sexo', 'FaixaIdade', 'AtividadeGeral', 'GrupamentoAtividade'], as_index=False).sum()
    df_gr = df_gr.rename(columns={'Peso': 'Trabalhadores'})
    # cria tabela com códigos das ufs
    df_municipio = pd.read_sql_table('tbmunicipios', con=con)
    df_uf = df_municipio[['CDUF', 'UF','NOUF']].drop_duplicates()
    df_gr = df_gr.merge(df_uf, on='CDUF', how='left')
    try:
        df_gr.to_sql(name='tbsexoidadeatividade', con=con, if_exists='replace', index=False)
    except ValueError:
        print('Falha ao carregar os dados')


def cria_tb_uf_atividade_populacao():
    # cria conexão com banco
    con = cria_conexao(user=user, passwd=password, database='TrabalhoInfantil')
    # le tabela com dados da pnad
    df = pd.read_sql_table('tbpnadc', con=con)
    df = df.astype({'Peso': float, 'Idade': int})
    df = df[(df['Ano'] == '2019') & (df['Trimestre'] == '4')]
    # cria tabela com códigos das ufs
    df_municipio = pd.read_sql_table('tbmunicipios', con=con)
    df_uf = df_municipio[['CDUF', 'UF']].drop_duplicates()
    # tabela de cnae
    df_cnae = pd.read_sql_table('tbcnae', con=con)
    df_cnae = df_cnae[['CDCnae', 'DSSecao']]
    #população
    df_populacao = df[['CDUF', 'Idade', 'Peso']]
    df_populacao = df_populacao.groupby(['CDUF', 'Idade'], as_index=False).sum()
    df_populacao = df_populacao.rename(columns={'Peso': 'Populacao'})
    df_populacao = df_populacao.merge(df_uf, on='CDUF', how='left')
    df_populacao = df_populacao[['UF', 'Idade', 'Populacao']]
    # ocupação
    df_ocupacao = df[(df['TrabDinheiro'] == '1') |
                     (df['TrabNatura'] == '1') |
                     (df['Bico'] == '1') |
                     (df['TrabSemReceber'] == '1') |
                     (df['TrabQueEstavaAfastado'] == '1') |
                     (df['TrabDinheiro5a13'] == '1') |
                     (df['TrabNatura5a13'] == '1') |
                     (df['Bico5a13'] == '1') |
                     (df['TrabSemReceber5a13'] == '1')]

    df_ocupacao = df_ocupacao[['CDUF', 'Idade', 'CnaeDomiciliar', 'CnaeDomicilliar5a13', 'Peso']]
    df_ocupacao_14 = df_ocupacao[df_ocupacao['Idade'] > 13].rename(columns={'CnaeDomiciliar': 'CDCnae'}).drop(
        columns=['CnaeDomicilliar5a13'])
    df_ocupacao_5 = df_ocupacao[df_ocupacao['Idade'] <= 13].rename(columns={'CnaeDomicilliar5a13': 'CDCnae'}).drop(
        columns=['CnaeDomiciliar'])
    df_concat = pd.concat([df_ocupacao_14, df_ocupacao_5])
    df_concat = df_concat[df_concat['CDCnae'].notna()]
    df_concat = df_concat.rename(columns={'Peso': 'Trabalhadores'})
    df_concat = df_concat.merge(df_uf, on='CDUF', how='left').drop(columns=['CDUF'])
    df_concat = df_concat.merge(df_cnae, on='CDCnae', how='left').drop(columns=['CDCnae'])
    df_concat = df_concat.rename(columns={'DSSecao': 'AtividadeEconomica'})
    df_concat = df_concat.groupby(['UF', 'AtividadeEconomica', 'Idade'], as_index=False).sum()
    df_return = df_concat.merge(df_populacao, on=['UF', 'Idade'], how='left')
    try:
        df_return.to_sql(name='tbpopulacaoufidade', con=con, if_exists='replace', index=False)
    except ValueError:
        print('Falha ao carregar os dados')
