from fastapi import APIRouter
from app.api.v1 import auth, public
from app.api.v1.admin import user, portfolio, projects, education

# Create main v1 router
api_router = APIRouter()

# Public routes
api_router.include_router(public.router, tags=["Public Portfolio"])

# Authentication routes
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])

# Admin routes
api_router.include_router(user.router, prefix="/admin", tags=["Admin - User"])
api_router.include_router(portfolio.router, prefix="/admin", tags=["Admin - Portfolio"])
api_router.include_router(projects.router, prefix="/admin", tags=["Admin - Projects"])
api_router.include_router(education.router, prefix="/admin", tags=["Admin - Education"])