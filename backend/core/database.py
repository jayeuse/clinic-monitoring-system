from sqlmodel import SQLModel, create_engine
from core.config import settings
import models

engine = create_engine(
    settings.DATABASE_URL, 
    connect_args={"check_same_thread": False}, 
    echo=True
)

def create_database():
    SQLModel.metadata.create_all(engine)
