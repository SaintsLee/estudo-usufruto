import pandas as pd
import streamlit as st
import plotly.express as px

# Configuração da página
st.set_page_config(layout="wide", page_title="Estudo Usufruto", page_icon = "portfel_logo.ico")

# Imagem do logo Portfel
st.image("portfel-curve-logo.svg", width=250, output_format="png")

# Título do Dashboard
st.title("Carteiras de Usufruto - Uma análise de desempenho")

# Criação dos containers principais
container_topo = st.container()
container_baixo = st.container()

# Cor do tema
tema = False
if tema:
    back_color = "#0E1117"
    text_color = "#FAFAFA"
    zero_line = "#FFFFFF"
    fil_color = "#A0A0A0"
else:
    back_color = "#FFFFFF"
    text_color = "#31333F"
    zero_line = "#000000"
    fil_color = "#4A4A4A"

# Dividir em duas colunas
col1, col2 = st.columns(2)

# Distância do canto superior da página
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
# Remoção do valor que fica em baixo do slider
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

# Armazenamento em cache da base de dados a ser apresentada no dashboard
@st.cache_data
def load_data():
    dados_completos = pd.read_parquet("dados_completos_brotli.parquet")

    dados_completos_retornos = pd.read_parquet("dados_completos__retornos_brotli.parquet")

    return dados_completos, dados_completos_retornos

dados_completos, dados_completos_retornos = load_data()

# Função para o cálculo do Drawdown
def calcula_drawdown(dataset):
    retornos = dataset.cummax()

    drawdowns = dataset / retornos - 1
    drawdown_max = drawdowns.min()
    return drawdowns, drawdown_max

# Função para o cálculo dos retornos
def calcula_retornos(dados_completos_retornos, periodo_carteira, nomes_carteiras, periodo_movel,opcao):
    retornos_totais = pd.DataFrame(columns=["Conservadora", "Moderada", "Arrojada", "Agressiva"])
    if opcao == 1:
        for i in range(len(nomes_carteiras)):
            retornos = dados_completos_retornos[(dados_completos_retornos["Periodo"] == "{} Anos".format(periodo_carteira))
                                                & (dados_completos_retornos["Carteira"] == nomes_carteiras[i].split()[
                0])].drop(columns=["Carteira", "Periodo"]).pct_change().dropna().rolling(periodo_movel).max().max(axis=0)

            retornos_totais[nomes_carteiras[i].split()[0]] = retornos.dropna()
    elif opcao == 2:
        for i in range(len(nomes_carteiras)):
            retornos = dados_completos_retornos[
                (dados_completos_retornos["Periodo"] == "{} Anos".format(periodo_carteira))
                & (dados_completos_retornos["Carteira"] == nomes_carteiras[i].split()[
                    0])].drop(columns=["Carteira", "Periodo"]).pct_change().dropna().rolling(periodo_movel).min().min(axis=0)

            retornos_totais[nomes_carteiras[i].split()[0]] = retornos.dropna()
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
                    0])].drop(columns=["Carteira", "Periodo"]).pct_change().dropna().rolling(periodo_movel).mean().mean(axis=0)

            retornos_totais[nomes_carteiras[i].split()[0]] = retornos.dropna()

    return retornos_totais

# Função para o cálculo das volatilidades
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

# Função para a formatação dos gráficos Boxplot
def desenha_box_formatado(dataset, title, titulo_y, titulo_x):
    fig = px.box(dataset, color_discrete_sequence=["black"], title = title)

    fig.update_layout(xaxis_title=titulo_x, yaxis_title=titulo_y, showlegend=False, height=650, plot_bgcolor=back_color,
                      xaxis=dict(
                          tickfont=dict(size=18, color = text_color),  # Tamanho da fonte para os números no eixo X
                      ),
                      yaxis=dict(
                          tickfont=dict(size=18, color = text_color),  # Tamanho da fonte para os números no eixo Y

                      ),
                      xaxis_title_font=dict(size=18, color = text_color),  # Tamanho da fonte do eixo X
                      yaxis_title_font=dict(size=18, color = text_color),  # Tamanho da fonte do eixo Y
                      )

    # Personalizar o grid
    fig.update_xaxes(
        showgrid=False,  # Exibir a grade no eixo X
        gridcolor=text_color,  # Cor das linhas da grade
        gridwidth=0.5,  # Largura das linhas da grade
        zeroline=True,  # Exibir linha de zero (para eixo X)
        zerolinecolor=text_color,  # Cor da linha de zero
        zerolinewidth=1.2,  # Largura da linha de zero
        showline=True,  # Exibir a linha do eixo
        linecolor=text_color,  # Cor da linha do eixo
        linewidth=0.8,  # Largura da linha do eixo,
        griddash='dot',
        layer="below traces"  # Coloca o Grid atrás
    )

    fig.update_yaxes(
        showgrid=True,  # Exibir a grade no eixo Y
        gridcolor=text_color,  # Cor das linhas da grade
        gridwidth=0.5,  # Largura das linhas da grade
        zeroline=True,  # Exibir linha de zero (para eixo Y)
        zerolinecolor=zero_line,  # Cor da linha de zero
        zerolinewidth=1.2,  # Largura da linha de zero
        showline=True,  # Exibir a linha do eixo
        linecolor=text_color,  # Cor da linha do eixo
        linewidth=0.8,  # Largura da linha do eixo
        griddash='dot',
        layer="below traces"  # Coloca o Grid atrás
    )

    # Personalização das cores
    # "#392B84"
    fig.update_traces(
        marker_color="Red",  # Cor da caixa
        line_color=text_color,  # Cor da linha da borda
        fillcolor=fil_color,
        marker_size=4,  # Tamanho dos pontos
        marker_opacity=1  # Opacidade dos pontos
    )
    return fig

# Função para a formatação dos gráficos Linha
def desenha_linha_formatado(dataset, title,titulo_y, titulo_x):
    cores_personalizadas = ["#6faf5f","#dfe300","#fca620", "#ff0100"]

    fig = px.line(dataset,
                  title = title,
                  color_discrete_sequence= cores_personalizadas)

    fig.update_layout(xaxis_title=titulo_x, yaxis_title=titulo_y, showlegend=True, legend_title_text = "Carteiras",height=650, plot_bgcolor=back_color,
                      xaxis=dict(
                          tickfont=dict(size=18, color = text_color),  # Tamanho da fonte para os números no eixo X
                          showticklabels = False
                      ),
                      yaxis=dict(
                          tickfont=dict(size=18, color = text_color),  # Tamanho da fonte para os números no eixo Y

                      ),
                      xaxis_title_font=dict(size=18, color = text_color),  # Tamanho da fonte do eixo X
                      yaxis_title_font=dict(size=18, color = text_color),  # Tamanho da fonte do eixo Y
                      )

    # Personalizar o grid
    fig.update_xaxes(
        showgrid=False,  # Exibir a grade no eixo X
        gridcolor=text_color,  # Cor das linhas da grade
        gridwidth=0.5,  # Largura das linhas da grade
        zeroline=True,  # Exibir linha de zero (para eixo X)
        zerolinecolor=zero_line,  # Cor da linha de zero
        zerolinewidth=1.2,  # Largura da linha de zero
        showline=True,  # Exibir a linha do eixo
        linecolor=text_color,  # Cor da linha do eixo
        linewidth=0.8,  # Largura da linha do eixo,
        griddash='dot',
        layer="below traces"  # Coloca o Grid atrás
    )

    fig.update_yaxes(
        showgrid=True,  # Exibir a grade no eixo Y
        gridcolor=text_color,  # Cor das linhas da grade
        gridwidth=0.5,  # Largura das linhas da grade
        zeroline=True,  # Exibir linha de zero (para eixo Y)
        zerolinecolor=text_color,  # Cor da linha de zero
        zerolinewidth=1.2,  # Largura da linha de zero
        showline=True,  # Exibir a linha do eixo
        linecolor=text_color,  # Cor da linha do eixo
        linewidth=0.8,  # Largura da linha do eixo
        griddash='dot',
        layer="below traces"  # Coloca o Grid atrás
    )

    return fig

# Função para a formatação dos gráficos Treemap
def desenha_treemap_formatado(dataset, title):
    # Lista de cores customizadas
    cores_personalizadas = ["#6faf5f","#dfe300","#fca620", "#ff0100"]

    fig = px.treemap(dataset,
                     path= [px.Constant("Carteiras"), 'Tipo', 'Classe', 'Ativos'],
                     values="Pesos",
                     title=title,
                     hover_data = {"Pesos":":.2f%"},
                     color_discrete_sequence= cores_personalizadas
                     )

    fig.update_layout(showlegend=True, legend_title_text="Carteiras",
                      height=800, plot_bgcolor=back_color,
                      xaxis=dict(
                          tickfont=dict(size=18, color=text_color),  # Tamanho da fonte para os números no eixo X
                          showticklabels=False
                      ),
                      yaxis=dict(
                          tickfont=dict(size=18, color=text_color),  # Tamanho da fonte para os números no eixo Y

                      ),
                      xaxis_title_font=dict(size=18, color=text_color),  # Tamanho da fonte do eixo X
                      yaxis_title_font=dict(size=18, color=text_color),  # Tamanho da fonte do eixo Y
                      font=dict(color="rgba(0,0,0,0)") # Altera a cor do nó raíz
                      )
    fig.update_traces(
        hovertemplate="<b>%{label}</b><br>Peso: %{value}%<br><extra></extra>",
        texttemplate='%{label}<br>%{value}%',
        textfont_size = 16,
        textposition = "middle center",
        marker_line_color = "white",
        root_color= "rgba(0,0,0,0)"
    )


    return fig

# Definição do nome e dos períodos das carteiras assim como foi feito na criação dos dados pela simulação
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

with container_baixo:

    with col1:
        periodo_carteira = st.slider("# Período de usufruto da carteira", 10, 30, 20, 2)
    with col2:
        taxa_carteira = st.slider("# Taxa de retirada para o usufruto", 2.5, 7.0, 3.5, 0.5)

    # Exibir gráficos em cada coluna
    with col1:

        col_1_1_1, col_1_1_2 = st.columns([2,1])

        with col_1_1_1:
            st.markdown("#### Dispersão do patrimônio")
            st.write("Taxa: **{:.2f} %** - Período: **{} Anos**".format(taxa_carteira, periodo_carteira))
        with col_1_1_2:
            st.write("")
            carteira_check = st.checkbox("Composição das carteiras", value=False)
            survival_check = st.checkbox("Sobrevivência das carteiras", value=False)

        # Box Plot 1 - Dispersão do PL
        cap_inicial = 3000000
        carteiras_pl = dados_completos[(dados_completos["Taxa"] == "{:.2f}%".format(taxa_carteira)) &
                                       (dados_completos["Periodo"] == "{} Anos".format(periodo_carteira))].copy()

        # Cálculo do PL final em %
        carteiras_pl_tratada = carteiras_pl.drop(columns=["Taxa", "Periodo"]) / cap_inicial * 100

        box_plot_1 = desenha_box_formatado(carteiras_pl_tratada,
                                           "Patrimônio final para cada simulação",
                                           "Patrimônio Final [%]",
                                           "Carteiras")

        # Botão para observar a taxa de sobrevivência
        if survival_check:
            col1_1, col1_2 = st.columns([1,5])
            with col1_1:
                st.write("")
                st.write("")
                st.write("")
                st.write("")
                st.write("")
                st.write("")
                st.write("")
                st.markdown("##### Taxa de Sobrevivência")

                # Cálculo da taxa de sobrevivência
                survival = carteiras_pl.drop(columns=["Taxa", "Periodo"]) / cap_inicial * 100
                survival_total = pd.DataFrame()
                survival_total["Sobrevivência"] = (
                            (1 - (survival == 0).sum(axis=0) / survival.shape[0]) * 100)  # .apply(lambda x: f'{x:.2f}')

                # Seleção da taxa de sobrevivência
                survival_conservadora = survival_total.loc["Conservadora"].iloc[0]
                survival_moderada = survival_total.loc["Moderada"].iloc[0]
                survival_arrojada = survival_total.loc["Arrojada"].iloc[0]
                survival_agressiva = survival_total.loc["Agressiva"].iloc[0]

                # Seleção dos limites para a troca de cor em %
                lim_inferior = 30
                lim_superior = 80

                # Função para formatar a cor da taxa de sobrevivência
                def formata_sidebar_survival(nome,valor,lim_min,lim_max):
                    if valor <= lim_min:
                        texto_formatado = f"**{nome}**\n#### :red[{valor:.2f}%]"
                    elif (valor > lim_min) and (valor <= lim_max):
                        texto_formatado = f"**{nome}**\n#### :orange[{valor:.2f}%]"
                    else:
                        texto_formatado = f"**{nome}**\n#### :green[{valor:.2f}%]"
                    return texto_formatado

                # Formatação
                st.write(formata_sidebar_survival("Conservadora",survival_conservadora,lim_inferior,lim_superior))
                # --------------------------------------------------------------------------------------------
                st.write(formata_sidebar_survival("Moderada",survival_moderada,lim_inferior,lim_superior))
                # --------------------------------------------------------------------------------------------
                st.write(formata_sidebar_survival("Arrojada",survival_arrojada,lim_inferior,lim_superior))
                # --------------------------------------------------------------------------------------------
                st.write(formata_sidebar_survival("Agressiva",survival_agressiva,lim_inferior,lim_superior))

            with col1_2:
                st.plotly_chart(box_plot_1, use_container_width=False)
        else:
            st.plotly_chart(box_plot_1, use_container_width=False)
        # _______________________________________________________

        # Box Plot 3 - Retorno das Carteiras
        st.markdown(f"#### Análise dos retornos no período: {periodo_carteira} Anos")
        opcoes_label1 = {f"Maior retorno [mensal] no periodo":                   1,
                         f"Menor retorno [mensal] no periodo":                   2,
                         f"Retorno total no periodo de {periodo_carteira} Anos": 3,
                         f"Média dos retornos [mensal] no período":              4}

        opcao_radio1 = st.radio("Opções interessantes para análise:", list(opcoes_label1.keys()),label_visibility="hidden", index = 2)
        janela_analise_ret = st.slider("# Período do retorno móvel [meses]", 2, 24, 6, 1)
        retornos = calcula_retornos(dados_completos_retornos,
                                    periodo_carteira,
                                    nomes_carteiras,
                                    janela_analise_ret,
                                    opcoes_label1[opcao_radio1])

        box_plot_3 = desenha_box_formatado(retornos*100,
                                           "Retorno no período para cada simulação",
                                           "Retornos [%]",
                                           "Carteiras")

        st.plotly_chart(box_plot_3, use_container_width=False)
        #_______________________________________________________

    with col2:
        # Box Plot 2 - Dispersão do Drawdown
        draw_downs_totais = pd.DataFrame(columns=["Conservadora", "Moderada", "Arrojada", "Agressiva"])
        for i in range(len(nomes_carteiras)):
            dd, mdd = calcula_drawdown(
                dados_completos_retornos[(dados_completos_retornos["Periodo"] == "{} Anos".format(periodo_carteira))
                                         & (dados_completos_retornos["Carteira"] == nomes_carteiras[i].split()[0])].drop(
                    columns=["Carteira", "Periodo"])
                )
            draw_downs_totais[nomes_carteiras[i].split()[0]] = mdd

        box_plot_2 = desenha_box_formatado(draw_downs_totais * 100,
                                           "Máximo drawdown no período para cada simulação",
                                           "Drawdown [%]",
                                           "Carteiras")

        st.markdown("#### Dispersão do Drawdown")
        st.write("Periodo: **{} Anos**".format(periodo_carteira))
        st.plotly_chart(box_plot_2, use_container_width=False)
        #_______________________________________________________

        # Box Plot 4 - Dispersão da Volatilidade
        st.markdown(f"#### Análise das volatilidades no período: {periodo_carteira} Anos")
        opcoes_label2 = {f"Maior volatilidade [mensal] no periodo":                   1,
                         f"Menor volatilidade [mensal] no periodo":                   2,
                         f"Volatilidade total no período de {periodo_carteira} Anos": 3,
                         f"Média das volatilidades [mensal] no periodo":              4}
        st.write()
        opcao_radio2 = st.radio("Opções interessantes para análise:", list(opcoes_label2.keys()),label_visibility="hidden", index=2)
        janela_analise_vol = st.slider("# Período da volatilidade móvel [meses]", 2, 24, 6, 1)
        volatilidade = calcula_volatilidade(dados_completos_retornos,
                                            periodo_carteira,
                                            nomes_carteiras,
                                            janela_analise_vol,
                                            opcoes_label2[opcao_radio2])

        box_plot_4 = desenha_linha_formatado(volatilidade*100,
                                             "Volatilidade no período para cada simulação",
                                             "Volatilidade [%]",
                                             "Carteiras")

        st.plotly_chart(box_plot_4, use_container_width=False)
        #_______________________________________________________

with container_topo:
    if carteira_check:
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

        st.plotly_chart(desenha_treemap_formatado(df_carteiras, "Composição das Carteiras"))
