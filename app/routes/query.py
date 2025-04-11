import json
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

# These will be injected from main.py
vstore = None
doc_store = None
embedder = EmbeddingEngine()
madb = MADB()

@router.post("/", response_model=list[QueryResult])
async def query(input: QueryInput, user: User = Depends(get_current_user)):
    logger.info(f"User {user.user_id} querying: {input.query}")

    cache_key = f"query:{input.query}:{input.top_k}"
    cached_result = await cache.get(cache_key)
    if cached_result:
        logger.debug("Cache hit. Returning cached results.")
        return json.loads(cached_result)

    query_vec = embedder.encode(input.query)
    logger.debug(f"Encoded query vector: {query_vec}")

    top_k_ids = vstore.search(query_vec, input.top_k)
    logger.debug(f"Top K IDs from VectorStore: {top_k_ids}")

    if not top_k_ids:  # Handle empty results
        logger.warning("No documents found for the query.")
        return []

    # Verify if vectors are retrieved correctly
    doc_vecs = []
    for doc_id in top_k_ids:
        vector = vstore.get_vector(doc_id)
        if vector is None:
            logger.error(f"Vector for document ID {doc_id} not found in VectorStore.")
        else:
            doc_vecs.append(vector)
    logger.debug(f"Document vectors retrieved: {doc_vecs}")

    # Ensure query vector and document vectors are valid
    if not query_vec or not doc_vecs:
        logger.error("Query vector or document vectors are invalid. Aborting.")
        return []

    attention_scores = madb.compute_attention(query_vec, doc_vecs)
    logger.debug(f"Attention scores: {attention_scores}")

    results = []
    for idx, chunk_id in enumerate(top_k_ids):
        chunk = doc_store.load(chunk_id)
        if not chunk:
            logger.error(f"Chunk with ID {chunk_id} not found in DocumentStore.")
            continue
        results.append(QueryResult(
            doc_id=chunk.get("parent_doc_id"),
            score=float(attention_scores[idx]),
            text=chunk["text"],
            meta=chunk.get("meta", {})
        ))

    if not results:
        logger.warning("No results could be generated from the query.")
        return []

    logger.info(f"Query results: {results}")
    # Serialize results using .dict() for JSON compatibility
    await cache.set(cache_key, json.dumps([result.dict() for result in results]))
    return results
