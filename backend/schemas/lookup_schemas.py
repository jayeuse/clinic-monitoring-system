from typing import Optional

from pydantic import BaseModel, ConfigDict

from models.lookups import DepartmentType


class DepartmentsLookupCreate(BaseModel):
    department_name: str
    department_type: DepartmentType
    is_active: bool = True

class DepartmentsLookupUpdate(BaseModel):
    department_name: Optional[str] = None
    department_type: Optional[DepartmentType] = None
    is_active: Optional[bool] = None

class DepartmentsLookupPublic(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    dl_id: str
    department_name: str
    department_type: DepartmentType
    is_active: bool


class MedicalConditionsLookupCreate(BaseModel):
    condition_name: str
    is_active: bool = True

class MedicalConditionsLookupUpdate(BaseModel):
    condition_name: Optional[str] = None
    is_active: Optional[bool] = None

class MedicalConditionsLookupPublic(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    mcl_id: str
    condition_name: str
    is_active: bool


class SmokingTypesLookupCreate(BaseModel):
    type_name: str
    is_active: bool = True

class SmokingTypesLookupUpdate(BaseModel):
    type_name: Optional[str] = None
    is_active: Optional[bool] = None

class SmokingTypesLookupPublic(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    stl_id: str
    type_name: str
    is_active: bool


class BodySystemsLookupCreate(BaseModel):
    system_name: str
    is_active: bool = True

class BodySystemsLookupUpdate(BaseModel):
    system_name: Optional[str] = None
    is_active: Optional[bool] = None

class BodySystemsLookupPublic(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    bsl_id: str
    system_name: str
    is_active: bool
