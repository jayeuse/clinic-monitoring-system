from enum import Enum

from sqlmodel import Field

from models.base import BaseModel


class DepartmentType(str, Enum):
    ACADEMIC = "ACADEMIC"
    ADMINISTRATIVE = "ADMINISTRATIVE"

class DepartmentsLookup(BaseModel, table=True):
    dl_id: str = Field(unique=True, index=True, max_length=20)
    department_name: str = Field(unique=True, max_length=100)
    department_type: DepartmentType = Field(index=True)

    is_active: bool = Field(default=True)

class MedicalConditionsLookup(BaseModel, table=True):
    mcl_id: str = Field(unique=True, index=True, max_length=20)
    condition_name: str = Field(unique=True, max_length=150)

    is_active: bool = Field(default=True)

class SmokingTypesLookup(BaseModel, table=True):
    stl_id: str = Field(unique=True, index=True, max_length=20)
    type_name: str = Field(unique=True, max_length=150)

    is_active: bool = Field(default=True)
    
class BodySystemsLookup(BaseModel, table=True):
    bsl_id: str = Field(unique=True, index=True, max_length=20)
    system_name: str = Field(unique=True, max_length=150)

    is_active: bool = Field(default=True)