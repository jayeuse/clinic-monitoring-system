from datetime import date
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field, field_validator

from models.dental import PeriodontalDiagnosis, SeverityType, ToothStatus


class ToothFindingBase(BaseModel):
    tooth_number: str
    status: ToothStatus = ToothStatus.SOUND

    @field_validator("tooth_number")
    @classmethod
    def validate_fdi_tooth(cls, v: str) -> str:
        if not v.isdigit():
            raise ValueError("Tooth number must be numeric")
        
        num = int(v)
        if not ((11 <= num <= 48) or (51 <= num <= 85)):
            raise ValueError(f"Invalid FDI Tooth Number: {v}")

        return v

class ToothFindingCreate(ToothFindingBase):
    pass

class ToothFindingPublic(ToothFindingBase):
    tf_id: str



class DentalExaminationCreate(BaseModel):
    patient_id: str
    examination_date: date = Field(default_factory=date.today)

    head_findings: Optional[str] = "WNL"
    face_findings: Optional[str] = "WNL"
    tmj_findings: Optional[str] = "WNL"

    periodontal_diagnosis: Optional[PeriodontalDiagnosis] = None
    periodontitis_severity: Optional[SeverityType] = None
    periodontal_others: Optional[str] = None

    lips_findings: Optional[str] = "WNL"
    palate_findings: Optional[str] = "WNL"
    floor_of_mouth_findings: Optional[str] = "WNL"
    tongue_findings: Optional[str] = "WNL"

    findings: List[ToothFindingBase] = []

class DentalExaminationUpdate(BaseModel):

    head_findings: Optional[str] = None
    face_findings: Optional[str] = None
    tmj_findings: Optional[str] = None

    periodontal_diagnosis: Optional[PeriodontalDiagnosis] = None
    periodontitis_severity: Optional[SeverityType] = None
    periodontal_others: Optional[str] = None

    lips_findings: Optional[str] = None
    palate_findings: Optional[str] = None
    floor_of_mouth_findings: Optional[str] = None
    tongue_findings: Optional[str] = None


class DentalExaminationPublic(BaseModel):
    dru_id: str
    dr_uuid: UUID

    examination_date: date

    head_findings: str
    face_findings: str
    tmj_findings: str

    periodontal_diagnosis: Optional[PeriodontalDiagnosis]
    periodontitis_severity: Optional[SeverityType]

class DentalTreatmentCreate(BaseModel):
    patient_id: str

    service_date: date = Field(default_factory=date.today)
    tooth_number: Optional[str]

    oral_prophy: bool = False
    temp_filling: bool = False
    perm_filling: bool = False
    sealant: bool = False
    extraction: bool = False
    consultation: bool = False
    others: Optional[str] = None
    remarks: Optional[str] = None

class DentalTreatmentUpdate(BaseModel):
    
    tooth_number: Optional[str] = None

    oral_prophy: Optional[bool] = None
    temp_filling: Optional[bool] = None 
    perm_filling: Optional[bool] = None 
    sealant: Optional[bool] = None
    extraction: Optional[bool] = None
    consultation: Optional[bool] = None

    others: Optional[str] = None
    remarks: Optional[str] = None

class DentalTreatmentPublic(BaseModel):
    dsr_id: str

    service_date: date
    tooth_number: Optional[str]
    remarks: Optional[str]

class DentalRecordCreate(BaseModel):
    patient_id: str

    last_dental_visit: Optional[date] = None
    reason_for_last_dental_visit: Optional[str] = None

    last_hospitalization: Optional[date] = None
    hospitalization_reason: Optional[str] = None

    known_allergies: Optional[str] = None
    tobacco_use: Optional[str] = None
    alcohol_drug_use: Optional[str] = None
    for_women_status: Optional[str] = None
    chart_image_url: Optional[str] = None

class DentalRecordPublic(BaseModel):
    dr_id: str
    patient_uuid: UUID
    last_dental_visit: Optional[date]
    chart_image_url: Optional[str]

class DentalRecordUpdate(BaseModel):
    
    last_dental_visit: Optional[date] = None
    reason_for_last_dental_visit: Optional[str] = None

    last_hospitalization: Optional[date] = None
    hospitalization_reason: Optional[str] = None

    known_allergies: Optional[str] = None
    tobacco_use: Optional[str] = None
    alcohol_drug_use: Optional[str] = None
    for_women_status: Optional[str] = None
    chart_image_url: Optional[str] = None