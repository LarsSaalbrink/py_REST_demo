from datetime import datetime
from sqlmodel import SQLModel, Field

class Task(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    title: str
    description: str
    due_date: datetime
    is_completed: bool
    owner_id: int = Field(default=None, foreign_key="user.id")

class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    email: str
    password_salt: str
    password_hash: str
