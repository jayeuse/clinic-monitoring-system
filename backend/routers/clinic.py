import math
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from core.database import get_session
from schemas.base_schemas import GenericResponse, PaginationMeta
from schemas.clinic_schemas import (
    ClinicTransactionCreate,
    ClinicTransactionPublic,
    ClinicTransactionUpdate,
    VitalSignsCreate,
    VitalSignsPublic,
    VitalSignsUpdate,
)
from services.clinic_service import clinic_service, vital_signs_service

router = APIRouter(prefix="/clinic", tags=["Clinic Operations"])

# CLINIC TRANSACTIONS
@router.get("/transactions/", response_model=GenericResponse[List[ClinicTransactionPublic]])
def read_transactions(
    db: Session = Depends(get_session), skip: int = 0, limit: int = 100
):
    get_transactions, total_count = clinic_service.get_all(db, skip=skip, limit=limit)

    current_page = (skip // limit) + 1
    total_pages = math.ceil(total_count / limit) if limit > 0 else 1

    meta = PaginationMeta(
        total_records=total_count,
        current_page=current_page,
        total_pages=total_pages,
        next_page=(current_page + 1) if (skip + limit) < total_count else None,
        prev_page=(current_page - 1) if skip > 0 else None
    )
    return GenericResponse(message="Transactions retrieved successfully", data=get_transactions, meta=meta)

@router.post("/transactions/", response_model=GenericResponse[ClinicTransactionPublic])
def create_transaction(
    transaction_in: ClinicTransactionCreate, db: Session = Depends(get_session)
):
    try:
        new_transaction = clinic_service.create(db, obj_in=transaction_in)
        return GenericResponse(message="Clinic Transaction recorded successfully", data=new_transaction)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/transactions/{ct_id}", response_model=GenericResponse[ClinicTransactionPublic])
def read_transaction(ct_id:str, db: Session = Depends(get_session)):
    get_transaction = clinic_service.get_by_ct_id(db, ct_id=ct_id)
    if not get_transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")

    return GenericResponse(message="Transaction retrieved successfully", data=get_transaction)

@router.patch("/transactions/{ct_id}", response_model=GenericResponse[ClinicTransactionPublic])
def update_transaction(ct_id:str, transaction_in: ClinicTransactionUpdate ,db: Session = Depends(get_session)):
    db_obj = clinic_service.get_by_ct_id(db, ct_id=ct_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Transaction not found")

    update_transaction = clinic_service.update(db, db_obj=db_obj, obj_in=transaction_in)
    return GenericResponse(message="Transaction updated successfully", data=update_transaction)

@router.delete("/transactions/{ct_id}", response_model=GenericResponse[ClinicTransactionPublic])
def delete_transaction(ct_id: str, db: Session = Depends(get_session)):
    db_obj = clinic_service.get_by_ct_id(db, ct_id=ct_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Transaction not found")

    delete_transaction = clinic_service.remove(db, uuid=db_obj.uuid)
    return GenericResponse(message="Transaction deleted successfully", data=delete_transaction)

@router.post("/transactions/{ct_id}/restore", response_model=GenericResponse[ClinicTransactionPublic])
def restore_clinic_transaction(
    ct_id: str,
    db: Session = Depends(get_session)
):
    db_obj = clinic_service.get_by_ct_id(db, ct_id=ct_id, include_deleted=True)

    if not db_obj:
        raise HTTPException(status_code=404, detail="Clinic transaction not found")
        
    if not db_obj.is_deleted:
        raise HTTPException(status_code=400, detail="Clinic transaction is not deleted")

    restored_ct = clinic_service.restore(db, uuid=db_obj.uuid)
    return GenericResponse(message="Clinic transaction restored successfully", data=restored_ct)

# VITAL SIGNS
@router.get("/vital-signs/", response_model=GenericResponse[List[VitalSignsPublic]])
def read_vital_signs(
    db: Session = Depends(get_session), skip: int = 0, limit: int = 100
):
    get_all_vital_signs, total_count = vital_signs_service.get_all(db, skip=skip, limit=limit)

    current_page = (skip // limit) + 1
    total_pages = math.ceil(total_count / limit) if limit > 0 else 1

    meta = PaginationMeta(
        total_records=total_count,
        current_page=current_page,
        total_pages=total_pages,
        next_page=(current_page + 1) if (skip + limit) < total_count else None,
        prev_page=(current_page - 1) if skip > 0 else None
    )

    return GenericResponse(message="Vital Signs retrieved successfully", data=get_all_vital_signs, meta=meta)

@router.post("/vital-signs/", response_model=GenericResponse[VitalSignsPublic])
def record_vital_sign(vs_in: VitalSignsCreate, db: Session = Depends(get_session)):
    try:
        new_vital_sign = vital_signs_service.create(db, obj_in=vs_in)
        return GenericResponse(message="Vital Sign recorded successfully", data=new_vital_sign)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/vital-signs/{vs_id}", response_model=GenericResponse[VitalSignsPublic])
def read_vital_sign(vs_id: str, db: Session = Depends(get_session)):
    get_vital_sign = vital_signs_service.get_by_vs_id(db, vs_id=vs_id)
    if not get_vital_sign:
        raise HTTPException(status_code=404, detail="Vital Sign not found")

    return GenericResponse(message="Vital Sign retrieved successfully", data=get_vital_sign)

@router.patch("/vital-signs/{vs_id}", response_model=GenericResponse[VitalSignsPublic])
def update_vital_sign(vs_id: str, vs_in: VitalSignsUpdate, db: Session = Depends(get_session)):
    db_obj = vital_signs_service.get_by_vs_id(db, vs_id=vs_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Vital Sign not found")

    update_vital_sign = vital_signs_service.update(db, db_obj=db_obj, obj_in=vs_in)
    return GenericResponse(message="Vital Sign updated successfully", data=update_vital_sign)

@router.delete("/vital-signs/{vs_id}", response_model=GenericResponse[VitalSignsPublic])
def delete_vital_sign(vs_id: str, db: Session = Depends(get_session)):
    db_obj = vital_signs_service.get_by_vs_id(db, vs_id=vs_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Vital Sign not found")

    delete_vital_sign = vital_signs_service.remove(db, uuid=db_obj.uuid)
    return GenericResponse(message="Vital Sign deleted successfully", data=delete_vital_sign)

@router.post("/vital-signs/{vs_id}/restore", response_model=GenericResponse[VitalSignsPublic])
def restore_vital_signs(
    vs_id: str,
    db: Session = Depends(get_session)
):
    db_obj = vital_signs_service.get_by_vs_id(db, vs_id=vs_id, include_deleted=True)

    if not db_obj:
        raise HTTPException(status_code=404, detail="Vital signs record not found")
        
    if not db_obj.is_deleted:
        raise HTTPException(status_code=400, detail="Vital signs record is not deleted")

    restored_vs = vital_signs_service.restore(db, uuid=db_obj.uuid)
    return GenericResponse(message="Vital signs record restored successfully", data=restored_vs)
