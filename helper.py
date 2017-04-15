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

def grafico_desvio_padrao(analise):
    means = analise.mean()
    errors = analise.std()

    fig, ax = plt.subplots()
    means.plot(title='Média de tempo (em $segundos$)', yerr=errors, ax=ax, kind='bar')
