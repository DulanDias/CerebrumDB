from fastapi import Depends, HTTPException, status
from app.models.user import User

# Simulated auth context
def get_current_user() -> User:
    # In production: decode from token or session
    return User(user_id="admin", role="admin")  # Stub user

def require_role(*roles: str):
    def dependency(user: User = Depends(get_current_user)):
        if user.role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied. Requires role: {roles}"
            )
        return user
    return dependency
