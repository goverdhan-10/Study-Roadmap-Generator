from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# load pretrained model once
model = SentenceTransformer('all-MiniLM-L6-v2')

def get_concept_similarity(concepts):
    embeddings = model.encode(concepts)
    similarity_matrix = cosine_similarity(embeddings)
    return similarity_matrix