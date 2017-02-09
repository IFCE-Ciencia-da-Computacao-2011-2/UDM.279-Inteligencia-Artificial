class Problema(object):
    """
    Um problema pode ser definido formalmente por cinco componentes:
     - Estado inicial
     - Ações possíveis
     - Modelo de transição, implementado como ``self.acao_resultado(estado, acao)``
       Caminho = Uma sequência de estados conectados por uma sequência de ações
     - Teste de objetivo, já implementado genericamente como ``self.testar_objetivo(estado)``
     - Custo de caminho.
       Custo do passo de um estado a outro por intermédio de uma ação
       está implementado em ``self.custo_do_passo``

    Espaço de estados = Estado inicial, as ações possíveis e o modelo de transição
    
    Uma solução para um problema é um caminho desde o estado inicial até um estado objetivo.
    A qualidade da solução é medida pela função de custo de caminho, e uma solução ótima tem
    o menor custo de caminho entre todas as soluções.
    """
    def __init__(self, estado_inicial, estados_objetivos):
        self.estado_inicial = estado_inicial
        self.acoes_possiveis = []
        self.estados_objetivos = estados_objetivos
    
    def acao_resultado(self, estado, acao):
        """
        Modelo de transição. Informa qual estado é alcançável ao realizar
        uma acao em um estado::
        
            RESULTADO(Em(Arad), Ir(Zerind)) = Em(Zerind)
        
        :param Acao acao: Ação a ser realizada em um estado
        :param Estado estado: Um estado corresponde a uma configuração do mundo
        """
        pass

    def acoes(self, estado):
        """
        Conjunto de ações possíveis de chegar a partir de estado
        """
        raise NotImplementedError

    def testar_objetivo(self, estado):
        """
        Verifica se um estado pertence a um dos objetivos estabelecidos
        """
        return estado in self.estados_objetivos

    def custo_do_passo(self, acao):
        """
        O _custo do passo_ de adotar a ação _s_ para alcançar o estado _s'_ é denotado por
        ``c(s, a, s')``
        
        :param list[(Estado, Acao)] caminho: lista de tuplas de (Estado, Acao)
        """
        return acao.custo

class Acao(object):
    """
    A ação de ir de um estado de origem para um de destino possui um custo.
    O custo é definido em ``Problema.custo_do_passo``
    """
    def __init__(self, origem, destino, custo=1):
        self.origem = origem
        self.destino = destino
        self.custo = custo # Custo de caminho

class No(object):
    """
    Um nó é uma anotação da estrutura de dados usada para representar a árvore de busca
    
    :param estado: o estado no espaço de estado a que o nó corresponde;
    :param No pai: o nó na árvore de busca que gerou esse nó;
    :param acao: a ação que foi aplicada ao pai para gerar o nó;
                 ``None`` quando o nó é o nó inicial
    :param int custo: o custo do caminho, tradicionalmente denotado por g(n), do caminho 
                      do estado inicial até o nó, indicado pelos ponteiros para os pais.
    """
    def __init__(self, pai, acao=None, destino=None):
        self.pai = pai
        self.acao = acao
        self.estado = destino
        
        self.custo = self.custo_do_passo(pai, acao) if acao is not None else 0
        
    def custo_do_passo(self, pai, acao):
        custo_pai = self.pai.custo if self.pai is not None else 0
        return custo_pai + acao.custo

    def __lt__(self, other):
        return self.custo < other.custo

class Estado(object):
    """
    Um estado corresponde a uma configuração do mundo
    """
    pass

class Solucao(object):
    """
    Conjunto de nós que representam a solução de um problema que vai
    de um estado inicial a um final
    """
    @staticmethod
    def gerar(no_destino):
        caminho = []
        no = no_destino
        while no.pai is not None:
            acao = no.acao
            caminho.append((acao.origem, acao.custo, acao.destino))
            no = no.pai

        return Solucao(caminho[::-1], no_destino)

    def __init__(self, caminho, no_destino):
        self.caminho = caminho
        self.no_destino = no_destino

    def __repr__(self):
        return self.caminho.__repr__()
    
    def beautify(self):
        print(' - Caminho')
        caminho = str(self.caminho[0][0])
        
        no = self.caminho
        for passo in self.caminho:
            caminho += ' -> ' + str(passo[2])
        
        print(caminho)

        print(' - Custo do caminho:', self.no_destino.custo)