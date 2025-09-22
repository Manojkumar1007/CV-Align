from fastapi import HTTPException, status
from typing import Any, Dict, Optional

class CVAlignException(HTTPException):
    """Base exception class for CV-Align application"""
    
    def __init__(
        self,
        status_code: int,
        detail: str,
        error_code: Optional[str] = None,
        headers: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(status_code=status_code, detail=detail, headers=headers)
        self.error_code = error_code

class ValidationException(CVAlignException):
    """Exception for validation errors"""
    
    def __init__(self, detail: str, field: Optional[str] = None):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=detail,
            error_code="VALIDATION_ERROR"
        )
        self.field = field

class AuthenticationException(CVAlignException):
    """Exception for authentication errors"""
    
    def __init__(self, detail: str = "Authentication required"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            error_code="AUTHENTICATION_ERROR",
            headers={"WWW-Authenticate": "Bearer"}
        )

class AuthorizationException(CVAlignException):
    """Exception for authorization errors"""
    
    def __init__(self, detail: str = "Insufficient permissions"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail,
            error_code="AUTHORIZATION_ERROR"
        )

class NotFoundException(CVAlignException):
    """Exception for resource not found errors"""
    
    def __init__(self, detail: str, resource_type: Optional[str] = None):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail,
            error_code="NOT_FOUND_ERROR"
        )
        self.resource_type = resource_type

class ConflictException(CVAlignException):
    """Exception for conflict errors"""
    
    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=detail,
            error_code="CONFLICT_ERROR"
        )

class BusinessLogicException(CVAlignException):
    """Exception for business logic errors"""
    
    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail,
            error_code="BUSINESS_LOGIC_ERROR"
        )

class FileProcessingException(CVAlignException):
    """Exception for file processing errors"""
    
    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=detail,
            error_code="FILE_PROCESSING_ERROR"
        )

class AIProcessingException(CVAlignException):
    """Exception for AI/ML processing errors"""
    
    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail,
            error_code="AI_PROCESSING_ERROR"
        )