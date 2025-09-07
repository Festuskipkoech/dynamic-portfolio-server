from typing import List, Optional, Tuple
from sqlalchemy.orm import Session, joinedload
from fastapi import UploadFile
from app.models.project import Project, ProjectImage, ProjectCategory, project_skills
from app.models.portfolio import Skill
from app.schemas.project import (
    ProjectCreate, ProjectUpdate, ProjectCategoryCreate, ProjectCategoryUpdate,
    ProjectImageCreate, ProjectSkillAssignment
)
from app.core.exceptions import NotFoundError
from app.services.base import BaseService
from app.services.file import FileService

class ProjectCategoryService(BaseService[ProjectCategory, ProjectCategoryCreate, ProjectCategoryUpdate]):
    def __init__(self):
        super().__init__(ProjectCategory)
    
    def get_by_name(self, db: Session, name: str) -> Optional[ProjectCategory]:
        """Get category by name"""
        return db.query(ProjectCategory).filter(ProjectCategory.name == name).first()

class ProjectService(BaseService[Project, ProjectCreate, ProjectUpdate]):
    def __init__(self):
        super().__init__(Project)
    
    def create(self, db: Session, obj_in: ProjectCreate) -> Project:
        """Create project with skills association"""
        # Extract skill_ids before creating project
        skill_ids = obj_in.skill_ids or []
        project_data = obj_in.model_dump(exclude={'skill_ids'})
        
        # Convert technologies list to string
        if 'technologies' in project_data:
            project_data['technologies'] = ', '.join(project_data['technologies'])
        
        # Create project
        db_project = Project(**project_data)
        db.add(db_project)
        db.commit()
        db.refresh(db_project)
        
        # Associate skills
        if skill_ids:
            self._associate_skills(db, db_project.id, skill_ids)
        
        return db_project
    
    def update_by_id(self, db: Session, id: int, obj_in: ProjectUpdate) -> Project:
        """Update project with skills association"""
        db_project = self.get_by_id_or_404(db, id)
        
        # Extract skill_ids before updating
        skill_ids = obj_in.skill_ids
        update_data = obj_in.model_dump(exclude_unset=True, exclude={'skill_ids'})
        
        # Convert technologies list to string if provided
        if 'technologies' in update_data:
            update_data['technologies'] = ', '.join(update_data['technologies'])
        
        # Update project fields
        for field, value in update_data.items():
            setattr(db_project, field, value)
        
        # Update skills association if provided
        if skill_ids is not None:
            self._update_skills_association(db, id, skill_ids)
        
        db.commit()
        db.refresh(db_project)
        return db_project
    
    def get_all_with_relations(self, db: Session) -> List[Project]:
        """Get all projects with category, images, and skills"""
        return db.query(Project).options(
            joinedload(Project.category),
            joinedload(Project.images),
            joinedload(Project.skills)
        ).order_by(Project.created_at.desc()).all()
    
    def get_featured(self, db: Session) -> List[Project]:
        """Get featured projects"""
        return db.query(Project).filter(
            Project.featured == True
        ).options(
            joinedload(Project.category),
            joinedload(Project.images),
            joinedload(Project.skills)
        ).all()
    
    def get_by_category(self, db: Session, category_id: int) -> List[Project]:
        """Get projects by category"""
        return db.query(Project).filter(
            Project.category_id == category_id
        ).options(
            joinedload(Project.images),
            joinedload(Project.skills)
        ).all()
    
    def get_by_skill(self, db: Session, skill_id: int) -> List[Project]:
        """Get projects that use a specific skill"""
        return db.query(Project).join(project_skills).filter(
            project_skills.c.skill_id == skill_id
        ).options(
            joinedload(Project.category),
            joinedload(Project.images),
            joinedload(Project.skills)
        ).all()
    
    def get_with_case_studies(self, db: Session) -> List[Project]:
        """Get projects that have complete case studies"""
        return db.query(Project).filter(
            Project.problem_statement.isnot(None),
            Project.solution_approach.isnot(None)
        ).options(
            joinedload(Project.category),
            joinedload(Project.images),
            joinedload(Project.skills)
        ).all()
    
    def _associate_skills(self, db: Session, project_id: int, skill_ids: List[int]):
        """Associate skills with project"""
        for skill_id in skill_ids:
            # Verify skill exists
            skill = db.query(Skill).filter(Skill.id == skill_id).first()
            if skill:
                # Insert into junction table
                stmt = project_skills.insert().values(
                    project_id=project_id,
                    skill_id=skill_id,
                    relevance_score=5  # Default relevance
                )
                db.execute(stmt)
        db.commit()
    
    def _update_skills_association(self, db: Session, project_id: int, skill_ids: List[int]):
        """Update skills association for project"""
        # Remove existing associations
        db.execute(
            project_skills.delete().where(project_skills.c.project_id == project_id)
        )
        
        # Add new associations
        if skill_ids:
            self._associate_skills(db, project_id, skill_ids)
    
    def assign_skill(self, db: Session, project_id: int, assignment: ProjectSkillAssignment) -> Project:
        """Assign a skill to project with relevance score"""
        project = self.get_by_id_or_404(db, project_id)
        
        # Check if skill exists
        skill = db.query(Skill).filter(Skill.id == assignment.skill_id).first()
        if not skill:
            raise NotFoundError("Skill", str(assignment.skill_id))
        
        # Remove existing association if any
        db.execute(
            project_skills.delete().where(
                project_skills.c.project_id == project_id,
                project_skills.c.skill_id == assignment.skill_id
            )
        )
        
        # Add new association
        stmt = project_skills.insert().values(
            project_id=project_id,
            skill_id=assignment.skill_id,
            relevance_score=assignment.relevance_score
        )
        db.execute(stmt)
        db.commit()
        
        return project

class ProjectImageService(BaseService[ProjectImage, ProjectImageCreate, ProjectImageCreate]):
    def __init__(self):
        super().__init__(ProjectImage)
    
    def upload_images(self, db: Session, project_id: int, files: List[UploadFile], 
                     captions: List[str] = None, main_index: int = 0) -> List[ProjectImage]:
        """Upload multiple images for a project"""
        # Verify project exists
        project = db.query(Project).filter(Project.id == project_id).first()
        if not project:
            raise NotFoundError("Project", str(project_id))
        
        uploaded_images = []
        captions = captions or []
        
        for i, file in enumerate(files):
            # Validate and process image
            image_data, mime_type = FileService.validate_image_file(file)
            
            # Create image record
            image = ProjectImage(
                project_id=project_id,
                image_data=image_data,
                image_type=mime_type,
                caption=captions[i] if i < len(captions) else None,
                is_main=(i == main_index)
            )
            
            db.add(image)
            uploaded_images.append(image)
        
        db.commit()
        for image in uploaded_images:
            db.refresh(image)
        
        return uploaded_images
    
    def get_project_images(self, db: Session, project_id: int) -> List[ProjectImage]:
        """Get all images for a project"""
        return db.query(ProjectImage).filter(
            ProjectImage.project_id == project_id
        ).all()
    
    def get_main_image(self, db: Session, project_id: int) -> Optional[ProjectImage]:
        """Get main image for a project"""
        return db.query(ProjectImage).filter(
            ProjectImage.project_id == project_id,
            ProjectImage.is_main == True
        ).first()
    
    def get_image_data(self, db: Session, image_id: int) -> Optional[Tuple[bytes, str]]:
        """Get image data and MIME type"""
        image = self.get_by_id(db, image_id)
        if image:
            return image.image_data, image.image_type
        return None
    
    def set_main_image(self, db: Session, image_id: int) -> ProjectImage:
        """Set an image as the main image for its project"""
        image = self.get_by_id_or_404(db, image_id)
        
        # Remove main flag from other images in the same project
        db.query(ProjectImage).filter(
            ProjectImage.project_id == image.project_id,
            ProjectImage.id != image_id
        ).update({"is_main": False})
        
        # Set this image as main
        image.is_main = True
        db.commit()
        db.refresh(image)
        
        return image

# Create singleton instances
project_category_service = ProjectCategoryService()
project_service = ProjectService()
project_image_service = ProjectImageService()