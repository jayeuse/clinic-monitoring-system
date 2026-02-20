from contextlib import asynccontextmanager
from fastapi import FastAPI
from core.config import settings
from core.database import create_database

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_database()
    yield

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Backend API for the Clinic Monitoring System",
    version=settings.VERSION,
    lifespan=lifespan
)


@app.get("/")
def read_root():
    return {"message": "Welcome to the Clinic Monitoring System API!"}
@app.get("/health")
def health_check():
    return {"status": "ok"}