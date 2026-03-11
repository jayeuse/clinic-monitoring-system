from datetime import date
from typing import Any, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, computed_field

from models.history import AlcoholStatus, BodySystemStatus, DrugStatus, SmokeStatus


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

class MedicalExaminationFindingsCreate(BaseModel):
    bsl_uuid: UUID
    status: BodySystemStatus = BodySystemStatus.NOT_ASSESSED
    condition_notes: Optional[str] = None

class MedicalExaminationFindingsPublic(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    me_uuid: UUID
    bsl_uuid: UUID
    status: BodySystemStatus
    condition_notes: Optional[str]


class MedicalExaminationCreate(BaseModel):
    patient_id: str
    mh_id: str
    date_taken: Optional[date] = None

    findings: Optional[list[MedicalExaminationFindingsCreate]] = None

class MedicalExaminationUpdate(BaseModel):
    date_taken: Optional[date] = None
    findings: Optional[list[MedicalExaminationFindingsCreate]] = None

class MedicalExaminationPublic(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    me_id: str
    patient_uuid: UUID
    mh_uuid: UUID
    date_taken: date

    findings: Optional[list[MedicalExaminationFindingsPublic]] = None