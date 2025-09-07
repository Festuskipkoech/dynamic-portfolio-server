from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.core.security import verify_token
from app.core.exceptions import AuthenticationError

security = HTTPBearer()

def get_current_admin(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> str:
    """Get current authenticated admin user"""
    username = verify_token(credentials.credentials)
    if username is None:
        raise AuthenticationError("Invalid authentication credentials")
    return username

def get_admin_session(
    current_admin: str = Depends(get_current_admin),
    db: Session = Depends(get_db)
) -> tuple[str, Session]:
    """Get admin user and database session"""
    return current_admin, db