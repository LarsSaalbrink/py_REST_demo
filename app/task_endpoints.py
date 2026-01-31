from sqlmodel import Session, select, SQLModel
from fastapi import Depends, Body, Response
from typing import Sequence, List, Optional
from datetime import datetime
from pydantic import BaseModel

from models import Task
from models import User
from auth import get_current_user
from database import get_session

class Api_Task(SQLModel):
    id: int
    title: str
    description: str
    due_date: Optional[datetime]
    is_completed: bool
def list_created_tasks(
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
) -> List[Api_Task]:
    tasks: Sequence[Task] = session.exec(
        select(Task).where(Task.owner_id == user.id)
    ).all()

    return [Api_Task.model_validate(task) for task in tasks]

class Create_Task_request(BaseModel):
    title: str
    description: str
    due_date: Optional[datetime]
def create_task(
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
    task_req: Create_Task_request = Body(...),
) -> Response:
    task: Task = Task(
        title=task_req.title,
        description=task_req.description,
        due_date=task_req.due_date,
        is_completed=False,
        owner_id=user.id,
    )
    session.add(task)
    session.commit()
    session.refresh(task) # Ensure that task object is up to date with DB before returning
    return Response(status_code=201)
