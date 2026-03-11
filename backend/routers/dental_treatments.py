import math
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from core.database import get_session
from schemas.base_schemas import GenericResponse, PaginationMeta
from schemas.dental_schemas import (
    DentalTreatmentCreate,
    DentalTreatmentPublic,
    DentalTreatmentUpdate,
)
from services.dental_service import treatment_service

router = APIRouter(prefix="/dental-treatments", tags=["Dental Treatments"])

@router.get("/", response_model=GenericResponse[List[DentalTreatmentPublic]])
def read_dental_treatments(skip: int = 0, limit: int = 100, db: Session = Depends(get_session)):
    treatments, total_count = treatment_service.get_all(db, skip=skip, limit=limit)

    current_page = (skip // limit) + 1
    total_pages = math.ceil(total_count / limit) if limit > 0 else 1

    meta = PaginationMeta(
        total_records=total_count,
        current_page=current_page,
        total_pages=total_pages,
        next_page=(current_page + 1) if (skip + limit) < total_count else None,
        prev_page=(current_page - 1) if skip > 0 else None
    )
    return GenericResponse(message="All Dental Treatments retrieved successfully", data=treatments, meta=meta)

@router.post("/", response_model=GenericResponse[DentalTreatmentPublic])
def record_dental_treatment(treatment_in: DentalTreatmentCreate, db: Session = Depends(get_session)):
    try:
        new_treatment = treatment_service.log_treatment(db, obj_in=treatment_in)
        return GenericResponse(message="Dental Treatment recorded successfully", data=new_treatment)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/patient/{patient_id}", response_model=GenericResponse[List[DentalTreatmentPublic]])
def read_patient_treatments(patient_id: str, db: Session = Depends(get_session)):
    treatments = treatment_service.get_by_patient_id(db, patient_id=patient_id)
    return GenericResponse(message="Patient's Dental Treatments retrieved successfully", data=treatments)

@router.patch("/{dsr_id}", response_model=GenericResponse[DentalTreatmentPublic])
def update_dental_treatment(dsr_id: str, obj_in: DentalTreatmentUpdate, db: Session = Depends(get_session)):
    db_obj = treatment_service.get_by_dsr_id(db, dsr_id=dsr_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Dental Treatment not found")

    updated = treatment_service.update(db, db_obj=db_obj, obj_in=obj_in)
    return GenericResponse(message="Dental Treatment updated successfully", data=updated)

@router.delete("/{dsr_id}", response_model=GenericResponse[DentalTreatmentPublic])
def delete_dental_treatment(dsr_id: str, db: Session = Depends(get_session)):
    db_obj = treatment_service.get_by_dsr_id(db, dsr_id=dsr_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Dental Treatment not found")

    treatment_service.remove(db, uuid=db_obj.uuid)
    return GenericResponse(message="Dental Treatment deleted successfully")

@router.post("/{dsr_id}/restore", response_model=GenericResponse[DentalTreatmentPublic])
def restore_dental_treatment(
    dsr_id: str,
    db: Session = Depends(get_session)
):
    db_obj = treatment_service.get_by_dsr_id(db, dsr_id=dsr_id, include_deleted=True)

    if not db_obj:
        raise HTTPException(status_code=404, detail="Dental treatment not found")
        
    if not db_obj.is_deleted:
        raise HTTPException(status_code=400, detail="Dental treatment is not deleted")

    restored_treatment = treatment_service.restore(db, uuid=db_obj.uuid)
    return GenericResponse(message="Dental treatment restored successfully", data=restored_treatment)
