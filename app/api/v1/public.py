from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from typing import List, Optional
from app.config.database import get_db
from app.schemas import (
    PortfolioSummary, Project, Skill, WorkExperience, Education
)
from app.services import (
    personal_info_service, skill_service, work_experience_service,
    project_service, education_service, project_image_service
)

router = APIRouter()

@router.get("/portfolio", response_model=PortfolioSummary)
def get_portfolio_summary(db: Session = Depends(get_db)):
    """Get complete portfolio data for public view"""
    personal_info = personal_info_service.get_personal_info(db)
    skills = skill_service.get_all(db)
    work_experiences = work_experience_service.get_all_ordered(db)
    projects = project_service.get_all_with_relations(db)
    education = education_service.get_all_ordered(db)
    
    return PortfolioSummary(
        personal_info=personal_info,
        skills=skills,
        work_experiences=work_experiences,
        projects=projects,
        education=education
    )

@router.get("/projects", response_model=List[Project])
def get_projects(
    category_id: Optional[int] = None,
    skill_id: Optional[int] = None,
    featured: Optional[bool] = None,
    with_case_studies: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    """Get projects with optional filtering"""
    if category_id:
        return project_service.get_by_category(db, category_id)
    elif skill_id:
        return project_service.get_by_skill(db, skill_id)
    elif featured:
        return project_service.get_featured(db)
    elif with_case_studies:
        return project_service.get_with_case_studies(db)
    else:
        return project_service.get_all_with_relations(db)

@router.get("/projects/{project_id}", response_model=Project)
def get_project_detail(project_id: int, db: Session = Depends(get_db)):
    """Get detailed project information"""
    project = project_service.get_by_id(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

@router.get("/skills", response_model=List[Skill])
def get_skills(category: Optional[str] = None, db: Session = Depends(get_db)):
    """Get skills with optional category filtering"""
    if category:
        return skill_service.get_by_category(db, category)
    return skill_service.get_all(db)

@router.get("/skills/categories")
def get_skill_categories(db: Session = Depends(get_db)):
    """Get all skill categories"""
    return {"categories": skill_service.get_categories(db)}

@router.get("/experience", response_model=List[WorkExperience])
def get_work_experience(current_only: Optional[bool] = None, db: Session = Depends(get_db)):
    """Get work experience"""
    if current_only:
        return work_experience_service.get_current_positions(db)
    return work_experience_service.get_all_ordered(db)

@router.get("/education", response_model=List[Education])
def get_education(
    type: Optional[str] = None,  # "degree" or "certification"
    current_only: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    """Get education records"""
    if current_only:
        return education_service.get_current(db)
    elif type == "degree":
        return education_service.get_degrees(db)
    elif type == "certification":
        return education_service.get_certifications(db)
    else:
        return education_service.get_all_ordered(db)

# Image serving endpoints
@router.get("/images/profile")
def get_profile_image(db: Session = Depends(get_db)):
    """Get profile image"""
    image_data = personal_info_service.get_profile_image(db)
    if not image_data:
        raise HTTPException(status_code=404, detail="Profile image not found")
    
    content, mime_type = image_data
    return Response(content=content, media_type=mime_type)

@router.get("/images/skills/{skill_id}")
def get_skill_icon(skill_id: int, db: Session = Depends(get_db)):
    """Get skill icon"""
    image_data = skill_service.get_icon(db, skill_id)
    if not image_data:
        raise HTTPException(status_code=404, detail="Skill icon not found")
    
    content, mime_type = image_data
    return Response(content=content, media_type=mime_type)

@router.get("/images/companies/{experience_id}")
def get_company_logo(experience_id: int, db: Session = Depends(get_db)):
    """Get company logo"""
    image_data = work_experience_service.get_company_logo(db, experience_id)
    if not image_data:
        raise HTTPException(status_code=404, detail="Company logo not found")
    
    content, mime_type = image_data
    return Response(content=content, media_type=mime_type)

@router.get("/images/projects/{image_id}")
def get_project_image(image_id: int, db: Session = Depends(get_db)):
    """Get project image"""
    image_data = project_image_service.get_image_data(db, image_id)
    if not image_data:
        raise HTTPException(status_code=404, detail="Project image not found")
    
    content, mime_type = image_data
    return Response(content=content, media_type=mime_type)

@router.get("/images/institutions/{education_id}")
def get_institution_logo(education_id: int, db: Session = Depends(get_db)):
    """Get institution logo"""
    image_data = education_service.get_institution_logo(db, education_id)
    if not image_data:
        raise HTTPException(status_code=404, detail="Institution logo not found")
    
    content, mime_type = image_data
    return Response(content=content, media_type=mime_type)

@router.get("/documents/certificates/{education_id}")
def get_certificate(education_id: int, db: Session = Depends(get_db)):
    """Get education certificate"""
    document_data = education_service.get_certificate(db, education_id)
    if not document_data:
        raise HTTPException(status_code=404, detail="Certificate not found")
    
    content, mime_type = document_data
    return Response(content=content, media_type=mime_type)