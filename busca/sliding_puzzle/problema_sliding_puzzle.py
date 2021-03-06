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
                peca = estado.map[linha][coluna]
                largura = problema.estado_inicial.width
                
                posicao_correta = self._posicao_correta(peca, largura)
                posicao = (coluna, linha)
                heuristica += self._distancia_quarteirao(posicao, posicao_correta)
        
        return heuristica

    def _posicao_correta(self, peca, largura):
        y = int(peca / largura)
        x = peca - y * largura
        
        return (x, y)

    def _distancia_quarteirao(self, posicao_atual, posicao_correta):
        x0, y0 = posicao_atual
        x1, y1 = posicao_correta
        return abs(x0 - x1) + abs(y0 - y1)
