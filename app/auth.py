import os

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session
from jose import jwt, JWTError
from datetime import datetime, timedelta
from typing import Any
from pydantic import BaseModel

from models import User
from database import get_session

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

SECRET_KEY: str
secret_raw: str | None = os.getenv("SECRET_KEY")
if not secret_raw:
    raise RuntimeError("SECRET_KEY not set in environment variables")
SECRET_KEY = secret_raw

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

    def __init__(self, access_token: str):
        self.access_token: str = access_token
        self.token_type: str = "bearer"

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode: dict = data.copy()
    expire: datetime = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_session),
) -> User:
    try:
        payload: dict[str, Any] = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        sub_raw: Any | None = payload.get("sub")
        if sub_raw is None or not isinstance(int(sub_raw), int):
            raise HTTPException(status_code=401, detail="Invalid token") # 401: Unauthorized
        user_id: int = int(sub_raw)
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token") # 401: Unauthorized

    user: User | None = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found") # 404: Not Found
    return user
