from fastapi import FastAPI
from app.routes import documents, query, auth, feedback
from app.utils.cache import cache

app = FastAPI(title="CerebrumDB")

app.include_router(documents.router, prefix="/document")
app.include_router(query.router, prefix="/query")
app.include_router(auth.router, prefix="/user")
app.include_router(feedback.router, prefix="/feedback")

@app.on_event("startup")
async def startup_event():
    await cache.connect()