from huggingface_integration import get_concept_similarity

def analyze_concepts(concepts):

    similarity = get_concept_similarity(concepts)

    relations = []

    for i in range(len(concepts)):
        for j in range(len(concepts)):
            if i != j and similarity[i][j] > 0.5:
                relations.append((concepts[i], concepts[j]))

    return relations