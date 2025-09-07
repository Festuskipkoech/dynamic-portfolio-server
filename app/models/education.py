from sqlalchemy import Column, String, Text, Boolean, LargeBinary
from app.models.base import BaseModel

class Education(BaseModel):
    __tablename__ = "education"
    
    institution = Column(String(100), nullable=False, index=True)
    degree = Column(String(100), nullable=False)
    field_of_study = Column(String(100))
    education_type = Column(String(20), default="degree", nullable=False)
    degree_level = Column(String(50))
    start_date = Column(String(20), nullable=False)
    end_date = Column(String(20))
    gpa = Column(String(10))
    honors = Column(String(100))
    description = Column(Text)
    is_current = Column(Boolean, default=False, nullable=False)
    is_certification = Column(Boolean, default=False, nullable=False)
    
    # Institution logo stored as binary data
    institution_logo = Column(LargeBinary)
    institution_logo_type = Column(String(50))
    
    # Certificate stored as binary data
    certificate_data = Column(LargeBinary)
    certificate_type = Column(String(50))
    
    def __repr__(self):
        return f"<Education(institution='{self.institution}', degree='{self.degree}')>"