import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import mplcursors

# Exemplo de mapeamento de id_municipio para nome
mapeamento_municipios = {
    2903409: 'Camaçari - BA',
    3550308: 'São Paulo - SP',
    5208707: 'Goiânia - GO',
    # Adicione mais conforme precisar
}

def classificar_intensidade(valor):
    if pd.isna(valor):
        return 'desconhecida'
    if valor < 100:
        return 'fraca'
    elif valor < 300:
        return 'media'
    else:
        return 'forte'

def gerar_mapa_brasil_estatico(dados, frame):
    try:
        # Criar coluna 'nome_municipio' com base no dicionário
        dados["nome_municipio"] = dados["id_municipio"].map(mapeamento_municipios).fillna("Desconhecido")

        # Classificar intensidade com base na potencia_radiativa_fogo
        dados["intensidade"] = dados["potencia_radiativa_fogo"].apply(classificar_intensidade)

        # Cores
        cor_por_intensidade = {
            "fraca": "yellow",
            "media": "orange",
            "forte": "red",
            "desconhecida": "gray"
        }

        # Carregar shapefile do Brasil (pode estar em data/brasil.shp)
        mapa_brasil = gpd.read_file("data/brasil.shp")

        fig, ax = plt.subplots(figsize=(10, 8))
        mapa_brasil.plot(ax=ax, color='white', edgecolor='black')

        for intensidade, cor in cor_por_intensidade.items():
            subset = dados[dados["intensidade"] == intensidade]
            ax.scatter(
                subset["longitude"], subset["latitude"],
                color=cor, label=intensidade.capitalize(),
                s=20, alpha=0.7
            )

        ax.set_title("Mapa de Queimadas com Intensidade")
        ax.legend(title="Intensidade", loc='lower left')

        # Adicionar interatividade com mplcursors
        pontos = ax.scatter(dados["longitude"], dados["latitude"], color="none", s=20)
        cursor = mplcursors.cursor(pontos, hover=True)

        @cursor.connect("add")
        def on_add(sel):
            linha = dados.iloc[sel.index]
            texto = (
                f"Município: {linha['nome_municipio']}\n"
                f"Estado: {linha['sigla_uf']}\n"
                f"Data/Hora: {linha['data_hora']}\n"
                f"Bioma: {linha['bioma']}\n"
                f"Lat: {linha['latitude']:.2f}, Lon: {linha['longitude']:.2f}\n"
                f"Risco Fogo: {linha['risco_fogo']}\n"
                f"Potência Fogo: {linha['potencia_radiativa_fogo']}"
            )
            sel.annotation.set_text(texto)

        # Embutir no Tkinter
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(expand=True)

    except Exception as e:
        from tkinter import messagebox
        messagebox.showerror("Erro", f"Erro ao gerar mapa: {e}")
