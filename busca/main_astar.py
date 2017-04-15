from sliding_puzzle.sliding_puzzle import SlidingMovement, SlidingPuzzle
from sliding_puzzle.problema_sliding_puzzle import ProblemaSlidingPuzzle, HeuristicaDistanciaQuarteirao, HeuristicaErrados

from busca import BuscaEmLargura
from busca import BuscaDeCustoUniforme
from busca import BuscaEmProfundidadeArvore, BuscaEmProfundidadeLimitada
from busca import BuscaDeAprofundamentoIterativo
from busca import BuscaEmProfunidadeGrafo
from busca_astar import BuscaAStar

from busca import LimiteError, BuscaError

import random
import time


def shuffle(puzzle, n=50):
    realized_movements = []

    last_movement = SlidingMovement.FROM_BOTTOM
    while n > 0:
        movement = random.choice(puzzle.possible_movements)
        if movement == ~last_movement:
            continue

        puzzle.move(movement)

        last_movement = movement
        realized_movements.append(movement)
        n -= 1

    return realized_movements



def executar(puzzle, metodo, heuristica):
    tempo_inicial = time.process_time()

    problema = ProblemaSlidingPuzzle(puzzle.copy(), heuristica)
    resultado = metodo.buscar(problema)
    #resultado.beautify()

    tempo_final = time.process_time()

    return tempo_final - tempo_inicial, len(resultado.caminho)




metodos = [
    (BuscaEmLargura(), None, 'Largura'),# Muito lenta 3x3
    #(BuscaDeCustoUniforme(), heuristica),
    #(BuscaEmProfundidadeArvore(), heuristica),
    (BuscaEmProfunidadeGrafo(), None, 'Profundidade (grafo)'),
    (BuscaEmProfundidadeLimitada(15), None, 'Profundidade limitada - 15'),# 2x2 limitada a 15 # 2x3 limitada a 20
    (BuscaDeAprofundamentoIterativo(), None, 'Aprofundamento Interativo'), #Muito lento 2x3
    (BuscaAStar(), HeuristicaDistanciaQuarteirao(), 'A* - Distância quarteirão'),
    (BuscaAStar(), HeuristicaErrados(), 'A* - Nº errados')
]


TOTAL_TENTATIVAS = 10
tamanhos = (2, 2), (2, 3)#, (3, 3)#, (3, 4)#, (4, 4), (4, 5), (5, 5)
#tamanhos = (2, 2), (2, 3), (3, 3)#, (3, 4)#, (4, 4), (4, 5), (5, 5)
#tamanhos = (3, 3), (3, 4), (4, 4), (4, 5), (5, 5)

resultado_geral = {}
for tamanho in tamanhos:

    puzzle = SlidingPuzzle(tamanho[0], tamanho[1])
    movimentos = shuffle(puzzle, 150)

    print('Tamanho: ', tamanho)
    print(puzzle)
    #print(movimentos)

    resultado = {}

    for metodo, heuristica, titulo in metodos:
        print(metodo.__class__.__name__)
        resultados = []

        for i in range(TOTAL_TENTATIVAS):
            print(i)

            try:
                tempo, passos = executar(puzzle, metodo, heuristica)
                resultados.append({
                    'tempo': tempo,
                    'passos': passos
                })

            except Exception as error:
                resultados.append({'tempo': -1, 'passos': -1})
                print(error)
                break
        print()
        resultado[titulo] = resultados

    resultado_geral[str(tamanho)] = resultado

import json
print(json.dumps(resultado_geral))
#print(resultado_geral)
