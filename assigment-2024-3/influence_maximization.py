import sys
import argparse
import random
from collections import deque

def influence_spread(graph, seeds, p):
    active = set(seeds)
    queue = deque(seeds)
    
    while queue:
        u = queue.popleft()
        for v in graph[u]:
            if v not in active and random.random() <= p:
                active.add(v)
                queue.append(v)
    
    return len(active)

def monteCarlo(graph,seeds, p, mc):
    influence = 0

    for i in range(mc):
        influence += len(influence_spread(graph, seeds, p))

    return influence / mc

def select_seed_degree(graph, active):
    best_node = None
    max_degree = -1
    for node in graph:
        if node not in active and len(graph[node]) > max_degree:
            max_degree = len(graph[node])
            best_node = node
    return best_node

def select_seed_greedy(graph, seeds, p, mc):
    max_influence = -1
    max_node = -1
    
    for i in graph:
        influence = monteCarlo(graph, seeds + [i], p, mc)
        if i not in seeds and influence > max_influence:
            max_influence = influence
            max_node = i
    return max_node

def maximize_influence(graph, p, k, method='max_degree'):
    seeds = []
    for _ in range(k):
        if method == 'max_degree':
            new_seed = select_seed_degree(graph, seeds)
        elif method == 'max_greedy':
            new_seed = select_seed_greedy(graph, seeds, p)
        seeds.append(new_seed)
    return seeds

def parse_graph(file_path):
    graph = {}
    with open(file_path) as f:
        for line in f:
            u, v = map(int, line.strip().split())
            if u not in graph:
                graph[u] = []
            graph[u].append(v)
    return graph

def main():
    parser = argparse.ArgumentParser(description='Influence Maximization')
    parser.add_argument('graph', type=str, help='Path to the graph file')
    parser.add_argument('k', type=int, help='Number of seeds to select')
    parser.add_argument('--method', type=str, choices=['max_degree', 'greedy'], default='max_degree',
                        help='Method to select seeds (max_degree or greedy)')
    parser.add_argument('p', type=float, help='Probability of influence')
    parser.add_argument('mc', type=int, help='Number of loops for monteCarlo method')
    parser.add_argument('-r', '--RANDOM_SEED', type=int, help='first seeds value used in random')
    
    args = parser.parse_args()
    
if args.random:
    random.seed(args.random)

    graph = parse_graph(args.graph)
    seeds = maximize_influence(graph, args.p, args.k, args.method)
    random = 
    print(f'Selected seeds: {seeds}')

if __name__ == '__main__':
    main()
