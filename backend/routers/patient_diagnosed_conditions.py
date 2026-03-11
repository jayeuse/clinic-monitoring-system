import math
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from core.database import get_session
from schemas.base_schemas import GenericResponse, PaginationMeta
from schemas.history_schemas import (
    PatientDiagnosedConditionsCreate,
    PatientDiagnosedConditionsPublic,
    PatientDiagnosedConditionsUpdate,
)
from services.history_service import patient_diagnosed_conditions_service

router = APIRouter(prefix="/patient-diagnosed-conditions", tags=["Patient Diagnosed Conditions"])

@router.get("/", response_model=GenericResponse[List[PatientDiagnosedConditionsPublic]])
def read_patient_diagnosed_conditions(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_session)
):
    conditions, total_count = patient_diagnosed_conditions_service.get_all(db, skip=skip, limit=limit)

    current_page = (skip // limit) + 1
    total_pages = math.ceil(total_count / limit) if limit > 0 else 1

    meta = PaginationMeta(
        total_records=total_count,
        current_page=current_page,
        total_pages=total_pages,
        next_page=(current_page + 1) if (skip + limit) < total_count else None,
        prev_page=(current_page - 1) if skip > 0 else None
    )

    return GenericResponse(message="Patient Diagnosed Conditions retrieved successfully", data=conditions, meta=meta)

@router.post("/", response_model=GenericResponse[PatientDiagnosedConditionsPublic])
def create_patient_diagnosed_condition(
    mh_id: str,
    condition_in: PatientDiagnosedConditionsCreate,
    db: Session = Depends(get_session)
):
    try:
        new_condition = patient_diagnosed_conditions_service.create(db, obj_in=condition_in, mh_id=mh_id)
        return GenericResponse(message="Patient Diagnosed Condition created successfully", data=new_condition)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/medical-history/{mh_id}", response_model=GenericResponse[List[PatientDiagnosedConditionsPublic]])
def read_diagnosed_conditions_by_mh_id(
    mh_id: str,
    db: Session = Depends(get_session)
):
    conditions = patient_diagnosed_conditions_service.get_by_mh_id(db, mh_id=mh_id)
    return GenericResponse(message="Medical History's Diagnosed Conditions retrieved successfully", data=conditions)

@router.get("/{pdc_id}", response_model=GenericResponse[PatientDiagnosedConditionsPublic])
def read_patient_diagnosed_condition_by_id(
    pdc_id: str,
    db: Session = Depends(get_session)
):
    condition = patient_diagnosed_conditions_service.get_by_pdc_id(db, pdc_id=pdc_id)
    if not condition:
        raise HTTPException(status_code=404, detail="Patient Diagnosed Condition not found")

    return GenericResponse(message="Patient Diagnosed Condition retrieved successfully", data=condition)

@router.patch("/{pdc_id}", response_model=GenericResponse[PatientDiagnosedConditionsPublic])
def update_patient_diagnosed_condition(
    pdc_id: str,
    condition_in: PatientDiagnosedConditionsUpdate,
    db: Session = Depends(get_session)
):
    db_obj = patient_diagnosed_conditions_service.get_by_pdc_id(db, pdc_id=pdc_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Patient Diagnosed Condition not found")

    try:
        updated_condition = patient_diagnosed_conditions_service.update(db, db_obj=db_obj, obj_in=condition_in)
        return GenericResponse(message="Patient Diagnosed Condition updated successfully", data=updated_condition)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/{pdc_id}", response_model=GenericResponse[PatientDiagnosedConditionsPublic])
def delete_patient_diagnosed_condition(
    pdc_id: str,
    db: Session = Depends(get_session)
):
    db_obj = patient_diagnosed_conditions_service.get_by_pdc_id(db, pdc_id=pdc_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Patient Diagnosed Condition not found")

    deleted_condition = patient_diagnosed_conditions_service.remove(db, uuid=db_obj.uuid)
    return GenericResponse(message="Patient Diagnosed Condition deleted successfully", data=deleted_condition)

@router.post("/{pdc_id}/restore", response_model=GenericResponse[PatientDiagnosedConditionsPublic])
def restore_patient_diagnosed_condition(
    pdc_id: str,
    db: Session = Depends(get_session)
):
    db_obj = patient_diagnosed_conditions_service.get_by_pdc_id(db, pdc_id=pdc_id, include_deleted=True)

    if not db_obj:
        raise HTTPException(status_code=404, detail="Patient Diagnosed Condition not found")
        
    if not db_obj.is_deleted:
        raise HTTPException(status_code=400, detail="Patient Diagnosed Condition is not deleted")

    restored_condition = patient_diagnosed_conditions_service.restore(db, uuid=db_obj.uuid)
    return GenericResponse(message="Patient Diagnosed Condition restored successfully", data=restored_condition)

