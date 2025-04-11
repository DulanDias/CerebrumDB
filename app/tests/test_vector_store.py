import numpy as np
from app.core.vector_store import VectorStore

def test_vector_search():
    vs = VectorStore()
    vs.add("doc1", np.random.rand(768))
    results = vs.search(np.random.rand(768), top_k=1)
    assert isinstance(results, list)
