# memory/vector_store.py

import faiss
import os
import pickle
import numpy as np
from typing import List, Tuple

# Import Embedder
from memory.embedder import Embedder

class VectorStore:
    """
    Handles storage and retrieval of vector embeddings using FAISS.
    Also stores associated metadata in a simple side index (pickle).
    """

    def __init__(self, dim: int, index_path: str = "./vector_store/index.faiss", meta_path: str = "./vector_store/metadata.pkl"):
        self.dim = dim
        self.index_path = index_path
        self.meta_path = meta_path

        self.index = faiss.IndexFlatL2(self.dim)
        self.metadata = []

        if os.path.exists(index_path) and os.path.exists(meta_path):
            self.load()

    def add(self, vectors: List[List[float]], texts: List[str]):
        np_vectors = np.array(vectors).astype("float32")
        self.index.add(np_vectors)
        self.metadata.extend(texts)
        self.save()

    def add_texts(self, texts: List[str], embedder: Embedder):
        """
        Converts texts to vectors using the provided embedder and adds them to the FAISS index.
        """
        vectors = embedder.embed_text_chunks(texts)
        if vectors:
            self.add(vectors, texts)

    def search(self, query_vector: List[float], top_k: int = 5) -> List[Tuple[str, float]]:
        query_np = np.array([query_vector]).astype("float32")
        distances, indices = self.index.search(query_np, top_k)
        results = []

        for idx, dist in zip(indices[0], distances[0]):
            if 0 <= idx < len(self.metadata):
                results.append((self.metadata[idx], float(dist)))

        return results

    def save(self):
        faiss.write_index(self.index, self.index_path)
        with open(self.meta_path, "wb") as f:
            pickle.dump(self.metadata, f)

    def load(self):
        self.index = faiss.read_index(self.index_path)
        with open(self.meta_path, "rb") as f:
            self.metadata = pickle.load(f)
