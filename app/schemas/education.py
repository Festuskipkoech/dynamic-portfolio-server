from pydantic import BaseModel, Field
from typing import Optional
from app.schemas.base import BaseEntitySchema

class EducationBase(BaseModel):
    institution: str = Field(..., min_length=1, max_length=100)
    degree: str = Field(..., min_length=1, max_length=100)
    field_of_study: Optional[str] = Field(None, max_length=100)
    education_type: str = Field(default="degree", max_length=20)
    degree_level: Optional[str] = Field(None, max_length=50)
    start_date: str = Field(..., min_length=1, max_length=20)
    end_date: Optional[str] = Field(None, max_length=20)
    gpa: Optional[str] = Field(None, max_length=10)
    honors: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = None
    is_current: bool = False
    is_certification: bool = False

class EducationCreate(EducationBase):
    pass

class EducationUpdate(BaseModel):
    institution: Optional[str] = Field(None, min_length=1, max_length=100)
    degree: Optional[str] = Field(None, min_length=1, max_length=100)
    field_of_study: Optional[str] = Field(None, max_length=100)
    education_type: Optional[str] = Field(None, max_length=20)
    degree_level: Optional[str] = Field(None, max_length=50)
    start_date: Optional[str] = Field(None, min_length=1, max_length=20)
    end_date: Optional[str] = Field(None, max_length=20)
    gpa: Optional[str] = Field(None, max_length=10)
    honors: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = None
    is_current: Optional[bool] = None
    is_certification: Optional[bool] = None

class Education(EducationBase, BaseEntitySchema):
    has_logo: bool = False
    has_certificate: bool = False