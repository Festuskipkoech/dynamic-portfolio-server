from fastapi import status

class PortfolioException(Exception):
    """Base exception for portfolio application"""
    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

class NotFoundError(PortfolioException):
    """Resource not found exception"""
    def __init__(self, resource: str, identifier: str = None):
        message = f"{resource} not found"
        if identifier:
            message += f" with id: {identifier}"
        super().__init__(message, status.HTTP_404_NOT_FOUND)

class ValidationError(PortfolioException):
    """Validation error exception"""
    def __init__(self, message: str):
        super().__init__(message, status.HTTP_400_BAD_REQUEST)

class AuthenticationError(PortfolioException):
    """Authentication error exception"""
    def __init__(self, message: str = "Authentication failed"):
        super().__init__(message, status.HTTP_401_UNAUTHORIZED)

class AuthorizationError(PortfolioException):
    """Authorization error exception"""
    def __init__(self, message: str = "Access denied"):
        super().__init__(message, status.HTTP_403_FORBIDDEN)

class FileError(PortfolioException):
    """File handling error exception"""
    def __init__(self, message: str):
        super().__init__(message, status.HTTP_400_BAD_REQUEST)

class SingletonViolationError(PortfolioException):
    """Singleton constraint violation exception"""
    def __init__(self, resource: str):
        message = f"Only one {resource} record is allowed"
        super().__init__(message, status.HTTP_409_CONFLICT)