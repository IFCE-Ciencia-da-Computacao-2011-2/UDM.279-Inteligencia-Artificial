from problema import Problema, Acao, Estado


class EstadoAspirador(Estado):

    def __init__(self, esquerdo_limpo=False, direito_limpo=False, localizado_no_esquerdo=True):
        self.esquerdo_limpo = esquerdo_limpo
        self.direito_limpo = direito_limpo
        self.localizado_no_esquerdo = localizado_no_esquerdo

    @property
    def localizado_no_direito(self):
        return not self.localizado_no_esquerdo

    def __eq__(self, other):
        return self.esquerdo_limpo == other.esquerdo_limpo \
           and self.direito_limpo == other.direito_limpo \
           and self.localizado_no_esquerdo == other.localizado_no_esquerdo

    def __repr__(self):
        data = '['
        if self.localizado_no_esquerdo:
            data += 'A'
        if not self.esquerdo_limpo:
            data += '*'
        data += ', '
        if self.localizado_no_direito:
            data += 'A'
        if not self.direito_limpo:
            data += '*'
        data += ']'
        
        return data

class ProblemaAspirador(Problema):

    def __init__(self, estado_inicial):
        super(ProblemaAspirador, self).__init__(estado_inicial, [])
        self.estados_objetivos = [
            EstadoAspirador(esquerdo_limpo=True, direito_limpo=True, localizado_no_esquerdo=True),
            EstadoAspirador(esquerdo_limpo=True, direito_limpo=True, localizado_no_esquerdo=False),
        ]

    def acoes(self, estado):
        fazer_nada = Acao(estado, estado, 1)
        
        estado_ir_para_outro_lado = EstadoAspirador(
            esquerdo_limpo=estado.esquerdo_limpo,
            direito_limpo=estado.direito_limpo,
            localizado_no_esquerdo=not estado.localizado_no_esquerdo
        )
        ir_para_outro_lado = Acao(estado, estado_ir_para_outro_lado, 1)
        
        estado_limpar = EstadoAspirador(
            esquerdo_limpo= True if estado.localizado_no_esquerdo else estado.esquerdo_limpo,
            direito_limpo= True if estado.localizado_no_direito else estado.direito_limpo,
            localizado_no_esquerdo=estado.localizado_no_esquerdo
        )
        limpar = Acao(estado, estado_limpar, 1)
        
        return fazer_nada, ir_para_outro_lado, limpar
