from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from core.database import get_session
from schemas.base_schemas import GenericResponse
from schemas.history_schemas import (
    MedicalHistoryCreate,
    MedicalHistoryPublic,
    MedicalHistoryUpdate,
)
from services.history_service import history_service

router = APIRouter(prefix="/medical_history", tags=["Medical History"])


@router.get("/", response_model=GenericResponse[List[MedicalHistoryPublic]])
def read_all_medical_histories(
    db: Session = Depends(get_session), skip: int = 0, limit: int = 100
):
    get_all_medical_records = history_service.get_all(db, skip=skip, limit=limit)
    return GenericResponse(
        message="All Medical Records retrieved successfully",
        data=get_all_medical_records,
    )


@router.post("/", response_model=GenericResponse[MedicalHistoryPublic])
def create_medical_history(
    history_in: MedicalHistoryCreate, db: Session = Depends(get_session)
):
    try:
        new_medical_record = history_service.create(db, obj_in=history_in)
        return GenericResponse(
            message="Medical Record created successfully", data=new_medical_record
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/{patient_id}", response_model=GenericResponse[List[MedicalHistoryPublic]])
def read_medical_history(patient_id: str, db: Session = Depends(get_session)):
    get_medical_records = history_service.get_by_patient_id(db, patient_id=patient_id)
    if not get_medical_records:
        raise HTTPException(
            status_code=404, detail="No Medical History found for this patient"
        )

    return GenericResponse(
        message="Medical Histories retrieved successfully", data=get_medical_records
    )


@router.patch("/{mh_id}", response_model=GenericResponse[MedicalHistoryPublic])
def update_medical_history(
    mh_id: str, history_out: MedicalHistoryUpdate, db: Session = Depends(get_session)
):
    db_obj = history_service.get_by_mh_id(db, mh_id=mh_id)
    if not db_obj:
        raise HTTPException(
            status_code=404, detail="Specific Medical History record not found"
        )

    update_medical_record = history_service.update(
        db, db_obj=db_obj, obj_in=history_out
    )
    return GenericResponse(
        message="Medical Record updated successfully", data=update_medical_record
    )


@router.delete("/{mh_id}", response_model=GenericResponse)
def delete_medical_history(mh_id: str, db: Session = Depends(get_session)):
    db_obj = history_service.get_by_mh_id(db, mh_id=mh_id)
    if not db_obj:
        raise HTTPException(
            status_code=404, detail="Specific Medical History record not found"
        )

    history_service.remove(db, uuid=db_obj.uuid)
    return GenericResponse(message="Medical Record deleted successfully")
