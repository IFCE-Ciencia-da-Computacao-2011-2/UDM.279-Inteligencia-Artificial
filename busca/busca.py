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
                    
        raise Exception("Caminho não encontrado")

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
        borda = [no] # https://docs.python.org/3.6/library/heapq.html
        explorado = []
        
        while borda:
            no = borda.pop(0)
            if problema.testar_objetivo(no.estado):
                return Solucao.gerar(no)
            explorado.append(no.estado)
            
            for acao in problema.acoes(no.estado):
                filho = self.gerarNo(no, acao)
                
                if filho.estado not in explorado or filho not in borda:
                    borda.append(filho)
                # senão se (filho.ESTADO) está na borda com o maior CUSTO-DE-CAMINHO então
                #else if filho.estado not in explorado or filho not in borda:
                #    substituir aquele nó borda por filho
                #    
    
        raise Exception("Caminho não encontrado")

class BuscaEmProfundidade(Busca):
    """
    função BUSCA-EM-PROFUNDIDADE-LIMITADA(problema, limite) retorna uma solução ou falha/corte
        retornar BPL-RECURSIVA(CRIAR-NÓ(problema, ESTADO-INICIAL), problema, limite)
    
    função BPL-RECURSIVA(nó, problema, limite) retorna uma solução ou falha/corte
        se problema. TESTAR-OBJETIVO (nó.ESTADO) então, retorna SOLUÇÃO (nó)
        se não se limite = 0 então retorna cortesenão
            corte_ocorreu? ← falso para cada ação no problema.AÇÕES(nó.ESTADO) faça
                filho ← NÓ-FILHO (problema, nó, ação)
                resultado ← BPL-RECURSIVA (criança, problema limite − 1)
                se resultado = corte então corte_ocorreu? ← verdadeiro
                senão se resultado ≠ falha então retorna resultado
            se corte_ocorreu? então retorna corte senão retorna falha
    """
    def __init__(self):
        self.limite = 1000000

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
    pass

class BuscaBidirecional(Busca):
    """Não vou implementar"""
    pass

