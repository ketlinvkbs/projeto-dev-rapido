import os
import basedosdados as bd
import pandas as pd

# Caminho correto para a chave JSON
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:/Users/Erick/OneDrive/Documentos/queimadas/chave_google.json"

def baixar_dados():
    csv_path = "queimadas.csv"

    if os.path.exists(csv_path):
        print("Arquivo já existe. Usando dados locais.")
        return csv_path

    try:
        print("Baixando dados da base do INPE...")

        query = """
        SELECT * FROM `basedosdados.br_inpe_queimadas.microdados`
        LIMIT 10000
        """

        df = bd.read_sql(query, billing_project_id="api-queimadas-459520")
        df.to_csv(csv_path, index=False)

        print("Dados baixados e salvos como CSV com sucesso!")
        return csv_path

    except Exception as e:
        raise Exception(f"Erro ao baixar os dados: {e}")
