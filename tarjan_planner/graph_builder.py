import matplotlib.pyplot as plt
import networkx as nx
from geopy.distance import geodesic


def create_complete_graph(relatives, home, transports, weight='time'):
    """
    Create a complete graph with edges dynamically weighted based on time or cost.
    Supports any transport modes provided in the `transports` list.
    """
    graph = nx.Graph()

    # Add nodes for home and relatives
    if home:
        graph.add_node(home.street_name, pos=(home.lat, home.lng))
    for rel in relatives:
        graph.add_node(rel.street_name, pos=(rel.lat, rel.lng))

    nodes = list(graph.nodes)

    # Iterate over all pairs of nodes to create edges
    for i in range(len(nodes) - 1):
        for j in range(i + 1, len(nodes)):
            loc1 = graph.nodes[nodes[i]]['pos']
            loc2 = graph.nodes[nodes[j]]['pos']

            if loc1 == loc2:
                continue

            distance = calculate_distance(loc1, loc2)
            print(f"Distance between {nodes[i]} and {nodes[j]}: {distance:.2f} km")

            # Dynamically calculate metrics for all transport modes
            metrics = {mode.name: calculate_metric(distance, mode, weight) for mode in transports}

            # Select the best transport mode based on the chosen metric
            best_mode_name, best_metric = min(metrics.items(), key=lambda x: x[1])
            best_mode = next(mode for mode in transports if mode.name == best_mode_name)

            # Add the edge with the best mode and its metric as the weight
            graph.add_edge(
                nodes[i], nodes[j],
                weight=best_metric,
                mode=best_mode.name
            )
            print(f"Added edge between {nodes[i]} and {nodes[j]} with weight {best_metric:.2f} using {best_mode.name}")

    return graph


def calculate_metric(distance, mode, weight):
    """
    Calculate a metric (time or cost) for a given transport mode.
    """
    if weight == 'time':
        return (distance / float(mode.speed_kmh)) * 60 + float(mode.transfer_time_min)
    elif weight == 'cost':
        return float(mode.cost_per_km) * distance
    else:
        raise ValueError("Invalid weight type. Use 'time' or 'cost'.")


def calculate_distance(loc1, loc2):
    """
    Calculate geographical distance between two points using geodesic.
    """
    return geodesic(loc1, loc2).kilometers


def plot_route(graph, route):
    """
    Plot the optimized route with edges color-coded by transport mode.
    """
    if not route:
        print("No route to plot.")
        return

    pos = nx.get_node_attributes(graph, 'pos')
    edge_labels = {(route[i], route[i + 1]): graph[route[i]][route[i + 1]]['mode'] for i in range(len(route) - 1)}

    # Color mapping for transport modes (dynamic)
    color_map = {
        'bus': 'red',
        'bicycle': 'green',
        'walking': 'blue',
        'train': 'black'
    }
    edge_colors = [
        color_map.get(graph[route[i]][route[i + 1]]['mode'], 'gray')  # Default to gray for unknown modes
        for i in range(len(route) - 1)
    ]

    plt.figure(figsize=(30, 20))

    # Draw nodes
    nx.draw_networkx_nodes(graph, pos, nodelist=route, node_size=500, node_color='yellow', edgecolors='black',
                           linewidths=2)
    nx.draw_networkx_labels(graph, pos, font_size=12, font_weight='bold')

    # Draw edges
    nx.draw_networkx_edges(graph, pos, edgelist=[(route[i], route[i + 1]) for i in range(len(route) - 1)],
                           edge_color=edge_colors, width=3)

    # Draw edge labels
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, font_color='purple', font_size=10, label_pos=0.5)

    plt.title("Optimized Route with Best Transport Mode", fontsize=16, fontweight='bold')
    plt.show()
