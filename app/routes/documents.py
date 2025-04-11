from fastapi import APIRouter
from app.core import document_store, embedding, vector_store

router = APIRouter()
store = document_store.DocumentStore()
embedder = embedding.EmbeddingEngine()
vstore = vector_store.VectorStore()

@router.post("/")
def add_document(doc: dict):
    text = doc["text"]
    vector = embedder.encode(text)
    doc_id = store.save(doc)
    vstore.add(doc_id, vector)
    return {"doc_id": doc_id}
