import pandas as pd
import requests

def adicionar_info_municipios():
    try:
        # Baixa o arquivo GeoJSON de municípios
        url = "https://raw.githubusercontent.com/tbrugz/geodata-br/master/geojson/geojs-100-mun.json"
        response = requests.get(url)
        response.raise_for_status()

        geojson = response.json()

        municipios_lista = []
        for feature in geojson['features']:
            props = feature['properties']
            municipios_lista.append({
                'id_municipio': str(props['cod']),
                'nome': props['name'],
                'uf': props['uf']
            })

        municipios_df = pd.DataFrame(municipios_lista)

        # Salva o CSV
        municipios_df.to_csv('municipios.csv', index=False, encoding='utf-8')
        print("Arquivo 'municipios.csv' criado com sucesso!")

    except Exception as e:
        print(f"Ocorreu um erro: {e}")
