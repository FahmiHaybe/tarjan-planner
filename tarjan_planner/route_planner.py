from itertools import permutations

from time_decorator import timethis

@timethis
def find_efficient_brute_force(G, home):
    nodes = list(G.nodes)
    nodes.remove(home)
    min_path = None
    min_weight = float('inf')
    transport_modes = None  # This will store the transport modes for each movement

    for perm in permutations(nodes):
        current_weight = 0
        current_modes = []  # List to store the transport modes for the current permutation
        path = [home] + list(perm) + [home]
        for i in range(len(path) - 1):
            edge_data = G[path[i]][path[i + 1]]
            current_weight += edge_data['weight']
            current_modes.append(edge_data['mode'])  # Append the mode used for the edge

        if current_weight < min_weight:
            min_weight = current_weight
            min_path = path
            transport_modes = current_modes  # Store the modes for the best path

    return min_path, transport_modes, min_weight