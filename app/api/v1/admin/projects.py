from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List, Optional
import json
from app.schemas import (
    Project, ProjectCreate, ProjectUpdate,
    ProjectCategory, ProjectCategoryCreate, ProjectCategoryUpdate,
    ProjectImage, ProjectImageCreate, ProjectSkillAssignment,
    ResponseSchema
)
from app.services import (
    project_service, project_category_service, project_image_service
)
from app.api.dependencies import get_admin_session

router = APIRouter()

# ============ PROJECT CATEGORIES ============
@router.get("/categories", response_model=List[ProjectCategory])
def get_project_categories(admin_session: tuple = Depends(get_admin_session)):
    """Get all project categories"""
    current_admin, db = admin_session
    return project_category_service.get_all(db)

@router.post("/categories", response_model=ProjectCategory)
def create_project_category(
    category: ProjectCategoryCreate,
    admin_session: tuple = Depends(get_admin_session)
):
    """Create new project category"""
    current_admin, db = admin_session
    return project_category_service.create(db, category)

@router.put("/categories/{category_id}", response_model=ProjectCategory)
def update_project_category(
    category_id: int,
    category_update: ProjectCategoryUpdate,
    admin_session: tuple = Depends(get_admin_session)
):
    """Update project category"""
    current_admin, db = admin_session
    return project_category_service.update_by_id(db, category_id, category_update)

@router.delete("/categories/{category_id}", response_model=ResponseSchema)
def delete_project_category(
    category_id: int,
    admin_session: tuple = Depends(get_admin_session)
):
    """Delete project category"""
    current_admin, db = admin_session
    project_category_service.delete_by_id(db, category_id)
    return ResponseSchema(message="Project category deleted successfully")

# ============ PROJECTS ============
@router.get("/projects", response_model=List[Project])
def get_projects(admin_session: tuple = Depends(get_admin_session)):
    """Get all projects with full details"""
    current_admin, db = admin_session
    return project_service.get_all_with_relations(db)

@router.get("/projects/{project_id}", response_model=Project)
def get_project(project_id: int, admin_session: tuple = Depends(get_admin_session)):
    """Get project by ID with full details"""
    current_admin, db = admin_session
    return project_service.get_by_id_or_404(db, project_id)

@router.post("/projects", response_model=Project)
def create_project(
    project: ProjectCreate,
    admin_session: tuple = Depends(get_admin_session)
):
    """Create new project"""
    current_admin, db = admin_session
    return project_service.create(db, project)

@router.put("/projects/{project_id}", response_model=Project)
def update_project(
    project_id: int,
    project_update: ProjectUpdate,
    admin_session: tuple = Depends(get_admin_session)
):
    """Update existing project"""
    current_admin, db = admin_session
    return project_service.update_by_id(db, project_id, project_update)

@router.delete("/projects/{project_id}", response_model=ResponseSchema)
def delete_project(project_id: int, admin_session: tuple = Depends(get_admin_session)):
    """Delete project and all associated data"""
    current_admin, db = admin_session
    project_service.delete_by_id(db, project_id)
    return ResponseSchema(message="Project deleted successfully")

# ============ PROJECT SKILLS MANAGEMENT ============
@router.post("/projects/{project_id}/skills", response_model=ResponseSchema)
def assign_skill_to_project(
    project_id: int,
    assignment: ProjectSkillAssignment,
    admin_session: tuple = Depends(get_admin_session)
):
    """Assign a skill to project with relevance score"""
    current_admin, db = admin_session
    project_service.assign_skill(db, project_id, assignment)
    return ResponseSchema(message="Skill assigned to project successfully")

@router.put("/projects/{project_id}/skills", response_model=ResponseSchema)
def update_project_skills(
    project_id: int,
    skill_ids: List[int],
    admin_session: tuple = Depends(get_admin_session)
):
    """Update all skills associated with a project"""
    current_admin, db = admin_session
    # Use the internal method to update skills association
    project_service._update_skills_association(db, project_id, skill_ids)
    return ResponseSchema(message="Project skills updated successfully")

# ============ PROJECT IMAGES MANAGEMENT ============
@router.get("/projects/{project_id}/images", response_model=List[ProjectImage])
def get_project_images(
    project_id: int,
    admin_session: tuple = Depends(get_admin_session)
):
    """Get all images for a specific project"""
    current_admin, db = admin_session
    return project_image_service.get_project_images(db, project_id)

@router.post("/projects/{project_id}/images", response_model=ResponseSchema)
def upload_project_images(
    project_id: int,
    files: List[UploadFile] = File(...),
    captions: Optional[str] = Form(None),
    main_index: int = Form(0),
    admin_session: tuple = Depends(get_admin_session)
):
    """Upload multiple images for a project"""
    current_admin, db = admin_session
    
    # Parse captions from JSON string if provided
    caption_list = []
    if captions:
        try:
            caption_list = json.loads(captions)
        except json.JSONDecodeError:
            # If JSON parsing fails, treat as empty list
            caption_list = []
    
    # Validate main_index
    if main_index >= len(files):
        main_index = 0
    
    # Upload images
    uploaded_images = project_image_service.upload_images(
        db, project_id, files, caption_list, main_index
    )
    
    return ResponseSchema(
        message=f"{len(uploaded_images)} images uploaded successfully for project"
    )

@router.put("/projects/images/{image_id}/main", response_model=ResponseSchema)
def set_main_project_image(
    image_id: int,
    admin_session: tuple = Depends(get_admin_session)
):
    """Set a specific image as the main image for its project"""
    current_admin, db = admin_session
    project_image_service.set_main_image(db, image_id)
    return ResponseSchema(message="Main project image updated successfully")

@router.put("/projects/images/{image_id}/caption", response_model=ResponseSchema)
def update_image_caption(
    image_id: int,
    caption: str = Form(...),
    admin_session: tuple = Depends(get_admin_session)
):
    """Update caption for a project image"""
    current_admin, db = admin_session
    
    # Get the image and update caption
    image = project_image_service.get_by_id_or_404(db, image_id)
    image.caption = caption
    db.commit()
    
    return ResponseSchema(message="Image caption updated successfully")

@router.delete("/projects/images/{image_id}", response_model=ResponseSchema)
def delete_project_image(
    image_id: int,
    admin_session: tuple = Depends(get_admin_session)
):
    """Delete a specific project image"""
    current_admin, db = admin_session
    project_image_service.delete_by_id(db, image_id)
    return ResponseSchema(message="Project image deleted successfully")

# ============ PROJECT FILTERING/SEARCH ============
@router.get("/projects/featured", response_model=List[Project])
def get_featured_projects(admin_session: tuple = Depends(get_admin_session)):
    """Get all featured projects"""
    current_admin, db = admin_session
    return project_service.get_featured(db)

@router.get("/projects/category/{category_id}", response_model=List[Project])
def get_projects_by_category(
    category_id: int,
    admin_session: tuple = Depends(get_admin_session)
):
    """Get all projects in a specific category"""
    current_admin, db = admin_session
    return project_service.get_by_category(db, category_id)

@router.get("/projects/skill/{skill_id}", response_model=List[Project])
def get_projects_by_skill(
    skill_id: int,
    admin_session: tuple = Depends(get_admin_session)
):
    """Get all projects that use a specific skill"""
    current_admin, db = admin_session
    return project_service.get_by_skill(db, skill_id)

@router.get("/projects/case-studies", response_model=List[Project])
def get_projects_with_case_studies(admin_session: tuple = Depends(get_admin_session)):
    """Get all projects that have complete case studies"""
    current_admin, db = admin_session
    return project_service.get_with_case_studies(db)

# ============ BULK OPERATIONS ============
@router.put("/projects/bulk/featured", response_model=ResponseSchema)
def update_featured_projects(
    project_ids: List[int],
    admin_session: tuple = Depends(get_admin_session)
):
    """Update featured status for multiple projects"""
    current_admin, db = admin_session
    
    # First, unfeatured all projects
    db.query(Project).update({"featured": False})
    
    # Then, feature the specified projects
    if project_ids:
        db.query(Project).filter(Project.id.in_(project_ids)).update(
            {"featured": True}, synchronize_session=False
        )
    
    db.commit()
    return ResponseSchema(message=f"{len(project_ids)} projects marked as featured")