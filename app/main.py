from fastapi import FastAPI
from app.routes import documents, query, auth, feedback
from app.utils.cache import cache
from app.core.vector_store import VectorStore
from app.core.document_store import DocumentStore

app = FastAPI(title="CerebrumDB")

# Shared instances of VectorStore and DocumentStore
vstore = VectorStore()
doc_store = DocumentStore()

# Inject shared instances into routers
documents.vstore = vstore
documents.store = doc_store
query.vstore = vstore
query.doc_store = doc_store

app.include_router(documents.router, prefix="/document")
app.include_router(query.router, prefix="/query")
app.include_router(auth.router, prefix="/user")
app.include_router(feedback.router, prefix="/feedback")

@app.on_event("startup")
async def startup_event():
    await cache.connect()