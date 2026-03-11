from datetime import date
from typing import Optional

from pydantic import BaseModel, computed_field

from models.patients import PatientType, SexType


class PatientCreate(BaseModel):
    patient_type: PatientType

    last_name: str
    first_name: str
    middle_name: Optional[str] = None

    birthdate: date
    sex: SexType

    civil_status: Optional[str] = None
    religion: Optional[str] = None
    nationality: Optional[str] = None

    contact_no: Optional[str] = None

    house_no: Optional[str] = None
    street: Optional[str] = None
    subdivision: Optional[str] = None
    barangay: Optional[str] = None
    city: Optional[str] = None
    province: Optional[str] = None
    zip_code: Optional[str] = None

class PatientUpdate(BaseModel):
    patient_type: Optional[PatientType] = None

    last_name: Optional[str] = None
    first_name: Optional[str] = None
    middle_name: Optional[str] = None

    birthdate: Optional[date] = None
    sex: Optional[SexType] = None

    civil_status: Optional[str] = None
    religion: Optional[str] = None
    nationality: Optional[str] = None

    contact_no: Optional[str] = None

    house_no: Optional[str] = None
    street: Optional[str] = None
    subdivision: Optional[str] = None
    barangay: Optional[str] = None
    city: Optional[str] = None
    province: Optional[str] = None
    zip_code: Optional[str] = None

class PatientPublic(BaseModel):
    patient_id: str
    patient_type: PatientType

    last_name: str
    first_name: str
    middle_name: Optional[str] = None

    birthdate: date
    sex: SexType

    civil_status: Optional[str] = None
    religion: Optional[str] = None
    nationality: Optional[str] = None

    contact_no: Optional[str] = None

    house_no: Optional[str] = None
    street: Optional[str] = None
    subdivision: Optional[str] = None
    barangay: Optional[str] = None
    city: Optional[str] = None
    province: Optional[str] = None
    zip_code: Optional[str] = None

    @computed_field
    @property
    def age(self) -> int:
        today = date.today()
        return today.year - self.birthdate.year - ((today.month, today.day) < (self.birthdate.month, self.birthdate.day))

class EmergencyContactCreate(BaseModel):
    patient_id: str
    last_name: str
    first_name: str
    middle_name: Optional[str] = None
    relation_to_patient: str
    house_no: Optional[str] = None
    street: Optional[str] = None
    subdivision: Optional[str] = None
    barangay: Optional[str] = None
    city: Optional[str] = None
    province: Optional[str] = None
    zip_code: Optional[str] = None

class EmergencyContactUpdate(BaseModel):
    last_name: Optional[str] = None
    first_name: Optional[str] = None
    middle_name: Optional[str] = None
    relation_to_patient: Optional[str] = None
    house_no: Optional[str] = None
    street: Optional[str] = None
    subdivision: Optional[str] = None
    barangay: Optional[str] = None
    city: Optional[str] = None
    province: Optional[str] = None
    zip_code: Optional[str] = None

class EmergencyContactPublic(BaseModel):
    ec_id: str
    last_name: str
    first_name: str
    middle_name: Optional[str] = None
    relation_to_patient: str
    house_no: Optional[str] = None
    street: Optional[str] = None
    subdivision: Optional[str] = None
    barangay: Optional[str] = None
    city: Optional[str] = None
    province: Optional[str] = None
    zip_code: Optional[str] = None

class StudentTypeCreate(BaseModel):
    student_id: str
    patient_id: str
    dl_id: str

    course: str
    batch: str
    school_year: str

class StudentTypeUpdate(BaseModel):
    dl_id: Optional[str] = None

    course: Optional[str] = None
    batch: Optional[str] = None
    school_year: Optional[str] = None

class StudentTypePublic(BaseModel):
    student_id: str
    patient_uuid: str
    dl_uuid: Optional[str] = None

    course: str
    batch: str
    school_year: str

class PersonnelTypeCreate(BaseModel):
    personnel_id: str
    patient_id: str

    dl_id: str
    teaching: bool

class PersonnelTypeUpdate(BaseModel):
    dl_id: Optional[str] = None

    teaching: Optional[bool] = None

class PersonnelTypePublic(BaseModel):
    personnel_id: str
    patient_uuid: str
    
    dl_uuid: Optional[str] = None
    teaching: bool

