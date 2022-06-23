import pandas as pd
import numpy as np
from .database import cria_conexao
from .secrets import *

def cria_dados_temporais():
    # cria conexão com banco
    con = cria_conexao(user=user, passwd=password, database='TrabalhoInfantil')
    # lê tabela
    df = pd.read_sql_table('tbpnadc', con=con)
    # aplica filtros e faz tratamento inicial
    df = df.astype({'Peso': float, 'Idade': int})
    df = df[(df['Ano'] > '2017') & (df['Idade'] < 18) & (df['Idade'] >= 5)]
    df = df[(df['TrabDinheiro'] == '1') |
            (df['TrabNatura'] == '1') |
            (df['Bico'] == '1') |
            (df['TrabSemReceber'] == '1') |
            (df['TrabQueEstavaAfastado'] == '1') |
            (df['TrabDinheiro5a13'] == '1') |
            (df['TrabNatura5a13'] == '1') |
            (df['Bico5a13'] == '1') |
            (df['TrabSemReceber5a13'] == '1')]
    df['FaixaIdade'] = np.where(df['Idade'].between(5, 13, inclusive=True), '5 a 13',
                                '14 a 17')
    df = df[['Peso', 'CDUF', 'FaixaIdade', 'Ano', 'Trimestre']]
    df_gr = df.groupby(['CDUF', 'FaixaIdade','Ano', 'Trimestre'], as_index=False).sum()
    df_gr = df_gr.rename(columns={'Peso': 'Trabalhadores'})
    # cria tabela com códigos das ufs
    df_municipio = pd.read_sql_table('tbmunicipios', con=con)
    df_uf = df_municipio[['CDUF', 'UF', 'NOUF']].drop_duplicates()
    df_gr = df_gr.merge(df_uf, on='CDUF', how='left')
    try:
        df_gr.to_sql(name='tbseriestemporais', con=con, if_exists='replace', index=False)
    except ValueError:
        print('Falha ao carregar os dados')
