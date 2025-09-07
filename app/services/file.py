import magic
from typing import Tuple
from fastapi import UploadFile
from app.config.settings import get_settings
from app.core.exceptions import FileError

settings = get_settings()

class FileService:
    """Service for handling file uploads and validation"""
    
    @staticmethod
    def validate_file_type(file: UploadFile) -> str:
        """Validate file type and return MIME type"""
        # Read file content to check actual type
        content = file.file.read()
        file.file.seek(0)  # Reset file pointer
        
        if not content:
            raise FileError("Empty file")
        
        # Check file size
        if len(content) > settings.max_file_size:
            raise FileError(f"File too large. Maximum size: {settings.max_file_size} bytes")
        
        # Detect MIME type from content
        mime_type = magic.from_buffer(content, mime=True)
        
        # Validate against allowed types
        if mime_type not in settings.allowed_file_types:
            raise FileError(f"File type not allowed: {mime_type}")
        
        return mime_type
    
    @staticmethod
    def process_upload(file: UploadFile) -> Tuple[bytes, str]:
        """Process file upload and return content and MIME type"""
        mime_type = FileService.validate_file_type(file)
        
        # Read file content
        content = file.file.read()
        file.file.seek(0)  # Reset file pointer
        
        return content, mime_type
    
    @staticmethod
    def validate_image_file(file: UploadFile) -> Tuple[bytes, str]:
        """Validate and process image file"""
        content, mime_type = FileService.process_upload(file)
        
        if mime_type not in settings.allowed_image_types:
            raise FileError(f"Invalid image type: {mime_type}")
        
        return content, mime_type
    
    @staticmethod
    def validate_document_file(file: UploadFile) -> Tuple[bytes, str]:
        """Validate and process document file"""
        content, mime_type = FileService.process_upload(file)
        
        if mime_type not in settings.allowed_document_types:
            raise FileError(f"Invalid document type: {mime_type}")
        
        return content, mime_type