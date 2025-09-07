from typing import List, Optional, Tuple
from sqlalchemy.orm import Session
from fastapi import UploadFile
from app.models.education import Education
from app.schemas.education import EducationCreate, EducationUpdate
from app.services.base import BaseService
from app.services.file import FileService

class EducationService(BaseService[Education, EducationCreate, EducationUpdate]):
    def __init__(self):
        super().__init__(Education)
    
    def get_all_ordered(self, db: Session) -> List[Education]:
        """Get all education records ordered by end date (newest first)"""
        return db.query(Education).order_by(
            Education.end_date.desc().nullsfirst()  # Current education first
        ).all()
    
    def get_degrees(self, db: Session) -> List[Education]:
        """Get formal degree education"""
        return db.query(Education).filter(
            Education.is_certification == False
        ).order_by(Education.end_date.desc()).all()
    
    def get_certifications(self, db: Session) -> List[Education]:
        """Get certifications"""
        return db.query(Education).filter(
            Education.is_certification == True
        ).order_by(Education.end_date.desc()).all()
    
    def get_current(self, db: Session) -> List[Education]:
        """Get current education/certifications"""
        return db.query(Education).filter(
            Education.is_current == True
        ).all()
    
    def upload_institution_logo(self, db: Session, education_id: int, file: UploadFile) -> Education:
        """Upload and set institution logo"""
        education = self.get_by_id_or_404(db, education_id)
        
        # Validate and process image
        image_data, mime_type = FileService.validate_image_file(file)
        
        # Update education with logo
        education.institution_logo = image_data
        education.institution_logo_type = mime_type
        db.commit()
        db.refresh(education)
        
        return education
    
    def get_institution_logo(self, db: Session, education_id: int) -> Optional[Tuple[bytes, str]]:
        """Get institution logo data and MIME type"""
        education = self.get_by_id(db, education_id)
        if education and education.institution_logo:
            return education.institution_logo, education.institution_logo_type
        return None
    
    def delete_institution_logo(self, db: Session, education_id: int) -> Education:
        """Remove institution logo"""
        education = self.get_by_id_or_404(db, education_id)
        education.institution_logo = None
        education.institution_logo_type = None
        db.commit()
        db.refresh(education)
        return education
    
    def upload_certificate(self, db: Session, education_id: int, file: UploadFile) -> Education:
        """Upload and set certificate"""
        education = self.get_by_id_or_404(db, education_id)
        
        # Validate and process document (can be image or PDF)
        document_data, mime_type = FileService.process_upload(file)
        
        # Update education with certificate
        education.certificate_data = document_data
        education.certificate_type = mime_type
        db.commit()
        db.refresh(education)
        
        return education
    
    def get_certificate(self, db: Session, education_id: int) -> Optional[Tuple[bytes, str]]:
        """Get certificate data and MIME type"""
        education = self.get_by_id(db, education_id)
        if education and education.certificate_data:
            return education.certificate_data, education.certificate_type
        return None
    
    def delete_certificate(self, db: Session, education_id: int) -> Education:
        """Remove certificate"""
        education = self.get_by_id_or_404(db, education_id)
        education.certificate_data = None
        education.certificate_type = None
        db.commit()
        db.refresh(education)
        return education

# Create singleton instance
education_service = EducationService()