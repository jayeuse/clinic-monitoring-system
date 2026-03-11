from typing import Optional

from sqlmodel import Session, func, select

from models.lookups import (
    BodySystemsLookup,
    DepartmentsLookup,
    MedicalConditionsLookup,
    SmokingTypesLookup,
)
from schemas.lookup_schemas import (
    BodySystemsLookupCreate,
    DepartmentsLookupCreate,
    MedicalConditionsLookupCreate,
    SmokingTypesLookupCreate,
)
from services.base import BaseService


class DepartmentsLookupService(BaseService[DepartmentsLookup]):
    def __init__(self):
        super().__init__(DepartmentsLookup)

    def get_by_dl_id(self, db: Session, dl_id: str) -> Optional[DepartmentsLookup]:
        statement = select(self.model).where(
            self.model.dl_id == dl_id, self.model.is_deleted.is_(False)
        )
        return db.exec(statement).first()

    def create(self, db: Session, *, obj_in: DepartmentsLookupCreate) -> DepartmentsLookup:
        statement = select(func.count()).select_from(self.model)
        count = db.exec(statement).one()
        new_id = f"DL-{count + 1:06d}"

        db_obj = DepartmentsLookup(**obj_in.model_dump(), dl_id=new_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


class MedicalConditionsLookupService(BaseService[MedicalConditionsLookup]):
    def __init__(self):
        super().__init__(MedicalConditionsLookup)

    def get_by_mcl_id(self, db: Session, mcl_id: str) -> Optional[MedicalConditionsLookup]:
        statement = select(self.model).where(
            self.model.mcl_id == mcl_id, self.model.is_deleted.is_(False)
        )
        return db.exec(statement).first()

    def create(self, db: Session, *, obj_in: MedicalConditionsLookupCreate) -> MedicalConditionsLookup:
        statement = select(func.count()).select_from(self.model)
        count = db.exec(statement).one()
        new_id = f"MCL-{count + 1:06d}"

        db_obj = MedicalConditionsLookup(**obj_in.model_dump(), mcl_id=new_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


class SmokingTypesLookupService(BaseService[SmokingTypesLookup]):
    def __init__(self):
        super().__init__(SmokingTypesLookup)

    def get_by_stl_id(self, db: Session, stl_id: str) -> Optional[SmokingTypesLookup]:
        statement = select(self.model).where(
            self.model.stl_id == stl_id, self.model.is_deleted.is_(False)
        )
        return db.exec(statement).first()

    def create(self, db: Session, *, obj_in: SmokingTypesLookupCreate) -> SmokingTypesLookup:
        statement = select(func.count()).select_from(self.model)
        count = db.exec(statement).one()
        new_id = f"STL-{count + 1:06d}"

        db_obj = SmokingTypesLookup(**obj_in.model_dump(), stl_id=new_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


class BodySystemsLookupService(BaseService[BodySystemsLookup]):
    def __init__(self):
        super().__init__(BodySystemsLookup)

    def get_by_bsl_id(self, db: Session, bsl_id: str) -> Optional[BodySystemsLookup]:
        statement = select(self.model).where(
            self.model.bsl_id == bsl_id, self.model.is_deleted.is_(False)
        )
        return db.exec(statement).first()

    def create(self, db: Session, *, obj_in: BodySystemsLookupCreate) -> BodySystemsLookup:
        statement = select(func.count()).select_from(self.model)
        count = db.exec(statement).one()
        new_id = f"BSL-{count + 1:06d}"

        db_obj = BodySystemsLookup(**obj_in.model_dump(), bsl_id=new_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


departments_lookup_service = DepartmentsLookupService()
medical_conditions_lookup_service = MedicalConditionsLookupService()
smoking_types_lookup_service = SmokingTypesLookupService()
body_systems_lookup_service = BodySystemsLookupService()
