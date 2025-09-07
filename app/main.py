from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config.settings import get_settings
from app.config.database import engine
from app.models import Base
from app.api.v1.router import api_router
from app.core.middleware import add_security_headers

settings = get_settings()

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="Professional Portfolio API",
    description="Production-ready portfolio management system",
    version="2.0.0",
    docs_url="/docs" if settings.environment == "development" else None,
    redoc_url="/redoc" if settings.environment == "development" else None
)

# Security middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Custom security headers
add_security_headers(app)

# Include API router
app.include_router(api_router, prefix="/api/v1")

# Health check
@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "version": "2.0.0",
        "environment": settings.environment
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=settings.port,
        reload=settings.environment == "development"
    )