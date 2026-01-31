import uvicorn
import argparse

from fastapi import FastAPI

from database import init_db
from auth import Token
from models import Task
from user_endpoints import create_user, login
from task_endpoints import Api_Task, list_created_tasks, create_task, update_task, delete_task

def on_startup() -> None:
    init_db()

app = FastAPI()

app.add_event_handler("startup", on_startup)

app.add_api_route("/register", create_user, methods=["POST"], response_model=None)
app.add_api_route("/login", login, methods=["POST"], response_model=Token)
app.add_api_route("/token", login, methods=["POST"], response_model=Token) # For use with FastAPI docs login feature

app.add_api_route("/tasks", list_created_tasks, methods=["GET"], response_model=list[Api_Task])
app.add_api_route("/tasks", create_task, methods=["POST"], response_model=int)          # Return ID
app.add_api_route("/tasks/{task_id}", update_task, methods=["PUT"], response_model=int) # Return ID
app.add_api_route("/tasks/{task_id}", delete_task, methods=["DELETE"], response_model=None)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run FastAPI app with optional hot-reload.")
    parser.add_argument("--host", default="127.0.0.1", help="Host to bind")
    parser.add_argument("--port", type=int, default=8000, help="Port to bind")
    parser.add_argument("--reload", action="store_true", help="Enable hot reload")
    args: argparse.Namespace = parser.parse_args()

    uvicorn.run("main:app", host=args.host, port=args.port, reload=args.reload)
