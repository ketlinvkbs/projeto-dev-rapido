import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import os
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from matplotlib.lines import Line2D

def gerar_mapa_com_pontos(dados, frame_destino):
    try:
        for col in ['latitude', 'longitude', 'frp']:
            if col not in dados.columns:
                raise ValueError("As colunas necessárias ('latitude', 'longitude', 'frp') não foram encontradas.")

        caminho_shapefile = os.path.join("Data", "Brasil.shp")
        if not os.path.exists(caminho_shapefile):
            raise FileNotFoundError("Shapefile do Brasil não encontrado em 'Data/Brasil.shp'.")

        brasil = gpd.read_file(caminho_shapefile)

        # Criar GeoDataFrame com geometria dos pontos
        gdf = gpd.GeoDataFrame(
            dados.dropna(subset=['latitude', 'longitude']),
            geometry=gpd.points_from_xy(dados['longitude'], dados['latitude']),
            crs='EPSG:4326'
        )

        # Classificação de intensidade
        def classificar_intensidade(frp):
            if frp >= 30:
                return 'Alta'
            elif frp >= 15:
                return 'Média'
            else:
                return 'Baixa'

        gdf['intensidade'] = gdf['frp'].apply(classificar_intensidade)
        gdf['cor'] = gdf['intensidade'].map({'Alta': 'red', 'Média': 'orange', 'Baixa': 'yellow'})
        gdf['tamanho'] = gdf['frp'].clip(5, 50)  # Limitando tamanho dos pontos

        # Criar o mapa
        fig, ax = plt.subplots(figsize=(8, 9))
        brasil.plot(ax=ax, color='white', edgecolor='black')

        # Plotar os pontos
        gdf.plot(
            ax=ax,
            color=gdf['cor'],
            markersize=gdf['tamanho'],
            alpha=0.6
        )

        # Título com total
        total = len(gdf)
        plt.title(f"Queimadas no Brasil: {total} registros", fontsize=14)

        # Remover eixos
        ax.set_axis_off()

        # Legenda personalizada
        legenda = [
            Line2D([0], [0], marker='o', color='w', label='Alta Intensidade', markerfacecolor='red', markersize=10),
            Line2D([0], [0], marker='o', color='w', label='Média Intensidade', markerfacecolor='orange', markersize=10),
            Line2D([0], [0], marker='o', color='w', label='Baixa Intensidade', markerfacecolor='yellow', markersize=10)
        ]
        ax.legend(handles=legenda, loc='lower left')

        # Integrar ao tkinter
        canvas = FigureCanvasTkAgg(fig, master=frame_destino)
        canvas.draw()
        canvas.get_tk_widget().pack(pady=10)

    except Exception as e:
        tk.messagebox.showerror("Erro ao gerar o mapa com pontos", str(e))
