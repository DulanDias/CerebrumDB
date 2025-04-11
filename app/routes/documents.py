from fastapi import APIRouter, Depends, HTTPException
from app.core import document_store, embedding, vector_store
from app.models.document import DocumentInput, DocumentOutput
from app.models.user import User
from app.core.rbac import require_role
from app.core.security import get_current_user
from typing import Dict
from app.core.embedding import EmbeddingEngine
from app.utils.logger import logger

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
    vector = embedder.encode(doc.text)
    full_doc = doc.dict()
    full_doc["owner"] = user.user_id
    doc_id = store.save(full_doc)
    vstore.add(doc_id, vector)
    logger.info(f"Document added: {doc_id}, Vector added to VectorStore.")
    return {"doc_id": doc_id}

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
