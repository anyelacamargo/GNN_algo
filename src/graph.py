import networkx as nx
import matplotlib.pyplot as plt

def build_graph(train_df):
    G = nx.DiGraph()
    for h, r, t in train_df.values:
        G.add_edge(h, t, relation=r)
    return G


def plot_degree_distribution(G):
    degrees = [d for _, d in G.degree()]
    plt.hist(degrees, bins=50)
    plt.title("Degree Distribution")
    plt.xlabel("Degree")
    plt.ylabel("Frequency")
    plt.show()


def print_stats(G):
    print("Nodes:", G.number_of_nodes())
    print("Edges:", G.number_of_edges())
