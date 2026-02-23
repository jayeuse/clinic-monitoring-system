from schemas.patient_schemas import PatientCreate
from typing import Optional
from sqlmodel import Session, select, func
from models.patients import PatientInformation
from services.base import BaseService

class PatientService(BaseService[PatientInformation]):
    def __init__(self):
        super().__init__(PatientInformation)

    def get_by_patient_id(self, db: Session, patient_id: str) -> Optional[PatientInformation]:
        statement = select(self.model).where(self.model.patient_id == patient_id)
        return db.exec(statement).first()

    def create(self, db: Session, *, obj_in: PatientCreate) -> PatientInformation:
        statement = select(func.count()).select_from(self.model)
        count = db.exec(statement).one()
        new_id = f"PAT-{count + 1:06d}"

        db_obj = PatientInformation.model_validate(
            obj_in,
            update={"patient_id": new_id}
        )

        return super().create(db, obj_in=db_obj)

patient_service = PatientService()