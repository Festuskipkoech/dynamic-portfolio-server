import re
from typing import Optional
from datetime import datetime

def validate_email(email: str) -> bool:
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_url(url: str) -> bool:
    """Validate URL format"""
    pattern = r'^https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)$'
    return re.match(pattern, url) is not None

def validate_phone(phone: str) -> bool:
    """Validate phone number format"""
    # Remove common formatting characters
    cleaned = re.sub(r'[\s\-\(\)\+]', '', phone)
    # Check if it's all digits and reasonable length
    return cleaned.isdigit() and 10 <= len(cleaned) <= 15

def validate_date_format(date_str: str, format_str: str = "%Y-%m") -> bool:
    """Validate date string format"""
    try:
        datetime.strptime(date_str, format_str)
        return True
    except ValueError:
        return False

def validate_gpa(gpa: str) -> bool:
    """Validate GPA format (e.g., '3.85', '3.85/4.0')"""
    if not gpa:
        return True  # Optional field
    
    # Pattern for GPA like "3.85" or "3.85/4.0"
    pattern = r'^\d+(\.\d{1,2})?(/\d+(\.\d{1,2})?)?$'
    return re.match(pattern, gpa) is not None

def sanitize_filename(filename: str) -> str:
    """Sanitize filename for safe storage"""
    # Remove or replace unsafe characters
    sanitized = re.sub(r'[^\w\-_\.]', '_', filename)
    # Limit length
    return sanitized[:255]

def validate_skill_proficiency(proficiency: int) -> bool:
    """Validate skill proficiency level"""
    return 1 <= proficiency <= 5

def validate_difficulty_level(level: int) -> bool:
    """Validate project difficulty level"""
    return 1 <= level <= 5

def validate_relevance_score(score: int) -> bool:
    """Validate skill relevance score"""
    return 1 <= score <= 10