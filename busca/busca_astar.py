from busca import Busca
from problema import Solucao

import heapq

class PriorityQueue:
    def __init__(self):
        self.elements = []
    
    def empty(self):
        return len(self.elements) == 0
    
    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))
    
    def get(self):
        return heapq.heappop(self.elements)[1]
    
class BuscaAStar(Busca):
    """
    Baseado em http://www.redblobgames.com/pathfinding/a-star/implementation.html
    """    
    def buscar(self, problema):
        no = self.gerarNoInicial(problema.estado_inicial)

        borda = PriorityQueue()
        borda.put(no, 0)

        menor_custo_origem = {problema.estado_inicial: 0}

        while not borda.empty():
            no = borda.get()

            if problema.testar_objetivo(no.estado):
                return Solucao.gerar(no)

            for acao in problema.acoes(no.estado):
                filho = self.gerarNo(no, acao)
                novo_custo = menor_custo_origem[no.estado] + problema.custo_do_passo(acao)

                if filho.estado not in menor_custo_origem or novo_custo < menor_custo_origem[filho.estado]:
                    menor_custo_origem[filho.estado] = novo_custo
                    prioridade = novo_custo + problema.heuristica(filho.estado)
                    borda.put(filho, prioridade)

        raise BuscaError("Caminho não encontrado")


if __name__ == '__main__':
    from problema_romenia import ProblemaRomenia

    problema = ProblemaRomenia('Arad', 'Bucharest')                           
    BuscaAStar().buscar(problema).beautify()
