from typing import List, Optional

from sqlmodel import Session, func, select

from models.history import (
    MedicalExamination,
    MedicalExaminationFindings,
    MedicalExaminationSnapshot,
    MedicalHistory,
    MedicalHistorySnapshot,
)
from schemas.history_schemas import (
    MedicalExaminationCreate,
    MedicalExaminationUpdate,
    MedicalHistoryCreate,
    MedicalHistoryUpdate,
)
from services.base import BaseService
from services.patient_service import patient_service


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

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        # Baseline Snapshot creation
        statement_snap = select(func.count()).select_from(MedicalHistorySnapshot)
        snap_count = db.exec(statement_snap).one()
        snap_id = f"MHS-{snap_count + 1:06d}"
        snapshot = MedicalHistorySnapshot(
            snapshot_id=snap_id,
            original_mh_uuid=db_obj.uuid,
            smoking_status=db_obj.smoking_status,
            smoking_started_since=db_obj.smoking_started_since,
            drug_status=db_obj.drug_status,
            drug_name=db_obj.drug_name,
            did_rehab=db_obj.did_rehab,
            alcohol_status=db_obj.alcohol_status,
            alcohol_est_consumption=db_obj.alcohol_est_consumption,
            no_of_pregnancies=db_obj.no_of_pregnancies,
            no_of_miscarriages=db_obj.no_of_miscarriages,
            no_of_term_deliveries=db_obj.no_of_term_deliveries,
            no_of_premature_deliveries=db_obj.no_of_premature_deliveries,
            total_children=db_obj.total_children,
            surgery_notes=db_obj.surgery_notes,
            maintenance_medications=db_obj.maintenance_medications
        )
        db.add(snapshot)
        db.commit()
        return db_obj

    def update(self, db: Session, *, db_obj: MedicalHistory, obj_in: MedicalHistoryUpdate) -> MedicalHistory:
        updated_history = super().update(db, db_obj=db_obj, obj_in=obj_in)

        statement_snap = select(func.count()).select_from(MedicalHistorySnapshot)
        snap_count = db.exec(statement_snap).one()
        snap_id = f"MHS-{snap_count + 1:06d}"

        snapshot = MedicalHistorySnapshot(
            snapshot_id=snap_id,
            original_mh_uuid=updated_history.uuid,
            smoking_status=updated_history.smoking_status,
            smoking_started_since=updated_history.smoking_started_since,
            drug_status=updated_history.drug_status,
            drug_name=updated_history.drug_name,
            did_rehab=updated_history.did_rehab,
            alcohol_status=updated_history.alcohol_status,
            alcohol_est_consumption=updated_history.alcohol_est_consumption,
            no_of_pregnancies=updated_history.no_of_pregnancies,
            no_of_miscarriages=updated_history.no_of_miscarriages,
            no_of_term_deliveries=updated_history.no_of_term_deliveries,
            no_of_premature_deliveries=updated_history.no_of_premature_deliveries,
            total_children=updated_history.total_children,
            surgery_notes=updated_history.surgery_notes,
            maintenance_medications=updated_history.maintenance_medications
        )

        db.add(snapshot)
        db.commit()

        return updated_history


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

    def update(self, db: Session, *, db_obj: MedicalExamination, obj_in: MedicalExaminationUpdate) -> MedicalExamination:
        updated_exam = super().update(db, db_obj=db_obj, obj_in=obj_in)

        if obj_in.findings is not None:
            old_findings = db.exec(select(MedicalExaminationFindings).where(MedicalExaminationFindings.me_uuid == db_obj.uuid)).all()
            for old_finding in old_findings:
                db.delete(old_finding)

            for finding_data in obj_in.findings:
                finding = MedicalExaminationFindings(
                    me_uuid=db_obj.uuid,
                    bsl_uuid=finding_data.bsl_uuid,
                    status=finding_data.status,
                    condition_notes=finding_data.condition_notes
                )
                db.add(finding)
                
            db.commit()

        statement_snap = select(func.count()).select_from(MedicalExaminationSnapshot)
        snap_count = db.exec(statement_snap).one()
        snap_id = f"MES-{snap_count + 1:06d}"

        snapshot = MedicalExaminationSnapshot(
            snapshot_id = snap_id,
            original_me_uuid=updated_exam.uuid,
            date_taken=updated_exam.date_taken
        )

        db.add(snapshot)
        db.commit()

        return updated_exam

history_service = MedicalHistoryService()
medical_examination_service = MedicalExaminationService()