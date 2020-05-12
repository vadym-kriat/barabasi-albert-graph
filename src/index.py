import random
import networkx as nx
from networkx import number_of_nodes, draw, empty_graph
import matplotlib.pyplot as plt

random.seed(3)


def barabasi_albert_graph(n, m0, k0):
    if m0 < 1 or m0 >= n:
        raise nx.NetworkXError("Barabási–Albert network must have m >= 1"
                               " and m < n, m = %d, n = %d" % (m0, n))

    # Add m initial nodes (m0 in barabasi-speak)
    G = empty_graph(m0)

    # Init empty graph with random edges
    init_edges_count = int(0.5 * m0 * k0)
    targets = list(range(m0))

    # List of existing nodes, with nodes repeated once for each adjacent edge
    repeated_nodes = []

    init_to = random.sample(targets, len(targets))
    repeated_nodes.extend(init_to)

    G.add_edges_from(zip(targets, init_to))
    rest_edges = init_edges_count - m0

    init_rest_from = random.sample(targets, rest_edges)
    init_rest_to = random.sample(targets, rest_edges)
    G.add_edges_from(zip(init_rest_from, init_rest_to))
    repeated_nodes.extend(init_rest_to)
    repeated_nodes.extend(init_rest_from)

    # Start adding the other n-m nodes. The first node is m.
    source = m0
    while source < n:

        # Add edges to k0 nodes from the source.
        k0from = [source] * k0
        k0to = random.sample(repeated_nodes, k0)
        G.add_edges_from(zip(k0from, random.sample(repeated_nodes, k0)))
        repeated_nodes.extend(k0from)
        repeated_nodes.extend(k0to)

        rest_from = random.sample(list(G.nodes), m0 - k0)
        rest_to = random.sample(repeated_nodes, m0 - k0)
        G.add_edges_from(zip(rest_from, rest_to))
        repeated_nodes.extend(rest_from)
        repeated_nodes.extend(rest_to)

        source += 1
    return G


def _random_subset(seq, m, rng):
    targets = set()
    while len(targets) < m:
        x = rng.choice(seq)
        targets.add(x)
    return targets


if __name__ == "__main__":
    graph = barabasi_albert_graph(8192, 10, 3)
    graph.degree()

    draw(graph, with_labels=False, node_size=1)
    plt.show()

    # Degree rank distribution
    degrees = dict(graph.degree())
    degree_sequence = sorted(degrees.values(), reverse=True)
    plt.loglog(degree_sequence, 'b-', marker='o')
    plt.title('Degree Rank Distribution of Barabasi Albert Graph')
    plt.ylabel("Degree")
    plt.xlabel("Rank")
    plt.show()

    # Degree frequency distribution
    degree_values = sorted(set(degrees.values()))
    histogram = [list(degrees.values()).count(i) / float(number_of_nodes(graph)) for i in degree_values]
    plt.figure()
    plt.plot(degree_values, histogram, 'o')
    plt.title('Degree Distribution of Barabasi Albert Graph')
    plt.xlabel('Degree')
    plt.ylabel('Fraction of Nodes')
    plt.xscale('log')
    plt.yscale('log')
    plt.show()
