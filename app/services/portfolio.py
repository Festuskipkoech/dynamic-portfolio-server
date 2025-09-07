from typing import List, Optional, Tuple
from sqlalchemy.orm import Session
from fastapi import UploadFile
from app.models.portfolio import Skill, WorkExperience
from app.schemas.portfolio import (
    SkillCreate, SkillUpdate,
    WorkExperienceCreate, WorkExperienceUpdate
)
from app.services.base import BaseService
from app.services.file import FileService

class SkillService(BaseService[Skill, SkillCreate, SkillUpdate]):
    def __init__(self):
        super().__init__(Skill)
    
    def get_by_category(self, db: Session, category: str) -> List[Skill]:
        """Get skills by category"""
        return db.query(Skill).filter(Skill.category == category).all()
    
    def get_categories(self, db: Session) -> List[str]:
        """Get all unique skill categories"""
        return [cat[0] for cat in db.query(Skill.category).distinct().all()]
    
    def upload_icon(self, db: Session, skill_id: int, file: UploadFile) -> Skill:
        """Upload and set skill icon"""
        skill = self.get_by_id_or_404(db, skill_id)
        
        # Validate and process image
        image_data, mime_type = FileService.validate_image_file(file)
        
        # Update skill with icon
        skill.icon_data = image_data
        skill.icon_type = mime_type
        db.commit()
        db.refresh(skill)
        
        return skill
    
    def get_icon(self, db: Session, skill_id: int) -> Optional[Tuple[bytes, str]]:
        """Get skill icon data and MIME type"""
        skill = self.get_by_id(db, skill_id)
        if skill and skill.icon_data:
            return skill.icon_data, skill.icon_type
        return None
    
    def delete_icon(self, db: Session, skill_id: int) -> Skill:
        """Remove skill icon"""
        skill = self.get_by_id_or_404(db, skill_id)
        skill.icon_data = None
        skill.icon_type = None
        db.commit()
        db.refresh(skill)
        return skill

class WorkExperienceService(BaseService[WorkExperience, WorkExperienceCreate, WorkExperienceUpdate]):
    def __init__(self):
        super().__init__(WorkExperience)
    
    def get_all_ordered(self, db: Session) -> List[WorkExperience]:
        """Get all work experiences ordered by start date (newest first)"""
        return db.query(WorkExperience).order_by(
            WorkExperience.start_date.desc()
        ).all()
    
    def get_current_positions(self, db: Session) -> List[WorkExperience]:
        """Get current work positions"""
        return db.query(WorkExperience).filter(
            WorkExperience.is_current == True
        ).all()
    
    def upload_company_logo(self, db: Session, experience_id: int, file: UploadFile) -> WorkExperience:
        """Upload and set company logo"""
        experience = self.get_by_id_or_404(db, experience_id)
        
        # Validate and process image
        image_data, mime_type = FileService.validate_image_file(file)
        
        # Update experience with logo
        experience.company_logo = image_data
        experience.company_logo_type = mime_type
        db.commit()
        db.refresh(experience)
        
        return experience
    
    def get_company_logo(self, db: Session, experience_id: int) -> Optional[Tuple[bytes, str]]:
        """Get company logo data and MIME type"""
        experience = self.get_by_id(db, experience_id)
        if experience and experience.company_logo:
            return experience.company_logo, experience.company_logo_type
        return None
    
    def delete_company_logo(self, db: Session, experience_id: int) -> WorkExperience:
        """Remove company logo"""
        experience = self.get_by_id_or_404(db, experience_id)
        experience.company_logo = None
        experience.company_logo_type = None
        db.commit()
        db.refresh(experience)
        return experience

# Create singleton instances
skill_service = SkillService()
work_experience_service = WorkExperienceService()