from typing import List
from schemas.base_schemas import GenericResponse
from schemas.history_schemas import MedicalHistoryUpdate
from fastapi import HTTPException
from services.history_service import history_service
from schemas.history_schemas import MedicalHistoryPublic
from core.database import get_session
from fastapi import Depends
from sqlmodel import Session
from schemas.history_schemas import MedicalHistoryCreate
from fastapi import APIRouter

router = APIRouter(prefix="/medical_history", tags=["Medical History"])

@router.get("/", response_model=GenericResponse[List[MedicalHistoryPublic]])
def read_all_medical_histories(db: Session = Depends(get_session), skip: int = 0, limit: int = 100):
    get_all_medical_records = history_service.get_all(db, skip=skip, limit=limit)
    return GenericResponse(message="All Medical Records retrieved successfully", data=get_all_medical_records)

@router.post("/", response_model=GenericResponse[MedicalHistoryPublic])
def create_medical_history(history_in: MedicalHistoryCreate, db: Session = Depends(get_session)):
    try:
        new_medical_record = history_service.create(db, obj_in=history_in)
        return GenericResponse(message="Medical Record created successfully", data=new_medical_record)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/{patient_id}", response_model=GenericResponse[MedicalHistoryPublic])
def read_medical_history(patient_id: str, db: Session = Depends(get_session)):

    get_medical_record = history_service.get_by_patient_id(db, patient_id=patient_id)
    if not get_medical_record:
        raise HTTPException(status_code=404, detail="Medical History not found for this patient")

    return GenericResponse(message="Medical History retrieved successfully", data=get_medical_record)

@router.patch("/{patient_id}", response_model=GenericResponse[MedicalHistoryPublic])
def update_medical_history(patient_id: str, history_out: MedicalHistoryUpdate, db: Session = Depends(get_session)):
    db_obj = history_service.get_by_patient_id(db, patient_id=patient_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Medical History not found for this patient")
    
    update_medical_record = history_service.update(db, db_obj=db_obj, obj_in=history_out)
    return GenericResponse(message="Medical Record updated successfully", data=update_medical_record)

@router.delete("/{patient_id}", response_model=GenericResponse[MedicalHistoryPublic])
def delete_medical_history(patient_id: str, db: Session = Depends(get_session)):
    db_obj = history_service.get_by_patient_id(db, patient_id=patient_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Medical History not found for this patient")

    delete_medical_record = history_service.remove(db, uuid=db_obj.uuid)
    return GenericResponse(message="Medical Record deleted successfully", data=delete_medical_record)