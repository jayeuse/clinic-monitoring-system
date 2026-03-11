import math
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from core.database import get_session
from schemas.base_schemas import GenericResponse, PaginationMeta
from schemas.patient_schemas import (
    EmergencyContactCreate,
    EmergencyContactPublic,
    EmergencyContactUpdate,
)
from services.emergency_contact_service import emergency_contact_service

router = APIRouter(prefix="/emergency-contacts", tags=["Emergency Contacts"])

@router.get("/", response_model=GenericResponse[List[EmergencyContactPublic]])
def read_emergency_contacts(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_session)
):
    contacts, total_count = emergency_contact_service.get_all(db, skip=skip, limit=limit)

    current_page = (skip // limit) + 1
    total_pages = math.ceil(total_count / limit) if limit > 0 else 1

    meta = PaginationMeta(
        total_records=total_count,
        current_page=current_page,
        total_pages=total_pages,
        next_page=(current_page + 1) if (skip + limit) < total_count else None,
        prev_page=(current_page - 1) if skip > 0 else None
    )

    return GenericResponse(message="Emergency Contacts retrieved successfully", data=contacts, meta=meta)

@router.post("/", response_model=GenericResponse[EmergencyContactPublic])
def create_emergency_contact(
    contact_in: EmergencyContactCreate,
    db: Session = Depends(get_session)
):
    try:
        new_contact = emergency_contact_service.create(db, obj_in=contact_in)
        return GenericResponse(message="Emergency Contact created successfully", data=new_contact)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/patient/{patient_id}", response_model=GenericResponse[List[EmergencyContactPublic]])
def read_patient_emergency_contacts(
    patient_id: str,
    db: Session = Depends(get_session)
):
    contacts = emergency_contact_service.get_by_patient_id(db, patient_id=patient_id)
    return GenericResponse(message="Patient's Emergency Contacts retrieved successfully", data=contacts)

@router.get("/{ec_id}", response_model=GenericResponse[EmergencyContactPublic])
def read_emergency_contact_by_id(
    ec_id: str,
    db: Session = Depends(get_session)
):
    contact = emergency_contact_service.get_by_ec_id(db, ec_id=ec_id)
    if not contact:
        raise HTTPException(status_code=404, detail="Emergency Contact not found")

    return GenericResponse(message="Emergency Contact retrieved successfully", data=contact)

@router.patch("/{ec_id}", response_model=GenericResponse[EmergencyContactPublic])
def update_emergency_contact(
    ec_id: str,
    contact_in: EmergencyContactUpdate,
    db: Session = Depends(get_session)
):
    db_obj = emergency_contact_service.get_by_ec_id(db, ec_id=ec_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Emergency Contact not found")
    
    updated_contact = emergency_contact_service.update(db, db_obj=db_obj, obj_in=contact_in)
    return GenericResponse(message="Emergency Contact updated successfully", data=updated_contact)

@router.delete("/{ec_id}", response_model=GenericResponse[EmergencyContactPublic])
def delete_emergency_contact(
    ec_id: str,
    db: Session = Depends(get_session)
):
    db_obj = emergency_contact_service.get_by_ec_id(db, ec_id=ec_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Emergency Contact not found")

    deleted_contact = emergency_contact_service.remove(db, uuid=db_obj.uuid)
    return GenericResponse(message="Emergency Contact deleted successfully", data=deleted_contact)
