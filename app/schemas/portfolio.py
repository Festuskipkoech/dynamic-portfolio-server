from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Optional, List, TYPE_CHECKING
from app.schemas.base import BaseEntitySchema

# Import the models you need for forward references
if TYPE_CHECKING:
    from app.schemas.user import PersonalInfo
    from app.schemas.project import Project
    from app.schemas.education import Education

# Skill Schemas
class SkillBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    category: str = Field(..., min_length=1, max_length=50)
    proficiency: int = Field(..., ge=1, le=5)
    years_experience: float = Field(..., ge=0)

class SkillCreate(SkillBase):
    pass

class SkillUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    category: Optional[str] = Field(None, min_length=1, max_length=50)
    proficiency: Optional[int] = Field(None, ge=1, le=5)
    years_experience: Optional[float] = Field(None, ge=0)

class Skill(SkillBase, BaseEntitySchema):
    has_icon: bool = False

# Work Experience Schemas
class WorkExperienceBase(BaseModel):
    company: str = Field(..., min_length=1, max_length=100)
    position: str = Field(..., min_length=1, max_length=100)
    start_date: str = Field(..., min_length=1, max_length=20)
    end_date: Optional[str] = Field(None, max_length=20)
    description: str = Field(..., min_length=1)
    achievements: Optional[str] = None
    location: Optional[str] = Field(None, max_length=100)
    is_current: bool = False

class WorkExperienceCreate(WorkExperienceBase):
    pass

class WorkExperienceUpdate(BaseModel):
    company: Optional[str] = Field(None, min_length=1, max_length=100)
    position: Optional[str] = Field(None, min_length=1, max_length=100)
    start_date: Optional[str] = Field(None, min_length=1, max_length=20)
    end_date: Optional[str] = Field(None, max_length=20)
    description: Optional[str] = Field(None, min_length=1)
    achievements: Optional[str] = None
    location: Optional[str] = Field(None, max_length=100)
    is_current: Optional[bool] = None

class WorkExperience(WorkExperienceBase, BaseEntitySchema):
    has_logo: bool = False

# Combined Portfolio Summary
class PortfolioSummary(BaseModel):
    personal_info: Optional[PersonalInfo] = None
    skills: List[Skill] = []
    work_experiences: List[WorkExperience] = []
    projects: List[Project] = []
    education: List[Education] = []