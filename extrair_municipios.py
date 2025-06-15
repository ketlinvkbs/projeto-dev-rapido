import pandas as pd

# Caminho do arquivo CSV com os dados de queimadas
arquivo_csv = "dados_queimadas.csv"

# Lê o arquivo CSV
dados = pd.read_csv(arquivo_csv)

# Seleciona as colunas de interesse (id_municipio e latitude, longitude)
municipios = dados[['id_municipio', 'latitude', 'longitude']]

# Remove duplicatas para ter IDs únicos de municípios
municipios_unicos = municipios.drop_duplicates(subset=['id_municipio'])

# Salva o resultado em outro CSV
municipios_unicos.to_csv('municipios_ids_unicos.csv', index=False)

print("Arquivo 'municipios_ids_unicos.csv' criado com sucesso!")
