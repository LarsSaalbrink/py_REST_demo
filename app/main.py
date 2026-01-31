import uvicorn
import argparse

from fastapi import FastAPI

from database import init_db
from endpoints import create_user, list_users, login
from models import User, Token

def on_startup() -> None:
    init_db()

app = FastAPI()

app.add_event_handler("startup", on_startup)

app.add_api_route("/register", create_user, methods=["POST"], response_model=None)
app.add_api_route("/users", list_users, methods=["GET"], response_model=list[User])
app.add_api_route("/token", login, methods=["POST"], response_model=Token)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run FastAPI app with optional reload.")
    parser.add_argument("--host", default="127.0.0.1", help="Host to bind")
    parser.add_argument("--port", type=int, default=8000, help="Port to bind")
    parser.add_argument("--reload", action="store_true", help="Enable hot reload")
    args: argparse.Namespace = parser.parse_args()

    uvicorn.run("main:app", host=args.host, port=args.port, reload=args.reload)
