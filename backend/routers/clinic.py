from services.clinic_service import vital_signs_service
from schemas.clinic_schemas import VitalSignsPublic
from schemas.clinic_schemas import VitalSignsCreate
from fastapi import HTTPException
from core.database import get_session
from fastapi import Depends
from typing import List
from sqlmodel import Session
from schemas.clinic_schemas import ClinicTransactionCreate
from fastapi import APIRouter

from schemas.clinic_schemas import ClinicTransactionPublic
from services.clinic_service import clinic_service

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


@router.post("/vital-signs/", response_model=VitalSignsPublic)
def record_vital_sign(vs_in: VitalSignsCreate, db: Session = Depends(get_session)):
    try:
        return vital_signs_service.create(db, obj_in=vs_in)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/vital-signs/", response_model=List[VitalSignsPublic])
def read_vital_signs(
    db: Session = Depends(get_session), skip: int = 0, limit: int = 100
):
    return vital_signs_service.get_all(db, skip=skip, limit=limit)
