from schemas.patient_schemas import PersonnelTypeUpdate
from schemas.patient_schemas import PersonnelTypeCreate
from services.patient_service import personnel_type_service
from schemas.patient_schemas import PersonnelTypePublic
from schemas.patient_schemas import StudentTypeUpdate
from schemas.patient_schemas import StudentTypeCreate
from services.patient_service import student_type_service
from schemas.patient_schemas import StudentTypePublic
import math
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from core.database import get_session
from schemas.base_schemas import GenericResponse, PaginationMeta
from schemas.patient_schemas import PatientCreate, PatientPublic, PatientUpdate
from services.patient_service import patient_service

router = APIRouter(prefix="/patients", tags=["Patients"])

@router.get("/", response_model=GenericResponse[List[PatientPublic]])
def read_patients(
    db: Session = Depends(get_session),
    skip: int = 0,
    limit: int = 100
):
    patients, total_count = patient_service.get_all(db, skip=skip, limit=limit)

    current_page = (skip // limit) + 1
    total_pages = math.ceil(total_count / limit) if limit > 0 else 1

    meta = PaginationMeta(
        total_records=total_count,
        current_page=current_page,
        total_pages=total_pages,
        next_page=(current_page + 1) if (skip + limit) < total_count else None,
        prev_page=(current_page - 1) if skip > 0 else None
    )

    return GenericResponse(message="Patients retrieved successfully", data=patients, meta=meta)

@router.get("/{patient_id}", response_model=GenericResponse[PatientPublic])
def read_patient_by_id(
    patient_id:str,
    db: Session = Depends(get_session)
):

    patient = patient_service.get_by_patient_id(db, patient_id=patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    return GenericResponse(message="Patient retrieved successfully", data=patient)

@router.post("/", response_model=GenericResponse[PatientPublic])
def create_patient(
    patient_in: PatientCreate,
    db: Session = Depends(get_session)
):
    try:
        new_patient = patient_service.create(db, obj_in=patient_in)
        return GenericResponse(message="Patient record created successfully", data=new_patient)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.patch("/{patient_id}", response_model=GenericResponse[PatientPublic])
def update_patient(
    patient_id: str,
    patient_in: PatientUpdate,
    db: Session = Depends(get_session)
):
    db_obj = patient_service.get_by_patient_id(db, patient_id=patient_id)

    if not db_obj:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    update_patient = patient_service.update(db, db_obj=db_obj, obj_in=patient_in)
    return GenericResponse(message="Patient record updated successfully", data=update_patient)

@router.delete("/{patient_id}", response_model=GenericResponse[PatientPublic])
def delete_patient(
    patient_id: str,
    db: Session = Depends(get_session)
):
    db_obj = patient_service.get_by_patient_id(db, patient_id=patient_id)

    if not db_obj:
        raise HTTPException(status_code=404, detail="Patient not found")

    delete_patient = patient_service.remove(db, uuid=db_obj.uuid)
    return GenericResponse(message="Patient record deleted successfully", data=delete_patient)

@router.post("/{patient_id}/restore", response_model=GenericResponse[PatientPublic])
def restore_patient(patient_id: str, db: Session = Depends(get_session)):
    db_obj = patient_service.get_by_patient_id(db, patient_id=patient_id, include_deleted=True)

    if not db_obj:
        raise HTTPException(status_code=404, detail="Patient not found.")

    if not db_obj.is_deleted:
        raise HTTPException(status_code=404, detail="Patient is not deleted.")

    restored_patient = patient_service.restore(db, uuid=db_obj.uuid)
    return GenericResponse(message="Patient record restored successfully.", data=restored_patient)

# --- Student Type Endpoints ---

@router.get("/{patient_id}/student-details", response_model=GenericResponse[StudentTypePublic])
def read_student_details(patient_id: str, db: Session = Depends(get_session)):
    db_obj = student_type_service.get_by_patient_id(db, patient_id=patient_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Student details not found for this patient.")
    return GenericResponse(message="Student details retrieved successfully", data=db_obj)

@router.post("/{patient_id}/student-details", response_model=GenericResponse[StudentTypePublic])
def create_student_details(patient_id: str, student_in: StudentTypeCreate, db: Session = Depends(get_session)):
    if patient_id != student_in.patient_id:
        raise HTTPException(status_code=400, detail="Path patient_id and body patient_id do not match.")
    try:
        new_student = student_type_service.create(db, obj_in=student_in)
        return GenericResponse(message="Student details added successfully", data=new_student)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.patch("/{patient_id}/student-details", response_model=GenericResponse[StudentTypePublic])
def update_student_details(patient_id: str, student_in: StudentTypeUpdate, db: Session = Depends(get_session)):
    db_obj = student_type_service.get_by_patient_id(db, patient_id=patient_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Student details not found for this patient.")
    
    try:
        updated_student = student_type_service.update(db, db_obj=db_obj, obj_in=student_in)
        return GenericResponse(message="Student details updated successfully", data=updated_student)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# --- Personnel Type Endpoints ---

@router.get("/{patient_id}/personnel-details", response_model=GenericResponse[PersonnelTypePublic])
def read_personnel_details(patient_id: str, db: Session = Depends(get_session)):
    db_obj = personnel_type_service.get_by_patient_id(db, patient_id=patient_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Personnel details not found for this patient.")
    return GenericResponse(message="Personnel details retrieved successfully", data=db_obj)

@router.post("/{patient_id}/personnel-details", response_model=GenericResponse[PersonnelTypePublic])
def create_personnel_details(patient_id: str, personnel_in: PersonnelTypeCreate, db: Session = Depends(get_session)):
    if patient_id != personnel_in.patient_id:
        raise HTTPException(status_code=400, detail="Path patient_id and body patient_id do not match.")
    try:
        new_personnel = personnel_type_service.create(db, obj_in=personnel_in)
        return GenericResponse(message="Personnel details added successfully", data=new_personnel)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.patch("/{patient_id}/personnel-details", response_model=GenericResponse[PersonnelTypePublic])
def update_personnel_details(patient_id: str, personnel_in: PersonnelTypeUpdate, db: Session = Depends(get_session)):
    db_obj = personnel_type_service.get_by_patient_id(db, patient_id=patient_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Personnel details not found for this patient.")
    
    try:
        updated_personnel = personnel_type_service.update(db, db_obj=db_obj, obj_in=personnel_in)
        return GenericResponse(message="Personnel details updated successfully", data=updated_personnel)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

