from schemas.base_schemas import GenericResponse
from services.clinic_service import vital_signs_service
from fastapi import HTTPException
from core.database import get_session
from fastapi import Depends
from typing import List
from sqlmodel import Session
from fastapi import APIRouter

from services.clinic_service import clinic_service

from schemas.clinic_schemas import (
    ClinicTransactionCreate, 
    ClinicTransactionPublic, 
    ClinicTransactionUpdate,
    VitalSignsCreate, 
    VitalSignsPublic,
    VitalSignsUpdate
)

router = APIRouter(prefix="/clinic", tags=["Clinic Operations"])

@router.get("/transactions/", response_model=GenericResponse[List[ClinicTransactionPublic]])
def read_transactions(
    db: Session = Depends(get_session), skip: int = 0, limit: int = 100
):
    get_transactions = clinic_service.get_all(db, skip=skip, limit=limit)
    return GenericResponse(message="Transactions retrieved successfully", data=get_transactions)

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


@router.get("/vital-signs/", response_model=GenericResponse[List[VitalSignsPublic]])
def read_vital_signs(
    db: Session = Depends(get_session), skip: int = 0, limit: int = 100
):
    get_all_vital_signs = vital_signs_service.get_all(db, skip=skip, limit=limit)
    return GenericResponse(message="Vital Signs retrieved successfully", data=get_all_vital_signs)
