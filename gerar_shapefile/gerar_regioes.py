import geopandas as gpd

print("🔄 Lendo shapefile dos estados...")
estados = gpd.read_file("shapefiles/ne_110m_admin_1_states_provinces.shp")

print("🔍 Filtrando apenas estados do Brasil...")
estados_brasil = estados[estados['admin'] == 'Brazil']

# Mapeamento de estados para regiões
mapa_regioes = {
    'AC': 'Norte', 'AP': 'Norte', 'AM': 'Norte', 'PA': 'Norte', 'RO': 'Norte', 'RR': 'Norte', 'TO': 'Norte',
    'AL': 'Nordeste', 'BA': 'Nordeste', 'CE': 'Nordeste', 'MA': 'Nordeste', 'PB': 'Nordeste', 'PE': 'Nordeste',
    'PI': 'Nordeste', 'RN': 'Nordeste', 'SE': 'Nordeste',
    'DF': 'Centro-Oeste', 'GO': 'Centro-Oeste', 'MT': 'Centro-Oeste', 'MS': 'Centro-Oeste',
    'ES': 'Sudeste', 'MG': 'Sudeste', 'RJ': 'Sudeste', 'SP': 'Sudeste',
    'PR': 'Sul', 'RS': 'Sul', 'SC': 'Sul'
}

print("🧩 Adicionando coluna 'regiao'...")
estados_brasil['regiao'] = estados_brasil['postal'].map(mapa_regioes)

print("🗺️ Agrupando por região...")
regioes = estados_brasil.dissolve(by='regiao', as_index=False)

print("💾 Salvando novo shapefile em shapefiles/regioes_brasil.shp ...")
regioes.to_file("shapefiles/regioes_brasil.shp")

print("✅ Shapefile das regiões criado com sucesso!")
