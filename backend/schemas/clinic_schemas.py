from pydantic import Field
from datetime import time
from datetime import date
from typing import Optional, Any
from pydantic import BaseModel, computed_field

class VitalSignsCreate(BaseModel):
    ct_id: str
    height: Optional[float] = None
    weight: Optional[float] = None
    temperature: Optional[float] = None
    pulse: Optional[int] = None
    blood_pressure: Optional[str] = None
    respiratory_rate: Optional[int] = None

class VitalSignsPublic(BaseModel):
    vs_id: str

    transaction: Optional[Any] = Field(default=None, exclude=True)
    date_taken: date
    height: Optional[float] = None
    weight: Optional[float] = None
    temperature: Optional[float] = None
    pulse: Optional[int] = None
    blood_pressure: Optional[str] = None
    respiratory_rate: Optional[int] = None

    @computed_field
    @property
    def ct_id(self) -> str:
        return self.transaction.ct_id if self.transaction else "UNK-000000"

    @computed_field
    @property
    def bmi(self) -> Optional[float]:
        if self.height and self.weight and self.height > 0:
            height_in_meters = self.height / 100
            return round(self.weight / (height_in_meters ** 2), 2)
        
        return None

class ClinicTransactionCreate(BaseModel):
    patient_id: str
    category: str
    reason: str
    medication_given: Optional[str] = None
    quantity: Optional[int] = None
    remarks: Optional[str] = None

class ClinicTransactionPublic(BaseModel):
    ct_id: str

    patient: Optional[Any] = Field(None, exclude=True)
    transaction_date: date
    time_in: time
    time_out: Optional[time] = None
    category: str
    reason: str
    medication_given: Optional[str] = None
    quantity: Optional[int] = None
    remarks: Optional[str] = None

    @computed_field
    @property
    def patient_id(self) -> str:
        return self.patient.patient_id if hasattr(self, 'patient') and self.patient else "UNK-000000"