from fastapi import HTTPException
from sqlmodel import Session

from user_endpoints import create_user, login
from user_endpoints import Create_user_request, Login_request

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

def test_login_valid_password() -> None:
    session: Session = create_test_session()

    create_user(
        Create_user_request(username="larssaalbrink@gmail.com", password="kaaskop"),
        session,
    )

    try:
        login(
            Login_request(username="larssaalbrink@gmail.com", password="kaaskop"),
            session,
        )
        assert True, "Login succeeded"
    except HTTPException as e:
        assert False, "Login failed"
