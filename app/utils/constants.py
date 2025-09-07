# Project status options
PROJECT_STATUS_OPTIONS = [
    "completed",
    "ongoing", 
    "deployed",
    "archived",
    "maintenance"
]

# Education types
EDUCATION_TYPES = [
    "degree",
    "certification",
    "course",
    "bootcamp",
    "workshop"
]

# Degree levels
DEGREE_LEVELS = [
    "associate",
    "bachelor",
    "master", 
    "doctorate",
    "certificate"
]

# Common skill categories
SKILL_CATEGORIES = [
    "Frontend",
    "Backend", 
    "Database",
    "DevOps",
    "Mobile",
    "Design",
    "Testing",
    "Management",
    "Languages",
    "Frameworks",
    "Tools"
]

# Employment types
EMPLOYMENT_TYPES = [
    "full-time",
    "part-time",
    "contract",
    "freelance",
    "internship",
    "volunteer"
]

# File size limits (in bytes)
MAX_IMAGE_SIZE = 5 * 1024 * 1024  # 5MB
MAX_DOCUMENT_SIZE = 10 * 1024 * 1024  # 10MB

# Image dimensions for optimization
PROFILE_IMAGE_SIZE = (400, 400)
COMPANY_LOGO_SIZE = (200, 200) 
PROJECT_IMAGE_SIZE = (800, 600)
SKILL_ICON_SIZE = (64, 64)

# API response messages
SUCCESS_MESSAGES = {
    "created": "Resource created successfully",
    "updated": "Resource updated successfully", 
    "deleted": "Resource deleted successfully",
    "uploaded": "File uploaded successfully"
}

ERROR_MESSAGES = {
    "not_found": "Resource not found",
    "unauthorized": "Authentication required",
    "forbidden": "Access denied",
    "invalid_file": "Invalid file type or size",
    "validation_error": "Validation failed"
}