from pydantic import BaseModel

class Feedback(BaseModel):
    query: str
    doc_id: str
    relevant: bool
    user_id: str
