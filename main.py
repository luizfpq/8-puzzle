from src.funcoes import *


def main():

    algoritmo = input("\n Escolha o Algoritmo: \n 1) A_Estrela \t 2) Profundidade\t 3) Largura\n ")
    quadro = input("\n\nEntre com uma sequencia numerica separada por virgula, entre 0 e 8.\n 0 - marca o quadro vazio\n ")
    
    read(quadro)

    function = escolhe_algoritmo[algoritmo]
    inicial = timeit.default_timer()

    fronteira = function(estado_inicial)

    final = timeit.default_timer()

    escreve_arquivo(fronteira, final-inicial)


escolhe_algoritmo = {
    '1': a_estrela,
    '2': bep,
    '3': bel
}

if __name__ == '__main__':
    main()
