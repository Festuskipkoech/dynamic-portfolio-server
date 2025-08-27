from fastapi import FastAPI,WebSocket
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

# Import all modules
from .config import get_settings
from .database import engine
from .models import Base
from .routes import public_router, admin_router


# Initialize settings
settings = get_settings()

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="Dynamic Portfolio API",
    description="A comprehensive API for managing a dynamic portfolio with admin authentication",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files for serving uploaded content
app.mount("/uploads", StaticFiles(directory=settings.upload_dir), name="uploads")

# Include routers
app.include_router(public_router, prefix="/api/v1", tags=["Public Portfolio"])
app.include_router(admin_router, prefix="/api/v1", tags=["Admin"])

# Health check endpoint
@app.get("/")
def root():
    return {
        "message": "Dynamic Portfolio API is running!",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc",
        "public_endpoints": {
            "portfolio": "/api/v1/portfolio",
            "projects": "/api/v1/projects",
            "project_detail": "/api/v1/projects/{project_id}",
            "skills": "/api/v1/skills",
            "experience": "/api/v1/experience"
        },
        "admin_endpoints": {
            "login": "/api/v1/admin/login",
            "dashboard": "/api/v1/admin/dashboard"
        }
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy", 
        "database": "connected",
        "version": "1.0.0"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )