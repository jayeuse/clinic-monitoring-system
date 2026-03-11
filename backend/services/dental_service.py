from typing import List, Optional

from sqlmodel import Session, func, select

from models.dental import (
    DentalExamination,
    DentalExaminationSnapshot,
    DentalRecord,
    DentalRecordSnapshot,
    DentalServiceRendered,
    ToothFinding,
)
from models.history import MedicalHistory
from schemas.dental_schemas import (
    DentalExaminationCreate,
    DentalExaminationUpdate,
    DentalRecordCreate,
    DentalRecordUpdate,
    DentalTreatmentCreate,
)
from services.base import BaseService
from services.patient_service import patient_service


class DentalRecordService(BaseService[DentalRecord]):
    def __init__(self):
        super().__init__(DentalRecord)

    def get_by_patient_id(self, db: Session, patient_id: str) -> Optional[DentalRecord]:
        patient = patient_service.get_by_patient_id(db, patient_id=patient_id)
        if not patient:
            return None

        return db.exec(select(self.model).where(self.model.patient_uuid == patient.uuid)).first()

    def create(self, db: Session, *, obj_in: DentalRecordCreate) -> DentalRecord:
        patient = patient_service.get_by_patient_id(db, patient_id=obj_in.patient_id)
        if not patient:
            raise ValueError(f"Patient {obj_in.patient_id} not found")

        existing_dr = self.get_by_patient_id(db, patient_id=obj_in.patient_id)
        if existing_dr: 
            raise ValueError(f"Patient {obj_in.patient_id} already has a Dental Record.")
        
        mh = db.exec(select(MedicalHistory).where(MedicalHistory.patient_uuid == patient.uuid)).first()
        if not mh:
            raise ValueError(f"Patient {obj_in.patient_id} has no Medical History. Please create one first.")

        count = db.exec(select(func.count()).select_from(self.model)).one()
        dr_id = f"DR-{count + 1:06d}"
        
        db_obj = DentalRecord(
            **obj_in.model_dump(exclude={"patient_id"}),
            dr_id=dr_id,
            patient_uuid=patient.uuid,
            mh_uuid=mh.uuid
        )

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

        statement_snap = select(func.count()).select_from(DentalRecordSnapshot)
        snap_count = db.exec(statement_snap).one()
        snap_id = f"DRS-{snap_count + 1:06d}"

        snapshot = DentalRecordSnapshot(
            snapshot_id=snap_id,
            original_dr_uuid=db_obj.uuid,
            last_dental_visit=db_obj.last_dental_visit,
            reason_for_last_dental_visit=db_obj.reason_for_last_dental_visit,
            last_hospitalization=db_obj.last_hospitalization,
            hospitalization_reason=db_obj.hospitalization_reason,
            known_allergies=db_obj.known_allergies,
            tobacco_use=db_obj.tobacco_use,
            alcohol_drug_use=db_obj.alcohol_drug_use,
            for_women_status=db_obj.for_women_status,
            chart_image_url=db_obj.chart_image_url
        )

        db.add(snapshot)
        db.commit()

        return db_obj

    def update(self,db: Session, *, db_obj: DentalRecord, obj_in: DentalRecordUpdate) -> DentalRecord:
        updated_dr = super().update(db, db_obj=db_obj, obj_in=obj_in)

        statement_snap = select(func.count()).select_from(DentalRecordSnapshot)
        snap_count = db.exec(statement_snap).one()
        snap_id = f"DRS-{snap_count + 1:06d}"

        snapshot = DentalRecordSnapshot(
            snapshot_id=snap_id,
            original_dr_uuid=db_obj.uuid,
            last_dental_visit=db_obj.last_dental_visit,
            reason_for_last_dental_visit=db_obj.reason_for_last_dental_visit,
            last_hospitalization=db_obj.last_hospitalization,
            hospitalization_reason=db_obj.hospitalization_reason,
            known_allergies=db_obj.known_allergies,
            tobacco_use=db_obj.tobacco_use,
            alcohol_drug_use=db_obj.alcohol_drug_use,
            for_women_status=db_obj.for_women_status,
            chart_image_url=db_obj.chart_image_url
        )

        db.add(snapshot)
        db.commit()

        return updated_dr

class DentalExaminationService(BaseService[DentalExamination]):
    def __init__(self):
        super().__init__(DentalExamination)

    def create(self, db: Session, *, obj_in: DentalExaminationCreate) -> DentalExamination:
        dr_service = DentalRecordService()

        dr = dr_service.get_by_patient_id(db, patient_id=obj_in.patient_id)
        if not dr:
            patient = patient_service.get_by_patient_id(db, patient_id=obj_in.patient_id)
            if not patient:
                raise ValueError(f"Patient {obj_in.patient_id} not found")

            mh = db.exec(select(MedicalHistory).where(MedicalHistory.patient_uuid == patient.uuid)).first()
            if not mh:
                raise ValueError(f"Patient {obj_in.patient_id} has no Medical History recorded yet. Please create one before recording dental exams.")

            count = db.exec(select(func.count()).select_from(DentalRecord)).one()
            dr = dr_service.create(db, obj_in=DentalRecord(dr_id=f"DR-{count + 1:06d}", patient_uuid=patient.uuid, mh_uuid=mh.uuid))

        count_dx = db.exec(select(func.count()).select_from(self.model)).one()
        dru_id = f"DX-{count_dx + 1:06d}"

        db_obj = DentalExamination(**obj_in.model_dump(exclude={"patient_id", "findings"}), dr_uuid=dr.uuid, dru_id=dru_id)

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

        if obj_in.findings:
            for finding in obj_in.findings:
                count_tf = db.exec(select(func.count()).select_from(ToothFinding)).one()

                tf_obj = ToothFinding(**finding.model_dump(), dru_uuid=db_obj.uuid, tf_id=f"TF-{count_tf + 1:06d}")
                
                db.add(tf_obj)
                db.commit()

        statement_snap = select(func.count()).select_from(DentalExaminationSnapshot)
        snap_count = db.exec(statement_snap).one()
        snap_id = f"DXS-{snap_count + 1:06d}"

        snapshot = DentalExaminationSnapshot(
            snapshot_id=snap_id,
            original_dr_uuid=db_obj.uuid, 
            examination_date=db_obj.examination_date,
            head_findings=db_obj.head_findings,
            face_findings=db_obj.face_findings,
            tmj_findings=db_obj.tmj_findings,
            periodontal_diagnosis=db_obj.periodontal_diagnosis,
            periodontitis_severity=db_obj.periodontitis_severity,
            periodontal_others=db_obj.periodontal_others,
            lips_findings=db_obj.lips_findings,
            palate_findings=db_obj.palate_findings,
            floor_of_mouth_findings=db_obj.floor_of_mouth_findings,
            tongue_findings=db_obj.tongue_findings
        )

        db.add(snapshot)
        db.commit()

        return db_obj

    def update(self, db: Session, *, db_obj: DentalExamination, obj_in: DentalExaminationUpdate) -> DentalExamination:
        updated_exam = super().update(db, db_obj=db_obj, obj_in=obj_in)

        statement_snap = select(func.count()).select_from(DentalExaminationSnapshot)
        snap_count = db.exec(statement_snap).one()
        snap_id = f"DXS-{snap_count + 1:06d}"
        snapshot = DentalExaminationSnapshot(
            snapshot_id=snap_id,
            original_dr_uuid=updated_exam.uuid, 
            examination_date=updated_exam.examination_date,
            head_findings=updated_exam.head_findings,
            face_findings=updated_exam.face_findings,
            tmj_findings=updated_exam.tmj_findings,
            periodontal_diagnosis=updated_exam.periodontal_diagnosis,
            periodontitis_severity=updated_exam.periodontitis_severity,
            periodontal_others=updated_exam.periodontal_others,
            lips_findings=updated_exam.lips_findings,
            palate_findings=updated_exam.palate_findings,
            floor_of_mouth_findings=updated_exam.floor_of_mouth_findings,
            tongue_findings=updated_exam.tongue_findings
        )
        
        db.add(snapshot)
        db.commit()
        return updated_exam

    def get_by_patient_id(self, db: Session, patient_id: str) -> List[DentalExamination]:
        dr_service = DentalRecordService()
        dr = dr_service.get_by_patient_id(db, patient_id=patient_id)
        if not dr:
            return []
            
        statement = select(self.model).where(
            self.model.dr_uuid == dr.uuid, self.model.is_deleted.is_(False)
        )
        return db.exec(statement).all()
    
    def get_by_dru_id(self, db: Session, dru_id: str) -> Optional[DentalExamination]:
        statement = select(self.model).where(self.model.dru_id == dru_id, self.model.is_deleted.is_(False))
        return db.exec(statement).first()

    def get_findings_by_exam(self, db: Session, *, dru_id: str) -> List[ToothFinding]:
        exam = self.get_by_dru_id(db, dru_id=dru_id)
        if not exam:
            return []

        statement = select(ToothFinding).where(ToothFinding.dru_uuid == exam.uuid)
        return db.exec(statement).all()

class DentalTreatmentService(BaseService[DentalServiceRendered]):
    def __init__(self):
        super().__init__(DentalServiceRendered)

    def log_treatment(self, db: Session, *, obj_in: DentalTreatmentCreate) -> DentalServiceRendered:
        dr_service = DentalRecordService()
        
        dr = dr_service.get_by_patient_id(db, patient_id=obj_in.patient_id)
        if not dr:
            raise ValueError(f"No Dental Record found for patient {obj_in.patient_id}. Please perform an exam first")

        count = db.exec(select(func.count()).select_from(self.model)).one()
        dsr_id = f"DTX-{count + 1:06d}"

        db_obj = DentalServiceRendered(**obj_in.model_dump(exclude={"patient_id"}), dr_uuid=dr.uuid, dsr_id=dsr_id)

        return super().create(db, obj_in=db_obj)

    def get_by_patient_id(self, db: Session, patient_id: str) -> List[DentalServiceRendered]:
        dr_service = DentalRecordService()
        dr = dr_service.get_by_patient_id(db, patient_id=patient_id)
        if not dr:
            return []
            
        statement = select(self.model).where(
            self.model.dr_uuid == dr.uuid, self.model.is_deleted.is_(False)
        )
        return db.exec(statement).all()

    
    def get_by_dsr_id(self, db: Session, dsr_id: str) -> Optional[DentalServiceRendered]:
        statement = select(self.model).where(self.model.dsr_id == dsr_id, self.model.is_deleted.is_(False))
        return db.exec(statement).first()

dental_record_service = DentalRecordService()
examination_service = DentalExaminationService()
treatment_service = DentalTreatmentService()