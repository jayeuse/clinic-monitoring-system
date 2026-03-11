from schemas.dental_schemas import DentalRecordCreate
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from core.database import get_session
from schemas.base_schemas import GenericResponse
from schemas.dental_schemas import DentalRecordPublic, DentalRecordUpdate
from services.dental_service import dental_record_service
from typing import List

router = APIRouter(prefix="/dental_records", tags=["Dental Records"])

@router.get("/", response_model=GenericResponse[List[DentalRecordPublic]])
def read_all_dental_records(skip: int = 0, limit: int = 100, db: Session = Depends(get_session)):
    records = dental_record_service.get_all(db, skip=skip, limit=limit)
    return GenericResponse(message="All Dental Records retrieved successfully", data=records)

@router.get("/{patient_id}", response_model=GenericResponse[DentalRecordPublic])
def read_dental_record(patient_id: str, db: Session = Depends(get_session)):
    dental_record = dental_record_service.get_by_patient_id(db, patient_id=patient_id)
    if not dental_record:
        raise HTTPException(status_code=404, detail="No Dental Record found for this patient")

    return GenericResponse(message="Dental Record retrieved successfully", data=dental_record)

@router.post("/", response_model=GenericResponse[DentalRecordPublic])
def record_dental_record(obj_in: DentalRecordCreate, db: Session = Depends(get_session)):
    try:
        new_record = dental_record_service.create(db, obj_in=obj_in)
        return GenericResponse(message="Dental Record created successfully", data=new_record)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.patch("/{patient_id}", response_model=GenericResponse[DentalRecordPublic])
def update_dental_record(patient_id: str, obj_in: DentalRecordUpdate, db: Session = Depends(get_session)):
    db_obj = dental_record_service.get_by_patient_id(db, patient_id=patient_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Dental Record not found")

    updated = dental_record_service.update(db, db_obj=db_obj, obj_in=obj_in)
    return GenericResponse(message="Dental Record updated successfully", data=updated)

@router.delete("/{patient_id}", response_model=GenericResponse[DentalRecordPublic])
def delete_dental_record(patient_id: str, db: Session = Depends(get_session)):
    
    db_obj = dental_record_service.get_by_patient_id(db, patient_id=patient_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Dental Record not found")

    deleted_record = dental_record_service.remove(db, uuid=db_obj.uuid)
    return GenericResponse(message="Dental Record deleted successfully", data=deleted_record)