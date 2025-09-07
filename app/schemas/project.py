from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, List
from app.schemas.base import BaseEntitySchema

# Project Category Schemas
class ProjectCategoryBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    description: Optional[str] = None

class ProjectCategoryCreate(ProjectCategoryBase):
    pass

class ProjectCategoryUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=50)
    description: Optional[str] = None

class ProjectCategory(ProjectCategoryBase, BaseEntitySchema):
    pass

# Project Image Schemas
class ProjectImageBase(BaseModel):
    caption: Optional[str] = Field(None, max_length=255)
    is_main: bool = False

class ProjectImageCreate(ProjectImageBase):
    pass

class ProjectImage(ProjectImageBase, BaseEntitySchema):
    project_id: int

# Project Schemas
class ProjectBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1)
    detailed_description: Optional[str] = None
    technologies: List[str] = Field(..., min_items=1)
    category_id: Optional[int] = None
    difficulty_level: int = Field(default=1, ge=1, le=5)
    status: str = Field(default="completed", max_length=20)
    is_deployed: bool = False
    live_url: Optional[HttpUrl] = None
    github_url: Optional[HttpUrl] = None
    client_name: Optional[str] = Field(None, max_length=100)
    start_date: Optional[str] = Field(None, max_length=20)
    end_date: Optional[str] = Field(None, max_length=20)
    featured: bool = False
    
    # Storytelling fields - NEW
    problem_statement: Optional[str] = None
    solution_approach: Optional[str] = None
    key_challenges: Optional[str] = None
    lessons_learned: Optional[str] = None
    results_achieved: Optional[str] = None

class ProjectCreate(ProjectBase):
    skill_ids: Optional[List[int]] = []  # Skills to associate with project

class ProjectUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, min_length=1)
    detailed_description: Optional[str] = None
    technologies: Optional[List[str]] = None
    category_id: Optional[int] = None
    difficulty_level: Optional[int] = Field(None, ge=1, le=5)
    status: Optional[str] = Field(None, max_length=20)
    is_deployed: Optional[bool] = None
    live_url: Optional[HttpUrl] = None
    github_url: Optional[HttpUrl] = None
    client_name: Optional[str] = Field(None, max_length=100)
    start_date: Optional[str] = Field(None, max_length=20)
    end_date: Optional[str] = Field(None, max_length=20)
    featured: Optional[bool] = None
    
    # Storytelling fields - NEW
    problem_statement: Optional[str] = None
    solution_approach: Optional[str] = None
    key_challenges: Optional[str] = None
    lessons_learned: Optional[str] = None
    results_achieved: Optional[str] = None
    
    skill_ids: Optional[List[int]] = None  # Skills to associate with project

class Project(ProjectBase, BaseEntitySchema):
    category: Optional[ProjectCategory] = None
    images: List[ProjectImage] = []
    skills: List["Skill"] = []
    has_case_study: bool = False

# Skill Assignment Schema
class ProjectSkillAssignment(BaseModel):
    skill_id: int
    relevance_score: int = Field(default=5, ge=1, le=10)