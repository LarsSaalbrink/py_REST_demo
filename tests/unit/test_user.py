import uvicorn
import argparse

from fastapi import FastAPI, HTTPException

from database import init_db
from auth import Token
from user_endpoints import create_user, login
from task_endpoints import Api_Task, list_created_tasks, create_task, update_task, delete_task
from user_endpoints import Create_user_request, Login_request

from sqlmodel import SQLModel, Session, create_engine
from sqlalchemy.pool import StaticPool

from common import create_test_session

def test_login_invalid_password() -> None:
    session: Session = create_test_session()

    create_user(
        Create_user_request(username="larssaalbrink@gmail.com", password="kaaskop"),
        session,
    )

    try:
        login(
            Login_request(username="larssaalbrink@gmail.com", password="wrong"),
            session,
        )
        assert False, "Expected HTTPException"
    except HTTPException as e:
        assert e.status_code == 401
