import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import init_db
from auth import Token
from user_endpoints import create_user, login
from task_endpoints import Api_Task, list_created_tasks, create_task, update_task, delete_task

def on_startup() -> None:
    init_db()

def enable_dev_cors(app: FastAPI) -> None:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173"],
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app = FastAPI()

app.add_event_handler("startup", on_startup)

app.add_api_route("/register", create_user, methods=["POST"], response_model=None)
app.add_api_route("/login", login, methods=["POST"], response_model=Token)
app.add_api_route("/token", login, methods=["POST"], response_model=Token) # For use with FastAPI docs login feature

app.add_api_route("/tasks", list_created_tasks, methods=["GET"], response_model=list[Api_Task])
app.add_api_route("/tasks", create_task, methods=["POST"], response_model=int)          # Return ID
app.add_api_route("/tasks/{task_id}", update_task, methods=["PUT"], response_model=int) # Return ID
app.add_api_route("/tasks/{task_id}", delete_task, methods=["DELETE"], response_model=None)

if os.getenv("DEV_MODE") == "1":
    enable_dev_cors(app)
