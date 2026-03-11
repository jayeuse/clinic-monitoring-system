from datetime import datetime, timezone
from typing import Generic, List, Optional, Tuple, Type, TypeVar, Union
from uuid import UUID

from sqlmodel import Session, func, select

from models import BaseModel

T = TypeVar("T", bound=BaseModel)

class BaseService(Generic[T]):
    def __init__(self, model: Type[T]):
        self.model = model

    def get(self, db: Session, uuid: UUID) -> Optional[T]:
        obj = db.get(self.model, uuid)

        if obj and getattr(obj, "is_deleted", False):
            return None

        return obj

    def get_all(self, db: Session, *, skip: int = 0, limit: int = 100) -> Tuple[List[T], int]:
        statement = select(self.model).where(self.model.is_deleted.is_(False)).offset(skip).limit(limit)
        
        count_statement = select(func.count()).select_from(self.model).where(self.model.is_deleted.is_(False))
        
        return db.exec(statement).all(), db.exec(count_statement).one()


    def create(self, db: Session, *, obj_in: T) -> T:
        db.add(obj_in)
        db.commit()
        db.refresh(obj_in)
        return obj_in

    def update(self, db: Session, *, db_obj: T, obj_in: Union[dict, T]) -> T:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)
        
        for field, value in update_data.items():
            setattr(db_obj, field, value)

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, uuid: UUID) -> T:
        obj = db.get(self.model, uuid)
        if obj:
            obj.is_deleted = True
            obj.deleted_at = datetime.now(timezone.utc)
            db.add(obj)
            db.commit()
            db.refresh(obj)

        return obj

    def restore(self, db: Session, *, uuid: UUID) -> T:
        obj = db.get(self.model, uuid)
        if obj and obj.is_deleted:
            obj.is_deleted = False
            obj.deleted_at = None
            db.add(obj)
            db.commit()
            db.refresh(obj)

        return obj
