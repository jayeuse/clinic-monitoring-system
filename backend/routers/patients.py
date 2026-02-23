from schemas.patient_schemas import PatientUpdate, PatientCreate, PatientPublic
from fastapi import HTTPException
from core.database import get_session
from fastapi import Depends
from sqlmodel import Session
from fastapi import APIRouter

from typing import List
from services.patient_service import patient_service

router = APIRouter(prefix="/patients", tags=["Patients"])

@router.get("/", response_model=List[PatientPublic])
def read_patients(
    db: Session = Depends(get_session),
    skip: int = 0,
    limit: int = 100
):
    return patient_service.get_all(db, skip=skip, limit=limit)

@router.get("/{patient_id}", response_model=PatientPublic)
def read_patient_by_id(
    patient_id:str,
    db: Session = Depends(get_session)
):

    patient = patient_service.get_by_patient_id(db, patient_id=patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    return patient

@router.post("/", response_model=PatientPublic)
def create_patient(
    patient_in: PatientCreate,
    db: Session = Depends(get_session)
):
    return patient_service.create(db, obj_in=patient_in)

@router.patch("/{patient_id}", response_model=PatientPublic)
def update_patient(
    patient_id: str,
    patient_in: PatientUpdate,
    db: Session = Depends(get_session)
):
    db_obj = patient_service.get_by_patient_id(db, patient_id=patient_id)

    if not db_obj:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    return patient_service.update(db, db_obj=db_obj, obj_in=patient_in)

@router.delete("/{patient_id}", response_model=PatientPublic)
def delete_patient(
    patient_id: str,
    db: Session = Depends(get_session)
):
    db_obj = patient_service.get_by_patient_id(db, patient_id=patient_id)

    if not db_obj:
        raise HTTPException(status_code=404, detail="Patient not found")

    return patient_service.remove(db, uuid=db_obj.uuid)