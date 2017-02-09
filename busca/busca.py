from heapq import heappush, heappop

from problema import No
from problema import Solucao


class Busca(object):
    def buscar(self):
        raise NotImplementedError

    def gerarNoInicial(self, estado):
        return No(None, None, estado)

    def gerarNo(self, estado, acao):
        return No(estado, acao, acao.destino)
        
class BuscaEmLargura(Busca):
    """
    função BUSCA-EM-LARGURA(problema) retorna uma solução ou falha
        nó ← um nó com ESTADO = problema.ESTADO-INICIAL, CUSTO-DE-CAMINHO = 0
        se problema.TESTE-DE-OBJETIVO(nó.ESTADO) senão retorne SOLUÇÃO(nó),
        borda ← uma fila FIFO com nó como elemento único
        explorado ← conjunto vazio
        repita
            se VAZIO?(borda), então retorne falha
            nó ← POP(borda) / * escolhe o nó mais raso na borda */
            adicione nó.ESTADO para explorado
            para cada ação em problema.AÇÕES(nó.ESTADO) faça
                filho ← NÓ-FILHO(problema, nó, ação),
                se (filho.ESTADO) não está em explorado ou borda então
                    se problema.TESTE-DE-OBJETIVO(filho.ESTADO) então
                        retorne SOLUÇÃO(filho)
                    borda ← INSIRA(filho, borda)
    """

    def buscar(self, problema):
        no = self.gerarNoInicial(problema.estado_inicial)
        borda = [no]
        explorado = []
        
        while borda:
            no = borda.pop(0)
            explorado.append(no.estado)
            
            for acao in problema.acoes(no.estado):
                filho = self.gerarNo(no, acao)

                if filho.estado not in explorado or filho not in borda:
                    if problema.testar_objetivo(filho.estado):
                        return Solucao.gerar(filho)

                    borda.append(filho)
                    
        raise BuscaError("Caminho não encontrado")

class BuscaDeCustoUniforme(Busca):
    """
    função BUSCA-DE-CUSTO-UNIFORME(problema) retorna uma solução ou falha
        nó ← um nó com ESTADO = problema.ESTADO-INICIAL, CUSTO-DE-CAMINHO = 0
        borda ← fila de prioridade ordenada pelo CUSTO-DE-CAMINHO, com nó como elemento único
        explorado ← um conjunto vazio
        repita
            se VAZIO?(borda), então retornar falha
            nó ← POP(borda) / * escolhe o nó de menor custo na borda */
            se problema.TESTE-OBJETIVO(nó.ESTADO) então retornar SOLUÇÃO(nó)
            adicionar (nó.ESTADO) para explorado
            para cada ação em problema. AÇÕES(nó.ESTADO) faça
                filho ← NÓ-FILHO (problema, nó, ação)
                se (filho.ESTADO) não está na borda ou explorado então
                    borda ← INSIRA (filho, borda)
                senão se (filho.ESTADO) está na borda com o maior CUSTO-DE-CAMINHO então
                    substituir aquele nó borda por filho
    """

    def buscar(self, problema):
        no = self.gerarNoInicial(problema.estado_inicial)
        borda = [] # https://docs.python.org/3.6/library/heapq.html
        explorado = []
        
        heappush(borda, (no.custo, no))
        counter = 5
        while counter > 0:#borda:
            counter -= 1
            no = heappop(borda)[1]
            print(borda)

            if problema.testar_objetivo(no.estado):
                return Solucao.gerar(no)

            explorado.append(no.estado)
            
            for acao in problema.acoes(no.estado):
                filho = self.gerarNo(no, acao)
                
                if filho.estado not in explorado or filho not in borda:
                    heappush(borda, (filho.custo, filho))
                    continue

                index = posicao_na_borda_com_custo_maior(borda, filho)
                #if index >= 0:
                #    borda
                #    substituir aquele nó borda por filho
    
        raise BuscaError("Caminho não encontrado")

    def posicao_na_borda_com_custo_maior(self, borda, elemento):
        for index, elemento in enumerate(borda):
            if elemento[1] == elemento and elemento[0] > elemento.custo:
                return index
        
        return -1
            
class LimiteError(Exception):
    pass

class BuscaError(Exception):
    pass

from sys import getrecursionlimit

class BuscaEmProfundidade(Busca):
    """
    função BUSCA-EM-PROFUNDIDADE-LIMITADA(problema, limite) retorna uma solução ou falha/corte
        retornar BPL-RECURSIVA(CRIAR-NÓ(problema, ESTADO-INICIAL), problema, limite)
    
    função BPL-RECURSIVA(nó, problema, limite) retorna uma solução ou falha/corte
        se problema.TESTAR-OBJETIVO(nó.ESTADO) então, retorna SOLUÇÃO (nó)
        se não se limite = 0 então retorna corte
        senão
            corte_ocorreu? ← falso
            para cada ação no problema.AÇÕES(nó.ESTADO) faça
                filho ← NÓ-FILHO(problema, nó, ação)
                resultado ← BPL-RECURSIVA(filho, problema, limite − 1)
                se resultado = corte então corte_ocorreu? ← verdadeiro
                senão se resultado ≠ falha então retorna resultado
            se corte_ocorreu? então retorna corte senão retorna falha
    """
    def __init__(self):
        self.limite = getrecursionlimit() * 4 / 5

    def buscar(self, problema):
        no = self.gerarNoInicial(problema.estado_inicial)
        return self.busca_recursiva(no, problema, self.limite)

    def busca_recursiva(self, no, problema, limite):
        if problema.testar_objetivo(no.estado):
            return Solucao.gerar(no)

        if limite == 0:
            raise LimiteError("Limite atingido. Corte realizado")
            
        for acao in problema.acoes(no.estado):
            filho = self.gerarNo(no, acao)
            
            resultado = None
            try:
                resultado = self.busca_recursiva(filho, problema, limite - 1)
                return resultado
            except LimiteError:
                corte_ocorreu = True

        if corte_ocorreu:
            raise LimiteError("Limite atingido. Corte realizado")
        else:
            raise BuscaError("Caminho não encontrado")

class BuscaEmProfundidadeLimitada(BuscaEmProfundidade):

    def __init__(self, limite):
        self.limite = limite

class BuscaDeAprofundamentoIterativo(Busca):
    """
    função BUSCA-DE-APROFUNDAMENTO-ITERATIVO(problema) retorna uma solução ou falha
        para profundidade = 0 até ∞ faça
        resultado ← BUSCA-EM-PROFUNDIDADE-LIMITADA(problema, profundidade)
        se resultado ≠ corte então retornar resultado
    """
    def buscar(self, problema):
        limite = 0
        while True:
            try:
                return BuscaEmProfundidadeLimitada(limite).buscar(problema)
            except:
                limite += 1
        

class BuscaBidirecional(Busca):
    """Não vou implementar"""
    pass

