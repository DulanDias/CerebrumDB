from fastapi import Depends, HTTPException, status
from app.models.user import User
from app.core.security import get_current_user

def require_role(*roles: str):
    def dependency(user: User = Depends(get_current_user)):
        if user.role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied. Requires role: {roles}"
            )
        return user
    return dependency
