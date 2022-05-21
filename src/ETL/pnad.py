from .helpers import colunas_pnadc
import pandas as pd
from pathlib import Path
import os
#from secrets import password, user
from .database import cria_conexao
user = 'user'
password = 'password'


def _read_dicionario_pnad(file = 'remote_data/dicionario_PNADC_microdados_2019_visita5_20210617.xls'):
    """
    Lê dicionário da pnad
    :param file:
    :return:
    """
    # arquivo de dicionário
    root = Path(__file__).parents[2]
    file = os.path.join(root, file)
    # ler dicionário para um dataframe pandas
    df_dicionario = pd.read_excel(file, skiprows=[0])
    df_dicionario = df_dicionario[df_dicionario['Tamanho'].notna()]
    # cria nome das colunas
    df_dicionario.columns = ['PosicaoInicial','Tamanho','variavel', 'quesito',
                             'referencia', 'Categorias','obs','Periodo']
    # seleciona colunas
    df_dicionario = df_dicionario[['PosicaoInicial','Tamanho','variavel']]
    df_dicionario['Tamanho'] = df_dicionario['Tamanho'].astype(int)
    #variáveis para exportação
    leng = list(df_dicionario['Tamanho'])
    cols = list(df_dicionario['variavel'])
    return leng, cols


def _read_parser_pnadc(file,
                        colunas_pnadc = colunas_pnadc,
                       dicionario = 'remote_data/dicionario_PNADC_microdados_2019_visita5_20210617.xls'
                       ):
    """
    Lê dicionário de dados da pnad e realiza parser nos arquivos txt.
    :param file:
    :param dicionario:
    :param colunas_pnadc:
    :return:
    """
    leng, cols = _read_dicionario_pnad(dicionario)
    df = pd.read_fwf(file, widths=leng, dtype=str)
    df.columns = cols
    df = df[list(colunas_pnadc.keys())]
    df = df.rename(columns=colunas_pnadc)
    return df


def carrega_pnad():
    """
    Carrega dados da Pnad.
    :return:
    """
    root = Path(__file__).parents[2]
    mypath = str(root) + '/remote_data/'
    print(mypath)
    filenames = next(os.walk(mypath), (None, None, []))[2]
    filenames = [file for file in filenames if file.startswith('PNADC_')]
    # cria conexão
    con = cria_conexao(user=user, passwd=password, database='TrabalhoInfantil')
    for file in filenames:
        fpath = os.path.join(mypath, file)
        df = _read_parser_pnadc(fpath)
        # efetua a carga
        try:
            df.to_sql(name='tbpnadc', con=con, if_exists='append', index=False)
        except ValueError:
            print('Falha ao carregar os dados')