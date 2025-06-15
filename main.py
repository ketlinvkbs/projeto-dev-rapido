# main.py (versão corrigida)
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import pandas as pd
import os

# Importação dos módulos da aplicação
from download_dados import baixar_dados
from tela_conscientizacao import mostrar_tela_conscientizacao
import tela_quiz
from mapa_regioes import gerar_mapa_por_regiao
import ranking_manager
import tela_ranking

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        ranking_manager.init_db()
        self.title("Interface Informativa sobre Queimadas")
        self.attributes("-fullscreen", True)
        self.default_bg_color = "#0B3D2E"
        self.configure(bg=self.default_bg_color)
        self.dados = None
        self.dados_baixados = False
        self.current_user_matricula = None
        self.current_user_municipio = None
        self.label_fundo = None
        self.setup_background_image()
        self.mostrar_tela_login()

    def setup_background_image(self):
        imagem_path = "imagens/fundo_floresta.jpg"
        if os.path.exists(imagem_path):
            try:
                screen_width = self.winfo_screenwidth()
                screen_height = self.winfo_screenheight()
                imagem_fundo_pil = Image.open(imagem_path).resize((screen_width, screen_height))
                self.foto_fundo_tk = ImageTk.PhotoImage(imagem_fundo_pil)
                self.label_fundo = tk.Label(self, image=self.foto_fundo_tk)
                self.label_fundo.place(x=0, y=0, relwidth=1, relheight=1)
                self.label_fundo.lower()
            except Exception as e:
                messagebox.showerror("Erro de Imagem", f"Não foi possível carregar a imagem de fundo: {e}")
        else:
            print(f"Imagem de fundo não encontrada: {imagem_path}")

    def limpar_tela(self, recarregar=False):
        for widget in self.winfo_children():
            if widget != self.label_fundo:
                widget.destroy()
        if recarregar:
            self.mostrar_menu_principal()

    def mostrar_tela_login(self):
        self.limpar_tela()
        login_frame = tk.Frame(self, bg="#FFFFFF", relief=tk.RIDGE, bd=5, padx=40, pady=40)
        login_frame.place(relx=0.5, rely=0.5, anchor="center")
        try:
            imagem_logo_pil = Image.open("imagens/logo_queimadas.jpg").resize((120, 120))
            self.foto_logo_login = ImageTk.PhotoImage(imagem_logo_pil)
            logo_label = tk.Label(login_frame, image=self.foto_logo_login, bg="#FFFFFF")
            logo_label.image = self.foto_logo_login
            logo_label.pack(pady=(0, 15))
        except Exception as e:
            print(f"Erro ao carregar logo na tela de login: {e}")
        tk.Label(login_frame, text="Login no Sistema", font=("Georgia", 22, "bold"), bg="#FFFFFF", fg=self.default_bg_color).pack(pady=10)
        tk.Label(login_frame, text="Matrícula ou CPF:", font=("Helvetica", 12), bg="#FFFFFF", fg="#333333").pack(pady=(10,0), anchor="w")
        self.entry_matricula = tk.Entry(login_frame, font=("Helvetica", 12), width=35, relief=tk.GROOVE, bd=2)
        self.entry_matricula.pack(pady=(0,10), ipady=4)
        tk.Label(login_frame, text="Município:", font=("Helvetica", 12), bg="#FFFFFF", fg="#333333").pack(pady=(10,0), anchor="w")
        self.entry_municipio = tk.Entry(login_frame, font=("Helvetica", 12), width=35, relief=tk.GROOVE, bd=2)
        self.entry_municipio.pack(pady=(0,20), ipady=4)
        tk.Button(login_frame, text="Entrar", command=self.processar_login, bg="goldenrod", fg="black", font=("Helvetica", 12, "bold"), width=20, height=1).pack(pady=15)
        tk.Button(login_frame, text="Sair do Aplicativo", command=self.destroy, bg="darkred", fg="white", font=("Helvetica", 10)).pack(pady=(5,0))
        if self.label_fundo:
            self.label_fundo.lower()

    def processar_login(self):
        matricula = self.entry_matricula.get().strip()
        
        # --- CORREÇÃO APLICADA AQUI ---
        # Padroniza o nome do município (ex: "são paulo" vira "São Paulo")
        # Isso garante que os dados no banco de dados fiquem consistentes.
        municipio = self.entry_municipio.get().strip().title()

        if not matricula or not municipio:
            messagebox.showwarning("Campos Obrigatórios", "Por favor, preencha a Matrícula/CPF e o Município.")
            return

        self.current_user_matricula = matricula
        self.current_user_municipio = municipio
        self.verificar_e_carregar_dados()
        self.mostrar_menu_principal()

    def mostrar_menu_principal(self):
        self.limpar_tela()
        
        # Frame principal com layout horizontal (dois lados)
        menu_frame = tk.Frame(self, bg=self.default_bg_color)
        menu_frame.pack(expand=True, fill="both")

        # Frame da esquerda (logo grande)
        frame_esquerda = tk.Frame(menu_frame, bg=self.default_bg_color)
        frame_esquerda.pack(side="left", fill="both", expand=True)

        # Frame da direita (botões)
        frame_direita = tk.Frame(menu_frame, bg=self.default_bg_color)
        frame_direita.pack(side="right", fill="both", expand=True)

        # --- LADO ESQUERDO: LOGO GRANDE ---
        try:
            imagem_logo = Image.open("imagens/logo_queimadas.jpg").resize((900, 900))
            self.foto_logo_menu = ImageTk.PhotoImage(imagem_logo)
            logo_label = tk.Label(frame_esquerda, image=self.foto_logo_menu, bg=self.default_bg_color)
            logo_label.place(relx=0.5, rely=0.5, anchor="center")
        except Exception as e:
            print(f"Erro ao carregar logo no menu principal: {e}")

        # --- LADO DIREITO: TÍTULO + BOTÕES ---
        container_direita = tk.Frame(frame_direita, bg=self.default_bg_color)
        container_direita.place(relx=0.5, rely=0.5, anchor="center")

        titulo_text = f"Bem-vindo, {self.current_user_municipio}!\nInterface informativa sobre"
        tk.Label(container_direita, text=titulo_text, font=("Helvetica", 22, "bold"), fg="white", bg=self.default_bg_color).pack(pady=(0, 20))

        tk.Label(container_direita, text="Queimadas", font=("Georgia", 34, "bold"), fg="white", bg=self.default_bg_color).pack(pady=(0, 30))
        tk.Label(container_direita, text="O que deseja acessar?", font=("Georgia", 18), fg="white", bg=self.default_bg_color).pack(pady=(0, 20))

        button_style = {"bg": "goldenrod", "fg": "black", "width": 32, "height": 3, "font": ("Helvetica", 13)}
        tk.Button(container_direita, text="Mapa Regional", command=self.abrir_mapa_por_regiao, **button_style).pack(pady=10)
        tk.Button(container_direita, text="Conscientização", command=self.abrir_conscientizacao, **button_style).pack(pady=10)
        tk.Button(container_direita, text="Quiz", command=self.abrir_quiz, **button_style).pack(pady=10)
        tk.Button(container_direita, text="Ranking por Cidade", command=self.abrir_tela_ranking, **button_style).pack(pady=10)

        # Botões de Logout e Sair
        action_buttons_frame = tk.Frame(container_direita, bg=self.default_bg_color)
        action_buttons_frame.pack(pady=30)
        tk.Button(action_buttons_frame, text="Logout", command=self.mostrar_tela_login, bg="#FF8C00", fg="white", width=15).pack(side=tk.LEFT, padx=10)
        tk.Button(action_buttons_frame, text="Sair", command=self.destroy, bg="darkred", fg="white", width=15).pack(side=tk.RIGHT, padx=10)

        if self.label_fundo:
            self.label_fundo.lower()


    def verificar_e_carregar_dados(self):
        if self.dados_baixados: return True
        if os.path.exists("queimadas.csv"):
            try:
                self.dados = pd.read_csv("queimadas.csv")
                self.dados_baixados = True
                return True
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao ler o arquivo CSV: {e}")
                return False
        else:
            user_choice = messagebox.askyesno("Dados Não Encontrados", "'queimadas.csv' não encontrado. Deseja tentar baixá-lo agora?")
            if user_choice:
                try:
                    path = baixar_dados()
                    if path and os.path.exists(path):
                        self.dados = pd.read_csv(path)
                        self.dados_baixados = True
                        return True
                except Exception as e:
                    messagebox.showerror("Erro de Download", f"Erro durante o download dos dados: {e}")
            return False

    def abrir_mapa_por_regiao(self):
        if not self.verificar_e_carregar_dados():
            messagebox.showwarning("Dados Ausentes", "Não foi possível carregar os dados para o mapa.")
            return
        gerar_mapa_por_regiao(self, self.dados)

    def abrir_conscientizacao(self):
        mostrar_tela_conscientizacao(self, self.limpar_tela)

    def abrir_quiz(self):
        tela_quiz.abrir_quiz(self, self.limpar_tela)

    def abrir_tela_ranking(self):
        tela_ranking.mostrar_ranking(self, self.limpar_tela)

if __name__ == "__main__":
    app = App()
    app.mainloop()