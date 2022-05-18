import mysql.connector
from pymysql import connect
from sqlalchemy import create_engine

def create_database(user: str = 'root', password=str):
    """
    Cria database MySql
    :param user: Usuário
    :param password: senha
    :return:
    """
    # cria conexão
    mydb = mysql.connector.connect(
        host="127.0.0.1",
        user=user,
        password=password
    )
    # cria cursor
    mycursor = mydb.cursor()

    try:
        mycursor.execute("CREATE DATABASE TrabalhoInfantil")
    except:
        raise Exception('Não foi possível criar database')


def cria_conexao(database:str, passwd: str,host:str="127.0.0.1", user:str='root'):
    engine = create_engine(f'mysql+pymysql://{user}:{passwd}@{host}/{database}')

    return engine