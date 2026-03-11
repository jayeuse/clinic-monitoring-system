import math
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from core.database import get_session
from schemas.base_schemas import GenericResponse, PaginationMeta
from schemas.history_schemas import (
    PatientFamilyHistoryCreate,
    PatientFamilyHistoryPublic,
    PatientFamilyHistoryUpdate,
)
from services.history_service import patient_family_history_service

router = APIRouter(prefix="/patient-family-history", tags=["Patient Family History"])

@router.get("/", response_model=GenericResponse[List[PatientFamilyHistoryPublic]])
def read_patient_family_histories(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_session)
):
    histories, total_count = patient_family_history_service.get_all(db, skip=skip, limit=limit)

    current_page = (skip // limit) + 1
    total_pages = math.ceil(total_count / limit) if limit > 0 else 1

    meta = PaginationMeta(
        total_records=total_count,
        current_page=current_page,
        total_pages=total_pages,
        next_page=(current_page + 1) if (skip + limit) < total_count else None,
        prev_page=(current_page - 1) if skip > 0 else None
    )

    return GenericResponse(message="Patient Family Histories retrieved successfully", data=histories, meta=meta)

@router.post("/", response_model=GenericResponse[PatientFamilyHistoryPublic])
def create_patient_family_history(
    mh_id: str,
    history_in: PatientFamilyHistoryCreate,
    db: Session = Depends(get_session)
):
    try:
        new_history = patient_family_history_service.create(db, obj_in=history_in, mh_id=mh_id)
        return GenericResponse(message="Patient Family History created successfully", data=new_history)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/medical-history/{mh_id}", response_model=GenericResponse[List[PatientFamilyHistoryPublic]])
def read_family_histories_by_mh_id(
    mh_id: str,
    db: Session = Depends(get_session)
):
    histories = patient_family_history_service.get_by_mh_id(db, mh_id=mh_id)
    return GenericResponse(message="Medical History's Family Histories retrieved successfully", data=histories)

@router.get("/{pfh_id}", response_model=GenericResponse[PatientFamilyHistoryPublic])
def read_patient_family_history_by_id(
    pfh_id: str,
    db: Session = Depends(get_session)
):
    history = patient_family_history_service.get_by_pfh_id(db, pfh_id=pfh_id)
    if not history:
        raise HTTPException(status_code=404, detail="Patient Family History not found")

    return GenericResponse(message="Patient Family History retrieved successfully", data=history)

@router.patch("/{pfh_id}", response_model=GenericResponse[PatientFamilyHistoryPublic])
def update_patient_family_history(
    pfh_id: str,
    history_in: PatientFamilyHistoryUpdate,
    db: Session = Depends(get_session)
):
    db_obj = patient_family_history_service.get_by_pfh_id(db, pfh_id=pfh_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Patient Family History not found")

    try:
        updated_history = patient_family_history_service.update(db, db_obj=db_obj, obj_in=history_in)
        return GenericResponse(message="Patient Family History updated successfully", data=updated_history)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/{pfh_id}", response_model=GenericResponse[PatientFamilyHistoryPublic])
def delete_patient_family_history(
    pfh_id: str,
    db: Session = Depends(get_session)
):
    db_obj = patient_family_history_service.get_by_pfh_id(db, pfh_id=pfh_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Patient Family History not found")

    deleted_history = patient_family_history_service.remove(db, uuid=db_obj.uuid)
    return GenericResponse(message="Patient Family History deleted successfully", data=deleted_history)
