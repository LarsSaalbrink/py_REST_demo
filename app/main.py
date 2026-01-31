import uvicorn
import argparse

from fastapi import FastAPI

from database import init_db
from user_endpoints import create_user, login
from models import User, Token

def on_startup() -> None:
    init_db()

app = FastAPI()

app.add_event_handler("startup", on_startup)

app.add_api_route("/register", create_user, methods=["POST"], response_model=None)
app.add_api_route("/login", login, methods=["POST"], response_model=Token)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run FastAPI app with optional reload.")
    parser.add_argument("--host", default="127.0.0.1", help="Host to bind")
    parser.add_argument("--port", type=int, default=8000, help="Port to bind")
    parser.add_argument("--reload", action="store_true", help="Enable hot reload")
    args: argparse.Namespace = parser.parse_args()

    uvicorn.run("main:app", host=args.host, port=args.port, reload=args.reload)
