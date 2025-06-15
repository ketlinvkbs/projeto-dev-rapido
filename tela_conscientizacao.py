import tkinter as tk

# Texto dividido em páginas
paginas_conscientizacao = [
    (
        "Conscientização sobre Queimadas no Brasil",
        "As queimadas são um dos problemas ambientais mais graves enfrentados pelo Brasil atualmente. "
        "Todos os anos, milhares de focos de incêndio são registrados em diferentes regiões do país, "
        "principalmente na Amazônia, no Cerrado e no Pantanal. Esses incêndios afetam a biodiversidade, "
        "a qualidade do ar, o clima, a saúde da população e até mesmo a economia."
    ),
    (
        "Causas das Queimadas",
        "Apesar de existirem queimadas naturais, causadas por raios e altas temperaturas, a imensa maioria "
        "dos incêndios florestais no Brasil é provocada pela ação humana. As principais causas são:\n\n"
        "- Desmatamento ilegal.\n"
        "- Práticas agrícolas inadequadas.\n"
        "- Queimadas domésticas e expansão urbana.\n"
        "- Atos criminosos ou negligência."
    ),
    (
        "Desmatamento e Práticas Agrícolas",
        "Áreas desmatadas são queimadas para transformar em pasto ou agricultura. "
        "O uso do fogo para renovar pastagens ou eliminar restos de colheitas é comum, "
        "mas extremamente perigoso e prejudicial."
    ),
    (
        "Consequências das Queimadas",
        "As queimadas causam:\n\n"
        "- Perda da biodiversidade.\n"
        "- Poluição do ar, agravando problemas respiratórios.\n"
        "- Emissão de CO₂, contribuindo para o aquecimento global.\n"
        "- Impacto social em comunidades indígenas, ribeirinhas e rurais.\n"
        "- Prejuízos econômicos no agronegócio, turismo e saúde."
    ),
    (
        "Prevenção e Combate",
        "A prevenção exige esforços conjuntos:\n\n"
        "- Educação ambiental nas escolas e comunidades.\n"
        "- Fiscalização e punição de práticas ilegais.\n"
        "- Uso de tecnologias como dados de satélite (INPE).\n"
        "- Incentivo à agricultura sustentável.\n"
        "- Participação comunitária e denúncias."
    ),
    (
        "Você Também Pode Ajudar",
        "Ações simples fazem a diferença:\n\n"
        "- Nunca ateie fogo em vegetação seca.\n"
        "- Não jogue lixo em terrenos ou estradas.\n"
        "- Denuncie queimadas ilegais (IBAMA, bombeiros, Defesa Civil).\n"
        "- Apoie ONGs e projetos de preservação.\n\n"
        "As queimadas afetam nossa vida, o ar que respiramos e o clima. "
        "Proteger o meio ambiente é uma responsabilidade de todos!"
    )
]

COR_FUNDO = "#0B3D2E"  # Verde escuro

def mostrar_tela_conscientizacao(janela, limpar_tela):
    limpar_tela()
    janela.configure(bg=COR_FUNDO)

    frame = tk.Frame(janela, bg=COR_FUNDO)
    frame.pack(expand=True, fill="both")

    titulo_label = tk.Label(
        frame, text="", font=("Helvetica", 24, "bold"),
        fg="white", bg=COR_FUNDO, wraplength=1000, justify="center"
    )
    titulo_label.pack(pady=(30, 10))

    texto_label = tk.Label(
        frame, text="", font=("Helvetica", 16),
        fg="white", bg=COR_FUNDO, wraplength=1000, justify="center"
    )
    texto_label.pack(pady=10)

    contador_pagina = tk.Label(
        frame, text="", font=("Helvetica", 14, "italic"),
        fg="white", bg=COR_FUNDO
    )
    contador_pagina.pack(pady=(5, 15))

    botoes_frame = tk.Frame(frame, bg=COR_FUNDO)
    botoes_frame.pack(pady=10)

    btn_anterior = tk.Button(
        botoes_frame, text="Anterior", bg="goldenrod", fg="black", width=12
    )
    btn_anterior.grid(row=0, column=0, padx=10)

    btn_proximo = tk.Button(
        botoes_frame, text="Próximo", bg="goldenrod", fg="black", width=12
    )
    btn_proximo.grid(row=0, column=1, padx=10)

    btn_voltar = tk.Button(
        frame, text="Voltar", command=lambda: limpar_tela(True),
        bg="darkred", fg="white", width=12
    )
    btn_voltar.pack(pady=(20, 30))

    pagina_atual = [0]

    def atualizar_conteudo():
        titulo, texto = paginas_conscientizacao[pagina_atual[0]]
        titulo_label.config(text=titulo)
        texto_label.config(text=texto)
        contador_pagina.config(
            text=f"Página {pagina_atual[0] + 1} de {len(paginas_conscientizacao)}"
        )
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
