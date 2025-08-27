from pydantic_settings import BaseSettings
from functools import lru_cache
import os

class Settings(BaseSettings):
    # Database
    database_url: str    
    # Security
    secret_key: str
    algorithm: str 
    access_token_expire_minutes: int = 60
    admin_password: str
    
    # File uploads 
    upload_dir: str ="uploads"
    max_file_size: int = 5 * 1024 * 1024
    allowed_extensions: set = {".jpg", ".jpeg", ".png", ".pdf", ".webp"}
    
    class Config:
        env_file = ".env"
        
@lru_cache()
def get_settings():
    return Settings()

# Create upload directory if it doe snot exists

settings = get_settings()
os.makedirs(settings.upload_dir, exist_ok=True)
os.makedirs(f"{settings.upload_dir}/projects", exist_ok=True)
os.makedirs(f"{settings.upload_dir}/certificates", exist_ok=True)
os.makedirs(f"{settings.upload_dir}/companies", exist_ok=True)