import plotly.express as px

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
