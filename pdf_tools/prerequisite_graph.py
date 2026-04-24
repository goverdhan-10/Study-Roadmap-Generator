import networkx as nx
from pyvis.network import Network
from pathlib import Path

def build_graph(prerequisites, relations, subject):
    Path("outputs").mkdir(exist_ok=True)

    G = nx.DiGraph()

    # 1. Add the Main Subject Node (The Ultimate Goal)
    # Make it a distinct shape and color so it stands out
    G.add_node(subject, 
               label=subject.title(), 
               color="#ff4b4b", 
               size=40, 
               shape="hexagon")

    # 2. Add all prerequisite nodes
    for concept in prerequisites:
        G.add_node(concept, 
                   label=concept.title(), 
                   color="#4da6ff", 
                   size=25, 
                   shape="box")

    # 3. Add Edges based on actual smart relations (not just a blind list)
    if relations:
        for c1, c2 in relations:
            G.add_edge(c1, c2, color="#aaaaaa")
        
        # Connect ONLY the final concepts to the main subject to avoid clutter
        if prerequisites:
            last_concept = prerequisites[-1]
            G.add_edge(last_concept, subject, color="#ff4b4b", label="Final Step")
    else:
        # Fallback if no relations: simple sequential chain
        for i, concept in enumerate(prerequisites):
            if i > 0:
                G.add_edge(prerequisites[i-1], concept, color="#aaaaaa")
        if prerequisites:
            G.add_edge(prerequisites[-1], subject, color="#ff4b4b", label="Final Step")

    # 4. Create the PyVis Network
    net = Network(
        height="600px", 
        width="100%", 
        directed=True, 
        bgcolor="#111111", # Dark mode background
        font_color="white"
    )

    net.from_nx(G)

    # 🔥 THE MAGIC: Turn on Hierarchical Layout 🔥
    # 🔥 THE MAGIC: Turn on Hierarchical Layout 🔥
    net.set_options("""
    var options = {
      "nodes": {
        "borderWidth": 2,
        "font": { "size": 18, "face": "Arial" }
      },
      "edges": {
        "arrows": { "to": { "enabled": true, "scaleFactor": 0.5 } },
        "smooth": { 
            "type": "cubicBezier", 
            "forceDirection": "horizontal", 
            "roundness": 0.4 
        }
      },
      "layout": {
        "hierarchical": {
          "enabled": true,
          "direction": "LR",
          "sortMethod": "directed",
          "levelSeparation": 250,
          "nodeSpacing": 100
        }
      },
      "physics": {
        "enabled": false
      },
      "interaction": {
        "zoomSpeed": 0.3, 
        "navigationButtons": true,
        "dragView": true
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