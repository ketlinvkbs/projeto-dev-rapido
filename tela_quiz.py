import tkinter as tk
from PIL import Image, ImageTk
from perguntas import perguntas # Certifique-se que este arquivo existe e 'perguntas' está formatado corretamente
import os
import random # Para embaralhar opções, se desejar

# Cores (podem ser movidas para dentro da classe ou mantidas se usadas apenas aqui)
COR_FUNDO_QUIZ = "#0B3D2E" # Cor de fundo específica para o quiz, se diferente do app principal
COR_TEXTO_QUIZ = "white"

class QuizApp:
    def __init__(self, master_frame, app_instance, callback_fim_quiz):
        self.master = master_frame  # O frame fornecido pelo main.py onde o quiz será construído
        self.app_instance = app_instance  # A instância da classe App de main.py
        self.callback_fim_quiz = callback_fim_quiz  # Função a ser chamada ao final do quiz

        self.indice_pergunta = 0
        self.pontuacao = 0
        self.gif_frames_tk = []  # Armazenará os PhotoImage para o "GIF"
        self.gif_canvas_item = None  # Referência ao item de imagem no canvas
        self.gif_animation_id = None # Para controlar o after da animação

        # Configura o frame mestre do quiz
        self.master.configure(bg=COR_FUNDO_QUIZ) # Define o fundo do frame do quiz

        self._carregar_frames_gif()
        self._mostrar_pergunta()

    def _carregar_frames_gif(self):
        """Carrega as imagens da sequência (simulando GIF)."""
        # Usar os mesmos nomes de arquivo que você forneceu
        fila_images_nomes = [
            "frame1.jpeg", "frame2.jpeg", "frame3.jpeg",
            "frame4.jpeg", "frame5.jpeg", "frame6.jpeg",
        ]
        
        # Tenta encontrar as imagens em um subdiretório 'imagens_quiz' ou no diretório atual
        # Isso torna um pouco mais flexível
        possiveis_paths = ["imagens_quiz/", ""] # Adicione outros caminhos se necessário
        
        imagens_encontradas = []
        for nome_img in fila_images_nomes:
            for base_path in possiveis_paths:
                path_completo = os.path.join(base_path, nome_img)
                if os.path.exists(path_completo):
                    imagens_encontradas.append(path_completo)
                    break # Vai para a próxima imagem da fila
            else: # Se o loop interno não deu break (imagem não encontrada em nenhum path)
                print(f"Aviso: Imagem '{nome_img}' não encontrada.")

        if not imagens_encontradas or len(imagens_encontradas) < len(fila_images_nomes):
            print("Erro: Algumas ou todas as imagens da sequência do quiz não foram encontradas.")
            # Opcional: Carregar uma imagem placeholder ou desabilitar o fundo animado
            self.gif_frames_tk = []
            return

        try:
            # Ajuste o tamanho do resize conforme necessário para o seu layout
            # Usar winfo_width/height do master_frame pode ser mais dinâmico se o frame não for tela cheia
            # Mas cuidado, o frame pode não ter tamanho definido ainda na inicialização.
            # Por enquanto, mantemos o resize grande que você tinha.
            # Se o master_frame for menor, a imagem será cortada pelo canvas.
            largura_gif = self.app_instance.winfo_screenwidth() # Largura da tela toda
            altura_gif = self.app_instance.winfo_screenheight() # Altura da tela toda

            images_pil = [Image.open(path).resize((largura_gif, altura_gif), Image.Resampling.LANCZOS) for path in imagens_encontradas]
            self.gif_frames_tk = [ImageTk.PhotoImage(img) for img in images_pil]
        except Exception as e:
            print(f"Erro ao processar imagens da sequência do quiz: {e}")
            self.gif_frames_tk = []

    def _animar_gif(self, canvas, count):
        """Atualiza a imagem no canvas para animar a sequência."""
        if self.gif_frames_tk and self.gif_canvas_item:
            try:
                canvas.itemconfig(self.gif_canvas_item, image=self.gif_frames_tk[count])
                next_count = (count + 1) % len(self.gif_frames_tk)
                # Armazena o ID do after para poder cancelar depois
                self.gif_animation_id = canvas.after(350, self._animar_gif, canvas, next_count)
            except tk.TclError as e:
                # Comum se o widget for destruído enquanto o after está pendente
                print(f"Erro no Tcl durante a animação do GIF (widget pode ter sido destruído): {e}")
                self.gif_animation_id = None # Reseta o ID

    def _limpar_widgets_internos(self):
        if self.gif_animation_id:
        # Verifica se o widget do canvas ainda existe antes de chamar after_cancel
            if hasattr(self, 'gif_canvas_widget') and self.gif_canvas_widget and self.gif_canvas_widget.winfo_exists():
                try:
                    self.gif_canvas_widget.after_cancel(self.gif_animation_id)
                except tk.TclError:
                    pass # Erro comum se o widget já foi destruído
            self.gif_animation_id = None

        # Reseta a referência ao canvas do GIF, pois ele será destruído no loop abaixo
        self.gif_canvas_widget = None 
        self.gif_canvas_item = None # Também reseta o item da imagem

        for widget in self.master.winfo_children():
            widget.destroy()
        self.master.configure(bg=COR_FUNDO_QUIZ)


    def _mostrar_pergunta(self):
        """Exibe a pergunta atual, opções e o fundo animado."""
        self._limpar_widgets_internos() # Limpa conteúdo anterior do quiz

        if not self.gif_frames_tk:
            # Fallback se o GIF não carregou: apenas um fundo sólido
            print("Aviso: Sequência de imagens (GIF) não carregada. Usando fundo sólido.")
            # self.master.configure(bg=COR_FUNDO_QUIZ) # Já feito no _limpar_widgets_internos
        else:
            # Canvas para o fundo animado, cobrindo todo o self.master
            gif_canvas = tk.Canvas(self.master, width=self.master.winfo_width(), height=self.master.winfo_height(), highlightthickness=0)
            gif_canvas.place(x=0, y=0, relwidth=1, relheight=1)
            # Posiciona a imagem no centro do canvas.
            # Se a imagem for do tamanho da tela e o canvas também, x=0, y=0, anchor="nw" também funciona.
            self.gif_canvas_item = gif_canvas.create_image(
                self.master.winfo_width() // 2, 
                self.master.winfo_height() // 2, 
                image=self.gif_frames_tk[0]
            )
            self._animar_gif(gif_canvas, 0)

        # Frame para o conteúdo da pergunta (sobre o canvas do GIF)
        # Este frame terá um fundo parcialmente transparente ou sólido para legibilidade
        conteudo_pergunta_frame = tk.Frame(self.master, bg=COR_FUNDO_QUIZ, relief=tk.SOLID, bd=2) # Cor de fundo para o box da pergunta
        # Você pode usar a propriedade alpha para transparência se estiver usando um Toplevel com overrideredirect
        # e wm_attributes, mas para frames normais, uma cor sólida que combine é mais fácil.
        # Exemplo: conteúdo_pergunta_frame.configure(bg="#000000") e depois usar alpha para o toplevel
        # Alternativa: Usar uma imagem PNG com transparência como fundo do frame.

        conteudo_pergunta_frame.place(relx=0.5, rely=0.5, anchor="center", width=750, height=400) # Ajuste tamanho

        pergunta_atual_data = perguntas[self.indice_pergunta]

        lbl_pergunta = tk.Label(
            conteudo_pergunta_frame,
            text=pergunta_atual_data["pergunta"],
            font=("Arial", 18, "bold"),
            fg=COR_TEXTO_QUIZ,
            bg=COR_FUNDO_QUIZ, # Mesma cor do frame de conteúdo
            wraplength=700,
            justify="center"
        )
        lbl_pergunta.pack(pady=(30, 20), padx=10)

        opcoes_frame = tk.Frame(conteudo_pergunta_frame, bg=COR_FUNDO_QUIZ)
        opcoes_frame.pack(pady=10, padx=10)

        alternativas = pergunta_atual_data["alternativas"]
        # random.shuffle(alternativas) # Se quiser embaralhar as alternativas

        for texto_alt, peso_alt in alternativas:
            btn_alt = tk.Button(
                opcoes_frame,
                text=texto_alt,
                command=lambda p=peso_alt: self._responder(p),
                bg="darkgreen", # Estilo do botão
                fg="white",
                font=("Arial", 13),
                width=60, # Ajuste a largura
                wraplength=580, # Para quebra de linha no botão
                relief=tk.RAISED, bd=3,
                pady=5
            )
            btn_alt.pack(pady=7)

    def _responder(self, peso_resposta):
        """Processa a resposta, atualiza a pontuação e avança."""
        print(f"Método _responder chamado com peso: {peso_resposta}") # Adicione este print

        # Desabilita os botões de opção para evitar cliques repetidos
        if hasattr(self, 'opcoes_frame_atual') and self.opcoes_frame_atual:
            for widget in self.opcoes_frame_atual.winfo_children():
                if isinstance(widget, tk.Button):
                    widget.configure(state=tk.DISABLED)

        self.pontuacao += peso_resposta
        self.indice_pergunta += 1

        # Pequeno delay antes de carregar a próxima pergunta/resultado
        # Às vezes, isso ajuda o loop de eventos a processar o clique do botão completamente.
        self.master.after(50, self._avancar_quiz) # 50ms de delay

    def _avancar_quiz(self):
        """Chamado após um pequeno delay em _responder."""
        if self.indice_pergunta < len(perguntas):
            self._mostrar_pergunta()
        else:
            self._mostrar_resultado_final()

    def _mostrar_resultado_final(self):
        """Exibe a pontuação final e a mensagem de resultado."""
        self._limpar_widgets_internos()

        # Mantém o fundo animado se carregado
        if self.gif_frames_tk:
            gif_canvas_resultado = tk.Canvas(self.master, width=self.master.winfo_width(), height=self.master.winfo_height(), highlightthickness=0)
            gif_canvas_resultado.place(x=0, y=0, relwidth=1, relheight=1)
            self.gif_canvas_item = gif_canvas_resultado.create_image(
                self.master.winfo_width() // 2, 
                self.master.winfo_height() // 2, 
                image=self.gif_frames_tk[0]
            )
            self._animar_gif(gif_canvas_resultado, 0)

        resultado_frame = tk.Frame(self.master, bg=COR_FUNDO_QUIZ, relief=tk.SOLID, bd=2)
        resultado_frame.place(relx=0.5, rely=0.5, anchor="center", width=700, height=350) # Ajuste o tamanho

        # Determina a mensagem de resultado baseada na pontuação
        if self.pontuacao >= 25: # Ajuste os limiares conforme sua lógica de pontuação
            texto_resultado = "Parabéns! Você sabe bastante sobre o tema."
        elif self.pontuacao >= 15:
            texto_resultado = "Você tem algum conhecimento, mas pode aprender mais."
        else:
            texto_resultado = "Você precisa se informar melhor sobre queimadas e natureza."

        tk.Label(resultado_frame, text="Resultado do Quiz", font=("Arial", 22, "bold"),
                  fg=COR_TEXTO_QUIZ, bg=COR_FUNDO_QUIZ).pack(pady=(30, 15))
        tk.Label(resultado_frame, text=f"Sua pontuação: {self.pontuacao}", font=("Arial", 16),
                  fg=COR_TEXTO_QUIZ, bg=COR_FUNDO_QUIZ).pack(pady=10)
        tk.Label(resultado_frame, text=texto_resultado, font=("Arial", 14),
                  fg=COR_TEXTO_QUIZ, bg=COR_FUNDO_QUIZ, wraplength=650, justify="center").pack(pady=15)

        # Envia a pontuação para o main.py para atualizar o ranking global
        if self.app_instance and hasattr(self.app_instance, 'atualizar_pontuacao_ranking'):
            self.app_instance.atualizar_pontuacao_ranking(self.pontuacao)

        btn_voltar_menu = tk.Button(
            resultado_frame,
            text="Voltar ao Menu Principal",
            command=self.callback_fim_quiz, # Usa o callback fornecido pelo main.py
            bg="gray",
            fg="white",
            font=("Arial", 14, "bold"), width=25, height=2,
            relief=tk.RAISED, bd=3
        )
        btn_voltar_menu.pack(pady=(20,30))


# Função de entrada que será chamada pelo main.py
def abrir_quiz_interface(master_frame, app_instance, callback_fim_quiz):
    """
    Ponto de entrada para criar e iniciar a interface do quiz.
    Esta função substitui a sua antiga 'abrir_quiz'.
    """
    # Limpa o master_frame ANTES de criar a instância do QuizApp,
    # caso haja algum conteúdo residual de uma chamada anterior ao quiz.
    for widget in master_frame.winfo_children():
        widget.destroy()
    
    QuizApp(master_frame, app_instance, callback_fim_quiz)