import json
import numpy as np
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

    query_vec = embedder.encode(input.query, is_query=True)  # Pass is_query=True
    if query_vec is None or query_vec.size == 0:  # Explicitly check if query_vec is empty or None
        logger.error("Query vector is empty or invalid. Aborting.")
        return []

    query_vec = np.pad(query_vec, (0, 768 - query_vec.shape[0]))  # Ensure consistent size
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
        if vector is None or vector.size == 0:  # Check if vector is None or empty
            logger.error(f"Vector for document ID {doc_id} not found or invalid in VectorStore.")
        else:
            vector = np.pad(vector, (0, 768 - vector.shape[0]))  # Ensure consistent size
            doc_vecs.append(vector)
    logger.debug(f"Document vectors retrieved: {doc_vecs}")

    if len(doc_vecs) == 0:  # Explicitly check if doc_vecs is empty
        logger.error("No valid document vectors retrieved. Aborting.")
        return []

    attention_scores = madb.compute_attention(query_vec, doc_vecs)
    if len(attention_scores) != len(doc_vecs):  # Validate attention scores length
        logger.error("Mismatch between attention scores and document vectors. Aborting.")
        return []

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
