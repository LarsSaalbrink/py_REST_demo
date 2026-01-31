from sqlmodel import Session, select, SQLModel
from fastapi import Depends, Body, Response, HTTPException, Path
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
    # Validate request
    if not task_req.title:
        raise HTTPException(status_code=400, detail="Title is required") # 400: Bad Request
    if not task_req.description:
        raise HTTPException(status_code=400, detail="Description is required") # 400: Bad Request

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

class Delete_Task_request(BaseModel):
    task_id: int
def delete_task(
    delete_req: Delete_Task_request = Path(...),
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
) -> Response:
    # Validate request
    if not delete_req.task_id:
        raise HTTPException(status_code=400, detail="Task ID is required") # 400: Bad Request
    task_raw: Task | None = session.exec(select(Task).where(Task.id == delete_req.task_id)).first()
    if not task_raw:
        raise HTTPException(status_code=404, detail="Task not found") # 404: Not Found
    task: Task = task_raw
    if task.owner_id != user.id:
        raise HTTPException(status_code=403, detail="Must be owner of task to delete") # 403: Forbidden

    session.delete(task)
    session.commit()
    return Response(status_code=200) # 200: OK