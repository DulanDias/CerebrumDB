import faiss
import numpy as np
import logging

class VectorStore:
    def __init__(self, dim=768):
        self.index = faiss.IndexFlatIP(dim)
        self.doc_map = {}
        logging.info("VectorStore initialized.")

    def add(self, doc_id: str, vector: np.ndarray):
        # Normalize the vector before adding
        vector = vector / np.linalg.norm(vector)
        idx = len(self.doc_map)
        self.index.add(np.array([vector]))
        self.doc_map[idx] = doc_id
        logging.info(f"Added document {doc_id} with index {idx}.")

    def search(self, query_vec, top_k=5):
        # Normalize the query vector
        query_vec = query_vec / np.linalg.norm(query_vec)
        D, I = self.index.search(np.array([query_vec]), top_k)
        logging.info(f"Search results: {I[0]} with distances: {D[0]}")
        return [self.doc_map[i] for i in I[0] if i != -1]

    def save_index(self, path):
        faiss.write_index(self.index, path)

    def load_index(self, path):
        self.index = faiss.read_index(path, faiss.IO_FLAG_MMAP)

    def get_vector(self, doc_id: str):
        for idx, stored_doc_id in self.doc_map.items():
            if stored_doc_id == doc_id:
                return self.index.reconstruct(idx)
        raise ValueError(f"Vector for document ID {doc_id} not found.")

    def get_index_size(self):
        return self.index.ntotal
