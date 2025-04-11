from pydantic import BaseModel, Field
from typing import Dict, Optional

class QueryInput(BaseModel):
    query: str = Field(..., min_length=3)
    filter: Optional[Dict[str, str]] = None
    top_k: int = 5

class QueryResult(BaseModel):
    doc_id: str
    score: float
    text: str
    meta: Dict[str, str]
