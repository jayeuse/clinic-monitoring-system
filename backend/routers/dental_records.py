from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from core.database import get_session
from schemas.base_schemas import GenericResponse
from schemas.dental_schemas import DentalRecordPublic
from services.dental_service import dental_record_service

router = APIRouter(prefix="/dental_records", tags=["Dental Records"])

@router.get("/{patient_id}", response_model=GenericResponse[DentalRecordPublic])
def read_dental_record(patient_id: str, db: Session = Depends(get_session)):
    dental_record = dental_record_service.get_by_patient_id(db, patient_id=patient_id)
    if not dental_record:
        raise HTTPException(status_code=404, detail="No Dental Record found for this patient")

    return GenericResponse(message="Dental Record retrieved successfully", data=dental_record)
