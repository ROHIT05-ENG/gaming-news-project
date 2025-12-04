import csv
import pickle
import faiss
from sentence_transformers import SentenceTransformer
import numpy as np
import os

DATA_PATH = "data/evidence/evidence_clean.csv"
INDEX_PATH = "data/index/faiss.index"
MAPPING_PATH = "data/index/doc_mapping.pkl"

def build_faiss_index():
    print("Loading model...")
    model = SentenceTransformer("all-MiniLM-L6-v2")

    titles = []
    texts = []

    print("Reading CSV...")
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            titles.append(row["title"])
            texts.append(row["text"])

    print("Encoding documents...")
    embeddings = model.encode(texts, show_progress_bar=True)
    embeddings = np.array(embeddings).astype("float32")

    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)

    print(f"Saving FAISS index to {INDEX_PATH}")
    faiss.write_index(index, INDEX_PATH)

    mapping = [{"title": titles[i], "content": texts[i]} for i in range(len(texts))]
    with open(MAPPING_PATH, "wb") as f:
        pickle.dump(mapping, f)

    print("Index build complete!")

if __name__ == "__main__":
    build_faiss_index()