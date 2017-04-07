from problema import Problema, Acao, Estado

from sliding_puzzle.sliding_puzzle import SlidingPuzzle, SlidingMovement, InvalidMovement

class ProblemaSlidingPuzzle(Problema):

    def __init__(self, sliding_puzzle, heuristica):
        super(ProblemaSlidingPuzzle, self).__init__(sliding_puzzle, [])
        objetivo = SlidingPuzzle(sliding_puzzle.width, sliding_puzzle.height)

        self.estados_objetivos = [objetivo]
        self.estado_objetivo_array = objetivo.asarray
        self._heuristica = heuristica

    def acoes(self, estado):
        custo = 1
        
        acoes = []
        for movimento in estado.possible_movements:
            copia = estado.copy()
            copia.move(movimento)
            
            acoes.append(Acao(estado, copia, custo))
        
        return acoes

    def heuristica(self, estado):
        return self._heuristica.heuristica(self, estado)

class HeuristicaErrados(object):
    
    def heuristica(self, problema, estado):
        heuristica = 0
        for peca, peca_correta in zip(estado.asarray, problema.estado_objetivo_array):
            if peca != peca_correta:
                heuristica += 1

        return heuristica
    
class HeuristicaDistanciaQuarteirao(object):
    
    def heuristica(self, problema, estado):
        heuristica = 0
        
        for linha in range(estado.height):
            for coluna in range(estado.width):
                coluna_correta, linha_correta = self._posicao_correta(estado.map[linha][coluna], problema.estado_inicial.width)
                heuristica += abs(linha - linha_correta) + abs(coluna - coluna_correta)
        
        return heuristica
    
    def _posicao_correta(self, peca, largura):
        y = int(peca / largura)
        x = peca - y * largura
        
        return (x, y)
