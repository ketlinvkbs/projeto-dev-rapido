import tkinter as tk
from PIL import Image, ImageTk
from perguntas import perguntas
import os
import ranking_manager

# Cores
COR_FUNDO = "#0B3D2E"
COR_TEXTO = "white"

# Variáveis globais
indice_pergunta = 0
pontuacao = 0
gif_frames = []
frame_container = None

def abrir_quiz(app, limpar_tela):
    global indice_pergunta, pontuacao, gif_frames
    indice_pergunta = 0
    pontuacao = 0
    limpar_tela()

    fila_images = [
        "frame1.jpeg", "frame2.jpeg", "frame3.jpeg",
        "frame4.jpeg", "frame5.jpeg", "frame6.jpeg",
    ]

    if all(os.path.exists(img) for img in fila_images):
        images = [Image.open(img).resize((2000, 1100), Image.Resampling.LANCZOS) for img in fila_images]
        gif_frames = [ImageTk.PhotoImage(img) for img in images]
    else:
        print("Erro: Uma ou mais imagens do GIF não foram encontradas.")
        gif_frames = []

    mostrar_pergunta(app, limpar_tela)

def gif(canvas, frame_container, count):
    if gif_frames:
        canvas.itemconfig(frame_container, image=gif_frames[count])
        canvas.after(350, gif, canvas, frame_container, (count + 1) % len(gif_frames))

def mostrar_pergunta(app, limpar_tela):
    global indice_pergunta, frame_container
    pergunta_atual = perguntas[indice_pergunta]

    app.configure(bg=COR_FUNDO)

    canvas = tk.Canvas(app, width=app.winfo_width(), height=app.winfo_height())
    canvas.place(x=0, y=0, relwidth=1, relheight=1)

    if not gif_frames:
        print("Erro: GIF não carregado corretamente.")
        return

    frame_container = canvas.create_image(app.winfo_width() // 2, app.winfo_height() // 2, image=gif_frames[0])
    gif(canvas, frame_container, 0)

    frame = tk.Frame(app, bg=COR_FUNDO)
    frame.place(relx=0.5, rely=0.5, anchor="center", width=800, height=400)

    pergunta_label = tk.Label(
        frame,
        text=pergunta_atual["pergunta"],
        font=("Arial", 18, "bold"),
        fg=COR_TEXTO,
        bg=COR_FUNDO,
        wraplength=700,
        justify="center"
    )
    pergunta_label.pack(pady=(20, 15))

    for texto, peso in pergunta_atual["alternativas"]:
        botao = tk.Button(
            frame,
            text=texto,
            command=lambda p=peso: responder(p, app, limpar_tela),
            bg="darkgreen",
            fg="white",
            font=("Arial", 16),
            wraplength=600,
            justify="left",
            anchor="w",
            width=60
        )
        botao.pack(pady=8, padx=20, fill="x", ipady=10)

def responder(peso, app, limpar_tela):
    global indice_pergunta, pontuacao
    pontuacao += peso
    indice_pergunta += 1

    limpar_tela()

    if indice_pergunta < len(perguntas):
        mostrar_pergunta(app, limpar_tela)
    else:
        mostrar_resultado(app, limpar_tela)

def mostrar_resultado(app, limpar_tela):
    app.configure(bg=COR_FUNDO)

    canvas = tk.Canvas(app, width=app.winfo_width(), height=app.winfo_height())
    canvas.place(x=0, y=0, relwidth=1, relheight=1)

    if not gif_frames:
        print("Erro: GIF não carregado corretamente.")
        return

    frame_container = canvas.create_image(app.winfo_width() // 2, app.winfo_height() // 2, image=gif_frames[0])
    gif(canvas, frame_container, 0)

    frame = tk.Frame(app, bg=COR_FUNDO)
    frame.place(relx=0.5, rely=0.5, anchor="center")

    if pontuacao >= 25:
        resultado = "Parabéns! Você sabe bastante sobre o tema."
    elif pontuacao >= 15:
        resultado = "Você tem algum conhecimento, mas pode aprender mais."
    else:
        resultado = "Você precisa se informar melhor sobre queimadas e natureza."

    tk.Label(
        frame, text="Resultado do Quiz",
        font=("Arial", 22, "bold"),
        fg=COR_TEXTO, bg=COR_FUNDO
    ).pack(pady=(40, 20))

    tk.Label(
        frame, text=f"Sua pontuação: {pontuacao}",
        font=("Arial", 16),
        fg=COR_TEXTO, bg=COR_FUNDO
    ).pack(pady=10)

    tk.Label(
        frame, text=resultado,
        font=("Arial", 14),
        fg=COR_TEXTO, bg=COR_FUNDO,
        wraplength=700,
        justify="center"
    ).pack(pady=10)

    tk.Button(
        frame,
        text="Voltar ao Menu",
        command=lambda: limpar_tela(True),
        bg="gray",
        fg="white",
        font=("Arial", 14), width=20
    ).pack(pady=40)
def responder(peso, app, limpar_tela):
    global indice_pergunta, pontuacao
    pontuacao += peso
    indice_pergunta += 1

    limpar_tela()

    if indice_pergunta < len(perguntas):
        mostrar_pergunta(app, limpar_tela)
    else:
        # A pontuação final é passada para a função de resultado
        mostrar_resultado(app, limpar_tela, pontuacao)

def mostrar_resultado(app, limpar_tela, pontuacao_final): # Modificado para receber a pontuação
    app.configure(bg=COR_FUNDO)

    # ... (código para criar o canvas e o frame de resultado) ...
    canvas = tk.Canvas(app, width=app.winfo_width(), height=app.winfo_height())
    canvas.place(x=0, y=0, relwidth=1, relheight=1)
    if gif_frames:
        frame_container = canvas.create_image(app.winfo_width() // 2, app.winfo_height() // 2, image=gif_frames[0])
        gif(canvas, frame_container, 0)
    
    frame = tk.Frame(app, bg=COR_FUNDO)
    frame.place(relx=0.5, rely=0.5, anchor="center")

    if pontuacao_final >= 25:
        resultado = "Parabéns! Você sabe bastante sobre o tema."
    elif pontuacao_final >= 15:
        resultado = "Você tem algum conhecimento, mas pode aprender mais."
    else:
        resultado = "Você precisa se informar melhor sobre queimadas e natureza."

    # <-- 2. SALVAR A PONTUAÇÃO NO BANCO DE DADOS
    try:
        ranking_manager.add_score(
            app.current_user_municipio, 
            app.current_user_matricula, 
            pontuacao_final
        )
    except Exception as e:
        print(f"Não foi possível salvar a pontuação no ranking: {e}")
    # Fim da adição

    tk.Label(frame, text="Resultado do Quiz", font=("Arial", 22, "bold"), fg=COR_TEXTO, bg=COR_FUNDO).pack(pady=(40, 20))
    tk.Label(frame, text=f"Sua pontuação: {pontuacao_final}", font=("Arial", 16), fg=COR_TEXTO, bg=COR_FUNDO).pack(pady=10)
    tk.Label(frame, text=resultado, font=("Arial", 14), fg=COR_TEXTO, bg=COR_FUNDO, wraplength=700, justify="center").pack(pady=10)
    tk.Button(frame, text="Voltar ao Menu", command=lambda: limpar_tela(True), bg="gray", fg="white", font=("Arial", 14), width=20).pack(pady=40)

# É necessário ajustar a função 'responder' para passar a pontuação
def responder(peso, app, limpar_tela):
    global indice_pergunta, pontuacao
    pontuacao += peso
    indice_pergunta += 1
    
    limpar_tela()

    if indice_pergunta < len(perguntas):
        mostrar_pergunta(app, limpar_tela)
    else:
        # Passa a pontuação final para a função mostrar_resultado
        mostrar_resultado(app, limpar_tela, pontuacao)
