from fastapi import APIRouter, Depends
from pydantic import BaseModel
from app.core.security import get_current_user
from app.models.user import User
import json

router = APIRouter()
FEEDBACK_FILE = "feedback_store.jsonl"

class Feedback(BaseModel):
    query: str
    doc_id: str
    relevant: bool

@router.post("/")
def submit_feedback(feedback: Feedback, user: User = Depends(get_current_user)):
    enriched = feedback.dict()
    enriched["user_id"] = user.user_id
    with open(FEEDBACK_FILE, "a") as f:
        f.write(json.dumps(enriched) + "\n")
    return {"status": "recorded"}
