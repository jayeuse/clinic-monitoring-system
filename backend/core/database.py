from sqlmodel import Session, SQLModel, create_engine

import models  # noqa: F401
from core.config import settings

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
