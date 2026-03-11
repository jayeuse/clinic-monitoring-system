import math
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from core.database import get_session
from schemas.base_schemas import GenericResponse, PaginationMeta
from schemas.dental_schemas import (
    DentalExaminationCreate,
    DentalExaminationPublic,
    DentalExaminationUpdate,
    ToothFindingPublic,
)
from services.dental_service import examination_service

router = APIRouter(prefix="/dental_examinations", tags=["Dental Examinations"])

@router.get("/", response_model=GenericResponse[List[DentalExaminationPublic]])
def read_dental_examinations(skip: int = 0, limit: int = 100,db: Session = Depends(get_session)):
    examinations, total_count = examination_service.get_all(db, skip=skip, limit=limit)

    current_page = (skip // limit) + 1
    total_pages = math.ceil(total_count / limit) if limit > 0 else 1

    meta = PaginationMeta(
        total_records=total_count,
        current_page=current_page,
        total_pages=total_pages,
        next_page=(current_page + 1) if (skip + limit) < total_count else None,
        prev_page=(current_page - 1) if skip > 0 else None
    )

    return GenericResponse(message="All Dental Examinations retrieved successfully", data=examinations, meta=meta)

@router.post("/", response_model=GenericResponse[DentalExaminationPublic])
def record_dental_examination(exam_in: DentalExaminationCreate, db: Session = Depends(get_session)):
    try:
        new_exam = examination_service.record_exam(db, obj_in=exam_in)
        return GenericResponse(message="Dental Examination and Tooth Findings recorded successfully", data=new_exam)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/patient/{patient_id}", response_model=GenericResponse[List[DentalExaminationPublic]])
def read_patient_examinations(patient_id: str, db: Session = Depends(get_session)):
    examinations = examination_service.get_by_patient_id(db, patient_id=patient_id)
    return GenericResponse(message="Patient's Dental Examinations retrieved successfully", data=examinations)


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

