from schemas.patient_schemas import PersonnelTypeUpdate
from typing import Any
from typing import Dict
from schemas.patient_schemas import StudentTypeUpdate
from typing import Union
from schemas.patient_schemas import PersonnelTypeCreate
from models.patients import PersonnelType
from services.lookup_service import departments_lookup_service
from schemas.patient_schemas import StudentTypeCreate
from models.patients import StudentType
from typing import Optional

from sqlmodel import Session, func, select

from models.patients import PatientInformation
from schemas.patient_schemas import PatientCreate
from services.base import BaseService


class PatientService(BaseService[PatientInformation]):
    def __init__(self):
        super().__init__(PatientInformation)

    def get_by_patient_id(self, db: Session, patient_id: str, include_deleted: bool = False) -> Optional[PatientInformation]:
        statement = select(self.model).where(self.model.patient_id == patient_id)

        if not include_deleted:
            statement = statement.where(self.model.is_deleted.is_(False))
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

class StudentTypeService(BaseService[StudentType]):
    def __init__(self):
        super().__init__(StudentType)

    def get_by_patient_id(self, db: Session, patient_id: str, include_deleted: bool = False) -> Optional[StudentType]:
        patient = patient_service.get_by_patient_id(db, patient_id=patient_id)
        if not patient:
            return None

        statement = select(self.model).where(self.model.patient_uuid == patient.uuid)
        
        if not include_deleted:
            statement = statement.where(self.model.is_deleted.is_(False))
            
        return db.exec(statement).first()

    def create(self, db: Session, *, obj_in: StudentTypeCreate) -> StudentType:
        patient = patient_service.get_by_patient_id(db, patient_id=obj_in.patient_id)
        if not patient:
            raise ValueError("Patient not found.")
        if patient.patient_type != "STUDENT":
            raise ValueError("Patient is not registered as a STUDENT.")

        existing_student = self.get_by_patient_id(db, patient_id=obj_in.patient_id)
        if existing_student:
            raise ValueError(f"Student details already exist for patient {obj_in.patient_id}")

        department = departments_lookup_service.get_by_dl_id(db, dl_id=obj_in.dl_id)
        if not department:
            raise ValueError(f"Department {obj_in.dl_id} not found.")

        data = obj_in.model_dump(exclude={"patient_id", "dl_id"})
        
        db_obj = StudentType(
            **data,
            patient_uuid=patient.uuid,
            dl_uuid=department.uuid
        )

        return super().create(db, obj_in=db_obj)

    def update(self, db: Session, *, db_obj: StudentType, obj_in: Union[StudentTypeUpdate, Dict[str, Any]]) -> StudentType:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)
            
        if "dl_id" in update_data:
            dl_id = update_data.pop("dl_id")
            department = departments_lookup_service.get_by_dl_id(db, dl_id=dl_id)
            if not department:
                raise ValueError(f"Department {dl_id} not found.")
            update_data["dl_uuid"] = department.uuid
            
        return super().update(db, db_obj=db_obj, obj_in=update_data)


class PersonnelTypeService(BaseService[PersonnelType]):
    def __init__(self):
        super().__init__(PersonnelType)

    def get_by_patient_id(self, db: Session, patient_id: str, include_deleted: bool = False) -> Optional[PersonnelType]:
        patient = patient_service.get_by_patient_id(db, patient_id=patient_id)
        if not patient:
            return None

        statement = select(self.model).where(self.model.patient_uuid == patient.uuid)
        
        if not include_deleted:
            statement = statement.where(self.model.is_deleted.is_(False))
            
        return db.exec(statement).first()

    def create(self, db: Session, *, obj_in: PersonnelTypeCreate) -> PersonnelType:
        patient = patient_service.get_by_patient_id(db, patient_id=obj_in.patient_id)
        if not patient:
            raise ValueError("Patient not found.")
        if patient.patient_type != "PERSONNEL":
            raise ValueError("Patient is not registered as PERSONNEL.")

        existing_personnel = self.get_by_patient_id(db, patient_id=obj_in.patient_id)
        if existing_personnel:
            raise ValueError(f"Personnel details already exist for patient {obj_in.patient_id}")

        department = departments_lookup_service.get_by_dl_id(db, dl_id=obj_in.dl_id)
        if not department:
            raise ValueError(f"Department {obj_in.dl_id} not found.")

        data = obj_in.model_dump(exclude={"patient_id", "dl_id"})
        
        db_obj = PersonnelType(
            **data,
            patient_uuid=patient.uuid,
            dl_uuid=department.uuid
        )

        return super().create(db, obj_in=db_obj)

    def update(self, db: Session, *, db_obj: PersonnelType, obj_in: Union[PersonnelTypeUpdate, Dict[str, Any]]) -> PersonnelType:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)
            
        if "dl_id" in update_data:
            dl_id = update_data.pop("dl_id")
            department = departments_lookup_service.get_by_dl_id(db, dl_id=dl_id)
            if not department:
                raise ValueError(f"Department {dl_id} not found.")
            update_data["dl_uuid"] = department.uuid
            
        return super().update(db, db_obj=db_obj, obj_in=update_data)


patient_service = PatientService()
student_type_service = StudentTypeService()
personnel_type_service = PersonnelTypeService()