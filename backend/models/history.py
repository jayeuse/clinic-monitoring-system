from sqlmodel import Relationship
from datetime import date
from typing import Optional, TYPE_CHECKING
from uuid import UUID
from sqlmodel import Field, TEXT
from models.base import BaseModel
from enum import Enum

class SmokeStatus(str, Enum):
    NEVER = "NEVER"
    TRIED_ONCE = "TRIED_ONCE"
    STOPPED_SINCE = "STOPPED_SINCE"
    ACTIVE = "ACTIVE"

class DrugStatus(str, Enum):
    NEVER = "NEVER"
    TRIED_ONCE = "TRIED_ONCE"
    SOMETIMES = "SOMETIMES"
    ACTIVE = "ACTIVE"

class AlcoholStatus(str, Enum):
    NEVER = "NEVER"
    ONCE_A_WEEK = "ONCE_A_WEEK"
    MORE_THAN_ONCE_A_WEEK = "MORE_THAN_ONCE_A_WEEK"

class BodySystemStatus(str, Enum):
    NORMAL = "NORMAL"
    ABNORMAL = "ABNORMAL"
    NOT_ASSESSED = "NOT_ASSESSED"

if TYPE_CHECKING:
    from .patients import PatientInformation

class MedicalHistory(BaseModel, table=True):
    mh_id: str = Field(unique=True, index=True, max_length=20)

    patient: "PatientInformation" = Relationship(back_populates="medical_history")

    patient_uuid: UUID = Field(foreign_key="patientinformation.uuid", index=True)

    smoking_status: SmokeStatus = Field(default=SmokeStatus.NEVER)
    smoking_started_since: Optional[date] = Field(default=None)

    drug_status: DrugStatus = Field(default=DrugStatus.NEVER)
    drug_name: Optional[str] = Field(default=None)
    did_rehab: Optional[bool] = Field(default=None)

    alcohol_status: AlcoholStatus = Field(default=AlcoholStatus.NEVER)
    alcohol_est_consumption: Optional[str] = Field(default=None)

    no_of_pregnancies: Optional[int] = Field(default=None)
    no_of_miscarriages: Optional[int] = Field(default=None)
    no_of_term_deliveries: Optional[int] = Field(default=None)
    no_of_premature_deliveries: Optional[int] = Field(default=None)
    total_children: Optional[int] = Field(default=None)

    surgery_notes: Optional[str] = Field(default=None, sa_type=TEXT)
    maintenance_medications: Optional[str] = Field(default=None, sa_type=TEXT)

class PatientSmokingTypes(BaseModel, table=True):
    mh_uuid: UUID = Field(foreign_key="medicalhistory.uuid")
    stl_uuid: UUID = Field(foreign_key="smokingtypeslookup.uuid")
    frequency: Optional[int] = Field(default=None)

class PatientDiagnosedConditions(BaseModel, table=True):
    mh_uuid: UUID = Field(foreign_key="medicalhistory.uuid")
    mcl_uuid: UUID = Field(foreign_key="medicalconditionslookup.uuid")

    date_diagnosed: Optional[date] = Field(default=None)

class MedicalHistoryUpdate(BaseModel, table=True):
    mhu_id: str = Field(unique=True, index=True, max_length=20)

    patient_uuid: UUID = Field(foreign_key="patientinformation.uuid")
    mh_uuid: UUID = Field(foreign_key="medicalhistory.uuid")

    # recorded_by = UUID = Field(foreign_key="user.uuid") To be added after auth + role based user access implementation

    date_taken: date = Field(default_factory=date.today)

class MHUSystemFindings(BaseModel, table=True):
    mhu_uuid: UUID = Field(foreign_key="medicalhistoryupdate.uuid")
    bsl_uuid: UUID = Field(foreign_key="bodysystemslookup.uuid")

    status: BodySystemStatus = Field(default=BodySystemStatus.NOT_ASSESSED)
    condition_notes: Optional[str] = Field(default=None, sa_type=TEXT)