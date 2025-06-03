import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import pandas as pd
import os

# Importações dos seus módulos
from download_dados import baixar_dados # Assumindo que existe
from tela_conscientizacao import mostrar_tela_conscientizacao # Assumindo que existe
import tela_quiz # Será modificado
from mapa_brasil_estatico import gerar_mapa_brasil_estatico # Assumindo que existe

# Importar o gerenciador de ranking
import ranking_manager # Adicionado

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        ranking_manager.init_db()

        self.title("Interface Informativa sobre Queimadas")
        self.attributes("-fullscreen", True)
        self.default_bg_color = "#0B3D2E" # Cor de fundo padrão
        self.configure(bg=self.default_bg_color)

        self.dados = None
        self.dados_baixados = False
        self.current_user_matricula = None
        self.current_user_municipio = None

        # Configuração da imagem de fundo
        self.imagem_fundo_pil = None
        self.foto_fundo_tk = None # Renomeado para evitar conflito com foto_logo
        self.label_fundo = None
        self.setup_background_image()

        # Frame central para todo o conteúdo dinâmico
        # Este frame não será colorido diretamente, ele conterá os frames de cada tela
        self.content_container = tk.Frame(self, bg=self.default_bg_color)
        self.content_container.pack(expand=True, fill="both")

        self.mostrar_tela_login()
        # self.verificar_e_carregar_dados() # Será chamado após o login bem-sucedido

    def setup_background_image(self):
        imagem_path = "fundoqueimadas.jpg"
        if os.path.exists(imagem_path):
            try:
                screen_width = self.winfo_screenwidth()
                screen_height = self.winfo_screenheight()
                self.imagem_fundo_pil = Image.open(imagem_path).resize((screen_width, screen_height))
                self.foto_fundo_tk = ImageTk.PhotoImage(self.imagem_fundo_pil)
                
                if self.label_fundo:
                    self.label_fundo.configure(image=self.foto_fundo_tk)
                else:
                    self.label_fundo = tk.Label(self, image=self.foto_fundo_tk)
                    self.label_fundo.place(x=0, y=0, relwidth=1, relheight=1)
                
                self.label_fundo.image = self.foto_fundo_tk # Manter referência
                self.label_fundo.lower() # Coloca o label do fundo atrás de outros widgets
            except Exception as e:
                print(f"Erro ao carregar imagem de fundo: {e}")
                messagebox.showerror("Erro de Imagem", f"Não foi possível carregar a imagem de fundo: {imagem_path}")
        else:
            print(f"Imagem de fundo não encontrada: {imagem_path}")
            # Opcional: definir uma cor de fundo sólida se a imagem falhar
            # self.configure(bg=self.default_bg_color)


    def limpar_content_container(self):
        """Limpa todos os widgets do container de conteúdo."""
        for widget in self.content_container.winfo_children():
            widget.destroy()
        # Garante que o container de conteúdo mantenha a cor de fundo da aplicação
        self.content_container.configure(bg=self.default_bg_color)


    def mostrar_tela_login(self):
        self.limpar_content_container()

        # Frame para o formulário de login, centralizado
        login_frame = tk.Frame(self.content_container, bg="#FFFFFF", relief=tk.RIDGE, bd=5, padx=40, pady=40)
        login_frame.place(relx=0.5, rely=0.5, anchor="center") # Centraliza o frame de login

        try:
            # Reutilizando a imagem de logo do seu projeto
            imagem_logo_pil = Image.open("logoqueimadas.jpg").resize((120, 120)) # Ajuste o tamanho
            self.foto_logo_login = ImageTk.PhotoImage(imagem_logo_pil)
            logo_label = tk.Label(login_frame, image=self.foto_logo_login, bg="#FFFFFF")
            logo_label.image = self.foto_logo_login 
            logo_label.pack(pady=(0, 15))
        except FileNotFoundError:
            tk.Label(login_frame, text="Logo Queimadas", font=("Georgia", 18, "bold"), bg="#FFFFFF", fg=self.default_bg_color).pack(pady=(0,15))
        except Exception as e:
            print(f"Erro ao carregar logo na tela de login: {e}")


        tk.Label(login_frame, text="Login no Sistema", font=("Georgia", 22, "bold"), bg="#FFFFFF", fg=self.default_bg_color).pack(pady=10)

        tk.Label(login_frame, text="Matrícula ou CPF:", font=("Helvetica", 12), bg="#FFFFFF", fg="#333333").pack(pady=(10,0), anchor="w")
        self.entry_matricula = tk.Entry(login_frame, font=("Helvetica", 12), width=35, relief=tk.GROOVE, bd=2)
        self.entry_matricula.pack(pady=(0,10), ipady=4)

        tk.Label(login_frame, text="Município:", font=("Helvetica", 12), bg="#FFFFFF", fg="#333333").pack(pady=(10,0), anchor="w")
        self.entry_municipio = tk.Entry(login_frame, font=("Helvetica", 12), width=35, relief=tk.GROOVE, bd=2)
        self.entry_municipio.pack(pady=(0,20), ipady=4)

        btn_login = tk.Button(login_frame, text="Entrar", command=self.processar_login,
                              bg="goldenrod", fg="black", font=("Helvetica", 12, "bold"), width=20, height=1, relief=tk.RAISED, bd=3)
        btn_login.pack(pady=15)
        
        btn_sair_app = tk.Button(login_frame, text="Sair do Aplicativo", command=self.destroy,
                                 bg="darkred", fg="white", font=("Helvetica", 10), width=20, relief=tk.RAISED, bd=2)
        btn_sair_app.pack(pady=(5,0))


    def processar_login(self):
        matricula = self.entry_matricula.get().strip()
        municipio = self.entry_municipio.get().strip()

        if not matricula or not municipio:
            messagebox.showwarning("Campos Obrigatórios", "Por favor, preencha a Matrícula/CPF e o Município.", parent=self.content_container)
            return

        self.current_user_matricula = matricula
        self.current_user_municipio = municipio
        
        # messagebox.showinfo("Login Bem-Sucedido", f"Bem-vindo, {municipio}!", parent=self.content_container)
        
        self.verificar_e_carregar_dados() # Carrega os dados principais do app
        self.mostrar_menu_principal() # Procede para o menu principal


    def mostrar_menu_principal(self): # Antiga criar_interface_inicial
        self.limpar_content_container()
        
        # Frame para os botões do menu, para melhor organização
        menu_buttons_frame = tk.Frame(self.content_container, bg=self.default_bg_color)
        menu_buttons_frame.place(relx=0.5, rely=0.5, anchor="center")

        titulo_text = f"Bem-vindo, {self.current_user_municipio}!\nInterface informativa sobre" if self.current_user_municipio else "Bem-vindo à interface\ninformativa sobre"
        titulo = tk.Label(menu_buttons_frame, text=titulo_text,
                          font=("Helvetica", 20), fg="white", bg=self.default_bg_color)
        titulo.pack(pady=20)

        try:
            imagem_logo = Image.open("logoqueimadas.jpg").resize((150, 150)) # Tamanho para o menu
            self.foto_logo_menu = ImageTk.PhotoImage(imagem_logo) # Manter referência diferente
            logo = tk.Label(menu_buttons_frame, image=self.foto_logo_menu, bg=self.default_bg_color)
            logo.image = self.foto_logo_menu
            logo.pack(pady=10)
        except Exception as e:
            print(f"Erro ao carregar logo no menu principal: {e}")


        nome = tk.Label(menu_buttons_frame, text="Queimadas", font=("Georgia", 32, "bold"), fg="white", bg=self.default_bg_color)
        nome.pack(pady=5)

        subtitulo = tk.Label(menu_buttons_frame, text="O que deseja acessar?", font=("Georgia", 18), fg="white", bg=self.default_bg_color)
        subtitulo.pack(pady=15)

        button_style = {"bg": "goldenrod", "fg": "black", "width": 30, "height": 2, "font":("Helvetica", 11), "relief":tk.RAISED, "bd":3}

        tk.Button(menu_buttons_frame, text="Mapa de Calor (Correlação)", command=self.abrir_mapa_calor, **button_style).pack(pady=7)
        tk.Button(menu_buttons_frame, text="Mapa Estático com Pontos", command=self.abrir_mapa_estatico, **button_style).pack(pady=7)
        tk.Button(menu_buttons_frame, text="Conscientização", command=self.abrir_conscientizacao, **button_style).pack(pady=7)
        tk.Button(menu_buttons_frame, text="Quiz Interativo", command=self.abrir_quiz, **button_style).pack(pady=7)
        tk.Button(menu_buttons_frame, text="Ver Ranking por Município", command=self.mostrar_tela_ranking, **button_style).pack(pady=7) # Botão do Ranking

        # Botão para Logout (voltar à tela de login) e Sair do App
        action_buttons_frame = tk.Frame(menu_buttons_frame, bg=self.default_bg_color)
        action_buttons_frame.pack(pady=20)

        tk.Button(action_buttons_frame, text="Logout (Trocar Usuário)", command=self.fazer_logout,
                  bg="#FF8C00", fg="white", width=20, font=("Helvetica", 10)).pack(side=tk.LEFT, padx=10)
        tk.Button(action_buttons_frame, text="Sair do Aplicativo", command=self.destroy,
                  bg="darkred", fg="white", width=15, font=("Helvetica", 10)).pack(side=tk.LEFT, padx=10)

    def fazer_logout(self):
        self.current_user_matricula = None
        self.current_user_municipio = None
        # messagebox.showinfo("Logout", "Você foi desconectado.", parent=self.content_container)
        self.mostrar_tela_login()

    def verificar_e_carregar_dados(self):
        # Seu código original para carregar 'queimadas.csv'
        # Retorna True se os dados foram carregados, False caso contrário
        if os.path.exists("queimadas.csv"):
            try:
                self.dados = pd.read_csv("queimadas.csv")
                self.dados_baixados = True
                print("Dados 'queimadas.csv' carregados com sucesso.")
                return True
            except Exception as e:
                messagebox.showerror("Erro de Dados", f"Erro ao ler o arquivo CSV 'queimadas.csv': {e}", parent=self.content_container)
                self.dados_baixados = False
                return False
        else:
            # Tentar baixar se não existir (se a função baixar_dados() fizer isso)
            user_choice = messagebox.askyesno("Dados Não Encontrados", 
                                              "'queimadas.csv' não encontrado. Deseja tentar baixá-lo agora?",
                                              parent=self.content_container)
            if user_choice:
                try:
                    path = baixar_dados() # Supondo que esta função baixa e retorna o caminho
                    if path and os.path.exists(path):
                        self.dados = pd.read_csv(path)
                        self.dados_baixados = True
                        print("Dados baixados e carregados com sucesso.")
                        return True
                    else:
                        messagebox.showerror("Erro de Download", "Não foi possível baixar ou encontrar o arquivo de dados.", parent=self.content_container)
                        return False
                except Exception as e:
                    messagebox.showerror("Erro de Download", f"Erro durante o download dos dados: {e}", parent=self.content_container)
                    return False
            else: # Usuário não quer baixar
                return False


    # --- Métodos para abrir as diferentes telas ---
    # Eles devem limpar o content_container e construir sua UI dentro dele.
    # Precisam de um botão "Voltar ao Menu" que chame self.mostrar_menu_principal()

    def _criar_frame_com_botao_voltar(self, titulo_tela=""):
        """Helper para criar um frame base para telas com título e botão voltar."""
        self.limpar_content_container()
        
        # Frame que ocupará o content_container
        screen_frame = tk.Frame(self.content_container, bg=self.default_bg_color)
        screen_frame.pack(expand=True, fill="both", padx=20, pady=20)

        # Título da tela (opcional)
        if titulo_tela:
            tk.Label(screen_frame, text=titulo_tela, font=("Georgia", 20, "bold"), fg="white", bg=self.default_bg_color).pack(pady=(0, 20))

        # Botão Voltar no topo
        btn_voltar = tk.Button(screen_frame, text="⬅ Voltar ao Menu Principal", command=self.mostrar_menu_principal,
                               bg="goldenrod", fg="black", font=("Helvetica", 10, "bold"), relief=tk.RAISED, bd=2)
        btn_voltar.pack(pady=(0, 15), anchor="nw") # Canto superior esquerdo

        # Frame de conteúdo específico da tela (onde o mapa, quiz, etc. serão colocados)
        inner_content_frame = tk.Frame(screen_frame, bg=self.default_bg_color)
        inner_content_frame.pack(expand=True, fill="both")
        
        return inner_content_frame # Retorna o frame onde o conteúdo específico será adicionado


    def abrir_mapa_calor(self):
        try:
            import seaborn as sns
            import matplotlib.pyplot as plt
            from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

            if not self.dados_baixados:
                if not self.verificar_e_carregar_dados(): # Tenta carregar/baixar
                    messagebox.showwarning("Dados Ausentes", "Não foi possível carregar os dados para o mapa de calor.", parent=self.content_container)
                    self.mostrar_menu_principal() # Volta ao menu se não houver dados
                    return
            
            inner_frame = self._criar_frame_com_botao_voltar("Mapa de Calor - Correlações")
            
            numeric_data = self.dados.select_dtypes(include=[float, int])
            if numeric_data.empty or len(numeric_data.columns) < 2:
                tk.Label(inner_frame, text="Não há dados numéricos suficientes para gerar um mapa de correlação.",
                         font=("Helvetica", 14), fg="white", bg=self.default_bg_color, wraplength=500).pack(pady=20)
                return

            fig, ax = plt.subplots(figsize=(12, 9), facecolor=self.default_bg_color) # Ajuste o tamanho
            ax.set_facecolor(self.default_bg_color)

            # Personalização do heatmap
            heatmap = sns.heatmap(numeric_data.corr(), annot=True, cmap="YlOrRd", fmt=".2f",
                                  cbar=True, linewidths=0.5, linecolor='gray', 
                                  annot_kws={"color": "black", "size": 8}, # Ajuste tamanho da anotação
                                  ax=ax) 
                                  # cbar_kws={'orientation': 'vertical', 'shrink': 0.75}) # Para barra de cores

            # ax.set_title("Correlação entre Variáveis Numéricas", color="white", fontsize=16) # Título já está no _criar_frame...
            plt.xticks(rotation=45, ha="right", color="white", fontsize=9) # Rotaciona e ajusta xticks
            plt.yticks(rotation=0, color="white", fontsize=9)      # Ajusta yticks
            plt.tight_layout() # Ajusta o layout para não cortar labels

            canvas = FigureCanvasTkAgg(fig, master=inner_frame)
            canvas_widget = canvas.get_tk_widget()
            canvas_widget.pack(pady=10, expand=True, fill=tk.BOTH)
            canvas.draw()

        except ImportError:
            messagebox.showerror("Erro de Importação", "As bibliotecas Seaborn ou Matplotlib não estão instaladas.", parent=self.content_container)
            self.mostrar_menu_principal()
        except Exception as e:
            messagebox.showerror("Erro Inesperado", f"Erro ao gerar mapa de calor: {e}", parent=self.content_container)
            self.mostrar_menu_principal()


    def abrir_mapa_estatico(self):
        if not self.dados_baixados:
            if not self.verificar_e_carregar_dados():
                messagebox.showwarning("Dados Ausentes", "Não foi possível carregar os dados para o mapa estático.", parent=self.content_container)
                self.mostrar_menu_principal()
                return
        
        inner_frame = self._criar_frame_com_botao_voltar("Mapa Estático de Queimadas")
        
        try:
            # A função gerar_mapa_brasil_estatico deve ser adaptada para renderizar em 'inner_frame'
            gerar_mapa_brasil_estatico(self.dados, inner_frame) 
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gerar o mapa estático: {e}", parent=self.content_container)
            tk.Label(inner_frame, text=f"Erro ao gerar mapa: {e}", fg="red", bg=self.default_bg_color).pack()


    def abrir_conscientizacao(self):
        inner_frame = self._criar_frame_com_botao_voltar("Conscientização sobre Queimadas")
        # A função mostrar_tela_conscientizacao deve ser adaptada
        # para aceitar 'inner_frame' como master e construir sua UI dentro dele.
        # Ela não precisará mais do callback 'limpar_tela' se o botão voltar já estiver lá.
        try:
            mostrar_tela_conscientizacao(inner_frame) # Modifique esta função no seu arquivo
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao abrir tela de conscientização: {e}", parent=self.content_container)
            tk.Label(inner_frame, text=f"Erro: {e}", fg="red", bg=self.default_bg_color).pack()


    def abrir_quiz(self): # Este é o método da classe App
        if not self.current_user_municipio:
            messagebox.showerror("Acesso Negado", "Faça o login antes de iniciar o quiz.", parent=self.content_container)
            self.mostrar_tela_login()
            return

        # Usa a função helper para criar o frame base com botão voltar (do main.py)
        # O título aqui é para o frame GERAL que contém o quiz.
        inner_quiz_frame = self._criar_frame_com_botao_voltar("Quiz Interativo sobre Queimadas")
        
        try:
            # Chama a função de entrada do tela_quiz.py, passando os parâmetros corretos
            tela_quiz.abrir_quiz_interface( # Use o nome da função importada
                master_frame=inner_quiz_frame,  # Onde o quiz será construído
                app_instance=self,        # A instância da App para callbacks e dados
                callback_fim_quiz=self.mostrar_menu_principal # O que fazer ao final
            )
        except Exception as e:
            messagebox.showerror("Erro no Quiz", f"Não foi possível iniciar o quiz: {e}", parent=self.content_container)
            # Opcional: Adicionar um label de erro no inner_quiz_frame
            tk.Label(inner_quiz_frame, text=f"Erro ao carregar quiz: {e}", fg="red", bg=self.default_bg_color).pack()

    def atualizar_pontuacao_ranking(self, pontuacao_obtida_no_quiz):
        """Chamado pelo módulo do quiz para registrar a pontuação."""
        if self.current_user_municipio:
            ranking_manager.update_score(self.current_user_municipio, pontuacao_obtida_no_quiz)
        # (Opcional) Feedback para o usuário pode ser melhorado
        # messagebox.showinfo("Pontuação Registrada", f"Sua pontuação ({pontuacao_obtida_no_quiz}) foi registrada para {self.current_user_municipio}!", parent=self.content_container)
        else:
            messagebox.showwarning("Ranking", "Usuário não identificado. Pontuação não registrada no ranking.", parent=self.content_container)


    # Dentro da classe App
    def mostrar_tela_ranking(self):
        inner_frame = self._criar_frame_com_botao_voltar("🏆 Ranking de Acertos por Município 🏆")

    # rankings_data já será uma lista de tuplas (municipio, score) ordenada
        rankings_data = ranking_manager.get_sorted_rankings() 

        if not rankings_data:
            tk.Label(inner_frame, text="Ainda não há pontuações registradas no ranking.",
                    font=("Helvetica", 16), fg="white", bg=self.default_bg_color).pack(pady=30)
        else:
            ranking_table_container = tk.Frame(inner_frame, bg=self.default_bg_color)
            ranking_table_container.pack(expand=True, fill=tk.BOTH, pady=10)

            header_frame = tk.Frame(ranking_table_container, bg="#333333")
            header_frame.pack(fill="x", pady=(0,5))
            tk.Label(header_frame, text="Pos.", font=("Helvetica", 12, "bold"), fg="white", bg="#333333", width=5, relief=tk.SOLID, borderwidth=1).pack(side=tk.LEFT, padx=(2,1), ipady=5)
            tk.Label(header_frame, text="Município", font=("Helvetica", 12, "bold"), fg="white", bg="#333333", width=35, relief=tk.SOLID, borderwidth=1, anchor="w").pack(side=tk.LEFT, padx=1, ipady=5)
            tk.Label(header_frame, text="Total de Acertos", font=("Helvetica", 12, "bold"), fg="white", bg="#333333", width=15, relief=tk.SOLID, borderwidth=1).pack(side=tk.LEFT, padx=(1,2), ipady=5)

            canvas = tk.Canvas(ranking_table_container, bg=self.default_bg_color, highlightthickness=0)
            scrollbar = tk.Scrollbar(ranking_table_container, orient="vertical", command=canvas.yview)
            scrollable_frame = tk.Frame(canvas, bg=self.default_bg_color)
            scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")

            for i, (municipio, score) in enumerate(rankings_data):
                entry_bg = self.default_bg_color if i % 2 == 0 else "#1E503D"
                entry_frame = tk.Frame(scrollable_frame, bg=entry_bg)
                entry_frame.pack(fill="x")
                tk.Label(entry_frame, text=f"{i+1}", font=("Helvetica", 11), fg="white", bg=entry_bg, width=5).pack(side=tk.LEFT, padx=(2,1), pady=1, ipady=3) # Removido relief e border para linhas
                tk.Label(entry_frame, text=municipio, font=("Helvetica", 11), fg="white", bg=entry_bg, width=35, anchor="w").pack(side=tk.LEFT, padx=1, pady=1, ipady=3)
                tk.Label(entry_frame, text=str(score), font=("Helvetica", 11), fg="white", bg=entry_bg, width=15).pack(side=tk.LEFT, padx=(1,2), pady=1, ipady=3)


if __name__ == "__main__":
    app = App()
    app.mainloop()