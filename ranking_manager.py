import sqlite3
import os

# Define o nome do arquivo do banco de dados. Ele será criado no mesmo diretório do script.
DB_FILE = "ranking_queimadas.db"

def _get_db_connection():
    """Cria e retorna uma conexão com o banco de dados."""
    conn = sqlite3.connect(DB_FILE)
    # Opcional: Usar Row factory para acessar colunas pelo nome
    # conn.row_factory = sqlite3.Row 
    return conn

def init_db():
    """
    Inicializa o banco de dados. Cria a tabela de ranking se ela não existir.
    Deve ser chamada uma vez quando a aplicação inicia.
    """
    try:
        conn = _get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ranking (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                municipio TEXT UNIQUE NOT NULL,
                acertos INTEGER NOT NULL DEFAULT 0
            )
        """)
        conn.commit()
        print(f"Banco de dados '{DB_FILE}' inicializado. Tabela 'ranking' pronta.")
    except sqlite3.Error as e:
        print(f"Erro ao inicializar o banco de dados: {e}")
    finally:
        if conn:
            conn.close()

def update_score(municipio, score_to_add):
    """
    Atualiza a pontuação de um município.
    Se o município não existir, ele é inserido.
    Caso contrário, os acertos são somados.
    """
    if not municipio or not isinstance(municipio, str) or not municipio.strip():
        print("Erro: Município inválido para atualizar o ranking.")
        return
    if not isinstance(score_to_add, int):
        print("Erro: Pontuação a adicionar deve ser um inteiro.")
        return

    conn = None # Inicializa conn como None
    try:
        conn = _get_db_connection()
        cursor = conn.cursor()
        
        # Tenta inserir. Se o município já existir (devido à restrição UNIQUE),
        # atualiza os acertos somando a nova pontuação.
        cursor.execute("""
            INSERT INTO ranking (municipio, acertos)
            VALUES (?, ?)
            ON CONFLICT(municipio) DO UPDATE SET
            acertos = acertos + excluded.acertos; 
        """, (municipio, score_to_add))
        # Nota: excluded.acertos refere-se ao valor de 'acertos' que seria inserido (score_to_add).
        
        conn.commit()
        print(f"Ranking atualizado para '{municipio}': +{score_to_add} acertos.")
    except sqlite3.Error as e:
        print(f"Erro ao atualizar pontuação para '{municipio}': {e}")
    finally:
        if conn:
            conn.close()

def get_sorted_rankings():
    """
    Retorna uma lista de tuplas (municipio, acertos) ordenada por acertos em ordem decrescente.
    """
    conn = None
    try:
        conn = _get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT municipio, acertos 
            FROM ranking 
            ORDER BY acertos DESC, municipio ASC
        """) # Ordena por acertos (maior primeiro), depois por nome do município
        rankings = cursor.fetchall() # Retorna uma lista de tuplas
        return rankings
    except sqlite3.Error as e:
        print(f"Erro ao buscar rankings: {e}")
        return [] # Retorna lista vazia em caso de erro
    finally:
        if conn:
            conn.close()

def clear_ranking_table(): # Função de utilidade para testes
    """Limpa todos os registros da tabela de ranking."""
    conn = None
    try:
        conn = _get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM ranking")
        conn.commit()
        print("Tabela 'ranking' foi limpa.")
    except sqlite3.Error as e:
        print(f"Erro ao limpar a tabela de ranking: {e}")
    finally:
        if conn:
            conn.close()
