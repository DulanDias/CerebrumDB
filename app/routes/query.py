from fastapi import APIRouter
from app.core.embedding import EmbeddingEngine
from app.core.vector_store import VectorStore
from app.core.document_store import DocumentStore
from app.core.madb import MADB
from app.models.query import QueryInput, QueryResult

router = APIRouter()
embedder = EmbeddingEngine()
vstore = VectorStore()
doc_store = DocumentStore()
madb = MADB()

@router.post("/", response_model=list[QueryResult])
def query(input: QueryInput):
    query_vec = embedder.encode(input.query)
    top_k_ids = vstore.search(query_vec, input.top_k)
    candidate_vecs = [embedder.encode(doc_store.load(doc_id)['text']) for doc_id in top_k_ids]
    scores = madb.compute_attention(query_vec, candidate_vecs)

    results = []
    for idx, doc_id in enumerate(top_k_ids):
        doc = doc_store.load(doc_id)
        results.append(QueryResult(
            doc_id=doc_id,
            score=float(scores[idx]),
            text=doc["text"],
            meta=doc.get("meta", {})
        ))

    return results
