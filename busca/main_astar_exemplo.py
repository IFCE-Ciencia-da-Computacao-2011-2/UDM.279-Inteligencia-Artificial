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
import json


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

tamanho = [3, 3]

#heuristica = resultado.beautify()
heuristica = HeuristicaDistanciaQuarteirao()
puzzle = SlidingPuzzle(tamanho[0], tamanho[1])
movimentos = shuffle(puzzle, 150)

problema = ProblemaSlidingPuzzle(puzzle.copy(), heuristica)
resultado = BuscaAStar().buscar(problema)
resultado.beautify()
