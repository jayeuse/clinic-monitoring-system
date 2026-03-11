# This file makes it easy to import all models at once
from models.base import BaseModel
from models.clinic import ClinicTransaction, VitalSigns
from models.dental import (
    DentalExamination,
    DentalExaminationSnapshot,
    DentalRecord,
    DentalRecordSnapshot,
    DentalServiceRendered,
    ToothFinding,
)
from models.history import (
    MedicalExamination,
    MedicalExaminationFindings,
    MedicalExaminationSnapshot,
    MedicalHistory,
    MedicalHistorySnapshot,
    MedicalTreatment,
    PatientDiagnosedConditions,
    PatientSmokingTypes,
)
from models.lookups import (
    BodySystemsLookup,
    DepartmentsLookup,
    MedicalConditionsLookup,
    SmokingTypesLookup,
)
from models.patients import PatientInformation, PersonnelType, StudentType
from models.users import User
