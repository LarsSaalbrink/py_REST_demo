from sqlmodel import Session, select, SQLModel
from fastapi import Depends
from typing import Sequence, List
from pydantic import BaseModel
from datetime import datetime

from models import Task
from models import User
from auth import get_current_user
from database import get_session

class Api_Task(SQLModel):
    id: int
    title: str
    description: str
    due_date: datetime
    is_completed: bool
def list_created_tasks(
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
) -> List[Api_Task]:
    tasks: Sequence[Task] = session.exec(
        select(Task).where(Task.owner_id == user.id)
    ).all()

    return [Api_Task.model_validate(task) for task in tasks]
