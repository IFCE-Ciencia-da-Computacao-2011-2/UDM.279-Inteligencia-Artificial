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


puzzle = SlidingPuzzle(4, 4)

# 28 passos
#[
#    [5, 6, 0],
#    [8, 7, 1],
#    [2, 4, 3],
#]

# 28 passos
#[[8, 3, 7], [1, 4, 6], [0, 5, 2]

#puzzle.map = [[5, 1, 0], [2, 3, 8], [6, 4, 7]]
#puzzle.position = (2, 0)

movimentos = shuffle(puzzle, 30)

print(puzzle)
#print(movimentos)

metodos = [
    #BuscaEmLargura(),
    #BuscaDeCustoUniforme(),
    #BuscaEmProfundidadeArvore(),
    #BuscaEmProfunidadeGrafo(),
    #BuscaEmProfundidadeLimitada(15),
    #BuscaDeAprofundamentoIterativo(),
    BuscaAStar()
]

for metodo in metodos:
    print('#' * 30)
    print('#', metodo.__class__.__name__)
    print('#' * 30)
    
    try:
        problema = ProblemaSlidingPuzzle(puzzle.copy(), HeuristicaDistanciaQuarteirao())
        metodo.buscar(problema).beautify()
        
        problema = ProblemaSlidingPuzzle(puzzle.copy(), HeuristicaErrados())
        metodo.buscar(problema).beautify()
    except RuntimeError as error:
        print('\033[0;31m', 'Error:', error, '\033[0m')
    except LimiteError as error:
        print('\033[1;33m', 'Error:', error, '\033[0m')
    except BuscaError as error:
        print('\033[1;33m', 'Error:', error, '\033[0m')

    print()

