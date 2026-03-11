import math
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from core.database import get_session
from schemas.base_schemas import GenericResponse, PaginationMeta
from schemas.lookup_schemas import (
    BodySystemsLookupCreate,
    BodySystemsLookupPublic,
    BodySystemsLookupUpdate,
    DepartmentsLookupCreate,
    DepartmentsLookupPublic,
    DepartmentsLookupUpdate,
    MedicalConditionsLookupCreate,
    MedicalConditionsLookupPublic,
    MedicalConditionsLookupUpdate,
    SmokingTypesLookupCreate,
    SmokingTypesLookupPublic,
    SmokingTypesLookupUpdate,
)
from services.lookup_service import (
    body_systems_lookup_service,
    departments_lookup_service,
    medical_conditions_lookup_service,
    smoking_types_lookup_service,
)

router = APIRouter(prefix="/lookups", tags=["Lookups"])

# --- Departments Lookup Endpoints ---

@router.get("/departments", response_model=GenericResponse[List[DepartmentsLookupPublic]])
def read_departments(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_session)
):
    departments, total_count = departments_lookup_service.get_all(db, skip=skip, limit=limit)

    current_page = (skip // limit) + 1
    total_pages = math.ceil(total_count / limit) if limit > 0 else 1

    meta = PaginationMeta(
        total_records=total_count,
        current_page=current_page,
        total_pages=total_pages,
        next_page=(current_page + 1) if (skip + limit) < total_count else None,
        prev_page=(current_page - 1) if skip > 0 else None
    )

    return GenericResponse(message="Departments retrieved successfully", data=departments, meta=meta)

@router.post("/departments", response_model=GenericResponse[DepartmentsLookupPublic])
def create_department(
    department_in: DepartmentsLookupCreate,
    db: Session = Depends(get_session)
):
    new_department = departments_lookup_service.create(db, obj_in=department_in)
    return GenericResponse(message="Department created successfully", data=new_department)

@router.get("/departments/{dl_id}", response_model=GenericResponse[DepartmentsLookupPublic])
def read_department_by_id(
    dl_id: str,
    db: Session = Depends(get_session)
):
    department = departments_lookup_service.get_by_dl_id(db, dl_id=dl_id)
    if not department:
        raise HTTPException(status_code=404, detail="Department not found")
    return GenericResponse(message="Department retrieved successfully", data=department)

@router.patch("/departments/{dl_id}", response_model=GenericResponse[DepartmentsLookupPublic])
def update_department(
    dl_id: str,
    department_in: DepartmentsLookupUpdate,
    db: Session = Depends(get_session)
):
    db_obj = departments_lookup_service.get_by_dl_id(db, dl_id=dl_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Department not found")
    
    updated_department = departments_lookup_service.update(db, db_obj=db_obj, obj_in=department_in)
    return GenericResponse(message="Department updated successfully", data=updated_department)

@router.delete("/departments/{dl_id}", response_model=GenericResponse[DepartmentsLookupPublic])
def delete_department(
    dl_id: str,
    db: Session = Depends(get_session)
):
    db_obj = departments_lookup_service.get_by_dl_id(db, dl_id=dl_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Department not found")
    
    deleted_department = departments_lookup_service.remove(db, uuid=db_obj.uuid)
    return GenericResponse(message="Department deleted successfully", data=deleted_department)


# --- Medical Conditions Lookup Endpoints ---

@router.get("/medical-conditions", response_model=GenericResponse[List[MedicalConditionsLookupPublic]])
def read_medical_conditions(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_session)
):
    conditions, total_count = medical_conditions_lookup_service.get_all(db, skip=skip, limit=limit)

    current_page = (skip // limit) + 1
    total_pages = math.ceil(total_count / limit) if limit > 0 else 1

    meta = PaginationMeta(
        total_records=total_count,
        current_page=current_page,
        total_pages=total_pages,
        next_page=(current_page + 1) if (skip + limit) < total_count else None,
        prev_page=(current_page - 1) if skip > 0 else None
    )

    return GenericResponse(message="Medical Conditions retrieved successfully", data=conditions, meta=meta)


@router.post("/medical-conditions", response_model=GenericResponse[MedicalConditionsLookupPublic])
def create_medical_condition(
    condition_in: MedicalConditionsLookupCreate,
    db: Session = Depends(get_session)
):
    new_condition = medical_conditions_lookup_service.create(db, obj_in=condition_in)
    return GenericResponse(message="Medical Condition created successfully", data=new_condition)

@router.get("/medical-conditions/{mcl_id}", response_model=GenericResponse[MedicalConditionsLookupPublic])
def read_medical_condition_by_id(
    mcl_id: str,
    db: Session = Depends(get_session)
):
    condition = medical_conditions_lookup_service.get_by_mcl_id(db, mcl_id=mcl_id)
    if not condition:
        raise HTTPException(status_code=404, detail="Medical Condition not found")
    return GenericResponse(message="Medical Condition retrieved successfully", data=condition)

@router.patch("/medical-conditions/{mcl_id}", response_model=GenericResponse[MedicalConditionsLookupPublic])
def update_medical_condition(
    mcl_id: str,
    condition_in: MedicalConditionsLookupUpdate,
    db: Session = Depends(get_session)
):
    db_obj = medical_conditions_lookup_service.get_by_mcl_id(db, mcl_id=mcl_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Medical Condition not found")
    
    updated_condition = medical_conditions_lookup_service.update(db, db_obj=db_obj, obj_in=condition_in)
    return GenericResponse(message="Medical Condition updated successfully", data=updated_condition)

@router.delete("/medical-conditions/{mcl_id}", response_model=GenericResponse[MedicalConditionsLookupPublic])
def delete_medical_condition(
    mcl_id: str,
    db: Session = Depends(get_session)
):
    db_obj = medical_conditions_lookup_service.get_by_mcl_id(db, mcl_id=mcl_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Medical Condition not found")
    
    deleted_condition = medical_conditions_lookup_service.remove(db, uuid=db_obj.uuid)
    return GenericResponse(message="Medical Condition deleted successfully", data=deleted_condition)


# --- Smoking Types Lookup Endpoints ---

@router.get("/smoking-types", response_model=GenericResponse[List[SmokingTypesLookupPublic]])
def read_smoking_types(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_session)
):
    types, total_count = smoking_types_lookup_service.get_all(db, skip=skip, limit=limit)

    current_page = (skip // limit) + 1
    total_pages = math.ceil(total_count / limit) if limit > 0 else 1

    meta = PaginationMeta(
        total_records=total_count,
        current_page=current_page,
        total_pages=total_pages,
        next_page=(current_page + 1) if (skip + limit) < total_count else None,
        prev_page=(current_page - 1) if skip > 0 else None
    )

    return GenericResponse(message="Smoking Types retrieved successfully", data=types, meta=meta)

@router.post("/smoking-types", response_model=GenericResponse[SmokingTypesLookupPublic])
def create_smoking_type(
    type_in: SmokingTypesLookupCreate,
    db: Session = Depends(get_session)
):
    new_type = smoking_types_lookup_service.create(db, obj_in=type_in)
    return GenericResponse(message="Smoking Type created successfully", data=new_type)

@router.get("/smoking-types/{stl_id}", response_model=GenericResponse[SmokingTypesLookupPublic])
def read_smoking_type_by_id(
    stl_id: str,
    db: Session = Depends(get_session)
):
    smoking_type = smoking_types_lookup_service.get_by_stl_id(db, stl_id=stl_id)
    if not smoking_type:
        raise HTTPException(status_code=404, detail="Smoking Type not found")
    return GenericResponse(message="Smoking Type retrieved successfully", data=smoking_type)

@router.patch("/smoking-types/{stl_id}", response_model=GenericResponse[SmokingTypesLookupPublic])
def update_smoking_type(
    stl_id: str,
    type_in: SmokingTypesLookupUpdate,
    db: Session = Depends(get_session)
):
    db_obj = smoking_types_lookup_service.get_by_stl_id(db, stl_id=stl_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Smoking Type not found")
    
    updated_type = smoking_types_lookup_service.update(db, db_obj=db_obj, obj_in=type_in)
    return GenericResponse(message="Smoking Type updated successfully", data=updated_type)

@router.delete("/smoking-types/{stl_id}", response_model=GenericResponse[SmokingTypesLookupPublic])
def delete_smoking_type(
    stl_id: str,
    db: Session = Depends(get_session)
):
    db_obj = smoking_types_lookup_service.get_by_stl_id(db, stl_id=stl_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Smoking Type not found")
    
    deleted_type = smoking_types_lookup_service.remove(db, uuid=db_obj.uuid)
    return GenericResponse(message="Smoking Type deleted successfully", data=deleted_type)


# --- Body Systems Lookup Endpoints ---

@router.get("/body-systems", response_model=GenericResponse[List[BodySystemsLookupPublic]])
def read_body_systems(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_session)
):
    systems, total_count = body_systems_lookup_service.get_all(db, skip=skip, limit=limit)

    current_page = (skip // limit) + 1
    total_pages = math.ceil(total_count / limit) if limit > 0 else 1

    meta = PaginationMeta(
        total_records=total_count,
        current_page=current_page,
        total_pages=total_pages,
        next_page=(current_page + 1) if (skip + limit) < total_count else None,
        prev_page=(current_page - 1) if skip > 0 else None
    )

    return GenericResponse(message="Body Systems retrieved successfully", data=systems, meta=meta)

@router.post("/body-systems", response_model=GenericResponse[BodySystemsLookupPublic])
def create_body_system(
    system_in: BodySystemsLookupCreate,
    db: Session = Depends(get_session)
):
    new_system = body_systems_lookup_service.create(db, obj_in=system_in)
    return GenericResponse(message="Body System created successfully", data=new_system)

@router.get("/body-systems/{bsl_id}", response_model=GenericResponse[BodySystemsLookupPublic])
def read_body_system_by_id(
    bsl_id: str,
    db: Session = Depends(get_session)
):
    system = body_systems_lookup_service.get_by_bsl_id(db, bsl_id=bsl_id)
    if not system:
        raise HTTPException(status_code=404, detail="Body System not found")
    return GenericResponse(message="Body System retrieved successfully", data=system)

@router.patch("/body-systems/{bsl_id}", response_model=GenericResponse[BodySystemsLookupPublic])
def update_body_system(
    bsl_id: str,
    system_in: BodySystemsLookupUpdate,
    db: Session = Depends(get_session)
):
    db_obj = body_systems_lookup_service.get_by_bsl_id(db, bsl_id=bsl_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Body System not found")
    
    updated_system = body_systems_lookup_service.update(db, db_obj=db_obj, obj_in=system_in)
    return GenericResponse(message="Body System updated successfully", data=updated_system)

@router.delete("/body-systems/{bsl_id}", response_model=GenericResponse[BodySystemsLookupPublic])
def delete_body_system(
    bsl_id: str,
    db: Session = Depends(get_session)
):
    db_obj = body_systems_lookup_service.get_by_bsl_id(db, bsl_id=bsl_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Body System not found")
    
    deleted_system = body_systems_lookup_service.remove(db, uuid=db_obj.uuid)
    return GenericResponse(message="Body System deleted successfully", data=deleted_system)
