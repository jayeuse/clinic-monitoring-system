import math
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from core.database import get_session
from schemas.base_schemas import GenericResponse, PaginationMeta
from schemas.patient_schemas import PatientCreate, PatientPublic, PatientUpdate
from services.patient_service import patient_service

router = APIRouter(prefix="/patients", tags=["Patients"])

@router.get("/", response_model=GenericResponse[List[PatientPublic]])
def read_patients(
    db: Session = Depends(get_session),
    skip: int = 0,
    limit: int = 100
):
    patients, total_count = patient_service.get_all(db, skip=skip, limit=limit)

    current_page = (skip // limit) + 1
    total_pages = math.ceil(total_count / limit) if limit > 0 else 1

    meta = PaginationMeta(
        total_records=total_count,
        current_page=current_page,
        total_pages=total_pages,
        next_page=(current_page + 1) if (skip + limit) < total_count else None,
        prev_page=(current_page - 1) if skip > 0 else None
    )

    return GenericResponse(message="Patients retrieved successfully", data=patients, meta=meta)

@router.get("/{patient_id}", response_model=GenericResponse[PatientPublic])
def read_patient_by_id(
    patient_id:str,
    db: Session = Depends(get_session)
):

    patient = patient_service.get_by_patient_id(db, patient_id=patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    return GenericResponse(message="Patient retrieved successfully", data=patient)

@router.post("/", response_model=GenericResponse[PatientPublic])
def create_patient(
    patient_in: PatientCreate,
    db: Session = Depends(get_session)
):
    new_patient = patient_service.create(db, obj_in=patient_in)
    return GenericResponse(message="Patient record created successfully", data=new_patient)

@router.patch("/{patient_id}", response_model=GenericResponse[PatientPublic])
def update_patient(
    patient_id: str,
    patient_in: PatientUpdate,
    db: Session = Depends(get_session)
):
    db_obj = patient_service.get_by_patient_id(db, patient_id=patient_id)

    if not db_obj:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    update_patient = patient_service.update(db, db_obj=db_obj, obj_in=patient_in)
    return GenericResponse(message="Patient record updated successfully", data=update_patient)

@router.delete("/{patient_id}", response_model=GenericResponse[PatientPublic])
def delete_patient(
    patient_id: str,
    db: Session = Depends(get_session)
):
    db_obj = patient_service.get_by_patient_id(db, patient_id=patient_id)

    if not db_obj:
        raise HTTPException(status_code=404, detail="Patient not found")

    delete_patient = patient_service.remove(db, uuid=db_obj.uuid)
    return GenericResponse(message="Patient record deleted successfully", data=delete_patient)