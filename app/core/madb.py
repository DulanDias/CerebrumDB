import numpy as np

class MADB:
    def compute_attention(self, query_vec, doc_vecs):
        scores = np.dot(doc_vecs, query_vec) / np.sqrt(len(query_vec))
        weights = np.exp(scores) / np.sum(np.exp(scores))
        return weights
