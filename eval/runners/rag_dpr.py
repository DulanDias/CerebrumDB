from app.core.vector_store import VectorStore
from app.core.embedding import EmbeddingEngine
from app.core.document_store import DocumentStore

vector_store = VectorStore()
embedder = EmbeddingEngine()
doc_store = DocumentStore()

def run_query(query: str) -> list:
    query_vector = embedder.encode(query)
    top_k_ids = vector_store.search(query_vector, top_k=10)
    results = [{"doc_id": doc_id, "score": 1.0} for doc_id in top_k_ids]
    return results
