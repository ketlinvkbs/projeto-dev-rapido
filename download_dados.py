import os
import basedosdados as bd
import pandas as pd

# --- CÓDIGO PARA ENCONTRAR A CHAVE AUTOMATICAMENTE ---

NOME_ARQUIVO_CHAVE = "chave_google.json"
diretorio_script = os.path.dirname(os.path.abspath(__file__))
caminho_chave = os.path.join(diretorio_script, NOME_ARQUIVO_CHAVE)

if not os.path.exists(caminho_chave):
    raise FileNotFoundError(
        f"\n\n[ERRO CRÍTICO] O arquivo da chave '{NOME_ARQUIVO_CHAVE}' não foi encontrado na pasta do projeto!"
        f"\n\nPor favor, verifique se:"
        f"\n  1. O arquivo está na mesma pasta que o script 'download_dados.py'."
        f"\n  2. O nome do arquivo é exatamente '{NOME_ARQUIVO_CHAVE}' (cuidado com extensões duplicadas como '.json.json').\n"
    )

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = caminho_chave


def baixar_dados():
    csv_path = "queimadas.csv"

    if os.path.exists(csv_path):
        print(f"Arquivo '{csv_path}' já existe. Para baixar novos dados, por favor, apague o arquivo existente.")
        return csv_path

    try:
        print("Baixando dados do INPE para o ano de 2024...")

        query = """
        SELECT * FROM `basedosdados.br_inpe_queimadas.microdados`
        WHERE ano = 2024
        LIMIT 15000
        """

        # --- CORREÇÃO APLICADA AQUI ---
        # Trocamos o ID antigo pelo ID correto do seu projeto, que está no seu arquivo de chave.
        df = bd.read_sql(query, billing_project_id="safegas-1fd63")
        
        df.to_csv(csv_path, index=False)

        print("Dados de 2024 baixados e salvos como 'queimadas.csv' com sucesso!")
        return csv_path

    except Exception as e:
        raise Exception(f"Erro ao baixar os dados: {e}\n\nVerifique se o seu projeto de cobrança ('billing_project_id') está ativo no Google Cloud.")