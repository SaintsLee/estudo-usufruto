import pandas as pd
import streamlit as st
from graficos_formatados import desenha_box_formatado, desenha_linha_formatado, desenha_treemap_formatado
from calculos_internos import calcula_drawdown, calcula_retornos, calcula_volatilidade
from auxiliares import load_data, apresenta_carteiras

# Configuração da página
st.set_page_config(layout="wide", page_title="Estudo Usufruto", page_icon = "portfel_logo.ico")

# Imagem do logo Portfel
st.image("portfel-curve-logo.svg", width=250, output_format="png")

# Título do Dashboard
st.title("Carteiras de Usufruto - Uma análise de desempenho")

# Criação dos containers principais
container_topo = st.container()
container_baixo = st.container()

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

dados_completos, dados_completos_retornos = load_data()

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

        col_1_1_1, col_1_1_2= st.columns(2)

        with col_1_1_1:
            st.markdown("#### Dispersão do patrimônio")
            st.write("Taxa: **{:.2f} %** - Período: **{} Anos**".format(taxa_carteira, periodo_carteira))
        with col_1_1_2:
            #st.write("")
            lista_opcoes_multiselect = ["Informações",
                                        "Composição",
                                        "Sobrevivência"]

            opcoes_multiselect = st.segmented_control("",
                                                      lista_opcoes_multiselect,
                                                      selection_mode="multi",
                                                      help="Opções adicionais")

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
        if lista_opcoes_multiselect[2] in opcoes_multiselect:
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
        opcoes_label1 = {f"Retorno total no periodo de {periodo_carteira} Anos": 1,
                         f"Menor retorno [mensal] no periodo":                   2,
                         f"Maior retorno [mensal] no periodo":                   3,
                         f"Média dos retornos [mensal] no período":              4}

        opcao_radio1 = st.radio("Opções interessantes para análise:",
                                list(opcoes_label1.keys()),
                                label_visibility="hidden",
                                index = 0)
        if not (opcoes_label1[opcao_radio1] == 1):
            janela_analise_ret = st.slider("# Período do retorno móvel [meses]", 2, 24, 6, 1)
        else:
            janela_analise_ret = 3

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
        opcoes_label2 = {f"Volatilidade total no período de {periodo_carteira} Anos": 1,
                         f"Menor volatilidade [mensal] no periodo":                   2,
                         f"Maior volatilidade [mensal] no periodo":                   3,
                         f"Média das volatilidades [mensal] no periodo":              4}

        opcao_radio2 = st.radio("Opções interessantes para análise:",
                                list(opcoes_label2.keys()),
                                label_visibility="hidden",
                                index=0)
        if not (opcoes_label2[opcao_radio2] == 1):
            janela_analise_vol = st.slider("# Período da volatilidade móvel [meses]", 2, 24, 6, 1)
        else:
            janela_analise_vol = 3
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
    if lista_opcoes_multiselect[0] in opcoes_multiselect:
        st.markdown("""
        ### Premissas básicas do modelo: 
        * Foi configurado um modelo **ARIMA + GARCH** para cada ativo que compõe a carteira;
        * A composição da carteira foi balanceada anualmente para manter o **_Asset Allocation_**;
        * Todos os retornos já estão considerados a **inflação no período**, que também teve um modelo **ARIMA + GARCH**;
        * Os dados de retorno foram obtidos e tratados através da **Comdinheiro**;
        * Para cada cenário no modelo foram realizadas **2000 simulações**;
            * Entenda cenário como: Um **período** de usufruto **atrelado** a uma **taxa** de retirada para cada tipo de **carteira**
            * Exemplo: **Cenário 1**
                * Período: 10 anos
                * Taxa: 3,50%
                * Carteira: Conservadora
                * Número de simulações: 2000
        * Análise de **Patrimônio Final** e **Drawdown**;
            * Dado um cenário, foi observado o **valor final do Patrimônio** em todas as simulações
            * Para o **Drawdown**, foi observado o **drawdown máximo** no **período** em cada uma das simulações
        * Análise de **Retorno** e **Volatilidade**.
            * Nas opções de **maior**, **menor** e **média** para os retornos e volatilidades, é possível analisar via **janelas móveis**
            * Para o **retorno total** foi realizado o cálculo do retorno real no período selecionado, assim como a volatilidade
        """)

    if lista_opcoes_multiselect[1] in opcoes_multiselect:

        df_carteiras = apresenta_carteiras()

        st.plotly_chart(desenha_treemap_formatado(df_carteiras, "Composição das Carteiras"))
