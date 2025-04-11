from app.config import REFRESH_TOKEN_EXPIRE_HOURS

from fastapi import APIRouter, HTTPException, Form, Depends
from pydantic import BaseModel
from typing import Dict, Optional
from pathlib import Path
import json
import os
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
from app.models.user import User
from app.utils.logger import logger

router = APIRouter()

USER_DB_PATH = Path("user_db.json")
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "supersecretkey")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ---- Data Access ----

def load_user_db() -> Dict[str, dict]:
    if not USER_DB_PATH.exists():
        return {}
    with open(USER_DB_PATH) as f:
        return json.load(f)

def save_user_db(db: Dict[str, dict]):
    with open(USER_DB_PATH, "w") as f:
        json.dump(db, f, indent=2)

# ---- API Models ----

class UserCreate(BaseModel):
    user_id: str
    password: str
    role: str  # admin, editor, viewer

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: Optional[str] = None
    token_type: str = "bearer"

# ---- Endpoints ----

@router.post("/init")
def init_user_db():
    if USER_DB_PATH.exists():
        raise HTTPException(400, "User DB already exists")
    save_user_db({})
    return {"status": "initialized"}

@router.post("/create")
def create_user(user: UserCreate):
    db = load_user_db()
    if user.user_id in db:
        raise HTTPException(400, "User already exists")
    db[user.user_id] = {
        "user_id": user.user_id,
        "password_hash": pwd_context.hash(user.password),
        "role": user.role
    }
    save_user_db(db)
    return {"status": f"User '{user.user_id}' created"}

@router.post("/token", response_model=TokenResponse)
def login(user_id: str = Form(...), password: str = Form(...)):
    try:
        db = load_user_db()
        user = db.get(user_id)
        if not user or not pwd_context.verify(password, user["password_hash"]):
            raise HTTPException(401, "Invalid credentials")
        
        # Generate access token
        access_expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_payload = {
            "sub": user["user_id"],
            "role": user["role"],
            "exp": access_expire
        }
        access_token = jwt.encode(access_payload, SECRET_KEY, algorithm=ALGORITHM)

        # Generate refresh token
        refresh_expire = datetime.utcnow() + timedelta(hours=REFRESH_TOKEN_EXPIRE_HOURS)
        refresh_payload = {
            "sub": user["user_id"],
            "type": "refresh",
            "exp": refresh_expire
        }
        refresh_token = jwt.encode(refresh_payload, SECRET_KEY, algorithm=ALGORITHM)

        logger.info(f"User {user_id} logged in successfully")
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }
    except Exception as e:
        logger.error(f"Login failed for user {user_id}: {e}")
        raise

@router.get("/{user_id}", response_model=User)
def get_user(user_id: str):
    db = load_user_db()
    user = db.get(user_id)
    if not user:
        raise HTTPException(404, "User not found")
    return User(user_id=user["user_id"], role=user["role"])

@router.post("/refresh", response_model=TokenResponse)
def refresh_token(refresh_token: str = Form(...)):
    try:
        # Decode the refresh token
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("type") != "refresh":
            raise HTTPException(401, "Invalid token type")

        # Generate a new access token
        access_expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_payload = {
            "sub": payload["sub"],
            "role": payload["role"],
            "exp": access_expire
        }
        access_token = jwt.encode(access_payload, SECRET_KEY, algorithm=ALGORITHM)

        logger.info(f"Access token refreshed for user {payload['sub']}")
        return {
            "access_token": access_token,
            "token_type": "bearer"
        }
    except JWTError:
        raise HTTPException(401, "Invalid or expired refresh token")