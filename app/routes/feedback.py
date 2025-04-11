from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

# In-memory feedback store (@TODO: upgrade to persistent)
feedback_log = []

class Feedback(BaseModel):
    query: str
    doc_id: str
    relevant: bool
    user_id: str

@router.post("/")
def submit_feedback(feedback: Feedback):
    feedback_log.append(feedback.dict())
    return {"status": "recorded"}
