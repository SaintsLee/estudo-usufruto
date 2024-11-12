import pandas as pd
import streamlit as st
import plotly.express as px

tema_base = st.get_option("theme.base")

st.set_page_config(layout="wide", page_title="Estudo Usufruto",page_icon = "portfel_logo.ico")

st.title("Análise do patrimônio final")

if tema_base == "dark":
    bckgroud_color = "#0E1117"
    txt_color = "#FAFAFA"
    zero_line = "#FFFFFF"
    fillcolor = "#A0A0A0"
else:
    bckgroud_color = "#FFFFFF"
    txt_color = "#31333F"
    zero_line = "#000000"
    fillcolor = "#4A4A4A"


st.markdown(
    """
    <style>
    body {
        margin-top: -20px;  /* Diminui a margem superior da página */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Dividir em duas colunas
col1, col2 = st.columns(2)

# Exibir sliders em cada coluna
st.markdown(
    """
    <style>
    .stSlider label {
        font-size: 20px; /* Aumente o valor para ajustar o tamanho */
        font-weight: bold; /* Opcional: para tornar o texto mais destacado */
    }
    </style>
    """,
    unsafe_allow_html=True
)
with col1:
    periodo_carteira = st.slider("# Período de usufruto da carteira", 10, 30, 10, 2)
with col2:
    taxa_carteira = st.slider("# Taxa de retirada para o usufruto", 2.5, 7.0, 2.5, 0.5)

@st.cache_data
def load_data():
    dados_completos = pd.read_parquet("dados_completos_brotli.parquet")

    dados_completos_retornos = pd.read_parquet("dados_completos__retornos_brotli.parquet")

    return dados_completos, dados_completos_retornos

dados_completos, dados_completos_retornos = load_data()

st.markdown(
    """
    <style>
    /* Remover o valor abaixo do slider*/
    .st-emotion-cache-hpex6h.ew7r33m0
    {
        visibility: hidden;
    }
    /* Diminuir o espaço entre os widgets */
    .stElementContainer.element-container.st-emotion-cache-1jm780e.e1f1d6gn4 { 
     /* O seletor CSS para widgets em Streamlit */
        margin-bottom: 0px;  /* Ajuste o valor para diminuir o espaço */
        margin-top: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

def calcula_drawdown(dataset):
    retornos = dataset.cummax()

    drawdowns = dataset / retornos - 1
    drawdown_max = drawdowns.min()
    return drawdowns, drawdown_max

def calcula_retornos(dados_completos_retornos, periodo_carteira, nomes_carteiras, opcao):
    retornos_totais = pd.DataFrame(columns=["Conservadora", "Moderada", "Arrojada", "Agressiva"])
    if opcao == 1:
        for i in range(len(nomes_carteiras)):
            retornos = dados_completos_retornos[(dados_completos_retornos["Periodo"] == "{} Anos".format(periodo_carteira))
                                                & (dados_completos_retornos["Carteira"] == nomes_carteiras[i].split()[
                0])].drop(columns=["Carteira", "Periodo"]).pct_change().dropna().max(axis=0)

            retornos_totais[nomes_carteiras[i].split()[0]] = retornos
    elif opcao == 2:
        for i in range(len(nomes_carteiras)):
            retornos = dados_completos_retornos[
                (dados_completos_retornos["Periodo"] == "{} Anos".format(periodo_carteira))
                & (dados_completos_retornos["Carteira"] == nomes_carteiras[i].split()[
                    0])].drop(columns=["Carteira", "Periodo"]).pct_change().dropna().min(axis=0)

            retornos_totais[nomes_carteiras[i].split()[0]] = retornos
    elif opcao == 3:
        for i in range(len(nomes_carteiras)):
            retornos = dados_completos_retornos[
                (dados_completos_retornos["Periodo"] == "{} Anos".format(periodo_carteira))
                & (dados_completos_retornos["Carteira"] == nomes_carteiras[i].split()[
                    0])].drop(columns=["Carteira", "Periodo"]).iloc[-1]/3000000 - 1

            retornos_totais[nomes_carteiras[i].split()[0]] = retornos
    elif opcao == 4:
        for i in range(len(nomes_carteiras)):
            retornos = dados_completos_retornos[
                (dados_completos_retornos["Periodo"] == "{} Anos".format(periodo_carteira))
                & (dados_completos_retornos["Carteira"] == nomes_carteiras[i].split()[
                    0])].drop(columns=["Carteira", "Periodo"]).pct_change().dropna().mean(axis=0)

            retornos_totais[nomes_carteiras[i].split()[0]] = retornos

    return retornos_totais

def calcula_volatilidade(dados_completos_retornos, periodo_carteira, nomes_carteiras, periodo_movel,opcao):
    vols_totais = pd.DataFrame(columns=["Conservadora", "Moderada", "Arrojada", "Agressiva"])
    if opcao == 1:
        for i in range(len(nomes_carteiras)):
            vols = dados_completos_retornos[(dados_completos_retornos["Periodo"] == "{} Anos".format(periodo_carteira))
                                                & (dados_completos_retornos["Carteira"] == nomes_carteiras[i].split()[
                0])].drop(columns=["Carteira", "Periodo"]).pct_change().dropna().rolling(periodo_movel).std().max(axis = 0)

            vols_totais[nomes_carteiras[i].split()[0]] = vols

    elif opcao == 2:
        for i in range(len(nomes_carteiras)):
            vols = dados_completos_retornos[(dados_completos_retornos["Periodo"] == "{} Anos".format(periodo_carteira))
                                                & (dados_completos_retornos["Carteira"] == nomes_carteiras[i].split()[
                0])].drop(columns=["Carteira", "Periodo"]).pct_change().dropna().rolling(periodo_movel).std().min(axis=0)

            vols_totais[nomes_carteiras[i].split()[0]] = vols

    elif opcao == 3:
        for i in range(len(nomes_carteiras)):
            vols = dados_completos_retornos[(dados_completos_retornos["Periodo"] == "{} Anos".format(periodo_carteira))
                                                & (dados_completos_retornos["Carteira"] == nomes_carteiras[i].split()[
                0])].drop(columns=["Carteira", "Periodo"]).pct_change().dropna().std()

            vols_totais[nomes_carteiras[i].split()[0]] = vols

    elif opcao == 4:
        for i in range(len(nomes_carteiras)):
            vols = dados_completos_retornos[(dados_completos_retornos["Periodo"] == "{} Anos".format(periodo_carteira))
                                                & (dados_completos_retornos["Carteira"] == nomes_carteiras[i].split()[
                0])].drop(columns=["Carteira", "Periodo"]).pct_change().dropna().rolling(periodo_movel).std().mean(axis=0)

            vols_totais[nomes_carteiras[i].split()[0]] = vols

    return vols_totais

def desenha_box_formatado(dataset, titulo_y, titulo_x):
    fig = px.box(dataset, color_discrete_sequence=["black"])

    fig.update_layout(xaxis_title=titulo_x, yaxis_title=titulo_y, showlegend=False, height=650, plot_bgcolor=bckgroud_color,
                      xaxis=dict(
                          tickfont=dict(size=18, color = txt_color),  # Tamanho da fonte para os números no eixo X
                      ),
                      yaxis=dict(
                          tickfont=dict(size=18, color = txt_color),  # Tamanho da fonte para os números no eixo Y

                      ),
                      xaxis_title_font=dict(size=18, color = txt_color),  # Tamanho da fonte do eixo X
                      yaxis_title_font=dict(size=18, color = txt_color),  # Tamanho da fonte do eixo Y
                      )

    # Personalizar o grid
    fig.update_xaxes(
        showgrid=False,  # Exibir a grade no eixo X
        gridcolor=txt_color,  # Cor das linhas da grade
        gridwidth=0.5,  # Largura das linhas da grade
        zeroline=True,  # Exibir linha de zero (para eixo X)
        zerolinecolor=txt_color,  # Cor da linha de zero
        zerolinewidth=1.2,  # Largura da linha de zero
        showline=True,  # Exibir a linha do eixo
        linecolor=txt_color,  # Cor da linha do eixo
        linewidth=0.8,  # Largura da linha do eixo,
        griddash='dot',
        layer="below traces"  # Coloca o Grid atrás
    )

    fig.update_yaxes(
        showgrid=True,  # Exibir a grade no eixo Y
        gridcolor=txt_color,  # Cor das linhas da grade
        gridwidth=0.5,  # Largura das linhas da grade
        zeroline=True,  # Exibir linha de zero (para eixo Y)
        zerolinecolor=zero_line,  # Cor da linha de zero
        zerolinewidth=1.2,  # Largura da linha de zero
        showline=True,  # Exibir a linha do eixo
        linecolor=txt_color,  # Cor da linha do eixo
        linewidth=0.8,  # Largura da linha do eixo
        griddash='dot',
        layer="below traces"  # Coloca o Grid atrás
    )

    # Personalização das cores
    # "#392B84"
    fig.update_traces(
        marker_color="Red",  # Cor da caixa
        line_color=txt_color,  # Cor da linha da borda
        fillcolor=fillcolor,
        marker_size=4,  # Tamanho dos pontos
        marker_opacity=1  # Opacidade dos pontos
    )
    return fig


def desenha_linha_formatado(dataset, titulo_y, titulo_x):
    fig = px.line(dataset)

    fig.update_layout(xaxis_title=titulo_x, yaxis_title=titulo_y, showlegend=True, legend_title_text = "Carteiras",height=650, plot_bgcolor=bckgroud_color,
                      xaxis=dict(
                          tickfont=dict(size=18, color = txt_color),  # Tamanho da fonte para os números no eixo X
                          showticklabels = False
                      ),
                      yaxis=dict(
                          tickfont=dict(size=18, color = txt_color),  # Tamanho da fonte para os números no eixo Y

                      ),
                      xaxis_title_font=dict(size=18, color = txt_color),  # Tamanho da fonte do eixo X
                      yaxis_title_font=dict(size=18, color = txt_color),  # Tamanho da fonte do eixo Y
                      )

    # Personalizar o grid
    fig.update_xaxes(
        showgrid=False,  # Exibir a grade no eixo X
        gridcolor=txt_color,  # Cor das linhas da grade
        gridwidth=0.5,  # Largura das linhas da grade
        zeroline=True,  # Exibir linha de zero (para eixo X)
        zerolinecolor=zero_line,  # Cor da linha de zero
        zerolinewidth=1.2,  # Largura da linha de zero
        showline=True,  # Exibir a linha do eixo
        linecolor=txt_color,  # Cor da linha do eixo
        linewidth=0.8,  # Largura da linha do eixo,
        griddash='dot',
        layer="below traces"  # Coloca o Grid atrás
    )

    fig.update_yaxes(
        showgrid=True,  # Exibir a grade no eixo Y
        gridcolor=txt_color,  # Cor das linhas da grade
        gridwidth=0.5,  # Largura das linhas da grade
        zeroline=True,  # Exibir linha de zero (para eixo Y)
        zerolinecolor=txt_color,  # Cor da linha de zero
        zerolinewidth=1.2,  # Largura da linha de zero
        showline=True,  # Exibir a linha do eixo
        linecolor=txt_color,  # Cor da linha do eixo
        linewidth=0.8,  # Largura da linha do eixo
        griddash='dot',
        layer="below traces"  # Coloca o Grid atrás
    )

    return fig

nomes_carteiras = ["Conservadora - Análise PL",
                   "Moderada - Análise PL",
                   "Arrojada - Análise PL",
                   "Agressiva - Análise PL"]

periodo_carteiras = ["10 Anos",
                     "12 Anos",
                     "14 Anos",
                     "16 Anos",
                     "18 Anos",
                     "20 Anos",
                     "22 Anos",
                     "24 Anos",
                     "26 Anos",
                     "28 Anos",
                     "30 Anos"]

# Exibir gráficos em cada coluna
with col1:
    # Box Plot 1 - Disperssão do PL
    cap_inicial = 3000000
    carteiras_pl = dados_completos[(dados_completos["Taxa"] == "{:.2f}%".format(taxa_carteira)) &
                                   (dados_completos["Periodo"] == "{} Anos".format(periodo_carteira))].copy()

    carteiras_pl_tratada = carteiras_pl.drop(columns=["Taxa", "Periodo"]) / cap_inicial * 100

    box_plot_1 = desenha_box_formatado(carteiras_pl_tratada, "Patrimônio Final [%]", "Carteiras")

    st.markdown("#### Dispersão do patrimônio")
    st.write("Taxa: {:.2f}% e Período: {} Anos".format(taxa_carteira,periodo_carteira))
    st.plotly_chart(box_plot_1, use_container_width=False)
    # _______________________________________________________

    # Box Plot 3 - Retorno das Carteiras
    st.markdown(f"#### Análise dos retornos no período: {periodo_carteira} Anos")
    opcoes_label1 = {f"Maior retorno [mensal] no periodo":                   1,
                     f"Menor retorno [mensal] no periodo":                   2,
                     f"Retorno total no periodo de {periodo_carteira} Anos": 3,
                     f"Média dos retornos [mensal] no período":              4}

    opcao_radio1 = st.radio("Opções interessantes para análise:", list(opcoes_label1.keys()),label_visibility="hidden")
    retornos = calcula_retornos(dados_completos_retornos, periodo_carteira, nomes_carteiras, opcoes_label1[opcao_radio1])

    st.markdown(
        """
        <div style="margin-top: 82px;"></div>
        """,
        unsafe_allow_html=True
    )

    box_plot_3 = desenha_box_formatado(retornos*100, "Retornos [%]", "Carteiras")
    st.plotly_chart(box_plot_3, use_container_width=False)
    #_______________________________________________________

with col2:
    # Box Plot 2 - Disperssão do Drawdown
    draw_downs_totais = pd.DataFrame(columns=["Conservadora", "Moderada", "Arrojada", "Agressiva"])
    for i in range(len(nomes_carteiras)):
        dd, mdd = calcula_drawdown(
            dados_completos_retornos[(dados_completos_retornos["Periodo"] == "{} Anos".format(periodo_carteira))
                                     & (dados_completos_retornos["Carteira"] == nomes_carteiras[i].split()[0])].drop(
                columns=["Carteira", "Periodo"])
            )
        draw_downs_totais[nomes_carteiras[i].split()[0]] = mdd

    box_plot_2 = desenha_box_formatado(draw_downs_totais * 100, "Drawdown [%]", "Carteiras")

    st.markdown("#### Dispersão do Drawdown")
    st.write("Taxa: {:.2f}%".format(taxa_carteira))
    st.plotly_chart(box_plot_2, use_container_width=False)
    #_______________________________________________________

    # Box Plot 4 - Disperssão da Volatilidade
    st.markdown(f"#### Análise das volatilidades no período: {periodo_carteira} Anos")
    opcoes_label2 = {f"Maior volatilidade [mensal] no periodo":                   1,
                     f"Menor volatilidade [mensal] no periodo":                   2,
                     f"Volatilidade total no período de {periodo_carteira} Anos": 3,
                     f"Média das volatilidades [mensal] no periodo":              4}

    opcao_radio2 = st.radio("Opções interessantes para análise:", list(opcoes_label2.keys()),label_visibility="hidden")
    janela_analise = st.slider("# Período da volatilidade móvel [meses]", 2, 24, 2, 1)
    volatilidade = calcula_volatilidade(dados_completos_retornos,
                                        periodo_carteira,
                                        nomes_carteiras,
                                        janela_analise,
                                        opcoes_label2[opcao_radio2])

    box_plot_4 = desenha_linha_formatado(volatilidade*100, "Volatilidade [%]", "Carteiras")

    st.plotly_chart(box_plot_4, use_container_width=False)
    #_______________________________________________________


