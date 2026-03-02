from services.dental_service import dental_record_service
from schemas.dental_schemas import DentalRecordPublic
from services.dental_service import treatment_service
from schemas.dental_schemas import DentalTreatmentCreate
from schemas.dental_schemas import DentalTreatmentPublic
from fastapi import HTTPException
from services.dental_service import examination_service
from core.database import get_session
from fastapi import Depends
from sqlmodel import Session
from schemas.dental_schemas import DentalExaminationCreate
from schemas.dental_schemas import DentalExaminationPublic
from schemas.base_schemas import GenericResponse
from fastapi import APIRouter
router = APIRouter(prefix="/dental_record", tags=["Dental Records"])

@router.post("/exams/", response_model=GenericResponse[DentalExaminationPublic])
def record_dental_examination(exam_in: DentalExaminationCreate, db: Session = Depends(get_session)):
    try:
        new_exam = examination_service.record_exam(db, obj_in=exam_in)
        return GenericResponse(message="Dental Examination and Tooth Findings recorded successfully", data=new_exam)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/treatments/", response_model=GenericResponse[DentalTreatmentPublic])
def record_dental_treatment(treatment_in: DentalTreatmentCreate, db: Session = Depends(get_session)):
    try:
        new_treatment = treatment_service.log_treatment(db, obj_in=treatment_in)
        return GenericResponse(message="Dental Treatment recorded successfully", data=new_treatment)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/record/{patient_id}", response_model=GenericResponse[DentalRecordPublic])
def get_patient_dental_record(patient_id: str, db: Session = Depends(get_session)):
    dental_record = dental_record_service.get_by_patient_id(db, patient_id=patient_id)
    if not dental_record:
        raise HTTPException(status_code=404, detail="No Dental Record found from this patient")

    return GenericResponse(message="Dental Record retrieved successfully", data=dental_record)