from src.function import *


def main():

    algorithm = input("\n Escolha o Algoritmo: \n 1) A_Estrela \t 2) Profundidade\t 3) Largura\n ")
    items = input("\n\nEntre com uma sequencia numerica separada por virgula, entre 0 e 9.\n 0 - marca o quadro vazio\n ")
    
    read(items)

    function = choose_algorithm[algorithm]
    frontier = function(initial_state)

    backtrace()


choose_algorithm = {
    '1': ast,
    '2': dfs,
    '3': bfs
}

if __name__ == '__main__':
    main()
