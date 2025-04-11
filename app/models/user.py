from pydantic import BaseModel

class User(BaseModel):
    user_id: str
    role: str  # e.g., "admin", "editor", "viewer"
