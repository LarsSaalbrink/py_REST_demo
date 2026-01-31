from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field

class Task(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    title: str
    description: str
    due_date: Optional[datetime] = Field(default=None, nullable=True)
    is_completed: bool
    owner_id: int = Field(default=None, foreign_key="user.id")

class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    username: str
    password_salt: str
    password_hash: str
