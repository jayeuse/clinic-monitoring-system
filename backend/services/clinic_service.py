from datetime import datetime
from typing import Optional

from sqlmodel import Session, func, select

from models.clinic import ClinicTransaction, VitalSigns
from schemas.clinic_schemas import ClinicTransactionCreate, VitalSignsCreate
from services.base import BaseService

from .patient_service import patient_service


class ClinicTransactionService(BaseService[ClinicTransaction]):
    def __init__(self):
        super().__init__(ClinicTransaction)

    def create(self, db: Session, *, obj_in: ClinicTransactionCreate) -> ClinicTransaction:
        patient = patient_service.get_by_patient_id(db, patient_id=obj_in.patient_id)

        if not patient:
            raise ValueError(f"Patient with ID {obj_in.patient_id} not found")

        statement = select(func.count()).select_from(self.model)
        count = db.exec(statement).one()
        new_id = f"CT-{count + 1:06d}"

        data = obj_in.model_dump(exclude={"patient_id"})
        db_obj = ClinicTransaction(
            **data,
            ct_id=new_id,
            patient_uuid=patient.uuid,
            time_in=datetime.now().time()
        )

        return super().create(db, obj_in=db_obj)

    def get_by_ct_id(self, db: Session, ct_id: str) -> Optional[ClinicTransaction]:
        statement = select(self.model).where(self.model.ct_id == ct_id, self.model.is_deleted.is_(False))
        return db.exec(statement).first()

class VitalSignsService(BaseService[VitalSigns]):
    def __init__(self):
        super().__init__(VitalSigns)

    def create(self, db: Session, *, obj_in: VitalSignsCreate) -> VitalSigns:
        statement = select(ClinicTransaction).where(ClinicTransaction.ct_id == obj_in.ct_id)
        transaction = db.exec(statement).first()

        if not transaction:
            raise ValueError(f"Transaction with ID {obj_in.ct_id} not found")

        statement = select(func.count()).select_from(self.model)
        count = db.exec(statement).one()
        new_id = f"VS-{count + 1:06d}"

        data = obj_in.model_dump(exclude={"ct_id"})
        db_obj = VitalSigns(
            **data,
            vs_id=new_id,
            ct_uuid=transaction.uuid
        )

        return super().create(db, obj_in=db_obj)

    def get_by_vs_id(self, db: Session, vs_id: str):
        statement = select(self.model).where(self.model.vs_id == vs_id, self.model.is_deleted.is_(False))
        return db.exec(statement).first()

clinic_service = ClinicTransactionService()
vital_signs_service = VitalSignsService()