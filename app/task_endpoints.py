from sqlmodel import Session, select, SQLModel
from fastapi import Depends, Body, Response, HTTPException, Path
from typing import Sequence, List, Optional
from datetime import datetime
from pydantic import BaseModel

from models import Task
from models import User
from auth import get_current_user, id_cipher
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

    # Encrypt IDs
    for task in tasks:
        id_bytes = task.id.to_bytes(16, byteorder='big')
        task.id = int.from_bytes(id_cipher.encrypt(id_bytes), byteorder='big')

    return [Api_Task.model_validate(task) for task in tasks]

class Create_Task_request(BaseModel):
    title: str
    description: str
    due_date: Optional[datetime]
def create_task(
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
    task_req: Create_Task_request = Body(...),
) -> int:
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

    # Return encrypted ID
    id_bytes: bytes = task.id.to_bytes(16, byteorder='big')
    return int.from_bytes(id_cipher.encrypt(id_bytes), byteorder='big')

class Update_Task_request(BaseModel):
    title: Optional[str]
    description: Optional[str]
    due_date: Optional[datetime]
def update_task(
    task_id: int = Path(...),
    update_req: Update_Task_request = Body(...),
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
) -> int:
    # Validate request
    if not task_id:
        raise HTTPException(status_code=400, detail="Task ID is required") # 400: Bad Request
    encrypted_id: int = task_id
    task_raw: Task | None = None

    # Decrypt ID
    try:
        decrypted_id_bytes: bytes = id_cipher.decrypt(task_id.to_bytes(16, byteorder='big'))
        task_id = int.from_bytes(decrypted_id_bytes, byteorder='big')
        task_raw = session.exec(select(Task).where(Task.id == task_id)).first()
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid task ID") # 400: Bad Request

    if not task_raw:
        raise HTTPException(status_code=404, detail="Task not found") # 404: Not Found
    task: Task = task_raw
    if task.owner_id != user.id:
        raise HTTPException(status_code=403, detail="Must be owner of task to update") # 403: Forbidden

    if update_req.title:
        task.title = update_req.title
    if update_req.description:
        task.description = update_req.description
    if update_req.due_date:
        task.due_date = update_req.due_date

    session.commit()
    return encrypted_id

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
    task_raw: Task | None = None

    # Decrypt ID
    try:
        decrypted_id_bytes: bytes = id_cipher.decrypt(delete_req.task_id.to_bytes(16, byteorder='big'))
        delete_req.task_id = int.from_bytes(decrypted_id_bytes, byteorder='big')
        task_raw: Task | None = session.exec(select(Task).where(Task.id == delete_req.task_id)).first()
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid task ID") # 400: Bad Request

    if not task_raw:
        raise HTTPException(status_code=404, detail="Task not found") # 404: Not Found
    task: Task = task_raw
    if task.owner_id != user.id:
        raise HTTPException(status_code=403, detail="Must be owner of task to delete") # 403: Forbidden

    session.delete(task)
    session.commit()
    return Response(status_code=200) # 200: OK