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


@router.post("/transactions/", response_model=ClinicTransactionPublic)
def create_transaction(
    transaction_in: ClinicTransactionCreate, db: Session = Depends(get_session)
):
    try:
        return clinic_service.create(db, obj_in=transaction_in)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/transactions/", response_model=List[ClinicTransactionPublic])
def read_transactions(
    db: Session = Depends(get_session), skip: int = 0, limit: int = 100
):
    return clinic_service.get_all(db, skip=skip, limit=limit)

@router.get("/transactions/{ct_id}", response_model=ClinicTransactionPublic)
def read_transaction(ct_id:str, db: Session = Depends(get_session)):
    transaction = clinic_service.get_by_ct_id(db, ct_id=ct_id)
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")

    return transaction

@router.patch("/transactions/{ct_id}", response_model=ClinicTransactionPublic)
def update_transaction(ct_id:str, transaction_in: ClinicTransactionUpdate ,db: Session = Depends(get_session)):
    db_obj = clinic_service.get_by_ct_id(db, ct_id=ct_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Transaction not found")

    return clinic_service.update(db, db_obj=db_obj, obj_in=transaction_in)

@router.delete("/transactions/{ct_id}", response_model=ClinicTransactionPublic)
def delete_transaction(ct_id: str, db: Session = Depends(get_session)):
    db_obj = clinic_service.get_by_ct_id(db, ct_id=ct_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Transaction not found")

    return clinic_service.remove(db, uuid=db_obj.uuid)

@router.post("/vital-signs/", response_model=VitalSignsPublic)
def record_vital_sign(vs_in: VitalSignsCreate, db: Session = Depends(get_session)):
    try:
        return vital_signs_service.create(db, obj_in=vs_in)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/vital-signs/{vs_id}", response_model=VitalSignsPublic)
def read_vital_sign(vs_id: str, db: Session = Depends(get_session)):
    vs = vital_signs_service.get_by_vs_id(db, vs_id=vs_id)
    if not vs:
        raise HTTPException(status_code=404, detail="Vital Sign not found")

    return vs

@router.patch("/vital-signs/{vs_id}", response_model=VitalSignsPublic)
def update_vital_sign(vs_id: str, vs_in: VitalSignsUpdate, db: Session = Depends(get_session)):
    db_obj = vital_signs_service.get_by_vs_id(db, vs_id=vs_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Vital Sign not found")

    return vital_signs_service.update(db, db_obj=db_obj, obj_in=vs_in)

@router.delete("/vital-signs/{vs_id}", response_model=VitalSignsPublic)
def delete_vital_sign(vs_id: str, db: Session = Depends(get_session)):
    db_obj = vital_signs_service.get_by_vs_id(db, vs_id=vs_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Vital Sign not found")

    return vital_signs_service.remove(db, uuid=db_obj.uuid)


@router.get("/vital-signs/", response_model=List[VitalSignsPublic])
def read_vital_signs(
    db: Session = Depends(get_session), skip: int = 0, limit: int = 100
):
    return vital_signs_service.get_all(db, skip=skip, limit=limit)
