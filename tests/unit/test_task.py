from sqlmodel import Session, select
from fastapi import HTTPException

from user_endpoints import create_user, login
from task_endpoints import Api_Task, list_created_tasks, create_task, update_task, delete_task, Create_Task_request, Update_Task_request, Delete_Task_request
from user_endpoints import Create_user_request, Login_request
from models import User

from common import create_test_session

def test_list_no_tasks() -> None:
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
    except HTTPException as e:
        assert False, "Login failed"

    tasks: list[Api_Task] = list_created_tasks(
        user=session.exec(select(User).where(User.username == "larssaalbrink@gmail.com")).first(),
        session=session,
        )

    assert len(tasks) == 0

def test_create_task() -> None:
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
    except HTTPException as e:
        assert False, "Login failed"

    tasks: list[Api_Task] = list_created_tasks(
        user=session.exec(select(User).where(User.username == "larssaalbrink@gmail.com")).first(),
        session=session,
        )

    assert len(tasks) == 0

    create_task(
        user=session.exec(select(User).where(User.username == "larssaalbrink@gmail.com")).first(),
        session=session,
        task_req=Create_Task_request(title="Eat cheese", description="Eat all cheese currently in the fridge", due_date="2025-02-21"),
        )

    tasks: list[Api_Task] = list_created_tasks(
        user=session.exec(select(User).where(User.username == "larssaalbrink@gmail.com")).first(),
        session=session,
        )

    assert len(tasks) == 1

    assert tasks[0].title == "Eat cheese"
    assert tasks[0].description == "Eat all cheese currently in the fridge"
    assert tasks[0].due_date.date().isoformat() == "2025-02-21"

def test_list_multiple_tasks() -> None:
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
    except HTTPException as e:
        assert False, "Login failed"

    tasks: list[Api_Task] = list_created_tasks(
        user=session.exec(select(User).where(User.username == "larssaalbrink@gmail.com")).first(),
        session=session,
        )

    assert len(tasks) == 0

    create_task(
        user=session.exec(select(User).where(User.username == "larssaalbrink@gmail.com")).first(),
        session=session,
        task_req=Create_Task_request(title="Eat cheese", description="Eat all cheese currently in the fridge", due_date="2025-02-21"),
        )

    create_task(
        user=session.exec(select(User).where(User.username == "larssaalbrink@gmail.com")).first(),
        session=session,
        task_req=Create_Task_request(title="Drink milk", description="Drink absurd amount of milk", due_date="2025-03-01"),
        )

    tasks: list[Api_Task] = list_created_tasks(
        user=session.exec(select(User).where(User.username == "larssaalbrink@gmail.com")).first(),
        session=session,
        )

    assert len(tasks) == 2

def test_update_task() -> None:
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
    except HTTPException as e:
        assert False, "Login failed"

    tasks: list[Api_Task] = list_created_tasks(
        user=session.exec(select(User).where(User.username == "larssaalbrink@gmail.com")).first(),
        session=session,
        )

    assert len(tasks) == 0

    encrypted_id: int = create_task(
        user=session.exec(select(User).where(User.username == "larssaalbrink@gmail.com")).first(),
        session=session,
        task_req=Create_Task_request(title="Eat cheese", description="Eat all cheese currently in the fridge", due_date="2025-02-21"),
        )

    tasks: list[Api_Task] = list_created_tasks(
        user=session.exec(select(User).where(User.username == "larssaalbrink@gmail.com")).first(),
        session=session,
        )
    assert len(tasks) == 1
    assert tasks[0].title == "Eat cheese"
    assert tasks[0].description == "Eat all cheese currently in the fridge"
    assert tasks[0].due_date.date().isoformat() == "2025-02-21"

    update_task(
        task_id=encrypted_id,
        update_req=Update_Task_request(title="Drink milk", description="Drink absurd amount of milk", due_date="2025-03-01"),
        user=session.exec(select(User).where(User.username == "larssaalbrink@gmail.com")).first(),
        session=session,
        )

    tasks: list[Api_Task] = list_created_tasks(
        user=session.exec(select(User).where(User.username == "larssaalbrink@gmail.com")).first(),
        session=session,
        )
    assert len(tasks) == 1
    assert tasks[0].title == "Drink milk"
    assert tasks[0].description == "Drink absurd amount of milk"
    assert tasks[0].due_date.date().isoformat() == "2025-03-01"

def test_delete_task() -> None:
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
    except HTTPException as e:
        assert False, "Login failed"

    tasks: list[Api_Task] = list_created_tasks(
        user=session.exec(select(User).where(User.username == "larssaalbrink@gmail.com")).first(),
        session=session,
        )

    assert len(tasks) == 0

    encrypted_id: int = create_task(
        user=session.exec(select(User).where(User.username == "larssaalbrink@gmail.com")).first(),
        session=session,
        task_req=Create_Task_request(title="Eat cheese", description="Eat all cheese currently in the fridge", due_date="2025-02-21"),
        )

    tasks: list[Api_Task] = list_created_tasks(
        user=session.exec(select(User).where(User.username == "larssaalbrink@gmail.com")).first(),
        session=session,
        )

    assert len(tasks) == 1

    delete_task(
        delete_req=Delete_Task_request(task_id=encrypted_id),
        user=session.exec(select(User).where(User.username == "larssaalbrink@gmail.com")).first(),
        session=session,
        )

    tasks: list[Api_Task] = list_created_tasks(
        user=session.exec(select(User).where(User.username == "larssaalbrink@gmail.com")).first(),
        session=session,
        )
    assert len(tasks) == 0