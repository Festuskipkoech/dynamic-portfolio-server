from sqlalchemy import Column, String, Text, Integer, Float, Boolean, LargeBinary
from app.models.base import BaseModel

class Skill(BaseModel):
    __tablename__ = "skills"
    
    name = Column(String(100), nullable=False, index=True)
    category = Column(String(50), nullable=False, index=True)
    proficiency = Column(Integer, nullable=False, default=1)  # 1-5 scale
    years_experience = Column(Float, nullable=False, default=0.0)
    
    # Icon stored as binary data
    icon_data = Column(LargeBinary)
    icon_type = Column(String(50))
    
    def __repr__(self):
        return f"<Skill(name='{self.name}', category='{self.category}')>"

class WorkExperience(BaseModel):
    __tablename__ = "work_experiences"
    
    company = Column(String(100), nullable=False, index=True)
    position = Column(String(100), nullable=False)
    start_date = Column(String(20), nullable=False)
    end_date = Column(String(20))
    description = Column(Text, nullable=False)
    achievements = Column(Text)
    location = Column(String(100))
    is_current = Column(Boolean, default=False, nullable=False)
    
    # Company logo stored as binary data
    company_logo = Column(LargeBinary)
    company_logo_type = Column(String(50))
    
    def __repr__(self):
        return f"<WorkExperience(company='{self.company}', position='{self.position}')>"