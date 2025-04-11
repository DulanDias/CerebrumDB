from app.core.vector_store import VectorStore
from app.core.embedding import EmbeddingEngine
from app.core.madb import MADB
from app.core.document_store import DocumentStore

vector_store = VectorStore()
embedder = EmbeddingEngine()
madb = MADB()
doc_store = DocumentStore()

def run_query(query: str) -> list:
    query_vector = embedder.encode(query)
    top_k_ids = vector_store.search(query_vector, top_k=10)
    doc_vectors = [vector_store.get_vector(doc_id) for doc_id in top_k_ids]
    attention_scores = madb.compute_attention(query_vector, doc_vectors)
    results = sorted(
        [{"doc_id": doc_id, "score": score} for doc_id, score in zip(top_k_ids, attention_scores)],
        key=lambda x: x["score"],
        reverse=True
    )
    return results
