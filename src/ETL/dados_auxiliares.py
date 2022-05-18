import pandas as pd
from .database import cria_conexao
from secrets import password, user
from pathlib import Path
import os


def carrega_municipios(arquivo: str = 'remote_data/RELATORIO_DTB_BRASIL_MUNICIPIO.xls'):
    """
    Trata e carrega tabela de municípios.
    :param arquivo:
    :return:
    """
    root = Path(__file__).parents[2]
    arquivo = os.path.join(root, arquivo)
    df = pd.read_excel(arquivo)
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
    con = cria_conexao(user=user, passwd=password, database='TrabalhoInfantil')

    try:
        df.to_sql(name='TBMunicipios', con=con, if_exists='replace', index=False)
    except ValueError:
        print('Falha ao carregar os dados')
