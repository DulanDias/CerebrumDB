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
from app.utils.preprocessor import Preprocessor

router = APIRouter()

# These will be injected from main.py
vstore = None
doc_store = None
embedder = EmbeddingEngine()
madb = MADB()
preprocessor = Preprocessor()

@router.post("/", response_model=list[QueryResult])
async def query(input: QueryInput, user: User = Depends(get_current_user), similarity_threshold: float = 0.5):
    logger.info(f"User {user.user_id} querying: {input.query}")

    # Clean the query input
    cleaned_query = preprocessor.clean_text(input.query)
    logger.debug(f"Cleaned query: {cleaned_query}")

    cache_key = f"query:{cleaned_query}:{input.top_k}"
    cached_result = await cache.get(cache_key)
    if cached_result:
        logger.debug("Cache hit. Returning cached results.")
        return json.loads(cached_result)

    query_vec = embedder.encode(cleaned_query, is_query=True)  # Pass cleaned query
    if query_vec is None or query_vec.size == 0:  # Explicitly check if query_vec is empty or None
        logger.error("Query vector is empty or invalid. Aborting.")
        return []

    query_vec = np.pad(query_vec, (0, 768 - query_vec.shape[0]))  # Ensure consistent size
    logger.debug(f"Encoded query vector: {query_vec}")
    logger.debug(f"Query vector: {query_vec}")

    top_k_ids = vstore.search(query_vec, input.top_k)
    logger.debug(f"Top K IDs from VectorStore: {top_k_ids}")

    if not top_k_ids:  # Handle empty results
        logger.warning("No documents found for the query. Check embeddings or vector store.")
        return []

    # Verify if vectors are retrieved correctly
    doc_vecs = []
    for doc_id in top_k_ids:
        vector = vstore.get_vector(doc_id)
        logger.debug(f"Retrieved vector for doc_id {doc_id}: {vector}")
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

    # Apply similarity threshold
    filtered_results = [
        (chunk_id, score) for chunk_id, score in zip(top_k_ids, attention_scores) if score >= similarity_threshold
    ]
    if not filtered_results:
        logger.warning("No documents passed the similarity threshold.")
        return []

    results = []
    for chunk_id, score in filtered_results:
        chunk = doc_store.load(chunk_id)
        if not chunk:
            logger.error(f"Chunk with ID {chunk_id} not found in DocumentStore.")
            continue

        # Apply key-value filter
        if input.filter:
            if not all(chunk["meta"].get(k) == v for k, v in input.filter.items()):
                logger.debug(f"Chunk {chunk_id} filtered out due to metadata mismatch.")
                continue

        results.append(QueryResult(
            doc_id=chunk.get("parent_doc_id"),
            score=float(score),
            text=chunk["text"],
            meta=chunk.get("meta", {})
        ))

    # Feedback loop: Adjust MADB weights based on feedback 
    # @TODO:: Incorporate user feedback to refine attention scores

    logger.info(f"Query results: {results}")
    # Serialize results using .dict() for JSON compatibility
    await cache.set(cache_key, json.dumps([result.dict() for result in results]))
    return results
