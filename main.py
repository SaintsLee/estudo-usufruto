import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(layout="wide", page_title="Estudo Usufruto",page_icon = "portfel_logo.ico")

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

@st.cache_data
def load_data():
    # Substitua pelo seu método de carregamento de dados, como pd.read_csv ou outro
    dados_completos = pd.read_parquet("dados_completos_brotli.parquet")

    dados_completos_retornos = pd.read_parquet("dados_completos__retornos_brotli.parquet")

    return dados_completos, dados_completos_retornos

dados_completos, dados_completos_retornos = load_data()

st.title("Análise do patrimônio final")



# Dividir em duas colunas
col1, col2 = st.columns(2)

# Exibir sliders em cada coluna
with col1:
    periodo_carteira = st.slider("# Período para a carteira", 10, 30, 10, 2)
with col2:
    taxa_carteira = st.slider("# Taxa para a carteira", 2.5, 7.0, 2.5, 0.5)

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

st.markdown(
    """
    <style>
    .stSlider label {
        font-size: 18px;  /* Altere para o tamanho desejado */
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

def desenha_box_formatado(dataset, titulo_y, titulo_x):
    fig = px.box(dataset, color_discrete_sequence=["black"])

    fig.update_layout(xaxis_title=titulo_x, yaxis_title=titulo_y, showlegend=False, height=650, plot_bgcolor='white',
                      xaxis=dict(
                          tickfont=dict(size=18, color = "black"),  # Tamanho da fonte para os números no eixo X
                      ),
                      yaxis=dict(
                          tickfont=dict(size=18, color = "black"),  # Tamanho da fonte para os números no eixo Y

                      ),
                      xaxis_title_font=dict(size=18, color = "black"),  # Tamanho da fonte do eixo X
                      yaxis_title_font=dict(size=18, color = "black"),  # Tamanho da fonte do eixo Y
                      )

    # Personalizar o grid
    fig.update_xaxes(
        showgrid=False,  # Exibir a grade no eixo X
        gridcolor='lightgrey',  # Cor das linhas da grade
        gridwidth=0.5,  # Largura das linhas da grade
        zeroline=True,  # Exibir linha de zero (para eixo X)
        zerolinecolor='black',  # Cor da linha de zero
        zerolinewidth=1,  # Largura da linha de zero
        showline=True,  # Exibir a linha do eixo
        linecolor='black',  # Cor da linha do eixo
        linewidth=1,  # Largura da linha do eixo,
        griddash='dot',
        layer="below traces"  # Coloca o Grid atrás
    )

    fig.update_yaxes(
        showgrid=True,  # Exibir a grade no eixo Y
        gridcolor='lightgrey',  # Cor das linhas da grade
        gridwidth=0.5,  # Largura das linhas da grade
        zeroline=True,  # Exibir linha de zero (para eixo Y)
        zerolinecolor='black',  # Cor da linha de zero
        zerolinewidth=1,  # Largura da linha de zero
        showline=True,  # Exibir a linha do eixo
        linecolor='black',  # Cor da linha do eixo
        linewidth=1,  # Largura da linha do eixo
        griddash='dot',
        layer="below traces"  # Coloca o Grid atrás
    )

    # Personalização das cores
    # "#392B84"
    fig.update_traces(
        marker_color="Red",  # Cor da caixa
        line_color="#272727",  # Cor da linha da borda
        fillcolor="#6E6E6E",
        marker_size=5,  # Tamanho dos pontos
        marker_opacity=1  # Opacidade dos pontos
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

carteiras_pl = dados_completos[(dados_completos["Taxa"] == "{:.2f}%".format(taxa_carteira)) &
                               (dados_completos["Periodo"] == "{} Anos".format(periodo_carteira))].copy()

cap_inicial = 3000000
carteiras_pl_tratada = carteiras_pl.drop(columns=["Taxa", "Periodo"])/cap_inicial*100

box_plot_1 = desenha_box_formatado(carteiras_pl_tratada,"Patrimônio Final [%]","Carteiras")

draw_downs_totais = pd.DataFrame(columns=["Conservadora", "Moderada", "Arrojada", "Agressiva"])
for i in range(len(nomes_carteiras)):
    dd, mdd = calcula_drawdown(dados_completos_retornos[(dados_completos_retornos["Periodo"] == "{} Anos".format(periodo_carteira))
                                     & (dados_completos_retornos["Carteira"] == nomes_carteiras[i].split()[0])].drop(columns = ["Carteira","Periodo"])
                              )
    draw_downs_totais[nomes_carteiras[i].split()[0]] = mdd

box_plot_2 = desenha_box_formatado(draw_downs_totais*100, "Drawdown [%]", "Carteiras")

# Exibir gráficos em cada coluna
with col1:
    st.markdown("#### Disperssão do patrimônio")
    st.write("Taxa: {:.2f}%".format(taxa_carteira))
    st.plotly_chart(box_plot_1, use_container_width=False)

with col2:
    st.markdown("#### Disperssão do Drawdown")
    st.write("Taxa: {:.2f}% e Período: {} Anos".format(taxa_carteira,periodo_carteira))
    st.plotly_chart(box_plot_2, use_container_width=False)
    #st.plotly_chart(fig2, use_container_width=True)
