import pandas as pd
import json
import matplotlib.pyplot as plt

def carregar_json(arquivo):
    with open(arquivo) as data_file:    
        return json.load(data_file)
    
def processar_resultados(data):
    resultados_dataframe = pd.DataFrame()
    passos_dataframe = pd.DataFrame()

    for algoritmo, execucoes in data.items():
        tempos = list(map(lambda execucao: execucao['tempo'], execucoes))
        tempos.sort()
        tempos_filtrado = tempos[1:-1]
        
        tempos = pd.Series(tempos_filtrado, name=algoritmo)
        resultados_dataframe[algoritmo] = tempos
        passos_dataframe[algoritmo] = [execucoes[0]['passos']]

    return resultados_dataframe, passos_dataframe


def processar_resultados_crescente(data):
    resultados_dataframe = pd.DataFrame()

    passos = list(map(lambda n: int(n), list(data.keys())))
    passos.sort()
    for total_passos in passos:
        total_passos = str(total_passos)
        tempos = data[total_passos]
        tempos.sort()
        tempos_filtrado = tempos[1:-1]
        
        tempos = pd.Series(tempos_filtrado, name=total_passos)
        resultados_dataframe[total_passos] = tempos

    return resultados_dataframe


def grafico_desvio_padrao(analise, kind='barh', title='Média de tempo (em $segundos$)', figsize=(6, 4)):
    means = analise.mean()
    errors = analise.std()

    fig, ax = plt.subplots()
    return means.plot(title=title, xerr=errors, ax=ax, kind=kind, figsize=figsize)
