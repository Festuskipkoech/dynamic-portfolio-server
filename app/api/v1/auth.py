from datetime import timedelta
from fastapi import APIRouter, HTTPException, status
from app.schemas.auth import AdminLogin, Token
from app.core.security import authenticate_admin, create_access_token
from app.config.settings import get_settings

settings = get_settings()
router = APIRouter()

@router.post("/login", response_model=Token)
def admin_login(credentials: AdminLogin):
    """Admin authentication endpoint"""
    if not authenticate_admin(credentials.username, credentials.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": credentials.username},
        expires_delta=access_token_expires
    )
    
    return Token(
        access_token=access_token,
        token_type="bearer",
        expires_in=settings.access_token_expire_minutes * 60  # Convert to seconds
    )