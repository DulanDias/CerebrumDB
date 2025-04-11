from pydantic import BaseModel
from typing import Dict, Optional

class QueryInput(BaseModel):
    query: str
    top_k: int = 5
    filter: Optional[Dict[str, str]] = None

class QueryResult(BaseModel):
    doc_id: str
    score: float
    text: str
    meta: Dict[str, str]
