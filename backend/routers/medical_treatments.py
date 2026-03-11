import math
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from core.database import get_session
from schemas.base_schemas import GenericResponse, PaginationMeta
from schemas.history_schemas import (
    MedicalTreatmentCreate,
    MedicalTreatmentPublic,
    MedicalTreatmentUpdate,
)
from services.history_service import medical_treatment_service

router = APIRouter(prefix="/medical-treatments", tags=["Medical Treatments"])

@router.get("/", response_model=GenericResponse[List[MedicalTreatmentPublic]])
def read_medical_treatments(*, db: Session = Depends(get_session), skip: int = 0, limit: int = 100):
    treatments, total_count = medical_treatment_service.get_all(db, skip=skip, limit=limit)

    current_page = (skip // limit) + 1
    total_pages = math.ceil(total_count / limit) if limit > 0 else 1

    meta = PaginationMeta(
        total_records=total_count,
        current_page=current_page,
        total_pages=total_pages,
        next_page=(current_page + 1) if (skip + limit) < total_count else None,
        prev_page=(current_page - 1) if skip > 0 else None
    )

    return GenericResponse(message="Medical Treatments retrieved successfully.", data=treatments, meta=meta)

@router.post("/", response_model=GenericResponse[MedicalTreatmentPublic])
def create_medical_treatment(*, db: Session = Depends(get_session), obj_in: MedicalTreatmentCreate):
    try:
        treatment = medical_treatment_service.create(db, obj_in=obj_in)
        return GenericResponse(message="Medical Treatment created successfully.", data=treatment)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/{mt_id}", response_model=GenericResponse[MedicalTreatmentPublic])
def read_medical_treatment(mt_id: str, db: Session = Depends(get_session)):
    treatment = medical_treatment_service.get_by_mt_id(db, mt_id=mt_id)
    if not treatment:
        raise HTTPException(status_code=404, detail="Medical Treatment record not found.")

@router.get("/patient/{patient_id}", response_model=GenericResponse[List[MedicalTreatmentPublic]])
def read_patient_treatments(patient_id: str, db: Session = Depends(get_session)):
    treatments= medical_treatment_service.get_by_patient_id(db, patient_id=patient_id)
    return GenericResponse(message="Patient's Medical Treatment records retrieved successfully.", data=treatments)

@router.patch("/{mt_id}", response_model=GenericResponse[MedicalTreatmentPublic])
def update_medical_treatment(mt_id: str, obj_in: MedicalTreatmentUpdate, db: Session = Depends(get_session)):
    db_obj = medical_treatment_service.get_by_mt_id(db, mt_id=mt_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Medical Treatment record not found.")

    treatment = medical_treatment_service.update(db, db_obj=db_obj, obj_in=obj_in)
    return GenericResponse(message="Medical Treatment record updated successfully.", data=treatment)

@router.delete("/{mt_id}", response_model=GenericResponse[MedicalTreatmentPublic])
def delete_medical_treatment(mt_id: str, db: Session = Depends(get_session)):
    db_obj = medical_treatment_service.get_by_mt_id(db, mt_id=mt_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Medical Treatment record not found.")

    treatment = medical_treatment_service.remove(db, uuid=db_obj.uuid)
    return GenericResponse(message="Medical Treatment record deleted successfully.", data=treatment)

@router.post("/{mt_id}/restore", response_model=GenericResponse[MedicalTreatmentPublic])
def restore_medical_treatment(
    mt_id: str,
    db: Session = Depends(get_session)
):
    db_obj = medical_treatment_service.get_by_mt_id(db, mt_id=mt_id, include_deleted=True)

    if not db_obj:
        raise HTTPException(status_code=404, detail="Medical treatment not found")
        
    if not db_obj.is_deleted:
        raise HTTPException(status_code=400, detail="Medical treatment is not deleted")

    restored_treatment = medical_treatment_service.restore(db, uuid=db_obj.uuid)
    return GenericResponse(message="Medical treatment restored successfully", data=restored_treatment)
