from typing import List
from schemas.history_schemas import MedicalExaminationUpdate
from schemas.history_schemas import MedicalExaminationCreate
from services.history_service import medical_examination_service
from core.database import get_session
from sqlmodel import Session
from schemas.history_schemas import MedicalExaminationPublic
from schemas.base_schemas import GenericResponse
from fastapi import APIRouter, Depends, HTTPException

router = APIRouter(prefix="/medical_examinations", tags=["Medical Examination"])

@router.get("/", response_model=GenericResponse[List[MedicalExaminationPublic]])
def read_all_medical_examinations(db: Session = Depends(get_session), skip: int = 0, limit: int = 0):
    get_all_examinations = medical_examination_service.get_all(db, skip=skip, limit=limit)
    return GenericResponse(message="All Medical Examinations Retrieved Successfully", data=get_all_examinations)

@router.post("/", response_model=GenericResponse[MedicalExaminationPublic])
def create_medical_examination(examination_in: MedicalExaminationCreate, db: Session = Depends(get_session)):
    try:
        new_examination = medical_examination_service.create(db, obj_in=examination_in)
        return GenericResponse(message="Medical Examination created successfully", data=new_examination)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/{patient_id}", response_model=GenericResponse[List[MedicalExaminationPublic]])
def read_medical_examination_by_patient(patient_id: str, db: Session = Depends(get_session)):
    examinations = medical_examination_service.get_by_patient_id(db, patient_id=patient_id)
    if not examinations:
        raise HTTPException(status_code=404, detail="No Medical Examinations found for this patient")

@router.patch("/{me_id}", response_model=GenericResponse[MedicalExaminationPublic])
def update_medical_examination(me_id: str, examination_out: MedicalExaminationUpdate, db: Session = Depends(get_session)):
    db_obj = medical_examination_service.get_by_me_id(db, me_id=me_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Specific Medical Examination not found")

    update_examination = medical_examination_service.update(db, db_obj=db_obj, obj_in=examination_out)
    return GenericResponse(message="Medical Examination updated succcessfully", data=update_examination)


@router.delete("/{me_id}", response_model=GenericResponse[MedicalExaminationPublic])
def delete_medical_examination(me_id: str, db: Session = Depends(get_session)):
    db_obj = medical_examination_service.get_by_me_id(db, me_id=me_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Specific Medical Examination record not found")

    medical_examination_service.remove(db, uuid=db_obj.uuid)
    return GenericResponse(message="Medical Record deleted successfully")