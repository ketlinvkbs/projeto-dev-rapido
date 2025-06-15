import tkinter as tk
from tkinter import messagebox
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib
matplotlib.use("TkAgg")


def gerar_mapa_por_regiao(root, dados):
    for widget in root.winfo_children():
        widget.destroy()

    frame = tk.Frame(root, bg="#0B3D2E")
    frame.pack(fill="both", expand=True)

    titulo = tk.Label(frame, text="Selecione uma Região", font=("Helvetica", 20), fg="white", bg="#0B3D2E")
    titulo.pack(pady=20)

    regioes = ["Norte", "Nordeste", "Centro-Oeste", "Sudeste", "Sul"]
    for regiao in regioes:
        botao = tk.Button(
            frame, text=regiao, font=("Helvetica", 14), bg="goldenrod", fg="black", width=20,
            command=lambda r=regiao: mostrar_mapa_regiao(root, r, dados)
        )
        botao.pack(pady=10)

    voltar = tk.Button(frame, text="Voltar", bg="darkred", fg="white", command=lambda: root.limpar_tela(recarregar=True))
    voltar.pack(pady=20)


def mostrar_mapa_regiao(root, regiao, dados):
    try:
        shapefile_path = "shapefiles/BR_UF_2024.shp"
        gdf = gpd.read_file(shapefile_path)

        estados_por_regiao = {
            "Norte": ["AC", "AP", "AM", "PA", "RO", "RR", "TO"],
            "Nordeste": ["AL", "BA", "CE", "MA", "PB", "PE", "PI", "RN", "SE"],
            "Centro-Oeste": ["DF", "GO", "MT", "MS"],
            "Sudeste": ["ES", "MG", "RJ", "SP"],
            "Sul": ["PR", "RS", "SC"]
        }

        def obter_regiao(sigla):
            for reg, estados in estados_por_regiao.items():
                if sigla in estados:
                    return reg
            return "Indefinida"

        gdf["regiao"] = gdf["SIGLA_UF"].apply(obter_regiao)
        gdf = gdf[gdf.geometry.notnull() & gdf.is_valid]
        gdf_regiao = gdf[gdf["regiao"] == regiao]

        estados_da_regiao = estados_por_regiao.get(regiao, [])

        dados_regiao = dados[dados["sigla_uf"].isin(estados_da_regiao)].copy()
        municipios_df = pd.read_csv("municipios.csv", dtype={"geocodigo": str})
        dados_regiao["id_municipio"] = dados_regiao["id_municipio"].astype(str)
        municipios_df["geocodigo"] = municipios_df["geocodigo"].astype(str)
        dados_regiao = dados_regiao.merge(municipios_df, left_on="id_municipio", right_on="geocodigo", how="left")
        dados_regiao["nome"].fillna("Desconhecido", inplace=True)

        for widget in root.winfo_children():
            widget.destroy()

        frame = tk.Frame(root, bg="#0B3D2E")
        frame.pack(fill="both", expand=True)

        tk.Label(frame, text=f"Região: {regiao}", font=("Helvetica", 18), fg="white", bg="#0B3D2E").pack(pady=10)

        bioma_mais_afetado = dados_regiao["bioma"].value_counts().idxmax() if not dados_regiao.empty else "Indefinido"
        tk.Label(frame, text=f"Bioma mais afetado: {bioma_mais_afetado}", font=("Helvetica", 14), fg="white", bg="#0B3D2E").pack(pady=5)

        fig, ax = plt.subplots(figsize=(10, 8))
        gdf_regiao.plot(ax=ax, color="#0B3D2E", edgecolor="white")

        scatter = ax.scatter(
            dados_regiao["longitude"], dados_regiao["latitude"],
            c='red', alpha=0.7, s=15
        )

        for _, row in gdf_regiao.iterrows():
            if row['geometry'] is not None and not row['geometry'].is_empty:
                centroid = row['geometry'].centroid
                ax.text(
                    centroid.x, centroid.y, row['SIGLA_UF'], fontsize=10,
                    fontweight='bold', ha='center', va='center', color='white',
                    bbox=dict(facecolor='black', alpha=0.5, boxstyle='round,pad=0.3')
                )

        ax.set_title(f"{regiao} - Mapa de Queimadas", fontsize=16)
        ax.axis("off")

        # Zoom com roda do mouse
        def zoom_fun(event):
            base_scale = 1.1
            cur_xlim = ax.get_xlim()
            cur_ylim = ax.get_ylim()
            xdata, ydata = event.xdata, event.ydata
            if xdata is None or ydata is None:
                return
            scale_factor = 1 / base_scale if event.button == 'up' else base_scale if event.button == 'down' else 1
            new_width = (cur_xlim[1] - cur_xlim[0]) * scale_factor
            new_height = (cur_ylim[1] - cur_ylim[0]) * scale_factor
            relx = (cur_xlim[1] - xdata) / (cur_xlim[1] - cur_xlim[0])
            rely = (cur_ylim[1] - ydata) / (cur_ylim[1] - cur_ylim[0])
            ax.set_xlim([xdata - new_width * (1 - relx), xdata + new_width * relx])
            ax.set_ylim([ydata - new_height * (1 - rely), ydata + new_height * rely])
            ax.figure.canvas.draw_idle()

        fig.canvas.mpl_connect('scroll_event', zoom_fun)

        # --- Hover annotation ---
        annot = ax.annotate(
            "", xy=(0, 0), xytext=(15, 15), textcoords="offset points",
            bbox=dict(boxstyle="round", fc="w"),
            arrowprops=dict(arrowstyle="->")
        )
        annot.set_visible(False)

        def hover(event):
            if event.inaxes == ax:
                cont, ind = scatter.contains(event)
                if cont:
                    idx = ind["ind"][0]
                    pos = scatter.get_offsets()[idx]
                    annot.xy = pos
                    texto = f"Cidade: {dados_regiao['nome'].iloc[idx]}\nData: {dados_regiao['data_hora'].iloc[idx]}"
                    annot.set_text(texto)
                    annot.get_bbox_patch().set_facecolor("lightyellow")
                    annot.get_bbox_patch().set_alpha(0.9)
                    annot.set_visible(True)
                    canvas.draw_idle()
                else:
                    if annot.get_visible():
                        annot.set_visible(False)
                        canvas.draw_idle()

        fig.canvas.mpl_connect("motion_notify_event", hover)

        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

        toolbar = NavigationToolbar2Tk(canvas, frame)
        toolbar.update()
        toolbar.pack(fill="x")

        tk.Button(frame, text="Voltar", bg="darkred", fg="white", command=lambda: root.limpar_tela(recarregar=True)).pack(pady=10)

    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao gerar o mapa por região:\n{str(e)}")