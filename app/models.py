from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class Skill(Base):
    __tablename__ = "skills"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    category = Column(String(50), nullable=False)  # Frontend, Backend, Database, etc.
    proficiency = Column(Integer, default=1)  # 1-5 scale
    years_experience = Column(Float, default=0.0)
    icon_url = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
class WorkExperience(Base):
    __tablename__="work_experiences"
    
    id = Column(Integer, primary_key=True,index=True)
    company = Column(String(100), nullable=False)
    position = Column(String(100), nullable=False)
    start_date = Column(String(20), nullable=False)  # "2023-01" format
    end_date = Column(String(20), nullable=True)  # null for current position
    description = Column(Text, nullable=False)
    achievements = Column(Text, nullable=True)
    company_logo_url = Column(String(255), nullable=True)
    is_current = Column(Boolean, default=False)
    location = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    


class Project(Base):
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    detailed_description = Column(Text, nullable=True)  # Added this line
    technologies = Column(Text, nullable=False)  # JSON string
    status = Column(String(20), default="completed")  # completed, ongoing, deployed
    is_deployed = Column(Boolean, default=False)
    live_url = Column(String(255), nullable=True)
    github_url = Column(String(255), nullable=True)
    client_name = Column(String(100), nullable=True)
    start_date = Column(String(20), nullable=True)
    end_date = Column(String(20), nullable=True)
    featured = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)    
    
    # relationship to project images
    images = relationship("ProjectImage", back_populates="project", cascade="all, delete-orphan")
    
class ProjectImage(Base):
    __tablename__="project_images"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    image_url = Column(String(255), nullable=False)
    caption = Column(String(255), nullable=True)
    is_main = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # relationship
    
    project = relationship("Project",back_populates="images")
    
class Education(Base):
    __tablename__ = "education"
    
    id = Column(Integer, primary_key=True, index=True)
    institution = Column(String(100), nullable=False)
    degree = Column(String(100), nullable=False)
    field_of_study = Column(String(100), nullable=True)
    education_type = Column(String(20), default="degree")      
    degree_level = Column(String(50), nullable=True)          
    start_date = Column(String(20), nullable=False)
    end_date = Column(String(20), nullable=True)
    gpa = Column(String(10), nullable=True)
    honors = Column(String(100), nullable=True)
    description = Column(Text, nullable=True)                 
    is_current = Column(Boolean, default=False)               
    institution_logo_url = Column(String(255), nullable=True)
    is_certification = Column(Boolean, default=False)
    certificate_url = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
class Admin(Base):
    __tablename__ = "admins"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class PersonalInfo(Base):
    __tablename__ = "personal_info"
    
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(100), nullable=False)
    title = Column(String(100), nullable=False)
    bio = Column(Text, nullable=True)
    email = Column(String(100), nullable=True)
    phone = Column(String(20), nullable=True)
    location = Column(String(100), nullable=True)
    linkedin = Column(String(255), nullable=True)
    github = Column(String(255), nullable=True)
    website = Column(String(255), nullable=True)
    profile_image = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
