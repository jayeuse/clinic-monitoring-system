from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.config import settings
from core.database import create_database
from routers import (
    clinic,
    dental_examinations,
    dental_records,
    dental_treatments,
    medical_examinations,
    medical_history,
    medical_treatments,
    patients,
)


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

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(patients.router)
app.include_router(clinic.router)
app.include_router(medical_history.router)
app.include_router(medical_examinations.router)
app.include_router(medical_treatments.router)
app.include_router(dental_records.router)
app.include_router(dental_examinations.router)
app.include_router(dental_treatments.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Clinic Monitoring System API!"}
@app.get("/health")
def health_check():
    return {"status": "ok"}