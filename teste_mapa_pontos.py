import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from shapely.geometry import Point

# Criar dados fictícios
dados_mock = pd.DataFrame({
    'latitude': [-15.78, -3.71, -22.9],
    'longitude': [-47.93, -38.52, -43.2],
    'frp': [10, 25, 45],  # Intensidade: fraca, média, forte
    'datahora': ['2025-05-01 14:00:00', '2025-05-02 10:00:00', '2025-05-03 16:00:00']
})

# Gerar geometria
gdf = gpd.GeoDataFrame(
    dados_mock,
    geometry=gpd.points_from_xy(dados_mock['longitude'], dados_mock['latitude']),
    crs='EPSG:4326'
)

# Categorizar a intensidade
def classificar_cor(frq):
    if frq >= 40:
        return 'red'
    elif frq >= 20:
        return 'orange'
    else:
        return 'yellow'

gdf['cor'] = gdf['frp'].apply(classificar_cor)

# Carregar shapefile do Brasil
brasil = gpd.read_file('Data/BR_UF_2022.shp')

# Plotar
fig, ax = plt.subplots(figsize=(8, 10))
brasil.plot(ax=ax, color='white', edgecolor='black')
gdf.plot(ax=ax, color=gdf['cor'], markersize=50, alpha=0.6)

plt.title("Pontos de Queimadas no Brasil (Exemplo de Teste)")
ax.set_axis_off()

# Legenda
from matplotlib.lines import Line2D
legend_elements = [
    Line2D([0], [0], marker='o', color='w', label='Alta Intensidade', markerfacecolor='red', markersize=10),
    Line2D([0], [0], marker='o', color='w', label='Média Intensidade', markerfacecolor='orange', markersize=10),
    Line2D([0], [0], marker='o', color='w', label='Baixa Intensidade', markerfacecolor='yellow', markersize=10)
]
ax.legend(handles=legend_elements, loc='lower left')

plt.show()
