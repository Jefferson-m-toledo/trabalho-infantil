from ETL import create_database, carrega_municipios, carrega_cnae_domiciliar, exporta_csv
from ETL import carrega_codigo_ocupacao, carrega_pnad, cria_tabela_genero_idade_atividade
from ETL import cria_tb_uf_atividade_populacao
from secrets import *

##
#create_database(user=user, password=password)

## carregar dados de municípios
#carrega_municipios()

## carrega dados de cnae
#carrega_cnae_domiciliar()

## carrega códigos de importação
#carrega_codigo_ocupacao()

## carrega pnad
#carrega_pnad()

# cria tabela por genero/faixa de idade/ atividade
#cria_tabela_genero_idade_atividade()
#exporta_csv(tabela='tbsexoidadeatividade', output='dados_tratados/trab_infantil_sexo_idade_atividade.csv')

# cria tabela oir uf idade
cria_tb_uf_atividade_populacao()
exporta_csv(tabela='tbpopulacaoufidade', output='dados_tratados/populacao_uf_idade.csv')