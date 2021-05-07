import argparse
import timeit
import resource
from collections import deque
from src.state import State
from heapq import heappush, heappop, heapify
import itertools

goal_state = [0, 1, 2, 3, 4, 5, 6, 7, 8]
goal_node = State
initial_state = list()
items_len = 0
items_side = 0

nodes_expanded = 0
max_search_depth = 0
max_frontier_size = 0

moves = list()
costs = set()


def bfs(start_state):

    global max_frontier_size, goal_node, max_search_depth

    explored, queue = set(), deque([State(start_state, None, None, 0, 0, 0)])

    while queue:

        node = queue.popleft()

        explored.add(node.map)

        if node.state == goal_state:
            goal_node = node
            return queue

        neighbors = expand(node)

        for neighbor in neighbors:
            if neighbor.map not in explored:
                queue.append(neighbor)
                explored.add(neighbor.map)

                if neighbor.depth > max_search_depth:
                    max_search_depth += 1

        if len(queue) > max_frontier_size:
            max_frontier_size = len(queue)


def dfs(start_state):

    global max_frontier_size, goal_node, max_search_depth

    explored, stack = set(), list([State(start_state, None, None, 0, 0, 0)])

    while stack:

        node = stack.pop()

        explored.add(node.map)

        if node.state == goal_state:
            goal_node = node
            return stack

        neighbors = reversed(expand(node))

        for neighbor in neighbors:
            if neighbor.map not in explored:
                stack.append(neighbor)
                explored.add(neighbor.map)

                if neighbor.depth > max_search_depth:
                    max_search_depth += 1

        if len(stack) > max_frontier_size:
            max_frontier_size = len(stack)


def ast(start_state):

    global max_frontier_size, goal_node, max_search_depth

    explored, heap, heap_entry, counter = set(), list(), {}, itertools.count()

    key = h(start_state)

    root = State(start_state, None, None, 0, 0, key)

    entry = (key, 0, root)

    heappush(heap, entry)

    heap_entry[root.map] = entry

    while heap:

        node = heappop(heap)

        explored.add(node[2].map)

        if node[2].state == goal_state:
            goal_node = node[2]
            return heap

        neighbors = expand(node[2])

        for neighbor in neighbors:

            neighbor.key = neighbor.cost + h(neighbor.state)

            entry = (neighbor.key, neighbor.move, neighbor)

            if neighbor.map not in explored:

                heappush(heap, entry)

                explored.add(neighbor.map)

                heap_entry[neighbor.map] = entry

                if neighbor.depth > max_search_depth:
                    max_search_depth += 1

            elif neighbor.map in heap_entry and neighbor.key < heap_entry[neighbor.map][2].key:

                hindex = heap.index((heap_entry[neighbor.map][2].key,
                                     heap_entry[neighbor.map][2].move,
                                     heap_entry[neighbor.map][2]))

                heap[int(hindex)] = entry

                heap_entry[neighbor.map] = entry

                heapify(heap)

        if len(heap) > max_frontier_size:
            max_frontier_size = len(heap)


def ida(start_state):

    global costs

    threshold = h(start_state)

    while 1:
        response = dls_mod(start_state, threshold)

        if type(response) is list:
            return response
            break

        threshold = response

        costs = set()


def dls_mod(start_state, threshold):

    global max_frontier_size, goal_node, max_search_depth, costs

    explored, stack = set(), list([State(start_state, None, None, 0, 0, threshold)])

    while stack:

        node = stack.pop()

        explored.add(node.map)

        if node.state == goal_state:
            goal_node = node
            return stack

        if node.key > threshold:
            costs.add(node.key)

        if node.depth < threshold:

            neighbors = reversed(expand(node))

            for neighbor in neighbors:
                if neighbor.map not in explored:

                    neighbor.key = neighbor.cost + h(neighbor.state)
                    stack.append(neighbor)
                    explored.add(neighbor.map)

                    if neighbor.depth > max_search_depth:
                        max_search_depth += 1

            if len(stack) > max_frontier_size:
                max_frontier_size = len(stack)

    return min(costs)


def expand(node):

    global nodes_expanded
    nodes_expanded += 1

    neighbors = list()

    neighbors.append(State(move(node.state, 1), node, 1, node.depth + 1, node.cost + 1, 0))
    neighbors.append(State(move(node.state, 2), node, 2, node.depth + 1, node.cost + 1, 0))
    neighbors.append(State(move(node.state, 3), node, 3, node.depth + 1, node.cost + 1, 0))
    neighbors.append(State(move(node.state, 4), node, 4, node.depth + 1, node.cost + 1, 0))

    nodes = [neighbor for neighbor in neighbors if neighbor.state]

    return nodes


def move(state, position):

    new_state = state[:]

    index = new_state.index(0)

    if position == 1:  # Up

        if index not in range(0, items_side):

            temp = new_state[index - items_side]
            new_state[index - items_side] = new_state[index]
            new_state[index] = temp

            return new_state
        else:
            return None

    if position == 2:  # Down

        if index not in range(items_len - items_side, items_len):

            temp = new_state[index + items_side]
            new_state[index + items_side] = new_state[index]
            new_state[index] = temp

            return new_state
        else:
            return None

    if position == 3:  # Left

        if index not in range(0, items_len, items_side):

            temp = new_state[index - 1]
            new_state[index - 1] = new_state[index]
            new_state[index] = temp

            return new_state
        else:
            return None

    if position == 4:  # Right

        if index not in range(items_side - 1, items_len, items_side):

            temp = new_state[index + 1]
            new_state[index + 1] = new_state[index]
            new_state[index] = temp

            return new_state
        else:
            return None


def h(state):

    return sum(abs(b % items_side - g % items_side) + abs(b//items_side - g//items_side)
               for b, g in ((state.index(i), goal_state.index(i)) for i in range(1, items_len)))


def backtrace():

    current_node = goal_node

    while initial_state != current_node.state:

        if current_node.move == 1:
            movement = 'Sobe'
        elif current_node.move == 2:
            movement = 'Desce'
        elif current_node.move == 3:
            movement = 'Esquerda'
        else:
            movement = 'Direita'

        moves.insert(0, movement)
        #show movement
        print("{} ".format(movement), end="")
        current_node = current_node.parent
    #force line break
    print()
    return moves




def read(configuration):

    global items_len, items_side

    data = configuration.split(",")

    for element in data:
        initial_state.append(int(element))

    items_len = len(initial_state)

    items_side = int(items_len ** 0.5)