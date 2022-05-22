import mysql.connector
from pymysql import connect
from sqlalchemy import create_engine

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