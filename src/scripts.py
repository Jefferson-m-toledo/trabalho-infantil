from ETL import create_database, carrega_municipios, carrega_cnae_domiciliar
from ETL import carrega_codigo_ocupacao, carrega_pnad
from secrets import user, password
##
create_database(user=user, password=password)

## carregar dados de municípios
carrega_municipios()

## carrega dados de cnae
carrega_cnae_domiciliar()

## carrega códigos de importação
carrega_codigo_ocupacao()

## carrega pnad
#carrega_pnad()
