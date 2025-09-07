from fastapi import APIRouter, Depends, UploadFile, File
from app.schemas import PersonalInfo, PersonalInfoUpdate, ResponseSchema
from app.services import personal_info_service
from app.api.dependencies import get_admin_session

router = APIRouter()

@router.get("/personal-info", response_model=PersonalInfo)
def get_personal_info(admin_session: tuple = Depends(get_admin_session)):
    """Get personal information"""
    db = admin_session
    personal_info = personal_info_service.get_personal_info(db)
    
    if not personal_info:
        # Return empty structure if no personal info exists
        return PersonalInfo(
            id=0,
            full_name="",
            title="",
            bio="",
            email="",
            phone="",
            location="",
            linkedin="",
            github="",
            website="",
            has_profile_image=False,
            created_at="2025-01-01T00:00:00",
            updated_at="2025-01-01T00:00:00"
        )
    
    return personal_info

@router.put("/personal-info", response_model=PersonalInfo)
def update_personal_info(
    personal_info_update: PersonalInfoUpdate,
    admin_session: tuple = Depends(get_admin_session)
):
    """Update personal information"""
    db = admin_session
    return personal_info_service.create_or_update(db, personal_info_update)

@router.post("/personal-info/profile-image", response_model=ResponseSchema)
def upload_profile_image(
    file: UploadFile = File(...),
    admin_session: tuple = Depends(get_admin_session)
):
    """Upload profile image"""
    db = admin_session
    personal_info_service.upload_profile_image(db, file)
    return ResponseSchema(message="Profile image uploaded successfully")

@router.delete("/personal-info/profile-image", response_model=ResponseSchema)
def delete_profile_image(admin_session: tuple = Depends(get_admin_session)):
    """Delete profile image"""
    db = admin_session
    personal_info_service.delete_profile_image(db)
    return ResponseSchema(message="Profile image deleted successfully")