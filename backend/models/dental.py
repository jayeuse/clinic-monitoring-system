from datetime import date, datetime, timezone
from enum import Enum
from typing import Optional
from uuid import UUID

from sqlmodel import TEXT, Field

from models.base import BaseModel


class PeriodontalDiagnosis(str, Enum):
    HEALTHY = "HEALTHY"
    GINGIVITIS_LOCALIZED = "GINGIVITIS_LOCALIZED"
    GINGIVITIS_GENERALIZED = "GINGIVITIS_GENERALIZED"
    PERIODONTITIS_LOCALIZED = "PERIODONTITIS_LOCALIZED"
    PERIODONTITIS_GENERALIZED = "PERIODONTITIS_GENERALIZED"
    OTHERS = "OTHERS"

class SeverityType(str, Enum):
    SLIGHT = "SLIGHT"
    MODERATE = "MODERATE"
    SEVERE = "SEVERE"

class ToothStatus(str, Enum):
    SOUND = "SOUND"
    DECAYED = "DECAYED"
    FILLED = "FILLED"
    MISSING = "MISSING"
    FOR_EXTRACTION = "FOR_EXTRACTION"
    UNERUPTED = "UNERUPTED"
    JACKET_CROWN = "JACKET_CROWN"
    PONTIC = "PONTIC"
    IMPACTED = "IMPACTED"

class DentalRecord(BaseModel, table=True):
    dr_id: str = Field(unique=True, index=True, max_length=20)

    patient_uuid: UUID = Field(foreign_key="patientinformation.uuid", index=True, unique=True)
    mh_uuid: UUID = Field(foreign_key="medicalhistory.uuid")

    last_dental_visit: Optional[date] = Field(default=None)
    reason_for_last_dental_visit: Optional[str] = Field(default=None, sa_type=TEXT)

    last_hospitalization: Optional[date] = Field(default=None)
    hospitalization_reason: Optional[str] = Field(default=None, sa_type=TEXT)
    
    known_allergies: Optional[str] = Field(default=None, sa_type=TEXT)
    tobacco_use: Optional[str] = Field(default=None, sa_type=TEXT)
    alcohol_drug_use: Optional[str] = Field(default=None, sa_type=TEXT)
    for_women_status: Optional[str] = Field(default=None, sa_type=TEXT)
    
    chart_image_url: Optional[str] = Field(default=None, max_length=500)

class DentalExamination(BaseModel, table=True):
    __tablename__ = "dentalrecordupdate"
    
    dru_id: str = Field(unique=True, index=True, max_length=20)

    dr_uuid: UUID = Field(foreign_key="dentalrecord.uuid", index=True, unique=True)

    # examined_by: UUID = Field(foreign_key="user.uuid") -> Noted for later
    examination_date: date = Field(default_factory=date.today)

    head_findings: Optional[str] = Field(default="WNL", max_length=255)
    face_findings: Optional[str] = Field(default="WNL", max_length=255)
    tmj_findings: Optional[str] = Field(default="WNL", max_length=255)

    periodontal_diagnosis: Optional[PeriodontalDiagnosis] = Field(default=None)
    periodontitis_severity: Optional[SeverityType] = Field(default=None)
    periodontal_others: Optional[str] = Field(default=None, sa_type=TEXT)

    #Intraoral Tissues
    lips_findings: Optional[str] = Field(default="WNL", max_length=255)
    palate_findings: Optional[str] = Field(default="WNL", max_length=255)
    floor_of_mouth_findings: Optional[str] = Field(default="WNL", max_length=255)
    tongue_findings: Optional[str] = Field(default="WNL", max_length=255)

class ToothFinding(BaseModel, table=True):
    tf_id: str = Field(unique=True, index=True, max_length=20)
    
    dru_uuid: UUID = Field(foreign_key="dentalrecordupdate.uuid")

    tooth_number: str = Field(max_length=5)
    status: ToothStatus = Field(default=ToothStatus.SOUND)

class DentalServiceRendered(BaseModel, table=True):
    dsr_id: str = Field(unique=True, index=True, max_length=20)

    dr_uuid: UUID = Field(foreign_key="dentalrecord.uuid")

    # performed_by: UUID = Field(foreign_key="user.uuid") To be implemented later

    service_date: date = Field(default_factory=date.today)

    tooth_number: Optional[str] = Field(default=None, max_length=5)

    oral_prophy: bool = Field(default=False)
    temp_filling: bool = Field(default=False)
    perm_filling: bool = Field(default=False)
    sealant: bool = Field(default=False)
    extraction: bool = Field(default=False)
    consultation: bool = Field(default=False)

    others: Optional[str] = Field(default=None, sa_type=TEXT)
    remarks: Optional[str] = Field(default=None, sa_type=TEXT)

class DentalRecordSnapshot(BaseModel, table=True):

    snapshot_id: str = Field(unique=True, index=True, max_length=20)
    original_dr_uuid: UUID = Field(foreign_key="dentalrecord.uuid", index=True)
    snapshot_date: datetime = Field(default_factory=lambda:datetime.now(timezone.utc))

    last_dental_visit: Optional[date] = Field(default=None)
    reason_for_last_dental_visit: Optional[str] = Field(default=None, sa_type=TEXT)

    last_hospitalization: Optional[date] = Field(default=None)
    hospitalization_reason: Optional[str] = Field(default=None, sa_type=TEXT)
    
    known_allergies: Optional[str] = Field(default=None, sa_type=TEXT)
    tobacco_use: Optional[str] = Field(default=None, sa_type=TEXT)
    alcohol_drug_use: Optional[str] = Field(default=None, sa_type=TEXT)
    for_women_status: Optional[str] = Field(default=None, sa_type=TEXT)
    
    chart_image_url: Optional[str] = Field(default=None, max_length=500)

class DentalExaminationSnapshot(BaseModel, table=True):

    snapshot_id: str = Field(unique=True, index=True, max_length=20)
    original_dr_uuid: UUID = Field(foreign_key="dentalrecordupdate.uuid", index=True)
    snapshot_date: datetime = Field(default_factory=lambda:datetime.now(timezone.utc))

    # examined_by: UUID = Field(foreign_key="user.uuid") -> Noted for later
    examination_date: date = Field(default_factory=date.today)

    head_findings: Optional[str] = Field(default="WNL", max_length=255)
    face_findings: Optional[str] = Field(default="WNL", max_length=255)
    tmj_findings: Optional[str] = Field(default="WNL", max_length=255)

    periodontal_diagnosis: Optional[PeriodontalDiagnosis] = Field(default=None)
    periodontitis_severity: Optional[SeverityType] = Field(default=None)
    periodontal_others: Optional[str] = Field(default=None, sa_type=TEXT)

    #Intraoral Tissues
    lips_findings: Optional[str] = Field(default="WNL", max_length=255)
    palate_findings: Optional[str] = Field(default="WNL", max_length=255)
    floor_of_mouth_findings: Optional[str] = Field(default="WNL", max_length=255)
    tongue_findings: Optional[str] = Field(default="WNL", max_length=255)

