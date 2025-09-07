from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from app.schemas.base import BaseEntitySchema

class PersonalInfoBase(BaseModel):
    full_name: str = Field(..., min_length=1, max_length=100)
    title: str = Field(..., min_length=1, max_length=100)
    bio: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, max_length=20)
    location: Optional[str] = Field(None, max_length=100)
    linkedin: Optional[str] = Field(None, max_length=255)
    github: Optional[str] = Field(None, max_length=255)
    website: Optional[str] = Field(None, max_length=255)

class PersonalInfoCreate(PersonalInfoBase):
    pass

class PersonalInfoUpdate(BaseModel):
    full_name: Optional[str] = Field(None, min_length=1, max_length=100)
    title: Optional[str] = Field(None, min_length=1, max_length=100)
    bio: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, max_length=20)
    location: Optional[str] = Field(None, max_length=100)
    linkedin: Optional[str] = Field(None, max_length=255)
    github: Optional[str] = Field(None, max_length=255)
    website: Optional[str] = Field(None, max_length=255)

class PersonalInfo(PersonalInfoBase, BaseEntitySchema):
    has_profile_image: bool = False