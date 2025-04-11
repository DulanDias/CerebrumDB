from fastapi import APIRouter, Depends
from app.core.embedding import EmbeddingEngine
from app.core.vector_store import VectorStore
from app.core.document_store import DocumentStore
from app.core.madb import MADB
from app.models.query import QueryInput, QueryResult
from app.core.security import get_current_user
from app.models.user import User
from app.utils.cache import cache
from app.utils.logger import logger

router = APIRouter()

embedder = EmbeddingEngine()
vstore = VectorStore()
doc_store = DocumentStore()
madb = MADB()

@router.post("/", response_model=list[QueryResult])
async def query(input: QueryInput, user: User = Depends(get_current_user)):

    logger.info(f"User {user.user_id} querying: {input.query}")

    cache_key = f"query:{input.query}:{input.top_k}"
    cached_result = await cache.get(cache_key)
    if cached_result:
        return json.loads(cached_result)

    query_vec = embedder.encode(input.query)
    top_k_ids = vstore.search(query_vec, input.top_k)

    logger.debug(f"Top K IDs: {top_k_ids}")
    doc_vecs = [embedder.encode(doc_store.load(doc_id)["text"]) for doc_id in top_k_ids]
    attention_scores = madb.compute_attention(query_vec, doc_vecs)

    results = []
    for idx, doc_id in enumerate(top_k_ids):
        doc = doc_store.load(doc_id)
        results.append(QueryResult(
            doc_id=doc_id,
            score=float(attention_scores[idx]),
            text=doc["text"],
            meta=doc.get("meta", {})
        ))

    await cache.set(cache_key, json.dumps(results))
    logger.info(f"Query results: {results}")
    return results
