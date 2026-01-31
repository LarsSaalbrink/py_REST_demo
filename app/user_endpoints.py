import bcrypt

from sqlmodel import Session, select
from fastapi import Depends, HTTPException, Form, Response
from datetime import timedelta
from pydantic import BaseModel
from sqlmodel.sql._expression_select_cls import SelectOfScalar

from models import User
from auth import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES, Token
from database import get_session

MINIMUM_PASSWORD_LENGTH: int = 5

class Create_user_request(BaseModel):
    username: str
    password: str
def create_user(user_req: Create_user_request, session: Session = Depends(get_session)) -> Response:
    # Validate request
    if not user_req.username:
        raise HTTPException(status_code=400, detail="username is required") # 400: Bad Request
    if not user_req.password or len(user_req.password) < MINIMUM_PASSWORD_LENGTH:
        raise HTTPException(status_code=400, detail="Password of at least " + str(MINIMUM_PASSWORD_LENGTH) + " characters is required") # 400: Bad Request

    # No duplicate usernames allowed
    statement: SelectOfScalar[User] = select(User).where(User.username == user_req.username)
    existing_user: User | None = session.exec(statement).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="username is already registered") # 400: Bad Request

    salt: bytes = bcrypt.gensalt(rounds=10)
    hashed_password: str = bcrypt.hashpw(user_req.password.encode("utf-8"), salt).decode("utf-8")

    user: User = User(
        username=user_req.username,
        password_salt=salt.decode("utf-8"),
        password_hash=hashed_password,
    )

    session.add(user)
    session.commit()
    session.refresh(user) # Ensure that user object is up to date with DB before returning
    return Response(status_code=201) # 201: Created

class Login_request(BaseModel):
    username: str
    password: str
def login(login_req: Login_request = Form(...), session: Session = Depends(get_session)) -> Token:
    # Validate request
    if not login_req.username:
        raise HTTPException(status_code=400, detail="username is required") # 400: Bad Request
    if not login_req.password:
        raise HTTPException(status_code=400, detail="Password is required") # 400: Bad Request

    # Get user from DB
    user_raw: User | None = session.exec(select(User).where(User.username == login_req.username)).first()
    if not user_raw:
        raise HTTPException(status_code=401, detail="Invalid credentials") # 401: Unauthorized
    user: User = user_raw

    # Verify password
    salt: bytes = user.password_salt.encode("utf-8")
    hashed_password: str = bcrypt.hashpw(login_req.password.encode("utf-8"), salt).decode("utf-8")
    if not hashed_password == user.password_hash:
        raise HTTPException(status_code=401, detail="Invalid credentials") # 401: Unauthorized

    token: str = create_access_token(
        {"sub": str(user.id)}, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return Token(access_token=token)
