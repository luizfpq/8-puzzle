import argparse
import timeit
import resource
from collections import deque
from src.estado import Estado
from heapq import heappush, heappop, heapify
import itertools

estado_esperado = [1, 2, 3, 4, 5, 6, 7, 8, 0]
no_esperado = Estado
estado_inicial = list()
tamanho_quadro = 0
lado_quadro = 0

nos_expandidos = 0
profundidade_maxima = 0
tamanho_max_fronteira = 0

movimentos = list()
custos = set()

# Busca em Amplitude
# Breadth-First Search - BFS
# https://pt.wikipedia.org/wiki/Busca_em_largura
def bel(estado_inicial):

    global tamanho_max_fronteira, no_esperado, profundidade_maxima

    explorado, fila = set(), deque([Estado(estado_inicial, None, None, 0, 0, 0)])

    while fila:

        no = fila.popleft()

        explorado.add(no.map)

        if no.estado == estado_esperado:
            no_esperado = no
            return fila

        vizinhos = expande(no)

        for vizinho in vizinhos:
            if vizinho.map not in explorado:
                fila.append(vizinho)
                explorado.add(vizinho.map)

                if vizinho.profundidade > profundidade_maxima:
                    profundidade_maxima += 1

        if len(fila) > tamanho_max_fronteira:
            tamanho_max_fronteira = len(fila)

# Busca em profundidade
# Depth-First Search - DFS
# https://pt.wikipedia.org/wiki/Busca_em_profundidade
def bep(estado_inicial):

    global tamanho_max_fronteira, no_esperado, profundidade_maxima

    explorado, pilha = set(), list([Estado(estado_inicial, None, None, 0, 0, 0)])

    while pilha:

        no = pilha.pop()

        explorado.add(no.map)

        if no.estado == estado_esperado:
            no_esperado = no
            return pilha

        vizinhos = reversed(expande(no))

        for vizinho in vizinhos:
            if vizinho.map not in explorado:
                pilha.append(vizinho)
                explorado.add(vizinho.map)

                if vizinho.profundidade > profundidade_maxima:
                    profundidade_maxima += 1

        if len(pilha) > tamanho_max_fronteira:
            tamanho_max_fronteira = len(pilha)

#A-Estrela
def a_estrela(estado_inicial):

    global tamanho_max_fronteira, no_esperado, profundidade_maxima

    explorado, heap, entrada_heap, contador = set(), list(), {}, itertools.count()

    chave = h(estado_inicial)

    root = Estado(estado_inicial, None, None, 0, 0, chave)

    entry = (chave, 0, root)

    heappush(heap, entry)

    entrada_heap[root.map] = entry

    while heap:

        no = heappop(heap)

        explorado.add(no[2].map)

        if no[2].estado == estado_esperado:
            no_esperado = no[2]
            return heap

        vizinhos = expande(no[2])

        for vizinho in vizinhos:

            vizinho.chave = vizinho.custo + h(vizinho.estado)

            entry = (vizinho.chave, vizinho.move, vizinho)

            if vizinho.map not in explorado:

                heappush(heap, entry)

                explorado.add(vizinho.map)

                entrada_heap[vizinho.map] = entry

                if vizinho.profundidade > profundidade_maxima:
                    profundidade_maxima += 1

            elif vizinho.map in entrada_heap and vizinho.chave < entrada_heap[vizinho.map][2].chave:

                hindex = heap.index((entrada_heap[vizinho.map][2].chave,
                                     entrada_heap[vizinho.map][2].move,
                                     entrada_heap[vizinho.map][2]))

                heap[int(hindex)] = entry

                entrada_heap[vizinho.map] = entry

                heapify(heap)

        if len(heap) > tamanho_max_fronteira:
            tamanho_max_fronteira = len(heap)


def expande(no):

    global nos_expandidos
    nos_expandidos += 1

    vizinhos = list()

    vizinhos.append(Estado(move(no.estado, 1), no, 1, no.profundidade + 1, no.custo + 1, 0))
    vizinhos.append(Estado(move(no.estado, 2), no, 2, no.profundidade + 1, no.custo + 1, 0))
    vizinhos.append(Estado(move(no.estado, 3), no, 3, no.profundidade + 1, no.custo + 1, 0))
    vizinhos.append(Estado(move(no.estado, 4), no, 4, no.profundidade + 1, no.custo + 1, 0))

    nos = [vizinho for vizinho in vizinhos if vizinho.estado]

    return nos


def move(estado, posicao):

    novo_estado = estado[:]

    index = novo_estado.index(0)

    if posicao == 1:  # Cima

        if index not in range(0, lado_quadro):

            temp = novo_estado[index - lado_quadro]
            novo_estado[index - lado_quadro] = novo_estado[index]
            novo_estado[index] = temp

            return novo_estado
        else:
            return None

    if posicao == 2:  # Baixo

        if index not in range(tamanho_quadro - lado_quadro, tamanho_quadro):

            temp = novo_estado[index + lado_quadro]
            novo_estado[index + lado_quadro] = novo_estado[index]
            novo_estado[index] = temp

            return novo_estado
        else:
            return None

    if posicao == 3:  # Esquerda

        if index not in range(0, tamanho_quadro, lado_quadro):

            temp = novo_estado[index - 1]
            novo_estado[index - 1] = novo_estado[index]
            novo_estado[index] = temp

            return novo_estado
        else:
            return None

    if posicao == 4:  # Direita

        if index not in range(lado_quadro - 1, tamanho_quadro, lado_quadro):

            temp = novo_estado[index + 1]
            novo_estado[index + 1] = novo_estado[index]
            novo_estado[index] = temp

            return novo_estado
        else:
            return None


def h(estado):

    return sum(abs(b % lado_quadro - g % lado_quadro) + abs(b//lado_quadro - g//lado_quadro)
               for b, g in ((estado.index(i), estado_esperado.index(i)) for i in range(1, tamanho_quadro)))


def passos():

    no_atual = no_esperado

    while estado_inicial != no_atual.estado:

        if no_atual.move == 1:
            movimento = 'Cima'
        elif no_atual.move == 2:
            movimento = 'Baixo'
        elif no_atual.move == 3:
            movimento = 'Esquerda'
        else:
            movimento = 'Direita'

        movimentos.insert(0, movimento)
        no_atual = no_atual.pai

    return movimentos


def escreve_arquivo(fronteira, time):

    global movimentos

    movimentos = passos()
    print("Caminho percorrido:\n ", str(movimentos))
    print("Movimentos executados: ", str(len(movimentos)))


def read(combinacao):

    global tamanho_quadro, lado_quadro

    data = combinacao.split(",")

    for element in data:
        estado_inicial.append(int(element))

    tamanho_quadro = len(estado_inicial)

    lado_quadro = int(tamanho_quadro ** 0.5)