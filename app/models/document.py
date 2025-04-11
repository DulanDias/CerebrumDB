from pydantic import BaseModel, Field
from typing import Dict, Optional

class DocumentInput(BaseModel):
    text: str = Field(..., min_length=5)
    meta: Optional[Dict[str, str]] = Field(default_factory=dict)

class DocumentOutput(BaseModel):
    doc_id: str
