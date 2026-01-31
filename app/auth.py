import os

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session
from jose import jwt, JWTError
from datetime import datetime, timedelta
from typing import Any
from pydantic import BaseModel
from Crypto.Cipher import AES
import hashlib

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

# Exposing ID's through API is a design requirement.
# However, Sqlite ids are simple and predictable, which is a cyber security risk. (Leaks information)
# To mitigate this, ids encrypted with a symmetrical encryption cipher before exposed to clients,
# then decrypted when client returns them for subsequent API calls.
# This way the true values can be masked, without interfering with database efficiency.
id_cipher = AES.new(hashlib.sha256(SECRET_KEY.encode("utf-8")).digest(), AES.MODE_ECB)

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode: dict = data.copy()
    expire: datetime = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Validate token
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
