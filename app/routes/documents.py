from fastapi import APIRouter, HTTPException
from app.core import document_store, embedding, vector_store
from app.models.document import DocumentInput, DocumentOutput
from typing import Dict

router = APIRouter()
store = document_store.DocumentStore()
embedder = embedding.EmbeddingEngine()
vstore = vector_store.VectorStore()

@router.post("/", response_model=DocumentOutput)
def add_document(doc: DocumentInput):
    vector = embedder.encode(doc.text)
    doc_id = store.save(doc.dict())
    vstore.add(doc_id, vector)
    return {"doc_id": doc_id}

@router.get("/{id}")
def get_document(id: str):
    try:
        return store.load(id)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Document not found")

@router.put("/{id}")
def update_document(id: str, doc: DocumentInput):
    try:
        store.delete(id)
    except FileNotFoundError:
        pass  # overwrite if not found
    doc_id = store.save(doc.dict())
    vector = embedder.encode(doc.text)
    vstore.add(doc_id, vector)
    return {"doc_id": doc_id, "status": "updated"}

@router.delete("/{id}")
def delete_document(id: str):
    try:
        store.delete(id)
        return {"status": "deleted"}
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Document not found")
