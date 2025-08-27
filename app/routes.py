from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form, WebSocket
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import timedelta, datetime
from jose import JWTError, jwt
import json

from .database import get_db
from .schemas import (
    PortfolioSummary, Token, AdminLogin,
    Skill, SkillCreate, SkillUpdate, 
    WorkExperience, WorkExperienceCreate, WorkExperienceUpdate,
    Project, ProjectCreate, ProjectImageCreate, ProjectUpdate,
    Education, EducationCreate, EducationUpdate, PersonalInfo,PersonalInfoUpdate
)
from .services import AuthService, WorkExperienceService, SkillService, EducationService, ProjectService, FileService, PersonalInfoService
from .config import get_settings

settings = get_settings()
security = HTTPBearer()

# Create routers
public_router = APIRouter()
admin_router = APIRouter(prefix="/admin")

def get_current_admin(credentials: HTTPAuthorizationCredentials = Depends(security)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(credentials.credentials, settings.secret_key, algorithms=[settings.algorithm])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return username

# ============ PUBLIC ROUTES ============
@public_router.get("/portfolio", response_model=PortfolioSummary)
def get_portfolio(db: Session = Depends(get_db)):
    """Get complete portfolio data for public view"""
    personal_info = PersonalInfoService.get_personal_info(db)
    skills = SkillService.get_all(db)
    work_experiences = WorkExperienceService.get_all(db)
    projects = ProjectService.get_all(db)
    education = EducationService.get_all(db)
    
    return PortfolioSummary(
        personal_info=personal_info,
        skills=skills,
        work_experiences=work_experiences,
        projects=projects,
        education=education
    )

@public_router.get("/projects/{project_id}", response_model=Project)
def get_project_detail(project_id: int, db: Session = Depends(get_db)):
    """Get detailed project information including all images"""
    project = ProjectService.get_by_id(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

# ============ AUTH ROUTES ============
@admin_router.post("/login", response_model=Token)
def admin_login(admin_login: AdminLogin):
    """Admin authentication"""
    if not AuthService.authenticate_admin(admin_login.username, admin_login.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Use a default value if access_token_expire_minutes is not in settings
    expire_minutes = getattr(settings, 'access_token_expire_minutes', 30)
    access_token_expires = timedelta(minutes=expire_minutes)
    access_token = AuthService.create_access_token(
        data={"sub": admin_login.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
# ============ PERSONAL INFO ROUTES ============
@admin_router.get("/personal-info", response_model=PersonalInfo)
def get_personal_info(db: Session = Depends(get_db), current_admin: str = Depends(get_current_admin)):
    """Get personal information"""
    personal_info = PersonalInfoService.get_personal_info(db)
    if not personal_info:
        # Return default empty structure if no personal info exists yet
        return PersonalInfo(
            id=0,
            full_name="",
            title="",
            bio="",
            email="",
            phone="",
            location="",
            linkedin="",
            github="",
            website="",
            profile_image="",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
    return personal_info

@admin_router.put("/personal-info", response_model=PersonalInfo)
def update_personal_info(
    personal_info_update: PersonalInfoUpdate, 
    db: Session = Depends(get_db), 
    current_admin: str = Depends(get_current_admin)
):
    """Update personal information"""
    return PersonalInfoService.update_personal_info(db, personal_info_update)

@admin_router.post("/personal-info/upload", response_model=dict)
def upload_personal_file(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_admin: str = Depends(get_current_admin)
):
    """Upload files for personal info (like profile image)"""
    try:
        file_url = FileService.save_file(file, "personal")
        return {"message": "File uploaded successfully", "file_url": file_url}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"File upload failed: {str(e)}"
        )

# ============ WEBSOCKET ROUTES ============
@admin_router.websocket("/ws/notifications")
async def websocket_endpoint(websocket: WebSocket, token: str = None):
    """
    WebSocket endpoint for real-time notifications.
    For now, this is a placeholder implementation.
    """
    try:
        await websocket.accept()
        
        # Optional: Verify token if provided
        if token:
            try:
                payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
                username = payload.get("sub")
                if not username:
                    await websocket.close(code=1008, reason="Invalid token")
                    return
            except JWTError:
                await websocket.close(code=1008, reason="Invalid token")
                return
        
        # Send welcome message
        await websocket.send_text(json.dumps({
            "type": "connection",
            "message": "WebSocket connected successfully"
        }))
        
        # Keep connection alive (placeholder - implement your notification logic here)
        try:
            while True:
                # Wait for messages from client
                message = await websocket.receive_text()
                # Echo back for now
                await websocket.send_text(json.dumps({
                    "type": "echo",
                    "message": f"Received: {message}"
                }))
        except Exception:
            pass
            
    except Exception as e:
        try:
            await websocket.close(code=1011, reason="Internal error")
        except:
            pass

# ============ SKILL ROUTES ============
@admin_router.get("/skills", response_model=List[Skill])
def get_skills(db: Session = Depends(get_db), current_admin: str = Depends(get_current_admin)):
    return SkillService.get_all(db)

@admin_router.get("/skills/{skill_id}", response_model=Skill)
def get_skill(skill_id: int, db: Session = Depends(get_db), current_admin: str = Depends(get_current_admin)):
    skill = SkillService.get_by_id(db, skill_id)
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    return skill

@admin_router.post("/skills", response_model=Skill)
def create_skill(skill: SkillCreate, db: Session = Depends(get_db), current_admin: str = Depends(get_current_admin)):
    return SkillService.create(db, skill)

@admin_router.put("/skills/{skill_id}", response_model=Skill)
def update_skill(skill_id: int, skill_update: SkillUpdate, db: Session = Depends(get_db), current_admin: str = Depends(get_current_admin)):
    updated_skill = SkillService.update(db, skill_id, skill_update)
    if not updated_skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    return updated_skill

@admin_router.delete("/skills/{skill_id}")
def delete_skill(skill_id: int, db: Session = Depends(get_db), current_admin: str = Depends(get_current_admin)):
    if not SkillService.delete(db, skill_id):
        raise HTTPException(status_code=404, detail="Skill not found")
    return {"message": "Skill deleted successfully"}

# ============ WORK EXPERIENCE ROUTES ============
@admin_router.get("/work-experiences", response_model=List[WorkExperience])
def get_work_experiences(db: Session = Depends(get_db), current_admin: str = Depends(get_current_admin)):
    return WorkExperienceService.get_all(db)

@admin_router.get("/work-experiences/{experience_id}", response_model=WorkExperience)
def get_work_experience(experience_id: int, db: Session = Depends(get_db), current_admin: str = Depends(get_current_admin)):
    experience = WorkExperienceService.get_by_id(db, experience_id)
    if not experience:
        raise HTTPException(status_code=404, detail="Work experience not found")
    return experience

@admin_router.post("/work-experiences", response_model=WorkExperience)
def create_work_experience(experience: WorkExperienceCreate, db: Session = Depends(get_db), current_admin: str = Depends(get_current_admin)):
    return WorkExperienceService.create(db, experience)
    return WorkExperienceService.create(db, experience)

@admin_router.put("/work-experiences/{experience_id}", response_model=WorkExperience)
def update_work_experience(experience_id: int, experience_update: WorkExperienceUpdate, db: Session = Depends(get_db), current_admin: str = Depends(get_current_admin)):
    updated_experience = WorkExperienceService.update(db, experience_id, experience_update)
    if not updated_experience:
        raise HTTPException(status_code=404, detail="Work experience not found")
    return updated_experience

@admin_router.delete("/work-experiences/{experience_id}")
def delete_work_experience(experience_id: int, db: Session = Depends(get_db), current_admin: str = Depends(get_current_admin)):
    if not WorkExperienceService.delete(db, experience_id):
        raise HTTPException(status_code=404, detail="Work experience not found")
    return {"message": "Work experience deleted successfully"}

@admin_router.post("/work-experiences/{experience_id}/logo")
def upload_company_logo(
    experience_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_admin: str = Depends(get_current_admin)
):
    # Save file and update work experience
    file_url = FileService.save_file(file, "companies")
    
    # Update work experience with logo URL
    experience = WorkExperienceService.get_by_id(db, experience_id)
    if not experience:
        # Clean up uploaded file if experience not found
        FileService.delete_file(file_url)
        raise HTTPException(status_code=404, detail="Work experience not found")
    
    # Delete old logo if exists
    if experience.company_logo_url:
        FileService.delete_file(experience.company_logo_url)
    
    # Update with new logo
    update_data = WorkExperienceUpdate(company_logo_url=file_url)
    WorkExperienceService.update(db, experience_id, update_data)
    
    return {"message": "Company logo uploaded successfully", "file_url": file_url}

# ============ PROJECT ROUTES ============
@admin_router.get("/projects", response_model=List[Project])
def get_projects(db: Session = Depends(get_db), current_admin: str = Depends(get_current_admin)):
    return ProjectService.get_all(db)

@admin_router.get("/projects/{project_id}", response_model=Project)
def get_project(project_id: int, db: Session = Depends(get_db), current_admin: str = Depends(get_current_admin)):
    project = ProjectService.get_by_id(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

@admin_router.post("/projects", response_model=Project)
def create_project(project: ProjectCreate, db: Session = Depends(get_db), current_admin: str = Depends(get_current_admin)):
    return ProjectService.create(db, project)
    return ProjectService.create(db, project)

@admin_router.put("/projects/{project_id}", response_model=Project)
def update_project(project_id: int, project_update: ProjectUpdate, db: Session = Depends(get_db), current_admin: str = Depends(get_current_admin)):
    updated_project = ProjectService.update(db, project_id, project_update)
    if not updated_project:
        raise HTTPException(status_code=404, detail="Project not found")
    return updated_project

@admin_router.delete("/projects/{project_id}")
def delete_project(project_id: int, db: Session = Depends(get_db), current_admin: str = Depends(get_current_admin)):
    if not ProjectService.delete(db, project_id):
        raise HTTPException(status_code=404, detail="Project not found")
    return {"message": "Project deleted successfully"}

@admin_router.post("/projects/{project_id}/images")
def upload_project_images(
    project_id: int,
    files: List[UploadFile] = File(...),
    captions: Optional[str] = Form(None),
    main_image_index: Optional[int] = Form(0),
    db: Session = Depends(get_db),
    current_admin: str = Depends(get_current_admin)
):
    # Check if project exists
    project = ProjectService.get_by_id(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Parse captions if provided
    caption_list = []
    if captions:
        try:
            caption_list = json.loads(captions)
        except json.JSONDecodeError:
            caption_list = []
    
    uploaded_images = []
    for i, file in enumerate(files):
        # Save file
        file_url = FileService.save_file(file, "projects")
        
        # Create image record
        caption = caption_list[i] if i < len(caption_list) else None
        is_main = i == main_image_index
        
        image_data = ProjectImageCreate(
            image_url=file_url,
            caption=caption,
            is_main=is_main
        )
        
        image = ProjectService.add_image(db, project_id, image_data)
        uploaded_images.append(image)
    
    return {"message": f"{len(uploaded_images)} images uploaded successfully", "images": uploaded_images}

@admin_router.delete("/projects/images/{image_id}")
def delete_project_image(image_id: int, db: Session = Depends(get_db), current_admin: str = Depends(get_current_admin)):
    if not ProjectService.delete_image(db, image_id):
        raise HTTPException(status_code=404, detail="Image not found")
    return {"message": "Image deleted successfully"}

# ============ EDUCATION ROUTES ============
@admin_router.get("/education", response_model=List[Education])
def get_education(db: Session = Depends(get_db), current_admin: str = Depends(get_current_admin)):
    return EducationService.get_all(db)

@admin_router.get("/education/{education_id}", response_model=Education)
def get_education_by_id(education_id: int, db: Session = Depends(get_db), current_admin: str = Depends(get_current_admin)):
    education = EducationService.get_by_id(db, education_id)
    if not education:
        raise HTTPException(status_code=404, detail="Education record not found")
    return education

@admin_router.post("/education", response_model=Education)
def create_education(education: EducationCreate, db: Session = Depends(get_db), current_admin: str = Depends(get_current_admin)):
    return EducationService.create(db, education)
    return EducationService.create(db, education)

@admin_router.put("/education/{education_id}", response_model=Education)
def update_education(education_id: int, education_update: EducationUpdate, db: Session = Depends(get_db), current_admin: str = Depends(get_current_admin)):
    updated_education = EducationService.update(db, education_id, education_update)
    if not updated_education:
        raise HTTPException(status_code=404, detail="Education record not found")
    return updated_education

@admin_router.delete("/education/{education_id}")
def delete_education(education_id: int, db: Session = Depends(get_db), current_admin: str = Depends(get_current_admin)):
    if not EducationService.delete(db, education_id):
        raise HTTPException(status_code=404, detail="Education record not found")
    return {"message": "Education record deleted successfully"}

@admin_router.post("/education/{education_id}/certificate")
def upload_certificate(
    education_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_admin: str = Depends(get_current_admin)
):
    # Save certificate file
    file_url = FileService.save_file(file, "certificates")
    
    # Update education record
    education = EducationService.get_by_id(db, education_id)
    if not education:
        FileService.delete_file(file_url)
        raise HTTPException(status_code=404, detail="Education record not found")
    
    # Delete old certificate if exists
    if education.certificate_url:
        FileService.delete_file(education.certificate_url)
    
    # Update with new certificate
    update_data = EducationUpdate(certificate_url=file_url)
    EducationService.update(db, education_id, update_data)
    
    return {"message": "Certificate uploaded successfully", "file_url": file_url}

@admin_router.post("/education/{education_id}/logo")
def upload_institution_logo(
    education_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_admin: str = Depends(get_current_admin)
):
    # Save logo file
    file_url = FileService.save_file(file, "certificates")
    
    # Update education record
    education = EducationService.get_by_id(db, education_id)
    if not education:
        FileService.delete_file(file_url)
        raise HTTPException(status_code=404, detail="Education record not found")
    
    # Delete old logo if exists
    if education.institution_logo_url:
        FileService.delete_file(education.institution_logo_url)
    
    # Update with new logo
    update_data = EducationUpdate(institution_logo_url=file_url)
    EducationService.update(db, education_id, update_data)
    
    return {"message": "Institution logo uploaded successfully", "file_url": file_url}