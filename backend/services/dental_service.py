from models.history import MedicalHistory
from schemas.dental_schemas import DentalTreatmentCreate
from models.dental import DentalServiceRendered
from models.dental import ToothFinding
from schemas.dental_schemas import DentalExaminationCreate
from models.dental import DentalRecordUpdate
from services.patient_service import patient_service
from typing import Optional
from sqlmodel import Session, func, select
from services.base import BaseService
from models.dental import DentalRecord

class DentalRecordService(BaseService[DentalRecord]):
    def __init__(self):
        super().__init__(DentalRecord)

    def get_by_patient_id(self, db: Session, patient_id: str) -> Optional[DentalRecord]:
        patient = patient_service.get_by_patient_id(db, patient_id=patient_id)
        if not patient:
            return None

        return db.exec(select(self.model).where(self.model.patient_uuid == patient.uuid)).first()

class DentalExaminationService(BaseService[DentalRecordUpdate]):
    def __init__(self):
        super().__init__(DentalRecordUpdate)

    def record_exam(self, db: Session, *, obj_in: DentalExaminationCreate) -> DentalRecordUpdate:
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

        db_obj = DentalRecordUpdate(**obj_in.model_dump(exclude={"patient_id", "findings"}), dr_uuid=dr.uuid, dru_id=dru_id)

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

        if obj_in.findings:
            for finding in obj_in.findings:
                count_tf = db.exec(select(func.count()).select_from(ToothFinding)).one()

                tf_obj = ToothFinding(**finding.model_dump(), dru_uuid=db_obj.uuid, tf_id=f"TF-{count_tf + 1:06d}")
                
                db.add(tf_obj)
                db.commit()

        return db_obj

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

dental_record_service = DentalRecordService()
examination_service = DentalExaminationService()
treatment_service = DentalTreatmentService()