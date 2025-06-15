import os
import zipfile
import requests

# URL oficial (IBGE)
url = "https://geoftp.ibge.gov.br/organizacao_do_territorio/malhas_territoriais/malhas_municipais/2022/Brasil/BR/BR_UF_2022.zip"
saida_zip = "regioes_brasil.zip"
pasta_destino = "shapefiles"

# Baixar o zip
print("Baixando o shapefile...")
r = requests.get(url)
with open(saida_zip, "wb") as f:
    f.write(r.content)

# Criar a pasta se não existir
if not os.path.exists(pasta_destino):
    os.makedirs(pasta_destino)

# Extrair o zip
print("Extraindo arquivos...")
with zipfile.ZipFile(saida_zip, 'r') as zip_ref:
    zip_ref.extractall(pasta_destino)

# Remover o zip
os.remove(saida_zip)

print("Download e extração concluídos.")

