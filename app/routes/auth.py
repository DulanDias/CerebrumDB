from fastapi import APIRouter, HTTPException
from app.models.user import User

router = APIRouter()

# In-memory user-role mapping for demo
fake_users_db = {
    "admin": {"user_id": "admin", "role": "admin"},
    "alice": {"user_id": "alice", "role": "editor"},
    "bob":   {"user_id": "bob", "role": "viewer"}
}

@router.get("/{user_id}", response_model=User)
def get_user(user_id: str):
    user = fake_users_db.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
