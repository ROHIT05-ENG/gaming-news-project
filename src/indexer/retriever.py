import pickle
import faiss
from sentence_transformers import SentenceTransformer
import numpy as np

INDEX_PATH = "data/index/faiss.index"
MAPPING_PATH = "data/index/doc_mapping.pkl"

model = SentenceTransformer("all-MiniLM-L6-v2")
index = faiss.read_index(INDEX_PATH)

with open(MAPPING_PATH, "rb") as f:
    mapping = pickle.load(f)

def search_faiss(query, top_k=5):
    embedding = model.encode([query])
    embedding = embedding.astype("float32")

    distances, indices = index.search(embedding, top_k)

    results = []
    for idx in indices[0]:
        results.append(mapping[idx])
    return results

if __name__ == "__main__":
    print(search_faiss("call of duty"))