import tkinter as tk

# Texto dividido em páginas
paginas_conscientizacao = [
    (
        "Conscientização sobre Queimadas",
        "As queimadas, sejam naturais ou causadas por humanos, destroem a vegetação, "
        "afetam a fauna e comprometem todo o ecossistema. São também uma grande fonte de emissão "
        "de gases poluentes que contribuem para o aquecimento global."
    ),
    (
        "Impactos Ambientais",
        "Além da perda de biodiversidade, as queimadas alteram o ciclo da água, aumentam "
        "a erosão do solo e comprometem a recuperação natural da vegetação."
    ),
    (
        "Consequências para a Saúde",
        "A fumaça causa problemas respiratórios, principalmente em crianças e idosos. "
        "Durante períodos críticos, aumenta a demanda nos hospitais e piora a qualidade de vida."
    ),
    (
        "Efeitos Econômicos e Sociais",
        "Propriedades agrícolas são destruídas, há perda de produtividade, danos a estruturas, "
        "e impacto negativo no turismo e na economia local."
    ),
    (
        "O Papel da Conscientização",
        "Entender os impactos é o primeiro passo para agir. Práticas sustentáveis, denúncia de queimadas "
        "ilegais e apoio a políticas ambientais são atitudes que fazem a diferença."
    ),
    (
        "Atitudes que Salvam",
        "Evite o uso do fogo, plante árvores, eduque outras pessoas e respeite o meio ambiente. "
        "Pequenas ações geram grandes resultados quando feitas em conjunto."
    )
]

COR_FUNDO = "#0B3D2E"  # Cor verde escura oficial

def mostrar_tela_conscientizacao(janela, limpar_tela):
    limpar_tela()
    janela.configure(bg=COR_FUNDO)

    frame = tk.Frame(janela, bg=COR_FUNDO)
    frame.pack(expand=True, fill="both")

    titulo_label = tk.Label(
        frame, text="", font=("Helvetica", 22, "bold"),
        fg="white", bg=COR_FUNDO, wraplength=800, justify="center"
    )
    titulo_label.pack(pady=(30, 10))

    texto_label = tk.Label(
        frame, text="", font=("Helvetica", 16),
        fg="white", bg=COR_FUNDO, wraplength=800, justify="center"
    )
    texto_label.pack(pady=10)

    botoes_frame = tk.Frame(frame, bg=COR_FUNDO)
    botoes_frame.pack(pady=20)

    btn_anterior = tk.Button(
        botoes_frame, text="Anterior", bg="gray", fg="white", width=12
    )
    btn_anterior.grid(row=0, column=0, padx=10)

    btn_proximo = tk.Button(
        botoes_frame, text="Próximo", bg="gray", fg="white", width=12
    )
    btn_proximo.grid(row=0, column=1, padx=10)

    btn_voltar = tk.Button(
        frame, text="Voltar", command=lambda: limpar_tela(True),
        bg="darkred", fg="white", width=12
    )
    btn_voltar.pack(pady=(10, 30))

    pagina_atual = [0]

    def atualizar_conteudo():
        titulo, texto = paginas_conscientizacao[pagina_atual[0]]
        titulo_label.config(text=titulo)
        texto_label.config(text=texto)
        btn_anterior.config(state="normal" if pagina_atual[0] > 0 else "disabled")
        btn_proximo.config(state="normal" if pagina_atual[0] < len(paginas_conscientizacao) - 1 else "disabled")

    def proxima_pagina():
        if pagina_atual[0] < len(paginas_conscientizacao) - 1:
            pagina_atual[0] += 1
            atualizar_conteudo()

    def pagina_anterior():
        if pagina_atual[0] > 0:
            pagina_atual[0] -= 1
            atualizar_conteudo()

    btn_proximo.config(command=proxima_pagina)
    btn_anterior.config(command=pagina_anterior)

    atualizar_conteudo()
