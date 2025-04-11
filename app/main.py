from fastapi import FastAPI
from app.routes import documents, query, auth

app = FastAPI(title="CerebrumDB")

app.include_router(documents.router, prefix="/document")
app.include_router(query.router, prefix="/query")
app.include_router(auth.router, prefix="/user")
