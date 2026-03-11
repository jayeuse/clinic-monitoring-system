from schemas.dental_schemas import ToothFindingPublic
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from core.database import get_session
from schemas.base_schemas import GenericResponse
from schemas.dental_schemas import (
    DentalExaminationCreate,
    DentalExaminationUpdate,
    DentalExaminationPublic,
    DentalTreatmentCreate,
    DentalTreatmentUpdate,
    DentalTreatmentPublic,
)
from services.dental_service import examination_service, treatment_service

router = APIRouter(prefix="/dental_examinations", tags=["Dental Examinations"])

@router.get("/", response_model=GenericResponse[List[DentalExaminationPublic]])
def read_dental_examinations(db: Session = Depends(get_session)):
    examinations = examination_service.get_all(db)
    return GenericResponse(message="All Dental Examinations retrieved successfully", data=examinations)

@router.post("/", response_model=GenericResponse[DentalExaminationPublic])
def record_dental_examination(exam_in: DentalExaminationCreate, db: Session = Depends(get_session)):
    try:
        new_exam = examination_service.record_exam(db, obj_in=exam_in)
        return GenericResponse(message="Dental Examination and Tooth Findings recorded successfully", data=new_exam)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.patch("/{dru_id}", response_model=GenericResponse[DentalExaminationPublic])
def update_dental_examination(dru_id: str, obj_in: DentalExaminationUpdate, db: Session = Depends(get_session)):
    db_obj = examination_service.get_by_dru_id(db, dru_id=dru_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Dental Examination not found")

    updated = examination_service.update(db, db_obj=db_obj, obj_in=obj_in)
    return GenericResponse(message="Dental Examination updated successfully", data=updated)

@router.delete("/{dru_id}", response_model=GenericResponse[DentalExaminationPublic])
def delete_dental_examination(dru_id: str, db: Session = Depends(get_session)):
    db_obj = examination_service.get_by_dru_id(db, dru_id=dru_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Dental Examination not found")

    deleted = examination_service.remove(db, uuid=db_obj.uuid)
    return GenericResponse(message="Dental Examination deleted successfully", data=deleted)

@router.get("/{dru_id}/findings", response_model=GenericResponse[List[ToothFindingPublic]])
def read_examination_findings(dru_id: str, db: Session = Depends(get_session)):
    try:
        findings = examination_service.get_findings_by_exam(db, dru_id=dru_id)
        return GenericResponse(message="Tooth findings retrieved successfully", data=findings)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/treatments/", response_model=GenericResponse[List[DentalTreatmentPublic]])
def read_dental_treatments(db: Session = Depends(get_session)):
    treatments = treatment_service.get_all(db)
    return GenericResponse(message="All Dental Treatments retrieved successfully", data=treatments)

@router.post("/treatments/", response_model=GenericResponse[DentalTreatmentPublic])
def record_dental_treatment(treatment_in: DentalTreatmentCreate, db: Session = Depends(get_session)):
    try:
        new_treatment = treatment_service.log_treatment(db, obj_in=treatment_in)
        return GenericResponse(message="Dental Treatment recorded successfully", data=new_treatment)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.patch("/treatments/{dsr_id}", response_model=GenericResponse[DentalTreatmentPublic])
def update_dental_treatment(dsr_id: str, obj_in: DentalTreatmentUpdate, db: Session = Depends(get_session)):
    db_obj = treatment_service.get_by_dsr_id(db, dsr_id=dsr_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Dental Treatment not found")

    updated = treatment_service.update(db, db_obj=db_obj, obj_in=obj_in)
    return GenericResponse(message="Dental Treatment updated successfully", data=updated)

@router.delete("/treatments/{dsr_id}", response_model=GenericResponse[DentalTreatmentPublic])
def delete_dental_treatment(dsr_id: str, db: Session = Depends(get_session)):
    db_obj = treatment_service.get_by_dsr_id(db, dsr_id=dsr_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Dental Treatment not found")

    treatment_service.remove(db, uuid=db_obj.uuid)
    return GenericResponse(message="Dental Treatment deleted successfully")