from pydantic import Field, computed_field
from typing import Any
from pydantic import ConfigDict
from models.history import AlcoholStatus
from models.history import DrugStatus
from datetime import date
from typing import Optional
from models.history import SmokeStatus
from pydantic import BaseModel

class MedicalHistoryCreate(BaseModel):
    patient_id: str

    smoking_status: SmokeStatus = SmokeStatus.NEVER
    smoking_started_since: Optional[date] = None

    drug_status: DrugStatus = DrugStatus.NEVER
    drug_name: Optional[str] = None
    did_rehab: Optional[bool] = None

    alcohol_status: AlcoholStatus = AlcoholStatus.NEVER
    alcohol_est_consumption: Optional[str] = None

    no_of_pregnancies: Optional[int] = None
    no_of_miscarriages: Optional[int] = None
    no_of_term_deliveries: Optional[int] = None
    no_of_premature_deliveries: Optional[int] = None
    total_children: Optional[int] = None

    surgery_notes: Optional[str] = None
    maintenance_medications: Optional[str] = None

class MedicalHistoryUpdate(BaseModel):
    smoking_status: Optional[SmokeStatus] = None
    smoking_started_since: Optional[date] = None

    drug_status: Optional[DrugStatus] = None
    drug_name: Optional[str] = None
    did_rehab: Optional[bool] = None

    alcohol_status: Optional[AlcoholStatus] = None
    alcohol_est_consumption: Optional[str] = None
    
    no_of_pregnancies: Optional[int] = None
    no_of_miscarriages: Optional[int] = None
    no_of_term_deliveries: Optional[int] = None
    no_of_premature_deliveries: Optional[int] = None
    total_children: Optional[int] = None
    
    surgery_notes: Optional[str] = None
    maintenance_medications: Optional[str] = None


class MedicalHistoryPublic(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    mh_id: str

    patient: Optional[Any] = Field(default=None, exclude=True)

    smoking_status: SmokeStatus
    smoking_started_since: Optional[date]
    drug_status: DrugStatus
    drug_name: Optional[str]
    did_rehab: Optional[bool]
    alcohol_status: AlcoholStatus
    alcohol_est_consumption: Optional[str]
    
    no_of_pregnancies: Optional[int]
    no_of_miscarriages: Optional[int]
    no_of_term_deliveries: Optional[int]
    no_of_premature_deliveries: Optional[int]
    total_children: Optional[int]
    
    surgery_notes: Optional[str]
    maintenance_medications: Optional[str]

    @computed_field
    @property
    def patient_id(self) -> str:
        return self.patient.patient_id if self.patient else "UNK-000000"