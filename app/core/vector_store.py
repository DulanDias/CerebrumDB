import faiss
import numpy as np

class VectorStore:
    def __init__(self, dim=768):
        self.index = faiss.IndexFlatIP(dim)
        self.doc_map = {}

    def add(self, doc_id: str, vector: np.ndarray):
        idx = len(self.doc_map)
        self.index.add(np.array([vector]))
        self.doc_map[idx] = doc_id

    def search(self, query_vec, top_k=5):
        D, I = self.index.search(np.array([query_vec]), top_k)
        return [self.doc_map[i] for i in I[0] if i != -1]

    def save_index(self, path):
        faiss.write_index(self.index, path)

    def load_index(self, path):
        self.index = faiss.read_index(path, faiss.IO_FLAG_MMAP)
