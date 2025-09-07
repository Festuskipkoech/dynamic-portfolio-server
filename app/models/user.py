from sqlalchemy import Column, String, Text, Boolean, LargeBinary
from app.models.base import BaseModel

class PersonalInfo(BaseModel):
    __tablename__ = "personal_info"
    
    full_name = Column(String(100), nullable=False)
    title = Column(String(100), nullable=False)
    bio = Column(Text)
    email = Column(String(100))
    phone = Column(String(20))
    location = Column(String(100))
    linkedin = Column(String(255))
    github = Column(String(255))
    website = Column(String(255))
    
    # Profile image stored as binary data
    profile_image = Column(LargeBinary)
    profile_image_type = Column(String(50))  # Store MIME type
    
    def __repr__(self):
        return f"<PersonalInfo(name='{self.full_name}')>"

class Admin(BaseModel):
    __tablename__ = "admins"
    
    username = Column(String(50), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    
    def __repr__(self):
        return f"<Admin(username='{self.username}')>"