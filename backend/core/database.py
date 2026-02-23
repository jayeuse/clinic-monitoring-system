from sqlmodel import Session
from sqlmodel import SQLModel, create_engine
from core.config import settings
import models # noqa: F401

engine = create_engine(
    settings.DATABASE_URL, 
    connect_args={"check_same_thread": False}, 
    echo=True
)

def get_session():
    with Session(engine) as session:
        yield session

def create_database():
    SQLModel.metadata.create_all(engine)
