import pandas as pd
import streamlit as st
import gdown

# Armazenamento em cache da base de dados a ser apresentada no dashboard
@st.cache_data
def load_data():
    dados_completos = pd.read_parquet("dados_completos_brotli.parquet")

    # ID do arquivo no Google Drive
    file_id = "1r9ZmWRLVhZhhjGrWO-u1U0rEdNkxK8JD"
    url = f"https://drive.google.com/uc?id={file_id}"
    
    # Baixando o arquivo do Google Drive
    output = "dados_completos__retornos_brotli.parquet"
    gdown.download(url, output, quiet=False)
    
    # Carregar o arquivo no pandas
    dados_completos_retornos = pd.read_parquet(output)

    #dados_completos_retornos = pd.read_parquet("dados_completos__retornos_brotli.parquet")
    
    return dados_completos, dados_completos_retornos

# Armazenamento em cache da criação do dataframe ajustado para as carteiras
def apresenta_carteiras():
    # Quais carteiras estão sendo analisadas
    tipos_carteiras = ["Conservadora", "Moderada", "Arrojada", "Agressiva"]

    # Classes dos ativos de cada carteira
    classe_ativos_conservadora = ["Renda Fixa - CDI",
                                  "Renda Fixa - CDI"]

    classe_ativos_moderada = ["Renda Fixa - CDI",
                              "Renda Fixa - CDI",
                              "Renda Fixa - Inflação",
                              "Renda Fixa - Inflação",
                              "Renda Fixa - Pré",
                              "Renda Variável - Imobiliário"]

    classe_ativos_arrojada = ["Renda Fixa - CDI",
                              "Renda Fixa - CDI",
                              "Renda Fixa - Inflação",
                              "Renda Fixa - Inflação",
                              "Renda Fixa - Pré",
                              "Renda Variável - Imobiliário",
                              "Renda Variável - Ações BR",
                              "Renda Fixa - Exterior",
                              "Renda Fixa - Exterior",
                              "Renda Variável - Ações Global",
                              "Ouro"]

    classe_ativos_agressiva = ["Renda Fixa - CDI",
                               "Renda Fixa - CDI",
                               "Renda Fixa - Inflação",
                               "Renda Fixa - Inflação",
                               "Renda Fixa - Pré",
                               "Renda Variável - Imobiliário",
                               "Renda Variável - Ações BR",
                               "Renda Fixa - Exterior",
                               "Renda Fixa - Exterior",
                               "Renda Variável - Ações Global",
                               "Ouro"]

    # Pesos dos ativos de cada carteira
    pesos_carteira_conservadora = [0.2,
                                   0.8]

    pesos_carteira_moderada = [0.08,
                               0.32, 0.2, 0.2, 0.15, 0.05]

    pesos_carteira_arrojada = [0.05,
                               0.2, 0.125, 0.125, 0.15, 0.05, 0.125, 0.025, 0.025, 0.10, 0.025]

    pesos_carteira_agressiva = [0.03,
                                0.12, 0.075, 0.075, 0.1, 0.1, 0.25, 0.025, 0.025, 0.175, 0.025]

    # Ativos de cada carteira
    ativos_carteira_conservadora = ["CDI",
                                    "TEVADI"]

    ativos_carteira_moderada = ["CDI",
                                "TEVADI", "IMAB-5", "IDA-LIQ-IPCA", "IFRM-P2", "IFIX"]

    ativos_carteira_arrojada = ["CDI",
                                "TEVADI", "IMAB-5", "IDA-LIQ-IPCA", "IFRM-P2", "IFIX", "IBRX", "BND", "BNDX",
                                "MSCI-World", "IAU"]

    ativos_carteira_agressiva = ["CDI",
                                 "TEVADI", "IMAB-5", "IDA-LIQ-IPCA", "IFRM-P2", "IFIX", "IBRX", "BND", "BNDX",
                                 "MSCI-World", "IAU"]

    # Colunas para o dataframe
    colunas_carteiras = ["Tipo", "Classe", "Ativos", "Pesos"]

    # Dados consolidados para o Treemap
    dados_consolidados_carteiras = [
        {
            colunas_carteiras[0]: tipos_carteiras[0],
            colunas_carteiras[1]: classe_ativos_conservadora,
            colunas_carteiras[2]: ativos_carteira_conservadora,
            colunas_carteiras[3]: pesos_carteira_conservadora
        },
        {
            colunas_carteiras[0]: tipos_carteiras[1],
            colunas_carteiras[1]: classe_ativos_moderada,
            colunas_carteiras[2]: ativos_carteira_moderada,
            colunas_carteiras[3]: pesos_carteira_moderada
        },
        {
            colunas_carteiras[0]: tipos_carteiras[2],
            colunas_carteiras[1]: classe_ativos_arrojada,
            colunas_carteiras[2]: ativos_carteira_arrojada,
            colunas_carteiras[3]: pesos_carteira_arrojada
        },
        {
            colunas_carteiras[0]: tipos_carteiras[3],
            colunas_carteiras[1]: classe_ativos_agressiva,
            colunas_carteiras[2]: ativos_carteira_agressiva,
            colunas_carteiras[3]: pesos_carteira_agressiva
        },
    ]

    linhas_aux = []
    for carteira in dados_consolidados_carteiras:
        tipo = carteira["Tipo"]
        for classe, ativo, peso in zip(carteira["Classe"], carteira["Ativos"], carteira["Pesos"]):
            linhas_aux.append({"Tipo": tipo, "Classe": classe, "Ativos": ativo, "Pesos": peso * 100})

    df_carteiras = pd.DataFrame(linhas_aux)

    # Definir a ordem personalizada para a coluna "Tipo"
    ordem_tipos = ["Conservadora", "Moderada", "Arrojada", "Agressiva"]
    df_carteiras["Tipo"] = pd.Categorical(df_carteiras["Tipo"], categories=ordem_tipos, ordered=True)

    df_carteiras["Risco"] = df_carteiras["Tipo"].apply(lambda x: 1 if x == "Conservadora" else
    2 if x == "Moderada" else
    3 if x == "Arrojada" else
    4)
    return df_carteiras
