import pandas as pd

# URL do arquivo CSV com os dados dos municípios
url = 'https://geoftp.ibge.gov.br/informacoes_ambientais/estudos_ambientais/grade_estatistica_de_dados_ambientais/dados_tabulares/municipios/municipios.csv'

# Carregar os dados
df = pd.read_csv(url)

# Selecionar as colunas desejadas
df_municipios = df[['id_municipio', 'nome_municipio']]

# Salvar o arquivo CSV
df_municipios.to_csv('municipios.csv', index=False)

print("Arquivo 'municipios.csv' gerado com sucesso!")
