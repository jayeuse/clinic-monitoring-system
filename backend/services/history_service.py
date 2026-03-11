from models.history import MedicalExaminationSnapshot
from models.history import MedicalExaminationFindings
from schemas.history_schemas import MedicalExaminationCreate
from models.history import MedicalExamination
from typing import Optional, List
from sqlmodel import select, func
from services.patient_service import patient_service
from schemas.history_schemas import MedicalHistoryCreate
from sqlmodel import Session
from models.history import MedicalHistory
from services.base import BaseService


class MedicalHistoryService(BaseService[MedicalHistory]):
    def __init__(self):
        super().__init__(MedicalHistory)

    def get_by_patient_id(self, db: Session, patient_id: str) -> List[MedicalHistory]:
        patient = patient_service.get_by_patient_id(db, patient_id=patient_id)
        if not patient:
            return []

        statement = select(self.model).where(
            self.model.patient_uuid == patient.uuid, self.model.is_deleted.is_(False)
        )
        return db.exec(statement).all()

    def get_by_mh_id(self, db: Session, mh_id: str) -> Optional[MedicalHistory]:
        statement = select(self.model).where(
            self.model.mh_id == mh_id, self.model.is_deleted.is_(False)
        )
        return db.exec(statement).first()

    def create(self, db: Session, *, obj_in: MedicalHistoryCreate) -> MedicalHistory:
        patient = patient_service.get_by_patient_id(db, patient_id=obj_in.patient_id)
        if not patient:
            raise ValueError(f"Patient with ID {obj_in.patient_id} not found")

        statement = select(func.count()).select_from(self.model)

        existing_History = db.exec(select(self.model).where(self.model.patient_uuid == patient.uuid, self.model.is_deleted.is_(False))).first()
        if existing_History:
            raise ValueError(f"A Medical History Record already exists for Patient {obj_in.patient_id}")

        count = db.exec(statement).one()
        new_id = f"MH-{count + 1:06d}"

        data = obj_in.model_dump(exclude={"patient_id"})
        db_obj = MedicalHistory(**data, mh_id=new_id, patient_uuid=patient.uuid)

        return super().create(db, obj_in=db_obj)


class MedicalExaminationService(BaseService[MedicalExamination]):
    def __init__(self):
        super().__init__(MedicalExamination)

    def get_by_patient_id(self, db: Session, patient_id: str) -> List[MedicalExamination]:
        patient = patient_service.get_by_patient_id(db, patient_id=patient_id)
        if not patient:
            return []

        statement = select(self.model).where(
            self.model.patient_uuid == patient.uuid, self.model.is_deleted.is_(False)
        )
        return db.exec(statement).all()

    def get_by_me_id(self, db: Session, me_id: str) -> Optional[MedicalExamination]:
        statement = select(self.model).where(self.model.me_id == me_id, self.model.is_deleted.is_(False))
        return db.exec(statement).first()

    def create(self, db: Session, *, obj_in: MedicalExaminationCreate) -> MedicalExamination:
        patient = patient_service.get_by_patient_id(db, patient_id=obj_in.patient_id)
        if not patient:
            raise ValueError(f"Patient with ID {obj_in.patient_id} not found.")

        history = history_service.get_by_mh_id(db, mh_id=obj_in.mh_id)
        if not history:
            raise ValueError(f"Medical History with ID {obj_in.mh_id} not found.")

        statement = select(func.count()).select_from(self.model)
        count = db.exec(statement).one()
        new_id = f"ME-{count + 1:06d}"

        data = obj_in.model_dump(exclude={"patient_id", "mh_id", "findings"})
        db_obj = MedicalExamination(**data, me_id=new_id, patient_uuid=patient.uuid, mh_uuid=history.uuid)

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

        if obj_in.findings:
            for finding_data in obj_in.findings:
                finding = MedicalExaminationFindings(
                    me_uuid=db_obj.uuid,
                    bsl_uuid=finding_data.bsl_uuid,
                    status=finding_data.status,
                    condition_notes=finding_data.condition_notes)
                db.add(finding)
            db.commit()

        statement_snap = select(func.count()).select_from(MedicalExaminationSnapshot)
        snap_count = db.exec(statement_snap).one()
        snap_id = f"MES-{snap_count + 1:06d}"

        snapshot = MedicalExaminationSnapshot(
            snapshot_id=snap_id,
            original_me_uuid=db_obj.uuid,
            date_taken=db_obj.date_taken
        )

        db.add(snapshot)
        db.commit()
        db.refresh(db_obj)

        return db_obj

history_service = MedicalHistoryService()
medical_examination_service = MedicalExaminationService()