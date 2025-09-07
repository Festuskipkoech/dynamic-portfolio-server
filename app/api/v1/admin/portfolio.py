from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
from app.schemas import (
    Skill, SkillCreate, SkillUpdate,
    WorkExperience, WorkExperienceCreate, WorkExperienceUpdate,
    ResponseSchema
)
from app.services import skill_service, work_experience_service
from app.api.dependencies import get_admin_session

router = APIRouter()

# ============ SKILLS ROUTES ============
@router.get("/skills", response_model=List[Skill])
def get_skills(admin_session: tuple = Depends(get_admin_session)):
    """Get all skills"""
    db = admin_session
    return skill_service.get_all(db)

@router.get("/skills/{skill_id}", response_model=Skill)
def get_skill(skill_id: int, admin_session: tuple = Depends(get_admin_session)):
    """Get skill by ID"""
    db = admin_session
    return skill_service.get_by_id_or_404(db, skill_id)

@router.post("/skills", response_model=Skill)
def create_skill(
    skill: SkillCreate,
    admin_session: tuple = Depends(get_admin_session)
):
    """Create new skill"""
    db = admin_session
    return skill_service.create(db, skill)

@router.put("/skills/{skill_id}", response_model=Skill)
def update_skill(
    skill_id: int,
    skill_update: SkillUpdate,
    admin_session: tuple = Depends(get_admin_session)
):
    """Update skill"""
    db = admin_session
    return skill_service.update_by_id(db, skill_id, skill_update)

@router.delete("/skills/{skill_id}", response_model=ResponseSchema)
def delete_skill(skill_id: int, admin_session: tuple = Depends(get_admin_session)):
    """Delete skill"""
    db = admin_session
    skill_service.delete_by_id(db, skill_id)
    return ResponseSchema(message="Skill deleted successfully")

@router.post("/skills/{skill_id}/icon", response_model=ResponseSchema)
def upload_skill_icon(
    skill_id: int,
    file: UploadFile = File(...),
    admin_session: tuple = Depends(get_admin_session)
):
    """Upload skill icon"""
    db = admin_session
    skill_service.upload_icon(db, skill_id, file)
    return ResponseSchema(message="Skill icon uploaded successfully")

@router.delete("/skills/{skill_id}/icon", response_model=ResponseSchema)
def delete_skill_icon(skill_id: int, admin_session: tuple = Depends(get_admin_session)):
    """Delete skill icon"""
    db = admin_session
    skill_service.delete_icon(db, skill_id)
    return ResponseSchema(message="Skill icon deleted successfully")

# ============ WORK EXPERIENCE ROUTES ============
@router.get("/work-experiences", response_model=List[WorkExperience])
def get_work_experiences(admin_session: tuple = Depends(get_admin_session)):
    """Get all work experiences"""
    db = admin_session
    return work_experience_service.get_all_ordered(db)

@router.get("/work-experiences/{experience_id}", response_model=WorkExperience)
def get_work_experience(
    experience_id: int,
    admin_session: tuple = Depends(get_admin_session)
):
    """Get work experience by ID"""
    db = admin_session
    return work_experience_service.get_by_id_or_404(db, experience_id)

@router.post("/work-experiences", response_model=WorkExperience)
def create_work_experience(
    experience: WorkExperienceCreate,
    admin_session: tuple = Depends(get_admin_session)
):
    """Create new work experience"""
    db = admin_session
    return work_experience_service.create(db, experience)

@router.put("/work-experiences/{experience_id}", response_model=WorkExperience)
def update_work_experience(
    experience_id: int,
    experience_update: WorkExperienceUpdate,
    admin_session: tuple = Depends(get_admin_session)
):
    """Update work experience"""
    db = admin_session
    return work_experience_service.update_by_id(db, experience_id, experience_update)

@router.delete("/work-experiences/{experience_id}", response_model=ResponseSchema)
def delete_work_experience(
    experience_id: int,
    admin_session: tuple = Depends(get_admin_session)
):
    """Delete work experience"""
    db = admin_session
    work_experience_service.delete_by_id(db, experience_id)
    return ResponseSchema(message="Work experience deleted successfully")

@router.post("/work-experiences/{experience_id}/logo", response_model=ResponseSchema)
def upload_company_logo(
    experience_id: int,
    file: UploadFile = File(...),
    admin_session: tuple = Depends(get_admin_session)
):
    """Upload company logo"""
    db = admin_session
    work_experience_service.upload_company_logo(db, experience_id, file)
    return ResponseSchema(message="Company logo uploaded successfully")

@router.delete("/work-experiences/{experience_id}/logo", response_model=ResponseSchema)
def delete_company_logo(
    experience_id: int,
    admin_session: tuple = Depends(get_admin_session)
):
    """Delete company logo"""
    db = admin_session
    work_experience_service.delete_company_logo(db, experience_id)
    return ResponseSchema(message="Company logo deleted successfully")