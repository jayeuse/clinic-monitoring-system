from typing import Optional
from sqlmodel import select, func
from services.patient_service import patient_service
from schemas.history_schemas import MedicalHistoryCreate
from sqlmodel import Session
from models.history import MedicalHistory
from services.base import BaseService

class MedicalHistoryService(BaseService[MedicalHistory]):
    def __init__(self):
        super().__init__(MedicalHistory)

    def get_by_patient_id(self, db: Session, patient_id: str) -> Optional[MedicalHistory]:
        patient = patient_service.get_by_patient_id(db, patient_id=patient_id)
        if not patient:
            return None

        statement = select(self.model).where(self.model.patient_uuid == patient.uuid)
        return db.exec(statement).first()

    def create(self, db: Session, *, obj_in: MedicalHistoryCreate) -> MedicalHistory:
        patient = patient_service.get_by_patient_id(db, patient_id=obj_in.patient_id)
        if not patient:
            raise ValueError(f"Patient with ID {obj_in.patient_id} not found")
        
        statement = select(self.model).where(self.model.patient_uuid == patient.uuid)
        existing_history = db.exec(statement).first()
        if existing_history:
            return existing_history

        statement = select(func.count()).select_from(self.model)
        count = db.exec(statement).one()
        new_id = f"MH-{count + 1:06d}"

        data = obj_in.model_dump(exclude={"patient_id"})
        db_obj = MedicalHistory(**data, mh_id=new_id, patient_uuid=patient.uuid)

        return super().create(db, obj_in=db_obj)

history_service = MedicalHistoryService()