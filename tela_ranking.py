# tela_ranking.py (versão corrigida)
import tkinter as tk
from tkinter import ttk
import ranking_manager

COR_FUNDO = "#0B3D2E"
COR_TEXTO = "white"

def mostrar_ranking(app, limpar_tela):
    """Cria e exibe a tela de ranking de forma mais robusta."""
    limpar_tela()
    
    frame = tk.Frame(app, bg=COR_FUNDO)
    frame.pack(fill="both", expand=True, padx=20, pady=20)

    tk.Label(frame, text="🏆 Ranking por Cidade 🏆", font=("Georgia", 24, "bold"), fg=COR_TEXTO, bg=COR_FUNDO).pack(pady=(0, 20))
    tk.Label(frame, text="Clique em uma cidade para expandir ou recolher o detalhamento.", font=("Helvetica", 12, "italic"), fg="lightgrey", bg=COR_FUNDO).pack(pady=(0, 15))

    # Estilo para a Treeview
    style = ttk.Style()
    style.theme_use("default")
    style.configure("Treeview", background="#2E2E2E", foreground="white", fieldbackground="#2E2E2E", rowheight=28, font=("Helvetica", 12))
    style.configure("Treeview.Heading", background="goldenrod", foreground="black", font=("Helvetica", 12, "bold"), relief="flat")
    style.map('Treeview', background=[('selected', '#FF8C00')])
    style.map('Treeview.Heading', relief=[('active','groove'),('pressed','sunken')])

    # --- CORREÇÃO 1: Adicionando uma coluna "Pos." para a posição no ranking ---
    tree = ttk.Treeview(frame, columns=("Pos.", "Cidade", "Pontuação Total"), show="headings")
    tree.heading("Pos.", text="Pos.")
    tree.heading("Cidade", text="Cidade")
    tree.heading("Pontuação Total", text="Pontuação Total")

    # Ajustando as colunas
    tree.column("Pos.", width=60, anchor="center", stretch=tk.NO)
    tree.column("Cidade", width=300, anchor="w")
    tree.column("Pontuação Total", width=150, anchor="center")

    city_ranking = ranking_manager.get_city_ranking()
    for i, (cidade, total_acertos) in enumerate(city_ranking):
        rank = i + 1
        tree.insert("", "end", iid=cidade, values=(f"{rank}º", cidade, total_acertos))

    tree.pack(fill="both", expand=True)

    def on_item_select(event):
        """Função chamada quando um item é selecionado, para expandir ou recolher."""
        # Pega o ID do item selecionado. Retorna uma tupla, pegamos o primeiro.
        selection = tree.selection()
        if not selection:
            return
        
        item_id = selection[0]

        # Verifica se o item já tem filhos (se já está expandido)
        if tree.get_children(item_id):
            # Se já tem, apaga os filhos para "recolher"
            tree.delete(*tree.get_children(item_id))
        else:
            # Se não tem, busca os dados e expande
            user_scores = ranking_manager.get_user_scores_for_city(item_id)
            for matricula, acertos in user_scores:
                # Insere os dados da matrícula com valores nas colunas certas
                tree.insert(item_id, "end", values=("", f"  - Matrícula: {matricula}", acertos))

    # --- CORREÇÃO 2: Usando o evento <<TreeviewSelect>>, que é mais confiável ---
    tree.bind("<<TreeviewSelect>>", on_item_select)

    tk.Button(frame, text="Voltar ao Menu", command=lambda: limpar_tela(True), bg="darkred", fg="white", font=("Arial", 14), width=20).pack(pady=20)