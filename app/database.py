from sqlmodel import SQLModel, Session, create_engine
from sqlalchemy.engine import Engine
from collections.abc import Generator

sqlite_url = "sqlite:///./db.sqlite3"
engine: Engine = create_engine(sqlite_url, echo=True)

def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session

def init_db():
    SQLModel.metadata.create_all(engine)