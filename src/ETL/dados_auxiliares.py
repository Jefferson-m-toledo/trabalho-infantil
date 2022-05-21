import pandas as pd
from .database import cria_conexao
#from secrets import password, user
from pathlib import Path
import os
user = 'user'
password = 'password'


def carrega_municipios(arquivo: str = 'remote_data/RELATORIO_DTB_BRASIL_MUNICIPIO.xls'):
    """
    Trata e carrega tabela de municípios.
    :param arquivo:
    :return:
    """
    root = Path(__file__).parents[2]
    arquivo = os.path.join(root, arquivo)
    # lê arquivo do IBGE
    df = pd.read_excel(arquivo, dtype=str)
    # altera nome das colunas
    change_names = {'UF': 'CDUF',
                    'Nome_UF': 'NOUF',
                    'Região Geográfica Intermediária': 'CDRGI',
                    'Nome Região Geográfica Intermediária': 'NORGI',
                    'Região Geográfica Imediata': 'RGInt',
                    'Nome Região Geográfica Imediata': 'NORGInt',
                    'Mesorregião Geográfica': 'CDMesorregiao',
                    'Nome_Mesorregião': 'NOMesorregiao',
                    'Microrregião Geográfica': 'CDMicrorregiao',
                    'Nome_Microrregião': 'NOMicrorregiao',
                    'Município': 'IndexMunicipio',
                    'Código Município Completo': 'CDMunicipio',
                    'Nome_Município': 'NOMunicipio'}
    df = df.rename(columns=change_names)
    # cria coluna com UF
    ufs = {'11': 'RO', '12': 'AC', '13': 'AM', '14': 'RR', '15': 'PA', '16': 'AP', '17': 'TO',
           '21': 'MA', '22': 'PI', '23': 'CE', '24': 'RN', '25': 'PB', '26': 'PE', '27': 'AL',
           '28': 'SE', '29': 'BA', '31': 'MG', '32': 'ES', '33': 'RJ', '35': 'SP', '41': 'PR',
           '42': 'SC', '43': 'RS', '50': 'MS', '51': 'MT', '52': 'GO', '53': 'DF'}
    df['UF'] = [ufs[uf] for uf in df['CDUF']]
    # cria coluna com regioes
    regioes = {'Norte': ['AC', 'AP', 'AM', 'PA', 'RO', 'RR', 'TO'],
               'Nordeste': ['AL', 'BA', 'CE', 'MA', 'PE', 'PB', 'PI', 'RN', 'SE'],
               'Sudeste': ['ES', 'MG', 'RJ', 'SP'],
               'Centro-Oeste': ['DF', 'MS', 'GO', 'MT'],
               'Sul': ['PR', 'SC', 'RS']
               }

    new_column=[]
    for uf in df['UF']:
        for key in regioes.keys():
            if uf in regioes[key]:
                new_column.append(key)
    df['Regiao'] = new_column
    # cria conexão
    con = cria_conexao(user=user, passwd=password, database='TrabalhoInfantil')
    #efetua a carga
    try:
        df.to_sql(name='tbmunicipios', con=con, if_exists='replace', index=False)
    except ValueError:
        print('Falha ao carregar os dados')


def carrega_cnae_domiciliar(arquivo:str = 'remote_data/CNAE_Domiciliar2.0(DEZEMBRO2008).xls'):
    """
    Carrega dados de cnae domiciliar (atividade econômica)
    :param arquivo: path do arquivo
    :return:
    """
    root = Path(__file__).parents[2]
    arquivo = os.path.join(root, arquivo)
    #ler arquivo
    df = pd.read_excel(arquivo)
    df = df.iloc[3:, 1:]
    df.columns = ['Seção', 'Divisão', 'Classes', 'Denominação']
    df1 = df.copy()
    df1['Seção'] = df1['Seção'].fillna(method='ffill')
    # trta seção de cnae
    df_sec = df[['Seção', 'Denominação']]
    df_sec = df_sec.dropna().drop_duplicates()
    df_sec = df_sec.rename(columns={'Seção': 'CDSecao', 'Denominação': 'DSSecao'}).astype(str)
    df_coresp = df1[['Seção', 'Divisão']].drop_duplicates().dropna()
    # trata divisão de cnae
    df_div = df[['Divisão', 'Denominação']]
    df_div = df_div.dropna().drop_duplicates()
    df_div = pd.merge(df_div, df_coresp, on='Divisão', how='left')
    df_div = df_div.rename(columns={'Divisão': 'CDDivisao', 'Denominação': 'DSDivisao', 'Seção': 'CDSecao'})
    df_div = pd.merge(df_div, df_sec, on='CDSecao', how='left').astype(str)
    # gera table para carga
    df_cnae = df[['Classes', 'Denominação']].dropna()
    df_cnae = df_cnae.rename(columns={'Classes': 'CDCnae', 'Denominação': 'DSCnae'}).astype(str)
    df_cnae['CDDivisao'] = df_cnae['CDCnae'].str[:2]
    df_cnae = pd.merge(df_cnae, df_div, on='CDDivisao', how='left')
    # cria conexão com o banco
    con = cria_conexao(user=user, passwd=password, database='TrabalhoInfantil')
    # efetua a carga
    try:
        df_cnae.to_sql(name='tbcnae', con=con, if_exists='replace', index=False)
    except ValueError:
        print('Falha ao carregar os dados')


def carrega_codigo_ocupacao(arquivo:str = 'remote_data/Estrutura_Ocupacao_COD.xls'):
    """
    Carrega dados de código de ocupação
    :param arquivo:
    :return:
    """
    root = Path(__file__).parents[2]
    arquivo = os.path.join(root, arquivo)
    #ler arquivo
    df = pd.read_excel(arquivo)
    df = df.iloc[2:, :]
    columns = ['GrandeGrupo', 'SubgrupoPrincipal', 'Subgrupo', 'GrupoBase', 'Denominacao']
    df.columns = columns
    df_grandeGrupo = df[['GrandeGrupo', 'Denominacao']]
    df_grandeGrupo = df_grandeGrupo[df_grandeGrupo.GrandeGrupo.notnull()]
    df_grandeGrupo = df_grandeGrupo.rename(columns={'GrandeGrupo': 'CDCODGrandGrupo', 'Denominacao': 'DSCODGrandGrupo'})
    df_grandeGrupo['CDCODGrandGrupo'] = df_grandeGrupo['CDCODGrandGrupo'].astype(str)
    df_subGrupo = df[['Subgrupo', 'Denominacao']]
    df_subGrupo = df_subGrupo[df_subGrupo.Subgrupo.notnull()]
    df_subGrupo = df_subGrupo.rename(columns={'Subgrupo': 'CDCODSubgrupo', 'Denominacao': 'DSCODSubgrupo'})
    df_subGrupo['CDCODSubgrupo'] = df_subGrupo['CDCODSubgrupo'].astype(str)
    df_subGrupoPrincipal = df[['SubgrupoPrincipal', 'Denominacao']]
    df_subGrupoPrincipal = df_subGrupoPrincipal[df_subGrupoPrincipal.SubgrupoPrincipal.notnull()]
    df_subGrupoPrincipal = df_subGrupoPrincipal.rename(columns={'SubgrupoPrincipal': 'CDCODSubgrupoPrincipal',
                                                                'Denominacao': 'DSCODSubgrupoPrincipal'})
    df_subGrupoPrincipal['CDCODSubgrupoPrincipal'] = df_subGrupoPrincipal['CDCODSubgrupoPrincipal'].astype(str)
    df_grupoBase = df[['GrupoBase', 'Denominacao']]
    df_grupoBase = df_grupoBase[df_grupoBase.GrupoBase.notnull()]
    df_grupoBase = df_grupoBase.rename(columns={'GrupoBase': 'CDCOD',
                                                'Denominacao': 'DSCOD'})
    df_grupoBase['CDCOD'] = df_grupoBase['CDCOD'].astype(str)
    df_grupoBase['CDCODSubgrupo'] = df_grupoBase['CDCOD'].astype(str).str[:3]
    df_grupoBase['CDCODSubgrupoPrincipal'] = df_grupoBase['CDCOD'].astype(str).str[:2]
    df_grupoBase['CDCODGrandGrupo'] = df_grupoBase['CDCOD'].astype(str).str[:1]
    df_export = pd.merge(df_grupoBase, df_subGrupo, on='CDCODSubgrupo', how='left')
    df_export = pd.merge(df_export, df_subGrupoPrincipal, on='CDCODSubgrupoPrincipal', how='left')
    df_export = pd.merge(df_export, df_grandeGrupo, on='CDCODGrandGrupo', how='left')
    # cria conexão com o banco
    con = cria_conexao(user=user, passwd=password, database='TrabalhoInfantil')
    # efetua a carga
    try:
        df_export.to_sql(name='tbcodocupacao', con=con, if_exists='replace', index=False)
    except ValueError:
        print('Falha ao carregar os dados')