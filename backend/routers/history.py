from schemas.history_schemas import MedicalHistoryUpdate
from fastapi import HTTPException
from services.history_service import history_service
from schemas.history_schemas import MedicalHistoryPublic
from core.database import get_session
from fastapi import Depends
from sqlmodel import Session
from schemas.history_schemas import MedicalHistoryCreate
from fastapi import APIRouter
router = APIRouter(prefix="/history", tags=["Medical History"])

@router.post("/", response_model=MedicalHistoryPublic)
def create_medical_history(history_in: MedicalHistoryCreate, db: Session = Depends(get_session)):
    try:
        return history_service.create(db, obj_in=history_in)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/{patient_id}", response_model=MedicalHistoryPublic)
def read_medical_history(patient_id: str, db: Session = Depends(get_session)):

    history = history_service.get_by_patient_id(db, patient_id=patient_id)
    if not history:
        raise HTTPException(status_code=404, detail="Medical History not found for this patient")

    return history

@router.patch("/{patient_id}", response_model=MedicalHistoryPublic)
def update_medical_history(patient_id: str, history_out: MedicalHistoryUpdate, db: Session = Depends(get_session)):
    db_obj = history_service.get_by_patient_id(db, patient_id=patient_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Medical History not found for this patient")
    
    return history_service.update(db, db_obj=db_obj, obj_in=history_out)

@router.delete("/{patient_id}", response_model=MedicalHistoryPublic)
def delete_medical_history(patient_id: str, db: Session = Depends(get_session)):
    db_obj = history_service.get_by_patient_id(db, patient_id=patient_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Medical History not found for this patient")

    return history_service.remove(db, uuid=db_obj.uuid)