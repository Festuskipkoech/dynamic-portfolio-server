from app.schemas.base import BaseSchema, BaseEntitySchema, ResponseSchema, ErrorSchema
from app.schemas.auth import AdminLogin, Token, TokenData
from app.schemas.user import PersonalInfo, PersonalInfoCreate, PersonalInfoUpdate
from app.schemas.education import Education, EducationCreate, EducationUpdate
from app.schemas.project import (
    Project, ProjectCreate, ProjectUpdate,
    ProjectCategory, ProjectCategoryCreate, ProjectCategoryUpdate,
    ProjectImage, ProjectImageCreate,
    ProjectSkillAssignment
)
from app.schemas.portfolio import (
    Skill, SkillCreate, SkillUpdate,
    WorkExperience, WorkExperienceCreate, WorkExperienceUpdate,
    PortfolioSummary
)

# Rebuild models to resolve forward references
PortfolioSummary.model_rebuild()

__all__ = [
    "BaseSchema", "BaseEntitySchema", "ResponseSchema", "ErrorSchema",
    "AdminLogin", "Token", "TokenData",
    "PersonalInfo", "PersonalInfoCreate", "PersonalInfoUpdate",
    "Skill", "SkillCreate", "SkillUpdate",
    "WorkExperience", "WorkExperienceCreate", "WorkExperienceUpdate",
    "Project", "ProjectCreate", "ProjectUpdate",
    "ProjectCategory", "ProjectCategoryCreate", "ProjectCategoryUpdate",
    "ProjectImage", "ProjectImageCreate", "ProjectSkillAssignment",
    "Education", "EducationCreate", "EducationUpdate",
    "PortfolioSummary"
]