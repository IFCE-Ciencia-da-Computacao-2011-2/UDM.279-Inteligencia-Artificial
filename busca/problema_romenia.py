from problema import Problema, Acao

class ProblemaRomenia(Problema):
    mapa = {
        'Arad': {'Zerind':75, 'Sibiu':140, 'Timisoara':118},
        'Bucharest': {'Urziceni':85, 'Pitesti':101, 'Giurgiu':90, 'Fagaras':211},
        'Craiova': {'Drobeta':120, 'Rimnicu':146, 'Pitesti':138},
        'Drobeta': {'Mehadia':75, 'Craiova':120},
        'Eforie': {'Hirsova':86},
        'Fagaras': {'Sibiu':99, 'Bucharest':211},
        'Giurgiu': {'Bucharest':89},
        'Hirsova': {'Urziceni':98, 'Eforie':86},
        'Iasi': {'Vaslui':92, 'Neamt':87},
        'Lugoj': {'Timisoara':111, 'Mehadia':70},
        'Mehadia': {'Lugoj':70, 'Drobeta':75},
        'Neamt': {'Iasi':87},
        'Oradea': {'Zerind':71, 'Sibiu':151},
        'Pitesti': {'Rimnicu':97, 'Bucharest':101, 'Craiova':138},
        'Rimnicu': {'Sibiu':80, 'Pitesti':97, 'Craiova':120},
        'Sibiu': {'Arad':140, 'Oradea':151, 'Fagaras':99, 'Rimnicu':80},
        'Timisoara': {'Arad':118, 'Lugoj':111},
        'Urziceni': {'Vaslui':142, 'Bucharest':85, 'Hirsova':98},
        'Vaslui': {'Urziceni':142, 'Iasi':92},
        'Zerind': {'Oradea':71, 'Arad':75}
    }
    
    heuristica_bucharest = {
        'Arad': 366,
        'Bucharest': 0,
        'Craiova': 160,
        'Dobreta': 242,
        'Eforie': 161,
        'Fagaras': 178,
        'Giurgiu': 77,
        'Hirsova': 151,
        'Iasi': 226,
        'Lugoj': 244,
        'Mehadia': 241,
        'Neamt': 234,
        'Oradea': 380,
        'Pitesti': 98,
        'Rimnicu': 193,
        'Sibiu': 253,
        'Timisoara': 329,
        'Urziceni': 80,
        'Vaslui': 199,
        'Zerind': 374
    }

    def acoes(self, estado):
        return self.gerarAcoes(estado)

    def gerarAcoes(self, estado):
        return [Acao(estado, k, v) for k, v in ProblemaRomenia.mapa[estado].items()]
    
    def heuristica(self, estado):
        """
        Heurística exclusivamente para Romênia
        """
        return self.heuristica_bucharest[estado]