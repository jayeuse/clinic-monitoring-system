# This file makes it easy to import all models at once
from models.base import BaseModel
from models.users import User
from models.patients import PatientInformation, StudentType, PersonnelType
from models.lookups import DepartmentsLookup, MedicalConditionsLookup, SmokingTypesLookup, BodySystemsLookup
from models.clinic import ClinicTransaction, VitalSigns
from models.history import MedicalHistory, PatientSmokingTypes, PatientDiagnosedConditions, MedicalHistoryUpdate, MHUSystemFindings
from models.dental import DentalRecord, DentalExamination, ToothFinding, DentalServiceRendered
