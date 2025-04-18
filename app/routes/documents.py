from fastapi import APIRouter, Depends, HTTPException
from app.core import document_store, embedding, vector_store
from app.models.document import DocumentInput, DocumentOutput
from app.models.user import User
from app.core.rbac import require_role
from app.core.security import get_current_user
from typing import Dict
from app.core.embedding import EmbeddingEngine
from app.utils.logger import logger
from uuid import uuid4  # Add this import for generating unique IDs
from numpy import ndarray
import numpy as np

router = APIRouter()

# These will be injected from main.py
store = None
vstore = None
embedder = EmbeddingEngine()

@router.post("/", response_model=DocumentOutput, dependencies=[Depends(require_role("admin", "editor"))])
def add_document(doc: DocumentInput, user: User = Depends(get_current_user)):
    """
    Add a new document. Only 'admin' and 'editor' roles are allowed.
    """
    # Preprocess and chunk the document
    embeddings, chunks = embedder.encode(doc.text)
    if not all(isinstance(embedding, ndarray) for embedding in embeddings):
        raise HTTPException(status_code=400, detail="Invalid embeddings generated.")

    # Ensure consistent vector shape
    max_dim = max(embedding.shape[0] for embedding in embeddings)
    embeddings = [np.pad(embedding, (0, max_dim - embedding.shape[0])) if embedding.shape[0] < max_dim else embedding[:max_dim] for embedding in embeddings]

    full_doc = doc.dict()
    full_doc["owner"] = user.user_id
    full_doc["doc_id"] = str(uuid4())  # Generate a unique doc_id

    # Save each chunk with metadata
    chunk_ids = []
    for idx, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
        if embedding.ndim != 1:
            raise HTTPException(status_code=400, detail="Embedding dimensions are inconsistent.")
        chunk_metadata = {
            "chunk_id": f"{idx}",
            "parent_doc_id": full_doc["doc_id"],  # Use the generated doc_id
            "text": chunk,
            "meta": doc.meta,
        }
        chunk_id = store.save(chunk_metadata)
        vstore.add(chunk_id, embedding)
        chunk_ids.append(chunk_id)

    logger.info(f"Document added with chunks: {chunk_ids}")
    return {"doc_id": full_doc["doc_id"], "chunk_ids": chunk_ids}

@router.get("/{id}")
def get_document(id: str, user: User = Depends(get_current_user)):
    """
    Retrieve a document by ID. All authenticated users allowed.
    """
    try:
        return store.load(id)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Document not found")

@router.put("/{id}", dependencies=[Depends(require_role("admin", "editor"))])
def update_document(id: str, doc: DocumentInput, user: User = Depends(get_current_user)):
    """
    Update a document. Requires 'admin' or 'editor' role.
    """
    try:
        store.delete(id)
    except FileNotFoundError:
        pass  # overwrite logic

    updated_doc = doc.dict()
    updated_doc["owner"] = user.user_id
    doc_id = store.save(updated_doc)
    vector = embedder.encode(doc.text)
    vstore.add(doc_id, vector)
    return {"doc_id": doc_id, "status": "updated"}

@router.delete("/{id}", dependencies=[Depends(require_role("admin"))])
def delete_document(id: str, user: User = Depends(get_current_user)):
    """
    Delete a document. Only 'admin' users are allowed.
    """
    try:
        store.delete(id)
        return {"status": "deleted"}
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Document not found")
