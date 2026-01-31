import bcrypt

from typing import Any, Sequence
from fastapi import Response
from sqlmodel import Session, select
from fastapi import Depends, HTTPException, Query
from datetime import timedelta
from pydantic import BaseModel
from sqlmodel.sql._expression_select_cls import SelectOfScalar

from models import User, Token
from auth import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES, get_current_user
from database import get_session

class Create_user_request(BaseModel):
    email: str
    password: str
def create_user(user_req: Create_user_request, session: Session = Depends(get_session)) -> Response:
    # No duplicate emails allowed
    statement: SelectOfScalar[User] = select(User).where(User.email == user_req.email.lower())
    existing_user: User | None = session.exec(statement).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email is already registered")

    salt: bytes = bcrypt.gensalt(rounds=10)
    hashed_password: str = bcrypt.hashpw(user_req.password.encode("utf-8"), salt).decode("utf-8")

    user: User = User(
        email=user_req.email.lower(),
        password_salt=salt.decode("utf-8"),
        password_hash=hashed_password,
    )

    session.add(user)
    session.commit()
    session.refresh(user) # Ensure that user object is up to date with DB before returning
    return Response(status_code=201)

def list_users(
    _: User = Depends(get_current_user),
    session: Session = Depends(get_session),
) -> Sequence[User]:
    return session.exec(select(User)).all()

def login(email: str = Query(...), session: Session = Depends(get_session)) -> Token:
    user_raw: User | None = session.exec(select(User).where(User.email == email)).first()
    if not user_raw:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    user: User = user_raw

    token: str = create_access_token(
        {"sub": str(user.id)}, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return Token(access_token=token)
