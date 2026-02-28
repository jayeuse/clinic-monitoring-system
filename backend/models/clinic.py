from sqlmodel import Relationship
from uuid import UUID
from typing import Optional, TYPE_CHECKING
from datetime import date, time
from sqlmodel import Field, TEXT
from models.base import BaseModel

if TYPE_CHECKING:
    from .patients import PatientInformation

class ClinicTransaction(BaseModel, table=True):
    ct_id: str = Field(unique=True, index=True, max_length=20)

    patient_uuid: UUID = Field(foreign_key="patientinformation.uuid", index=True)

    patient: "PatientInformation" = Relationship(back_populates="transactions")
    vital_signs: list["VitalSigns"] = Relationship(back_populates="transaction")

    transaction_date: date = Field(default_factory=date.today)
    time_in: time
    time_out: Optional[time] = Field(default=None)

    category: str = Field(max_length=100)
    reason: str = Field(sa_type=TEXT)

    medication_given: Optional[str] = Field(default=None, max_length=255)
    quantity: Optional[int] = Field(default=None)
    remarks: Optional[str] = Field(default=None, sa_type=TEXT)


class VitalSigns(BaseModel, table=True):
    vs_id: str = Field(unique=True, index=True, max_length=20)

    ct_uuid: UUID = Field(foreign_key="clinictransaction.uuid", index=True)

    transaction: "ClinicTransaction" = Relationship(back_populates="vital_signs")

    date_taken: date = Field(default_factory=date.today)

    height: Optional[float] = Field(default=None)
    weight: Optional[float] = Field(default=None)
    bmi: Optional[float] = Field(default=None)

    temperature: Optional[float] = Field(default=None)
    pulse: Optional[int] = Field(default=None)
    blood_pressure: Optional[str] = Field(default=None, max_length=10)
    respiratory_rate: Optional[int] = Field(default=None)