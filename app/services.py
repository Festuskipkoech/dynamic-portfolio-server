from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status, UploadFile
import os
import uuid
from .config import get_settings

from .schemas import (
    SkillCreate, SkillUpdate, 
    WorkExperienceCreate, WorkExperienceUpdate,
    ProjectCreate, ProjectImageCreate, ProjectUpdate,
    EducationCreate, EducationUpdate, PersonalInfoCreate,PersonalInfoUpdate, PersonalInfo
)
from .models import Skill, WorkExperience, Project, ProjectImage, Education, PersonalInfo
settings = get_settings()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)
    
    @staticmethod
    def get_password_hash(password: str) -> str:
        return pwd_context.hash(password)
    
    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
        return encoded_jwt
    
    @staticmethod
    def authenticate_admin(username: str, password: str) -> bool:
        # Simple authentication 
        return username == "Festus" and password == settings.admin_password

class FileService:
    @staticmethod
    def validate_file(file: UploadFile) -> bool:
        file_extension = os.path.splitext(file.filename)[1].lower()
        return file_extension in settings.allowed_extensions
    
    @staticmethod
    def save_file(file: UploadFile, folder: str) -> str:
        if not FileService.validate_file(file):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="File type not allowed"
            )
        
        file_extension = os.path.splitext(file.filename)[1]
        filename = f"{uuid.uuid4()}{file_extension}"
        file_path = os.path.join(settings.upload_dir, folder, filename)
        
        with open(file_path, "wb") as buffer:
            content = file.file.read()
            if len(content) > settings.max_file_size:
                raise HTTPException(
                    status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                    detail="File too large"
                )
            buffer.write(content)
        
        return f"/{settings.upload_dir}/{folder}/{filename}"
    
    @staticmethod
    def delete_file(file_path: str) -> bool:
        try:
            full_path = file_path.lstrip('/')
            if os.path.exists(full_path):
                os.remove(full_path)
                return True
        except:
            pass
        return False

class SkillService:
    @staticmethod
    def get_all(db: Session) -> List[Skill]:
        return db.query(Skill).all()
    
    @staticmethod
    def get_by_id(db: Session, skill_id: int) -> Optional[Skill]:
        return db.query(Skill).filter(Skill.id == skill_id).first()
    
    @staticmethod
    def create(db: Session, skill: SkillCreate) -> Skill:
        db_skill = Skill(**skill.dict())
        db.add(db_skill)
        db.commit()
        db.refresh(db_skill)
        return db_skill
    
    @staticmethod
    def update(db: Session, skill_id: int, skill_update: SkillUpdate) -> Optional[Skill]:
        db_skill = SkillService.get_by_id(db, skill_id)
        if not db_skill:
            return None
        
        update_data = skill_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_skill, field, value)
        
        db.commit()
        db.refresh(db_skill)
        return db_skill
    
    @staticmethod
    def delete(db: Session, skill_id: int) -> bool:
        db_skill = SkillService.get_by_id(db, skill_id)
        if not db_skill:
            return False
        db.delete(db_skill)
        db.commit()
        return True
class WorkExperienceService:
    @staticmethod
    def _map_frontend_to_backend(data: dict) -> dict:
        """Map frontend field names and data types to backend format"""
        mapped_data = {}
        
        # Map field names
        field_mapping = {
            'job_title': 'position',  # Frontend sends job_title, backend expects position
        }
        
        for frontend_field, backend_field in field_mapping.items():
            if frontend_field in data:
                mapped_data[backend_field] = data[frontend_field]
        
        # Copy fields that don't need mapping
        direct_copy_fields = [
            'company', 'start_date', 'end_date', 'description', 
            'is_current', 'location', 'company_logo_url'
        ]
        for field in direct_copy_fields:
            if field in data:
                mapped_data[field] = data[field]
        
        # Convert achievements array to newline-separated string
        if 'achievements' in data and data['achievements']:
            if isinstance(data['achievements'], list):
                mapped_data['achievements'] = '\n'.join(data['achievements'])
            else:
                mapped_data['achievements'] = data['achievements']
        
        # Handle technologies_used - store as JSON string or comma-separated
        if 'technologies_used' in data and data['technologies_used']:
            if isinstance(data['technologies_used'], list):
                # Store as comma-separated string
                mapped_data['technologies_used'] = ', '.join(data['technologies_used'])
            else:
                mapped_data['technologies_used'] = data['technologies_used']
        
        # Handle company_website and employment_type (store as JSON or separate fields)
        # Since your current model doesn't have these fields, we'll store them as JSON in a text field
        # or you can add these columns to your database
        
        # Remove None values
        mapped_data = {k: v for k, v in mapped_data.items() if v is not None and v != ''}
        
        return mapped_data

    @staticmethod
    def get_all(db: Session) -> List[WorkExperience]:
        return db.query(WorkExperience).order_by(WorkExperience.start_date.desc()).all()
    
    @staticmethod
    def get_by_id(db: Session, experience_id: int) -> Optional[WorkExperience]:
        return db.query(WorkExperience).filter(WorkExperience.id == experience_id).first()
    
    @staticmethod
    def create(db: Session, experience: WorkExperienceCreate) -> WorkExperience:
        # Convert frontend data to backend format
        experience_data = WorkExperienceService._map_frontend_to_backend(experience.dict())
        
        print("DEBUG - Mapped work experience data:", experience_data)  # Debug logging
        
        db_experience = WorkExperience(**experience_data)
        db.add(db_experience)
        db.commit()
        db.refresh(db_experience)
        return db_experience
    
    @staticmethod
    def update(db: Session, experience_id: int, experience_update: WorkExperienceUpdate) -> Optional[WorkExperience]:
        db_experience = WorkExperienceService.get_by_id(db, experience_id)
        if not db_experience:
            return None
        
        # Convert frontend data to backend format
        update_data = WorkExperienceService._map_frontend_to_backend(experience_update.dict(exclude_unset=True))
        
        for field, value in update_data.items():
            setattr(db_experience, field, value)
        
        db.commit()
        db.refresh(db_experience)
        return db_experience
    
    @staticmethod
    def delete(db: Session, experience_id: int) -> bool:
        db_experience = WorkExperienceService.get_by_id(db, experience_id)
        if not db_experience:
            return False
        
        # Delete company logo if exists
        if db_experience.company_logo_url:
            FileService.delete_file(db_experience.company_logo_url)
        
        db.delete(db_experience)
        db.commit()
        return True
class ProjectService:
    @staticmethod
    def _map_frontend_to_backend(data: dict) -> dict:
        """Map frontend field names and data types to backend format"""
        mapped_data = {}
        
        # Map field names
        field_mapping = {
            'name': 'title',
            'project_url': 'live_url',
            'is_featured': 'featured'
        }
        
        for frontend_field, backend_field in field_mapping.items():
            if frontend_field in data:
                mapped_data[backend_field] = data[frontend_field]
        
        # Copy fields that don't need mapping
        direct_copy_fields = [
            'description', 'detailed_description', 'github_url', 
            'start_date', 'end_date', 'status', 'is_deployed', 'client_name'
        ]
        for field in direct_copy_fields:
            if field in data:
                mapped_data[field] = data[field]
        
        # Convert technologies array to comma-separated string
        if 'technologies' in data and isinstance(data['technologies'], list):
            mapped_data['technologies'] = ', '.join(data['technologies'])
        elif 'technologies' in data:
            mapped_data['technologies'] = data['technologies']
        
        # Set defaults for required fields if missing
        if 'status' not in mapped_data:
            mapped_data['status'] = 'completed'
        if 'is_deployed' not in mapped_data:
            mapped_data['is_deployed'] = False
        if 'featured' not in mapped_data:
            mapped_data['featured'] = False
        
        # Remove None values
        mapped_data = {k: v for k, v in mapped_data.items() if v is not None}
        
        return mapped_data

    @staticmethod
    def get_all(db: Session) -> List[Project]:
        return db.query(Project).order_by(Project.created_at.desc()).all()
    
    @staticmethod
    def get_by_id(db: Session, project_id: int) -> Optional[Project]:
        return db.query(Project).filter(Project.id == project_id).first()
    
    @staticmethod
    def create(db: Session, project: ProjectCreate) -> Project:
        # Convert frontend data to backend format
        project_data = ProjectService._map_frontend_to_backend(project.dict())
        
        print("DEBUG - Mapped project data:", project_data)  # Debug logging
        
        db_project = Project(**project_data)
        db.add(db_project)
        db.commit()
        db.refresh(db_project)
        return db_project
    
    @staticmethod
    def update(db: Session, project_id: int, project_update: ProjectUpdate) -> Optional[Project]:
        db_project = ProjectService.get_by_id(db, project_id)
        if not db_project:
            return None
        
        # Convert frontend data to backend format
        update_data = ProjectService._map_frontend_to_backend(project_update.dict(exclude_unset=True))
        
        for field, value in update_data.items():
            setattr(db_project, field, value)
        
        db.commit()
        db.refresh(db_project)
        return db_project
    
    @staticmethod
    def delete(db: Session, project_id: int) -> bool:
        db_project = ProjectService.get_by_id(db, project_id)
        if not db_project:
            return False
        
        # Delete project images
        for image in db_project.images:
            FileService.delete_file(image.image_url)
        
        db.delete(db_project)
        db.commit()
        return True
    
    @staticmethod
    def add_image(db: Session, project_id: int, image_data: ProjectImageCreate) -> Optional[ProjectImage]:
        project = ProjectService.get_by_id(db, project_id)
        if not project:
            return None
        
        db_image = ProjectImage(**image_data.dict(), project_id=project_id)
        db.add(db_image)
        db.commit()
        db.refresh(db_image)
        return db_image
    
    @staticmethod
    def delete_image(db: Session, image_id: int) -> bool:
        db_image = db.query(ProjectImage).filter(ProjectImage.id == image_id).first()
        if not db_image:
            return False
        
        FileService.delete_file(db_image.image_url)
        db.delete(db_image)
        db.commit()
        return True

class EducationService:
    @staticmethod
    def _map_frontend_to_backend(data: dict) -> dict:
        """Map frontend field names and data to backend format"""
        mapped_data = {}
        
        # Map field names from frontend to backend
        field_mapping = {
            'institution_name': 'institution',
            'degree_title': 'degree',
        }
        
        for frontend_field, backend_field in field_mapping.items():
            if frontend_field in data:
                mapped_data[backend_field] = data[frontend_field]
        
        # Copy fields that don't need mapping
        direct_copy_fields = [
            'field_of_study', 'start_date', 'end_date', 'gpa',
            'institution_logo_url', 'certificate_url'
        ]
        for field in direct_copy_fields:
            if field in data:
                mapped_data[field] = data[field]
        
        # Handle education type conversion
        if 'education_type' in data:
            mapped_data['is_certification'] = data['education_type'] == 'certification'
        
        # Handle honors field (could map from description or leave empty)
        if 'description' in data and data['description']:
            # You could extract honors from description or leave it as None
            # For now, we'll leave honors as None and handle description separately
            pass
        
        # Set defaults
        if 'is_certification' not in mapped_data:
            mapped_data['is_certification'] = False
            
        # Remove None values
        mapped_data = {k: v for k, v in mapped_data.items() if v is not None}
        
        return mapped_data

    @staticmethod
    def get_all(db: Session) -> List[Education]:
        return db.query(Education).order_by(Education.end_date.desc()).all()
    
    @staticmethod
    def get_by_id(db: Session, education_id: int) -> Optional[Education]:
        return db.query(Education).filter(Education.id == education_id).first()
    
    @staticmethod
    def create(db: Session, education: EducationCreate) -> Education:
        # Convert frontend data to backend format
        education_data = EducationService._map_frontend_to_backend(education.dict())
        
        print("DEBUG - Mapped education data:", education_data)  # Debug logging
        
        db_education = Education(**education_data)
        db.add(db_education)
        db.commit()
        db.refresh(db_education)
        return db_education
    
    @staticmethod
    def update(db: Session, education_id: int, education_update: EducationUpdate) -> Optional[Education]:
        db_education = EducationService.get_by_id(db, education_id)
        if not db_education:
            return None
        
        # Convert frontend data to backend format
        update_data = EducationService._map_frontend_to_backend(education_update.dict(exclude_unset=True))
        
        for field, value in update_data.items():
            setattr(db_education, field, value)
        
        db.commit()
        db.refresh(db_education)
        return db_education
    
    @staticmethod
    def delete(db: Session, education_id: int) -> bool:
        db_education = EducationService.get_by_id(db, education_id)
        if not db_education:
            return False
        
        # Delete files if they exist
        if db_education.certificate_url:
            FileService.delete_file(db_education.certificate_url)
        if db_education.institution_logo_url:
            FileService.delete_file(db_education.institution_logo_url)
        
        db.delete(db_education)
        db.commit()
        return True
class PersonalInfoService:
    @staticmethod
    def get_personal_info(db: Session) -> Optional[PersonalInfo]:
        """Get personal info (there should be only one record)"""
        return db.query(PersonalInfo).first()
    
    @staticmethod
    def create_personal_info(db: Session, personal_info: PersonalInfoCreate) -> PersonalInfo:
        """Create personal info record"""
        db_info = PersonalInfo(**personal_info.dict())
        db.add(db_info)
        db.commit()
        db.refresh(db_info)
        return db_info
    
    @staticmethod
    def update_personal_info(db: Session, personal_info_update: PersonalInfoUpdate) -> PersonalInfo:
        """Update personal info (create if doesn't exist)"""
        db_info = PersonalInfoService.get_personal_info(db)
        
        if not db_info:
            # Create new record if none exists
            create_data = PersonalInfoCreate(**personal_info_update.dict())
            return PersonalInfoService.create_personal_info(db, create_data)
        
        # Update existing record
        update_data = personal_info_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_info, field, value)
        
        db_info.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(db_info)
        return db_info
    
    @staticmethod
    def delete_personal_info(db: Session) -> bool:
        """Delete personal info record"""
        db_info = PersonalInfoService.get_personal_info(db)
        if not db_info:
            return False
        
        # Delete profile image if exists
        if db_info.profile_image:
            FileService.delete_file(db_info.profile_image)
        
        db.delete(db_info)
        db.commit()
        return True