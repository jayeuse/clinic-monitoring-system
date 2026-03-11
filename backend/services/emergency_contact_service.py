from typing import List, Optional

from sqlmodel import Session, func, select

from models.patients import EmergencyContact
from schemas.patient_schemas import EmergencyContactCreate
from services.base import BaseService
from services.patient_service import patient_service


class EmergencyContactService(BaseService[EmergencyContact]):
    def __init__(self):
        super().__init__(EmergencyContact)

    def get_by_ec_id(self, db: Session, ec_id: str) -> Optional[EmergencyContact]:
        statement = select(self.model).where(
            self.model.ec_id == ec_id, self.model.is_deleted.is_(False)
        )
        return db.exec(statement).first()

    def get_by_patient_id(self, db: Session, patient_id: str) -> List[EmergencyContact]:
        patient = patient_service.get_by_patient_id(db, patient_id=patient_id)
        if not patient:
            return []

        statement = select(self.model).where(
            self.model.patient_uuid == patient.uuid, self.model.is_deleted.is_(False)
        )
        return db.exec(statement).all()

    def create(self, db: Session, *, obj_in: EmergencyContactCreate) -> EmergencyContact:
        patient = patient_service.get_by_patient_id(db, patient_id=obj_in.patient_id)
        if not patient:
            raise ValueError(f"Patient with ID {obj_in.patient_id} not found.")

        existing_ec = db.exec(
            select(self.model).where(self.model.patient_uuid == patient.uuid, self.model.is_deleted.is_(False))).first()
        if existing_ec:
            raise ValueError(f"Patient {obj_in.patient_id} already has an Emergency Contact.")

        statement = select(func.count()).select_from(self.model)
        count = db.exec(statement).one()
        new_id = f"EC-{count + 1:06d}"

        data = obj_in.model_dump(exclude={"patient_id"})
        db_obj = EmergencyContact(**data, ec_id=new_id, patient_uuid=patient.uuid)

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

        return db_obj


emergency_contact_service = EmergencyContactService()
