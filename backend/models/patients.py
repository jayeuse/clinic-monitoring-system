from sqlmodel import Relationship
from uuid import UUID
from typing import Optional, TYPE_CHECKING
from datetime import date
from sqlmodel import Field
from models.base import BaseModel
from enum import Enum

if TYPE_CHECKING:
    from .clinic import ClinicTransaction

class PatientType(str, Enum):
    STUDENT = "STUDENT"
    PERSONNEL = "PERSONNEL"

class SexType(str, Enum):
    M = "M"
    F = "F"

class PatientInformation(BaseModel, table=True):
    patient_id: str = Field(unique=True, index=True, max_length=20)
    patient_type: PatientType = Field(index=True)

    last_name: str = Field(max_length=100)
    first_name: str = Field(max_length=100)
    middle_name: Optional[str] = Field(default=None, max_length=100)

    birthdate: date
    sex: SexType

    civil_status: Optional[str] = Field(default=None, max_length=50)
    religion: Optional[str] = Field(default=None, max_length=50)
    nationality: Optional[str] = Field(default=None, max_length=50)
    contact_no: Optional[str] = Field(default=None, max_length=50)

    house_no: Optional[str] = Field(default=None, max_length=20)
    street: Optional[str] = Field(default=None, max_length=100)
    subdivision: Optional[str] = Field(default=None, max_length=100)
    barangay: Optional[str] = Field(default=None, max_length=100)
    city: Optional[str] = Field(default=None, max_length=100)
    province: Optional[str] = Field(default=None, max_length=100)
    zip_code: Optional[str] = Field(default=None, max_length=10)

    transactions: list["ClinicTransaction"] = Relationship(back_populates="patient")

class StudentType(BaseModel, table=True):
    patient_uuid: UUID = Field(foreign_key="patientinformation.uuid", unique=True)
    
    student_id: str = Field(unique=True, index=True, max_length=20)

    dl_uuid: Optional[UUID] = Field(default=None, foreign_key="departmentslookup.uuid")

    course: str = Field(max_length=100)
    batch: str = Field(max_length=20)
    school_year: str = Field(max_length=20)

class PersonnelType(BaseModel, table=True):
    patient_uuid: UUID = Field(foreign_key="patientinformation.uuid", unique=True)

    personnel_id: str = Field(unique=True, index=True, max_length=20)

    dl_uuid: Optional[UUID] = Field(default=None, foreign_key="departmentslookup.uuid")

    teaching: bool = Field(default=False)