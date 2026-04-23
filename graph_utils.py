import networkx as nx
import matplotlib.pyplot as plt

def create_prerequisite_graph(prereq_dict):
    G = nx.DiGraph()

    for subject, prereqs in prereq_dict.items():
        for prereq in prereqs:
            G.add_edge(prereq, subject)

    plt.figure(figsize=(10, 7))
    pos = nx.spring_layout(G, seed=42)

    nx.draw(
        G, pos,
        with_labels=True,
        node_size=3000,
        node_color="skyblue",
        font_size=10,
        font_weight="bold",
        arrows=True
    )

    plt.title("Prerequisite Learning Graph")
    return plt