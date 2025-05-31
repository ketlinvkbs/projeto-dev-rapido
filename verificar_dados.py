import pandas as pd

# Caminho do CSV com os dados
CAMINHO_CSV = "queimadas.csv"

try:
    # Carrega os dados
    dados = pd.read_csv(CAMINHO_CSV)

    # Mostra as primeiras linhas dos dados
    print("\n📌 Primeiras linhas do arquivo:")
    print(dados.head())

    # Mostra as estatísticas da coluna de intensidade
    print("\n🔥 Estatísticas da coluna 'potencia_radiativa_fogo':")
    print(dados['potencia_radiativa_fogo'].describe())

    # Mostra os valores únicos e quantas vezes aparecem
    print("\n🌈 Distribuição de valores:")
    print(dados['potencia_radiativa_fogo'].value_counts(bins=5, sort=False))

except FileNotFoundError:
    print(f"❌ Arquivo {CAMINHO_CSV} não encontrado!")
except Exception as e:
    print(f"⚠️ Erro: {e}")
