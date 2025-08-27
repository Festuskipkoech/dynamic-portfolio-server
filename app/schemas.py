from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

# Auth schemas

class AdminLogin(BaseModel):
    username: str
    password: str
    
class Token(BaseModel):
    access_token: str
    token_type: str

# Base schemas
class SkillBase(BaseModel):
    name: str = Field(..., max_length=100)
    category: str = Field(..., max_length=50)
    proficiency: int = Field(default=1, ge=1, le=5)
    years_experience: float = Field(default=0.0, ge=0)
    icon_url:Optional [str] = None
    
class SkillCreate(SkillBase):
    pass


class SkillUpdate(SkillBase):
    name: Optional[str] = None
    category: Optional[str] = None
    proficiency: Optional[int] = Field(None, ge=1, le=5)
    years_experience: Optional[float] = Field(None, ge=0)

class Skill(SkillBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True
        
# work experience schemas
class WorkExperienceBase(BaseModel):
    company: str = Field(..., max_length=100)
    position: str = Field(..., max_length=100)  # Maps to job_title from frontend
    start_date: str = Field(..., max_length=20)
    end_date: Optional[str] = Field(None, max_length=20)
    description: str
    achievements: Optional[str] = None
    company_logo_url: Optional[str] = None
    is_current: bool = False
    location: Optional[str] = Field(None, max_length=100)

class WorkExperienceCreate(BaseModel):
    # Accept frontend field names exactly
    job_title: str = Field(..., max_length=100)  # Frontend sends this
    company: str = Field(..., max_length=100)
    company_website: Optional[str] = None  # Frontend sends this
    location: Optional[str] = Field(None, max_length=100)
    employment_type: Optional[str] = Field(None, max_length=20)  # Frontend sends this
    start_date: str = Field(..., max_length=20)
    end_date: Optional[str] = Field(None, max_length=20)
    is_current: bool = False
    description: str
    achievements: Optional[List[str]] = None  # Frontend sends array
    technologies_used: Optional[List[str]] = None  # Frontend sends array

class WorkExperienceUpdate(BaseModel):
    # Accept frontend field names for updates
    job_title: Optional[str] = Field(None, max_length=100)
    company: Optional[str] = Field(None, max_length=100)
    company_website: Optional[str] = None
    location: Optional[str] = Field(None, max_length=100)
    employment_type: Optional[str] = Field(None, max_length=20)
    start_date: Optional[str] = Field(None, max_length=20)
    end_date: Optional[str] = Field(None, max_length=20)
    is_current: Optional[bool] = None
    description: Optional[str] = None
    achievements: Optional[List[str]] = None  # Frontend sends array
    technologies_used: Optional[List[str]] = None  # Frontend sends array

class WorkExperience(WorkExperienceBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# Project Image Schemas
class ProjectImageBase(BaseModel):
    image_url: str
    caption: Optional[str] = None
    is_main: bool = False

class ProjectImageCreate(ProjectImageBase):
    pass

class ProjectImage(ProjectImageBase):
    id: int
    project_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# Project Schemas

class ProjectBase(BaseModel):
    title: str = Field(..., max_length=100)
    description: str
    detailed_description: Optional[str] = None  # Added field
    technologies: str  # Keep as string for database storage
    status: str = Field(default="completed", max_length=20)
    is_deployed: bool = False
    live_url: Optional[str] = None
    github_url: Optional[str] = None
    client_name: Optional[str] = Field(None, max_length=100)
    start_date: Optional[str] = Field(None, max_length=20)
    end_date: Optional[str] = Field(None, max_length=20)
    featured: bool = False

class ProjectCreate(BaseModel):
    # Accept frontend field names exactly as sent
    name: str = Field(..., max_length=100)  # Frontend sends 'name'
    description: str
    detailed_description: Optional[str] = None  # Frontend sends this
    technologies: List[str]  # Frontend sends array
    project_url: Optional[str] = None  # Frontend sends 'project_url'
    github_url: Optional[str] = None
    start_date: Optional[str] = Field(None, max_length=20)
    end_date: Optional[str] = Field(None, max_length=20)
    is_featured: bool = False  # Frontend sends 'is_featured'

class ProjectUpdate(BaseModel):
    # Accept frontend field names for updates too
    name: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = None
    detailed_description: Optional[str] = None
    technologies: Optional[List[str]] = None  # Array from frontend
    status: Optional[str] = Field(None, max_length=20)
    is_deployed: Optional[bool] = None
    project_url: Optional[str] = None  # Frontend field name
    github_url: Optional[str] = None
    client_name: Optional[str] = Field(None, max_length=100)
    start_date: Optional[str] = Field(None, max_length=20)
    end_date: Optional[str] = Field(None, max_length=20)
    is_featured: Optional[bool] = None  # Frontend field name

class Project(ProjectBase):
    id: int
    created_at: datetime
    images: List[ProjectImage] = []
    
    class Config:
        from_attributes = True

# Education Schemas
class EducationBase(BaseModel):
    institution: str = Field(..., max_length=100)
    degree: str = Field(..., max_length=100)
    field_of_study: Optional[str] = Field(None, max_length=100)
    start_date: str = Field(..., max_length=20)
    end_date: Optional[str] = Field(None, max_length=20)
    gpa: Optional[str] = Field(None, max_length=10)
    honors: Optional[str] = Field(None, max_length=100)
    institution_logo_url: Optional[str] = None
    is_certification: bool = False
    certificate_url: Optional[str] = None

class EducationCreate(BaseModel):
    # Accept frontend field names
    institution_name: str = Field(..., max_length=100)  
    degree_title: str = Field(..., max_length=100)     
    field_of_study: Optional[str] = Field(None, max_length=100)
    education_type: str = Field(default="degree", max_length=20)  
    degree_level: Optional[str] = Field(None, max_length=50)      
    start_date: str = Field(..., max_length=20)
    end_date: Optional[str] = Field(None, max_length=20)
    gpa: Optional[str] = Field(None, max_length=10)
    description: Optional[str] = None                             
    is_current: bool = False                                      
class EducationUpdate(BaseModel):
    # Accept frontend field names for updates
    institution_name: Optional[str] = Field(None, max_length=100)
    degree_title: Optional[str] = Field(None, max_length=100)
    field_of_study: Optional[str] = Field(None, max_length=100)
    education_type: Optional[str] = Field(None, max_length=20)
    degree_level: Optional[str] = Field(None, max_length=50)
    start_date: Optional[str] = Field(None, max_length=20)
    end_date: Optional[str] = Field(None, max_length=20)
    gpa: Optional[str] = Field(None, max_length=10)
    description: Optional[str] = None
    is_current: Optional[bool] = None

class Education(EducationBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True
# Personal Info Schemas
class PersonalInfoBase(BaseModel):
    full_name: str = Field(..., max_length=100)
    title: str = Field(..., max_length=100)
    bio: Optional[str] = None
    email: Optional[str] = Field(None, max_length=100)
    phone: Optional[str] = Field(None, max_length=20)
    location: Optional[str] = Field(None, max_length=100)
    linkedin: Optional[str] = Field(None, max_length=255)
    github: Optional[str] = Field(None, max_length=255)
    website: Optional[str] = Field(None, max_length=255)
    profile_image: Optional[str] = None

class PersonalInfoCreate(PersonalInfoBase):
    pass

class PersonalInfoUpdate(PersonalInfoBase):
    full_name: Optional[str] = Field(None, max_length=100)
    title: Optional[str] = Field(None, max_length=100)

class PersonalInfo(PersonalInfoBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
# Portfolio Summary Schema (for public view)
class PortfolioSummary(BaseModel):
    personal_info: Optional[PersonalInfo] = None
    skills: List[Skill]
    work_experiences: List[WorkExperience]
    projects: List[Project]
    education: List[Education]    
