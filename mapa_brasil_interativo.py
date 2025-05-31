import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backend_bases import MouseEvent
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import os

def gerar_mapa_brasil_interativo(dados, frame):
    try:
        # Carrega shapefile do Brasil
        shp_path = os.path.join("data", "BR_UF_2022.shp")
        brasil = gpd.read_file(shp_path)

        # Remove nulos
        dados = dados.dropna(subset=["latitude", "longitude"])

        # Criar GeoDataFrame dos pontos
        gdf_pontos = gpd.GeoDataFrame(
            dados,
            geometry=gpd.points_from_xy(dados["longitude"], dados["latitude"]),
            crs="EPSG:4326"
        )

        # Define cores com base na frp
        def cor_frp(frp):
            if frp >= 100:
                return "red"
            elif frp >= 50:
                return "orange"
            else:
                return "yellow"

        cores = dados["potencia_radiativa_fogo"].apply(lambda x: cor_frp(float(x)) if pd.notnull(x) else "gray")

        fig, ax = plt.subplots(figsize=(10, 8))
        brasil.plot(ax=ax, color="whitesmoke", edgecolor="black")
        scatter = ax.scatter(
            dados["longitude"],
            dados["latitude"],
            c=cores,
            s=20,
            alpha=0.6,
            edgecolor="black"
        )

        ax.set_title("Pontos de Queimadas no Brasil", fontsize=16)

        # Tooltip
        annot = ax.annotate("", xy=(0, 0), xytext=(20, 20),
                            textcoords="offset points", bbox=dict(boxstyle="round", fc="w"),
                            arrowprops=dict(arrowstyle="->"))
        annot.set_visible(False)

        def atualizar_tooltip(indice):
            info = dados.iloc[indice]
            texto = (
                f"Município: {info.get('id_municipio', 'Desconhecido')}\n"
                f"UF: {info.get('sigla_uf', '')}\n"
                f"Bioma: {info.get('bioma', '')}\n"
                f"Data: {info.get('data_hora', '')}\n"
                f"Latitude: {info.get('latitude', '')}\n"
                f"Longitude: {info.get('longitude', '')}\n"
                f"Risco de Fogo: {info.get('risco_fogo', '')}\n"
                f"Potência (FRP): {info.get('potencia_radiativa_fogo', '')}"
            )
            return texto

        def hover(event: MouseEvent):
            vis = annot.get_visible()
            if event.inaxes == ax:
                cont, ind = scatter.contains(event)
                if cont:
                    i = ind["ind"][0]
                    pos = scatter.get_offsets()[i]
                    annot.xy = pos
                    texto = atualizar_tooltip(i)
                    annot.set_text(texto)
                    annot.set_visible(True)
                    fig.canvas.draw_idle()
                elif vis:
                    annot.set_visible(False)
                    fig.canvas.draw_idle()

        fig.canvas.mpl_connect("motion_notify_event", hover)

        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(expand=True, fill="both", padx=10, pady=10)

    except Exception as e:
        import tkinter.messagebox as msg
        msg.showerror("Erro", f"Erro ao gerar mapa interativo: {e}")
