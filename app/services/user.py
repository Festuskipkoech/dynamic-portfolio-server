from typing import Optional, Tuple
from sqlalchemy.orm import Session
from fastapi import UploadFile
from app.models.user import PersonalInfo
from app.schemas.user import PersonalInfoCreate, PersonalInfoUpdate
from app.services.base import BaseService
from app.services.file import FileService
from app.core.exceptions import SingletonViolationError

class PersonalInfoService(BaseService[PersonalInfo, PersonalInfoCreate, PersonalInfoUpdate]):
    def __init__(self):
        super().__init__(PersonalInfo)
    
    def get_personal_info(self, db: Session) -> Optional[PersonalInfo]:
        """Get the single personal info record"""
        return db.query(PersonalInfo).first()
    
    def create_or_update(self, db: Session, obj_in: PersonalInfoUpdate) -> PersonalInfo:
        """Create or update personal info (singleton pattern)"""
        existing = self.get_personal_info(db)
        
        if existing:
            return self.update(db, existing, obj_in)
        else:
            # Convert update schema to create schema
            create_data = PersonalInfoCreate(**obj_in.model_dump(exclude_unset=True))
            return self.create(db, create_data)
    
    def create(self, db: Session, obj_in: PersonalInfoCreate) -> PersonalInfo:
        """Create personal info (enforce singleton)"""
        existing = self.get_personal_info(db)
        if existing:
            raise SingletonViolationError("PersonalInfo")
        
        return super().create(db, obj_in)
    
    def upload_profile_image(self, db: Session, file: UploadFile) -> PersonalInfo:
        """Upload and set profile image"""
        # Validate and process image
        image_data, mime_type = FileService.validate_image_file(file)
        
        # Get or create personal info
        personal_info = self.get_personal_info(db)
        if not personal_info:
            # Create minimal personal info record
            personal_info = self.create(db, PersonalInfoCreate(
                full_name="",
                title=""
            ))
        
        # Update with image
        personal_info.profile_image = image_data
        personal_info.profile_image_type = mime_type
        db.commit()
        db.refresh(personal_info)
        
        return personal_info
    
    def get_profile_image(self, db: Session) -> Optional[Tuple[bytes, str]]:
        """Get profile image data and MIME type"""
        personal_info = self.get_personal_info(db)
        if personal_info and personal_info.profile_image:
            return personal_info.profile_image, personal_info.profile_image_type
        return None
    
    def delete_profile_image(self, db: Session) -> PersonalInfo:
        """Remove profile image"""
        personal_info = self.get_personal_info(db)
        if personal_info:
            personal_info.profile_image = None
            personal_info.profile_image_type = None
            db.commit()
            db.refresh(personal_info)
        return personal_info

# Create singleton instance
personal_info_service = PersonalInfoService()