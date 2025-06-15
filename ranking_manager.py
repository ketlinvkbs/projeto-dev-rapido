# ranking_manager.py
import sqlite3

DB_FILE = "ranking_queimadas.db"

def _get_db_connection():
    """Cria e retorna uma conexão com o banco de dados."""
    conn = sqlite3.connect(DB_FILE)
    return conn

def init_db():
    """Inicializa o banco de dados e cria a tabela 'ranking' se ela não existir."""
    conn = None
    try:
        conn = _get_db_connection()
        cursor = conn.cursor()
        # Tabela para armazenar a pontuação de cada usuário (matrícula) por município
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ranking (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                municipio TEXT NOT NULL,
                matricula TEXT NOT NULL,
                acertos INTEGER NOT NULL,
                UNIQUE(municipio, matricula)
            )
        """)
        conn.commit()
        print(f"Banco de dados '{DB_FILE}' inicializado com sucesso.")
    except sqlite3.Error as e:
        print(f"Erro ao inicializar o banco de dados: {e}")
    finally:
        if conn:
            conn.close()

def add_score(municipio, matricula, score):
    """Adiciona ou atualiza a pontuação de um usuário no banco de dados."""
    if not all([municipio, matricula, isinstance(score, int)]):
        print("Erro: Dados inválidos para adicionar ao ranking.")
        return

    conn = None
    try:
        conn = _get_db_connection()
        cursor = conn.cursor()
        # Insere uma nova pontuação. Se o par (municipio, matricula) já existir,
        # atualiza a pontuação com o novo valor.
        cursor.execute("""
            INSERT INTO ranking (municipio, matricula, acertos)
            VALUES (?, ?, ?)
            ON CONFLICT(municipio, matricula) DO UPDATE SET
            acertos = excluded.acertos;
        """, (municipio, matricula, score))
        conn.commit()
        print(f"Pontuação de {matricula} em {municipio} salva: {score} acertos.")
    except sqlite3.Error as e:
        print(f"Erro ao adicionar pontuação: {e}")
    finally:
        if conn:
            conn.close()

def get_city_ranking():
    """Retorna um ranking de cidades baseado na SOMA das pontuações de seus usuários."""
    conn = None
    try:
        conn = _get_db_connection()
        cursor = conn.cursor()
        # Agrupa por município, soma os acertos e ordena do maior para o menor
        cursor.execute("""
            SELECT municipio, SUM(acertos) as total_acertos
            FROM ranking
            GROUP BY municipio
            ORDER BY total_acertos DESC
        """)
        return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Erro ao buscar ranking por cidade: {e}")
        return []
    finally:
        if conn:
            conn.close()

def get_user_scores_for_city(municipio):
    """Retorna as pontuações individuais dos usuários de uma cidade específica."""
    conn = None
    try:
        conn = _get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT matricula, acertos
            FROM ranking
            WHERE municipio = ?
            ORDER BY acertos DESC
        """, (municipio,))
        return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Erro ao buscar pontuações para {municipio}: {e}")
        return []
    finally:
        if conn:
            conn.close()