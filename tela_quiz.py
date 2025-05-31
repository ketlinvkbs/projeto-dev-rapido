import tkinter as tk
from perguntas import perguntas

COR_FUNDO = "#0B3D2E"
COR_TEXTO = "white"

indice_pergunta = 0
pontuacao = 0

def abrir_quiz(app, limpar_tela):
    global indice_pergunta, pontuacao
    indice_pergunta = 0
    pontuacao = 0
    limpar_tela()
    mostrar_pergunta(app, limpar_tela)

def mostrar_pergunta(app, limpar_tela):
    pergunta_atual = perguntas[indice_pergunta]

    app.configure(bg=COR_FUNDO)

    frame = tk.Frame(app, bg=COR_FUNDO)
    frame.pack(expand=True, fill="both")

    pergunta_label = tk.Label(
        frame,
        text=pergunta_atual["pergunta"],
        font=("Arial", 18, "bold"),
        fg=COR_TEXTO,
        bg=COR_FUNDO,
        wraplength=700,
        justify="center"
    )
    pergunta_label.pack(pady=(50, 30))

    for texto, peso in pergunta_atual["alternativas"]:
        botao = tk.Button(
            frame,
            text=texto,
            command=lambda p=peso: responder(p, app, limpar_tela),
            bg="darkgreen",
            fg="white",
            font=("Arial", 14),
            width=50,
            wraplength=600,
            justify="center"
        )
        botao.pack(pady=10)

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

    frame = tk.Frame(app, bg=COR_FUNDO)
    frame.pack(expand=True, fill="both")

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
        bg="gray",  # agora igual ao botão da conscientização
        fg="white",
        font=("Arial", 14), width=20
    ).pack(pady=40)
