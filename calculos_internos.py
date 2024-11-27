import pandas as pd

# Função para o cálculo do Drawdown
def calcula_drawdown(dataset):
    retornos = dataset.cummax()

    drawdowns = dataset / retornos - 1
    drawdown_max = drawdowns.min()
    return drawdowns, drawdown_max

# Função para o cálculo dos retornos
def calcula_retornos(dados_completos_retornos, periodo_carteira, nomes_carteiras, periodo_movel,opcao):
    retornos_totais = pd.DataFrame(columns=["Conservadora", "Moderada", "Arrojada", "Agressiva"])
    if opcao == 3:
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
    elif opcao == 1:
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
    if opcao == 3:
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

    elif opcao == 1:
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
