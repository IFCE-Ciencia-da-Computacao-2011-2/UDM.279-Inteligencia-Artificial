from busca import BuscaEmLargura
from busca import BuscaDeCustoUniforme
from busca import BuscaEmProfundidadeArvore, BuscaEmProfundidadeLimitada
from busca import BuscaDeAprofundamentoIterativo
from busca import BuscaEmProfunidadeGrafo

from busca import LimiteError, BuscaError

from problema_aspirador import ProblemaAspirador, EstadoAspirador
from problema_romenia import ProblemaRomenia

problema = ProblemaRomenia('Arad', 'Bucharest')

#sujo = EstadoAspirador(esquerdo_limpo=False, direito_limpo=False, localizado_no_esquerdo=True)
#problema = ProblemaAspirador(sujo)


metodos = [
    BuscaEmLargura(),
    #BuscaDeCustoUniforme(),
    BuscaEmProfundidadeArvore(),
    BuscaEmProfunidadeGrafo(),
    BuscaEmProfundidadeLimitada(2),
    BuscaDeAprofundamentoIterativo()
]

for metodo in metodos:
    print('#' * 30)
    print('#', metodo.__class__.__name__)
    print('#' * 30)
    
    try:
        metodo.buscar(problema).beautify()
    except RuntimeError as error:
        print('\033[0;31m', 'Error:', error, '\033[0m')
    except LimiteError as error:
        print('\033[1;33m', 'Error:', error, '\033[0m')
    except BuscaError as error:
        print('\033[1;33m', 'Error:', error, '\033[0m')

    print()