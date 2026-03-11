import math
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from core.database import get_session
from schemas.base_schemas import GenericResponse, PaginationMeta
from schemas.history_schemas import (
    MedicalExaminationCreate,
    MedicalExaminationPublic,
    MedicalExaminationUpdate,
)
from services.history_service import medical_examination_service

router = APIRouter(prefix="/medical_examinations", tags=["Medical Examination"])

@router.get("/", response_model=GenericResponse[List[MedicalExaminationPublic]])
def read_all_medical_examinations(db: Session = Depends(get_session), skip: int = 0, limit: int = 0):
    get_all_examinations, total_count = medical_examination_service.get_all(db, skip=skip, limit=limit)

    current_page = (skip // limit) + 1
    total_pages = math.ceil(total_count / limit) if limit > 0 else 1

    meta = PaginationMeta(
        total_records=total_count,
        current_page=current_page,
        total_pages=total_pages,
        next_page=(current_page + 1) if (skip + limit) < total_count else None,
        prev_page=(current_page - 1) if skip > 0 else None
    )

    return GenericResponse(
        message="All Medical Examinations Retrieved Successfully", 
        data=get_all_examinations,
        meta=meta)

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