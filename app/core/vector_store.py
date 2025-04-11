import faiss
import numpy as np
import logging

class VectorStore:
    def __init__(self, dim=768):
        self.index = faiss.IndexFlatIP(dim)
        self.doc_map = {}
        logging.info("VectorStore initialized.")

    def add(self, doc_id: str, vector: np.ndarray):
        idx = len(self.doc_map)
        self.index.add(np.array([vector]))
        self.doc_map[idx] = doc_id
        logging.info(f"Added document {doc_id} with index {idx}.")

    def search(self, query_vec, top_k=5):
        D, I = self.index.search(np.array([query_vec]), top_k)
        logging.info(f"Search results: {I[0]} with distances: {D[0]}")
        return [self.doc_map[i] for i in I[0] if i != -1]

    def save_index(self, path):
        faiss.write_index(self.index, path)

    def load_index(self, path):
        self.index = faiss.read_index(path, faiss.IO_FLAG_MMAP)
