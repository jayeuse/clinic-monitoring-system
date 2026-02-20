from sqlmodel import SQLModel
from sqlmodel import create_engine, Session
from core.config import settings

engine = create_engine(
    settings.DATABASE_URL, 
    connect_args={"check_same_thread": False}, 
    echo=True
)

def create_database():
    SQLModel.metadata.create_all(engine)
