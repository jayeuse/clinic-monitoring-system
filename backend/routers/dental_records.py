import math
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from core.database import get_session
from schemas.base_schemas import GenericResponse, PaginationMeta
from schemas.dental_schemas import (
    DentalRecordCreate,
    DentalRecordPublic,
    DentalRecordUpdate,
)
from services.dental_service import dental_record_service

router = APIRouter(prefix="/dental_records", tags=["Dental Records"])

@router.get("/", response_model=GenericResponse[List[DentalRecordPublic]])
def read_all_dental_records(skip: int = 0, limit: int = 100, db: Session = Depends(get_session)):
    records, total_count = dental_record_service.get_all(db, skip=skip, limit=limit)

    current_page = (skip // limit) + 1
    total_pages = math.ceil(total_count / limit) if limit > 0 else 1

    meta = PaginationMeta(
        total_records=total_count,
        current_page=current_page,
        total_pages=total_pages,
        next_page=(current_page + 1) if (skip + limit) < total_count else None,
        prev_page=(current_page - 1) if skip > 0 else None
    )
    
    return GenericResponse(message="All Dental Records retrieved successfully", data=records, meta=meta)

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

@router.post("/{patient_id}/restore", response_model=GenericResponse[DentalRecordPublic])
def restore_dental_record(
    patient_id: str,
    db: Session = Depends(get_session)
):
    db_obj = dental_record_service.get_by_patient_id(db, patient_id=patient_id, include_deleted=True)

    if not db_obj:
        raise HTTPException(status_code=404, detail="Dental record not found")
        
    if not db_obj.is_deleted:
        raise HTTPException(status_code=400, detail="Dental record is not deleted")

    restored_record = dental_record_service.restore(db, uuid=db_obj.uuid)
    return GenericResponse(message="Dental record restored successfully", data=restored_record)
