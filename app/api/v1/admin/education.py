from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
from app.schemas import Education, EducationCreate, EducationUpdate, ResponseSchema
from app.services import education_service
from app.api.dependencies import get_admin_session

router = APIRouter()

@router.get("/education", response_model=List[Education])
def get_education(admin_session: tuple = Depends(get_admin_session)):
    """Get all education records"""
    current_admin, db = admin_session
    return education_service.get_all_ordered(db)

@router.get("/education/{education_id}", response_model=Education)
def get_education_by_id(
    education_id: int,
    admin_session: tuple = Depends(get_admin_session)
):
    """Get education record by ID"""
    current_admin, db = admin_session
    return education_service.get_by_id_or_404(db, education_id)

@router.post("/education", response_model=Education)
def create_education(
    education: EducationCreate,
    admin_session: tuple = Depends(get_admin_session)
):
    """Create new education record"""
    current_admin, db = admin_session
    return education_service.create(db, education)

@router.put("/education/{education_id}", response_model=Education)
def update_education(
    education_id: int,
    education_update: EducationUpdate,
    admin_session: tuple = Depends(get_admin_session)
):
    """Update education record"""
    current_admin, db = admin_session
    return education_service.update_by_id(db, education_id, education_update)

@router.delete("/education/{education_id}", response_model=ResponseSchema)
def delete_education(
    education_id: int,
    admin_session: tuple = Depends(get_admin_session)
):
    """Delete education record"""
    current_admin, db = admin_session
    education_service.delete_by_id(db, education_id)
    return ResponseSchema(message="Education record deleted successfully")

@router.post("/education/{education_id}/logo", response_model=ResponseSchema)
def upload_institution_logo(
    education_id: int,
    file: UploadFile = File(...),
    admin_session: tuple = Depends(get_admin_session)
):
    """Upload institution logo"""
    current_admin, db = admin_session
    education_service.upload_institution_logo(db, education_id, file)
    return ResponseSchema(message="Institution logo uploaded successfully")

@router.delete("/education/{education_id}/logo", response_model=ResponseSchema)
def delete_institution_logo(
    education_id: int,
    admin_session: tuple = Depends(get_admin_session)
):
    """Delete institution logo"""
    current_admin, db = admin_session
    education_service.delete_institution_logo(db, education_id)
    return ResponseSchema(message="Institution logo deleted successfully")

@router.post("/education/{education_id}/certificate", response_model=ResponseSchema)
def upload_certificate(
    education_id: int,
    file: UploadFile = File(...),
    admin_session: tuple = Depends(get_admin_session)
):
    """Upload education certificate"""
    current_admin, db = admin_session
    education_service.upload_certificate(db, education_id, file)
    return ResponseSchema(message="Certificate uploaded successfully")

@router.delete("/education/{education_id}/certificate", response_model=ResponseSchema)
def delete_certificate(
    education_id: int,
    admin_session: tuple = Depends(get_admin_session)
):
    """Delete education certificate"""
    current_admin, db = admin_session
    education_service.delete_certificate(db, education_id)
    return ResponseSchema(message="Certificate deleted successfully")