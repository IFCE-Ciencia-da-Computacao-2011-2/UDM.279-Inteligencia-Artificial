from sliding_puzzle.sliding_puzzle import SlidingMovement, SlidingPuzzle
from sliding_puzzle.problema_sliding_puzzle import ProblemaSlidingPuzzle, HeuristicaDistanciaQuarteirao, HeuristicaErrados

from busca_astar import BuscaAStar
import numpy as np
import time
import json


def executar(puzzle, metodo, heuristica):
    tempo_inicial = time.process_time()

    problema = ProblemaSlidingPuzzle(puzzle.copy(), heuristica)
    resultado = metodo.buscar(problema)
    #resultado.beautify()

    tempo_final = time.process_time()

    return tempo_final - tempo_inicial, len(resultado.caminho)



TOTAL_TENTATIVAS = 10

mapa = np.asarray([
    [5, 7, 11],
    [4, 10, 2],
    [3, 1, 0],
    [6, 8, 9]
], dtype='uint8')

puzzle = SlidingPuzzle(len(mapa[0]), len(mapa), map=mapa)
puzzle.position = (2, 2)

problema = ProblemaSlidingPuzzle(puzzle.copy(), HeuristicaDistanciaQuarteirao())
resultado = BuscaAStar().buscar(problema)

resultado_geral = {}
for index, acao in enumerate(reversed(resultado.caminho)):
    puzzle = acao[0]

    resultados = []

    print("Nº passos para solucionar:", index)
    for i in range(TOTAL_TENTATIVAS):
        print(i)

        tempo, passos = executar(puzzle.copy(), BuscaAStar(), HeuristicaDistanciaQuarteirao())
        resultados.append(tempo)

    resultado_geral[str(index)] = resultados
    print(json.dumps(resultado_geral))

print(json.dumps(resultado_geral))