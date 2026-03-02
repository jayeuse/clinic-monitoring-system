from typing import List
from schemas.dental_schemas import DentalTreatmentUpdate
from schemas.dental_schemas import DentalExaminationUpdate
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

@router.get("/", response_model=GenericResponse[List[DentalExaminationPublic]])
def read_dental_records(db: Session = Depends(get_session)):
    get_all_medical_records = examination_service.get_all(db)
    return GenericResponse(message="All Dental Records retrieved successfully", data=get_all_medical_records)

@router.post("/", response_model=GenericResponse[DentalExaminationPublic])
def record_dental_examination(exam_in: DentalExaminationCreate, db: Session = Depends(get_session)):
    try:
        new_exam = examination_service.record_exam(db, obj_in=exam_in)
        return GenericResponse(message="Dental Examination and Tooth Findings recorded successfully", data=new_exam)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/{patient_id}", response_model=GenericResponse[DentalRecordPublic])
def read_dental_record(patient_id: str, db: Session = Depends(get_session)):
    get_dental_record = dental_record_service.get_by_patient_id(db, patient_id=patient_id)
    if not get_dental_record:
        raise HTTPException(status_code=404, detail="No Dental Record found from this patient")

    return GenericResponse(message="Dental Record retrieved successfully", data=get_dental_record)

@router.patch("/{dru_id}", response_model=GenericResponse[DentalExaminationPublic])
def update_dental_record(dru_id: str, obj_in: DentalExaminationUpdate, db: Session = Depends(get_session)):
    db_obj = examination_service.get_by_dru_id(db, dru_id=dru_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Dental Record not found")
    
    update_dental_record = examination_service.update(db, db_obj=db_obj, obj_in=obj_in)
    
    return GenericResponse(message="Dental Record updated successfully", data=update_dental_record)

@router.delete("/{dru_id}", response_model=GenericResponse[DentalExaminationPublic])
def delete_dental_record(dru_id: str, db: Session = Depends(get_session)):
    db_obj = examination_service.get_by_dru_id(db, dru_id=dru_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Dental Record not found")

    delete_dental_recordd = examination_service.remove(db, uuid=db_obj.uuid) #dont mind the typo

    return GenericResponse(message="Dental Record deleted successfully", data=delete_dental_recordd)

@router.get("/render_service/", response_model=GenericResponse[List[DentalTreatmentPublic]])
def read_dental_services(db: Session = Depends(get_session)):
    rendered_services = treatment_service.get_all(db)

    return GenericResponse(message="All Rendered Dental Services retrieved successfully", data=rendered_services)

@router.post("/render_service/", response_model=GenericResponse[DentalTreatmentPublic])
def record_dental_service(treatment_in: DentalTreatmentCreate, db: Session = Depends(get_session)):
    try:
        new_dental_service = treatment_service.log_treatment(db, obj_in=treatment_in)
        return GenericResponse(message="Dental Service rendered successfully", data=new_dental_service)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.patch("/render_service/{dsr_id}", response_model=GenericResponse[DentalTreatmentPublic])
def update_dental_service(dsr_id: str, obj_in: DentalTreatmentUpdate, db: Session = Depends(get_session)):
    db_obj = treatment_service.get_by_dsr_id(db, dsr_id=dsr_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Rendered Dental Service not found")

    update_dental_service = treatment_service.update(db, db_obj=db_obj, obj_in=obj_in)

    return GenericResponse(message="Dental Service updated successfully", data=update_dental_service)

@router.delete("/render_service/{dsr_id}", response_model=GenericResponse[DentalTreatmentPublic])
def delete_dental_service(dsr_id: str, db: Session = Depends(get_session)):
    db_obj = treatment_service.get_by_dsr_id(db, dsr_id=dsr_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Rendered Dental Service not found")

    treatment_service.remove(db, uuid=db_obj.uuid)

    return GenericResponse(message="Dental Service deleted successfully")