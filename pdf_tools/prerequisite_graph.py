import networkx as nx
from pyvis.network import Network
from pathlib import Path


def build_graph(prerequisites, subject):

    Path("outputs").mkdir(exist_ok=True)

    G = nx.DiGraph()

    # main topic
    G.add_node(subject,
               label=subject,
               color="#ff4b4b",
               size=40)

    for i, concept in enumerate(prerequisites):

        G.add_node(concept,
                   label=concept,
                   color="#4da6ff",
                   size=25)

        G.add_edge(concept, subject, label="required for")

        if i > 0:
            G.add_edge(prerequisites[i-1], concept, label="learn before")


    net = Network(
        height="750px",
        width="100%",
        directed=True,
        bgcolor="#111111",
        font_color="white"
    )

    net.from_nx(G)

    net.set_options("""
    var options = {
      "nodes": {
        "shape": "dot",
        "font": { "size": 20 }
      },
      "edges": {
        "arrows": { "to": { "enabled": true }},
        "smooth": true
      },
      "physics": {
        "barnesHut": {
          "gravitationalConstant": -3000,
          "springLength": 200
        }
      }
    }
    """)

    path = "outputs/knowledge_graph.html"

    net.save_graph(path)

    return path


def learning_order(prerequisites):

    order = []

    for topic in prerequisites:
        order.append(topic)

    return order