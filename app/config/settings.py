from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import List

class Settings(BaseSettings):
    # Environment
    environment: str = "development"
    port: int = 8000
    
    # Database
    database_url: str
    
    # Security
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60
    admin_username: str
    admin_password: str
    
    # CORS
    allowed_origins: List[str] = ["http://localhost:3000"]
    
    # File handling
    max_file_size: int = 5 * 1024 * 1024  # 5MB
    allowed_image_types: List[str] = ["image/jpeg", "image/png", "image/webp"]
    allowed_document_types: List[str] = ["application/pdf"]
    
    class Config:
        env_file = ".env"
        
    @property
    def allowed_file_types(self) -> List[str]:
        return self.allowed_image_types + self.allowed_document_types

@lru_cache()
def get_settings():
    return Settings()