from typing import Sequence
from sqlmodel import Session, select
from fastapi import Depends, HTTPException, Query
from datetime import timedelta

from models import User, Token
from auth import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES, get_current_user
from database import get_session

def create_user(user: User, session: Session = Depends(get_session)) -> User:
    session.add(user)
    session.commit()
    session.refresh(user) # Ensure that user object is up to date with DB before returning
    return user

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
