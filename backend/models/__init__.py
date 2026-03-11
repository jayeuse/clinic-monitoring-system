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
    PatientFamilyHistory,
)
from models.lookups import (
    BodySystemsLookup,
    DepartmentsLookup,
    MedicalConditionsLookup,
)
from models.patients import (
    EmergencyContact,
    PatientInformation,
    PersonnelType,
    StudentType,
)
from models.users import User
