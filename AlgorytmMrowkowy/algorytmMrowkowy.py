#!/usr/bin/python3

# Ant Algorithm
# Ant algorithm is used to find a best way between nodes in a graph. As a best we understood the most optimal way. It simulates the way how ants traces its routes from the ant shelter (start node) to the foor (desired node). 
# Each ant, when follows some way leaves pheromones. The pheromones that keeps on the way ant chosen. If the way is shorter (more optimal), the ant is able to trace more times threw the way than on the longer way. Doe to that fact, more pheromones is kept on
# the way, and in consequence more ants more liekly choose that way.

# For the algorithm we will define a 4 node graph. Distances between nodes will be defined as a matrix:
# 
#   A  B   C  D
# A 0  3   2  2
# B 3  0   3  1.5
# C 2  3   0  1
# D 2  1.5 1  0

# The algorithm shall find a best way between all nodes, as shorter as possible.

# Paths costs to compare:
# 0 - 1 - 2 - 3: 9
# 0 - 1 - 3 - 2: 9,5
# 0 - 2 - 3 - 1: 7,5 BEST
# 0 - 2 - 1 - 3: 8,5
# 0 - 3 - 2 - 1: 8,5
# 0 - 3 - 1 - 2: 8,5

import random
import copy

nr_of_nodes = 4
nodes_distances = [
    [0, 3, 2, 2],
    [3, 0, 3, 1.5],
    [2, 3, 0, 1],
    [2, 1.5, 1, 0]
]

nr_of_ants = 50

pheromones_per_route = 100
pheromones_excavation = 1     #Loss of pheromones per rpute per iteration

pheromones = [
    [0, 1, 1, 1],
    [1, 0, 1, 1],
    [1, 1, 0, 1],
    [1, 1, 1, 0]
]

start_node = 0
nr_of_iterations = 50

def getDistance(p1, p2):         #p1, p2 numbers from 0 to 3 (A - D)
    return nodes_distances[p1][p2]

def getNextAvailableNodes(visited_nodes):
    return [i for i in range(nr_of_nodes) if i not in visited_nodes]

def getDistances(current_node, next_nodes):
    return [nodes_distances[current_node][p2] for p2 in next_nodes]

def getPheromones(current_node, next_nodes):
    return [pheromones[current_node][p2] for p2 in next_nodes]

def getNextNode(current_node, visited_nodes):
    next_nodes = getNextAvailableNodes(visited_nodes)  
    pheromone_per_route = getPheromones(current_node, next_nodes)
    next_node = random.choices(next_nodes, pheromone_per_route)
    #print(f"Nodes: {next_nodes}, Pher: {pheromone_per_route}, next: {next_node}")
    return next_node[0]

def pheromones_excavate():
    for x in range(nr_of_nodes):
        for y in range(nr_of_nodes):
            if pheromones[x][y] > pheromones_excavation:
                pheromones[x][y] = round(pheromones[x][y] - pheromones_excavation, 1)

def pheromones_add(pher, route, pheromone_per_path):
    for x in range(len(route)):
        node = route[x]
        if (route[x] == route[-1]):
            next_node = start_node
        else:
            next_node = route[x + 1]
        pher[node][next_node] = round(pheromone_per_path + pher[node][next_node], 1)

def single_ant_route(pher, n):
    current_node = start_node
    visited_nodes = [current_node]
    av = getNextAvailableNodes(visited_nodes)
    total_path = 0
    while (len(visited_nodes) < nr_of_nodes):
        next_node = getNextNode(current_node, visited_nodes)
        total_path = total_path + getDistance(current_node, next_node)

        current_node = next_node
        visited_nodes.append(current_node)

    pheromone_per_path = round((pheromones_per_route / total_path), 1)
    pheromones_add(pher, visited_nodes, pheromone_per_path)
    return visited_nodes
    #print(f"Ant {n} route: {visited_nodes} phers: {pher}")

def sum_pheromones(ant_pher):
    for pher in ant_pher:
        for x in range(nr_of_nodes):
            for y in range(nr_of_nodes):
                pheromones[x][y] += pher[x][y]

if __name__ == "__main__":
    print("AlgorytmMrowkowy:")
    paths = dict()
    for it in range(nr_of_iterations):
        ant_pher = [copy.deepcopy(pheromones) for ant in range(nr_of_ants)]
        for ant in range(nr_of_ants):
            route = single_ant_route(ant_pher[ant], ant)
            key = " ".join(str (e) for e in route)
            if key not in paths:
                paths[key] = 1
            else:
                paths[key] += 1
        sum_pheromones(ant_pher)
        pheromones_excavate()
        print(f"Pheromones updated: {pheromones}")
    
    print(paths)

