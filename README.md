# Projeto de Conscientização sobre Queimadas no Brasil

## 📝 Descrição

Este projeto é uma aplicação interativa desenvolvida em Python que visa conscientizar sobre a problemática das queimadas no Brasil. A aplicação apresenta dados, um mapa interativo e um quiz para testar os conhecimentos do usuário sobre o tema.

## ✨ Funcionalidades

* **Tela de Conscientização:** Exibe informações e dados relevantes sobre as queimadas.
* **Quiz Interativo:** Um jogo de perguntas e respostas para engajar e educar o usuário.
* **Ranking de Jogadores:** Salva e exibe a pontuação dos usuários no quiz.
* **Mapa de Calor:** Apresenta um mapa do Brasil destacando os estados com maiores focos de queimadas.
* **Processamento de Dados:** Scripts para baixar, extrair e processar dados geográficos e de queimadas.

## 🔧 Configuração e Instalação

Para executar este projeto, você precisará ter o Python 3 instalado em seu sistema. Siga os passos abaixo para configurar o ambiente.

**1. Clone o repositório:**
(Se estiver no GitHub)
```bash
git clone [https://github.com/seu-usuario/projeto-dev-rapido.git](https://github.com/seu-usuario/projeto-dev-rapido.git)
cd projeto-dev-rapido

** 2. Instale as dependências:
As bibliotecas necessárias podem ser instaladas via pip. É altamenterecomendável criar um ambiente virtual (venv) primeiro.

```bash
# Crie e ative um ambiente virtual (opcional, mas recomendado)
python -m venv venv
source venv/bin/activate  # No Windows, use: venv\Scripts\activate
# Instale as bibliotecas
pip install pygame pandas geopandas requests tqdm
```

** 3. Baixe e prepare os dados:
Antes de executar a aplicação principal, é necessário baixar e processar os dados de municípios e focos de queimadas. Execute o script `download_dados.py` para automatizar este processo:

```bash
python download_dados.py
```

Este script irá:
- Baixar e extrair os dados dos municípios do site do IBGE.
- Converter os dados para o formato CSV (`municipios.csv`).
- Baixar os dados de focos de queimadas.
- Baixar os shapefiles para a geração de mapas.

## 🚀 Como Executar
Com o ambiente configurado e os dados processados, inicie a aplicação principal executando o arquivo `main.py`:

```bash
python main.py
```

A tela principal da aplicação será aberta, e você poderá navegar entre a tela de conscientização, o quiz e o ranking.

## 📁 Estrutura do Projeto
```
.
├── .vscode/
│   └── launch.json
├── gerar_shapefile/
│   └── gerar_regioes.py
├── shapefiles/
│   └── ...
├── baixar_municipios.py
├── baixar_shapefile.py
├── converter_municipios.py
├── download_dados.py
├── extrair_municipios.py
├── gera_municipios_csv.py
├── main.py
├── mapa_regioes.py
├── municipios.csv
├── perguntas.py
├── queimadas.csv
├── ranking_manager.py
├── tela_conscientizacao.py
├── tela_quiz.py
├── tela_ranking.py
├── usuarios.csv
└── README.md
```
