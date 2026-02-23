from models.patients import SexType
from datetime import date
from typing import Optional
from models.patients import PatientType
from pydantic import BaseModel, computed_field

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