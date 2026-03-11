from typing import Optional

from sqlmodel import Session, func, select

from models.patients import PatientInformation
from schemas.patient_schemas import PatientCreate
from services.base import BaseService


class PatientService(BaseService[PatientInformation]):
    def __init__(self):
        super().__init__(PatientInformation)

    def get_by_patient_id(self, db: Session, patient_id: str) -> Optional[PatientInformation]:
        statement = select(self.model).where(self.model.patient_id == patient_id)
        return db.exec(statement).first()

    def create(self, db: Session, *, obj_in: PatientCreate) -> PatientInformation:
        existing_patient = db.exec(
            select(self.model).where(
                self.model.last_name == obj_in.last_name,
                self.model.first_name == obj_in.first_name,
                self.model.birthdate == obj_in.birthdate,
                self.model.is_deleted.is_(False)
            )
        ).first()
        
        if existing_patient:
            raise ValueError(f"Patient {obj_in.first_name} {obj_in.last_name} born on {obj_in.birthdate} already exists.")
        statement = select(func.count()).select_from(self.model)
        count = db.exec(statement).one()
        new_id = f"PAT-{count + 1:06d}"

        db_obj = PatientInformation.model_validate(
            obj_in,
            update={"patient_id": new_id}
        )

        return super().create(db, obj_in=db_obj)

patient_service = PatientService()