import mysql.connector
from pymysql import connect
from sqlalchemy import create_engine
from .secrets import user,password
import pandas as pd
from pathlib import Path
import os

def create_database(user: str = 'root', password=str, database='TrabalhoInfantil'):
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
    mycursor.execute("SHOW DATABASES")
    databases = [x[0] for x in mycursor]
    if database not in databases:
        try:
            mycursor.execute(f"CREATE DATABASE {database}")
        except:
            print('A database já existe')


def cria_conexao(database:str, passwd: str,host:str="127.0.0.1", user:str='root'):
    engine = create_engine(f'mysql+pymysql://{user}:{passwd}@{host}/{database}')

    return engine

def exporta_csv(tabela: str, output:str):
    con = cria_conexao(user=user, passwd=password, database='TrabalhoInfantil')
    df = pd.read_sql_table(tabela, con=con)
    root = Path(__file__).parents[2]
    file = os.path.join(root, output)
    df.to_csv(file, index=False)
