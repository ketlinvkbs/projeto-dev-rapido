import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import pandas as pd
import os

from download_dados import baixar_dados
from tela_conscientizacao import mostrar_tela_conscientizacao
import tela_quiz
from mapa_brasil_estatico import gerar_mapa_brasil_estatico

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Interface Informativa sobre Queimadas")
        self.attributes("-fullscreen", True)
        self.configure(bg="#0B3D2E")

        self.dados = None
        self.dados_baixados = False

        # Imagem de fundo
        imagem_path = "fundoqueimadas.jpg"
        if os.path.exists(imagem_path):
            self.imagem_fundo = Image.open(imagem_path).resize((self.winfo_screenwidth(), self.winfo_screenheight()))
            self.foto_fundo = ImageTk.PhotoImage(self.imagem_fundo)
            self.label_fundo = tk.Label(self, image=self.foto_fundo)
            self.label_fundo.place(x=0, y=0, relwidth=1, relheight=1)

        self.main_frame = tk.Frame(self, bg="#0B3D2E")
        self.main_frame.pack(expand=True, fill="both")

        self.criar_interface_inicial()
        self.verificar_e_carregar_dados()

    def limpar_tela(self, recarregar=False):
        for widget in self.winfo_children():
            if not isinstance(widget, tk.Label):
                widget.destroy()

        if recarregar:
            self.main_frame = tk.Frame(self, bg="#0B3D2E")
            self.main_frame.pack(expand=True, fill="both")
            self.criar_interface_inicial()

    def criar_interface_inicial(self):
        titulo = tk.Label(self.main_frame, text="Bem-vindo à interface\ninformativa sobre",
                          font=("Helvetica", 20), fg="white", bg="#0B3D2E")
        titulo.pack(pady=20)

        imagem_logo = Image.open("logoqueimadas.jpg").resize((200, 200))
        foto_logo = ImageTk.PhotoImage(imagem_logo)
        logo = tk.Label(self.main_frame, image=foto_logo, bg="#0B3D2E")
        logo.image = foto_logo
        logo.pack(pady=10)

        nome = tk.Label(self.main_frame, text="Queimadas", font=("Georgia", 32, "bold"), fg="white", bg="#0B3D2E")
        nome.pack(pady=5)

        subtitulo = tk.Label(self.main_frame, text="O que deseja acessar?", font=("Georgia", 18), fg="white", bg="#0B3D2E")
        subtitulo.pack(pady=5)

        tk.Button(self.main_frame, text="Mapa de Calor (Correlação)", command=self.abrir_mapa_calor,
                  bg="goldenrod", fg="black", width=30, height=2).pack(pady=10)

        tk.Button(self.main_frame, text="Mapa Estático com Pontos", command=self.abrir_mapa_estatico,
                  bg="goldenrod", fg="black", width=30, height=2).pack(pady=10)

        tk.Button(self.main_frame, text="Conscientização", command=self.abrir_conscientizacao,
                  bg="goldenrod", fg="black", width=30, height=2).pack(pady=10)

        tk.Button(self.main_frame, text="Quiz", command=self.abrir_quiz,
                  bg="goldenrod", fg="black", width=30, height=2).pack(pady=10)

        tk.Button(self.main_frame, text="Sair", command=self.destroy,
                  bg="darkred", fg="white", width=15).pack(pady=20)

    def verificar_e_carregar_dados(self):
        if os.path.exists("queimadas.csv"):
            try:
                self.dados = pd.read_csv("queimadas.csv")
                self.dados_baixados = True
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao ler o arquivo CSV: {e}")

    def abrir_mapa_calor(self):
        try:
            import seaborn as sns
            import matplotlib.pyplot as plt
            from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

            if not self.dados_baixados:
                path = baixar_dados()
                self.dados = pd.read_csv(path)
                self.dados_baixados = True

            self.limpar_tela()
            frame = tk.Frame(self, bg="#0B3D2E")
            frame.pack(expand=True, fill="both")

            btn_voltar = tk.Button(frame, text="Voltar", command=lambda: [frame.destroy(), self.limpar_tela(True)],
                                   bg="goldenrod", fg="black", width=15)
            btn_voltar.pack(pady=10)

            numeric_data = self.dados.select_dtypes(include=[float, int])

            fig, ax = plt.subplots(figsize=(10, 8), facecolor="#0B3D2E")
            ax.set_facecolor("#0B3D2E")

            heatmap = sns.heatmap(numeric_data.corr(), annot=True, cmap="YlOrRd", fmt=".2f",
                                  cbar=True, linewidths=0.5, linecolor='gray', annot_kws={"color": "black"})

            ax.set_title("Correlação entre Variáveis Numéricas", color="white", fontsize=16)
            for label in ax.get_xticklabels() + ax.get_yticklabels():
                label.set_color("white")

            canvas = FigureCanvasTkAgg(fig, master=frame)
            canvas.draw()
            canvas.get_tk_widget().pack(pady=10, expand=True)

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gerar mapa de calor: {e}")

    def abrir_mapa_estatico(self):
        try:
            if not self.dados_baixados:
                path = baixar_dados()
                self.dados = pd.read_csv(path)
                self.dados_baixados = True

            self.limpar_tela()
            frame = tk.Frame(self, bg="#0B3D2E")
            frame.pack(expand=True, fill="both")

            btn_voltar = tk.Button(frame, text="Voltar", command=lambda: [frame.destroy(), self.limpar_tela(True)],
                                   bg="goldenrod", fg="black", width=15)
            btn_voltar.pack(pady=10)

            gerar_mapa_brasil_estatico(self.dados, frame)
            

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gerar o mapa: {e}")

    def abrir_conscientizacao(self):
        self.limpar_tela()
        mostrar_tela_conscientizacao(self, self.limpar_tela)

    def abrir_quiz(self):
        self.limpar_tela()
        tela_quiz.abrir_quiz(self, self.limpar_tela)

if __name__ == "__main__":
    app = App()
    app.mainloop()