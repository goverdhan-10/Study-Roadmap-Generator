from collections import defaultdict, deque
from concept_analysis import analyze_concepts


def generate_learning_order(concepts):

    if not concepts:
        return [], []
    relations = analyze_concepts(concepts)

    # -------- GRAPH BUILD --------
    graph = defaultdict(list)
    indegree = {c: 0 for c in concepts}

    for c1, c2 in relations:
        if c2 not in graph[c1]:
            graph[c1].append(c2)
            indegree[c2] += 1

    # -------- TOPOLOGICAL SORT --------
    queue = deque([c for c in concepts if indegree[c] == 0])
    order = []

    while queue:
        node = queue.popleft()
        order.append(node)

        for neighbor in graph[node]:
            indegree[neighbor] -= 1
            if indegree[neighbor] == 0:
                queue.append(neighbor)

    # fill missing
    for c in concepts:
        if c not in order:
            order.append(c)

    # -------- CLEAN RELATIONS (ORDER BASED) --------
    clean_relations = []

    for i in range(len(order) - 1):
        c1 = order[i]
        c2 = order[i + 1]
        clean_relations.append((c1, c2))

    return order, clean_relations