from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from .exceptions import CVAlignException
import logging
from typing import Union
import traceback

logger = logging.getLogger(__name__)

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle Pydantic validation errors"""
    logger.warning(f"Validation error on {request.method} {request.url}: {exc.errors()}")
    
    error_details = []
    for error in exc.errors():
        field = " -> ".join(str(loc) for loc in error["loc"])
        error_details.append({
            "field": field,
            "message": error["msg"],
            "type": error["type"]
        })
    
    return JSONResponse(
        status_code=422,
        content={
            "error": "Validation Error",
            "error_code": "VALIDATION_ERROR",
            "message": "Input validation failed",
            "details": error_details,
            "path": str(request.url)
        }
    )

async def cvalign_exception_handler(request: Request, exc: CVAlignException):
    """Handle custom CV-Align exceptions"""
    logger.error(f"CV-Align error on {request.method} {request.url}: {exc.detail}")
    
    content = {
        "error": "Application Error",
        "error_code": exc.error_code or "UNKNOWN_ERROR",
        "message": exc.detail,
        "path": str(request.url)
    }
    
    # Add additional context for specific exception types
    if hasattr(exc, 'field') and exc.field:
        content["field"] = exc.field
    if hasattr(exc, 'resource_type') and exc.resource_type:
        content["resource_type"] = exc.resource_type
    
    return JSONResponse(
        status_code=exc.status_code,
        content=content,
        headers=exc.headers
    )

async def http_exception_handler(request: Request, exc: Union[HTTPException, StarletteHTTPException]):
    """Handle standard HTTP exceptions"""
    logger.error(f"HTTP error on {request.method} {request.url}: {exc.detail}")
    
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": "HTTP Error",
            "error_code": f"HTTP_{exc.status_code}",
            "message": exc.detail,
            "path": str(request.url)
        }
    )

async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
    """Handle SQLAlchemy database errors"""
    logger.error(f"Database error on {request.method} {request.url}: {str(exc)}")
    
    if isinstance(exc, IntegrityError):
        return JSONResponse(
            status_code=409,
            content={
                "error": "Database Integrity Error",
                "error_code": "INTEGRITY_ERROR",
                "message": "Operation conflicts with existing data",
                "path": str(request.url)
            }
        )
    
    return JSONResponse(
        status_code=500,
        content={
            "error": "Database Error",
            "error_code": "DATABASE_ERROR",
            "message": "An error occurred while processing your request",
            "path": str(request.url)
        }
    )

async def general_exception_handler(request: Request, exc: Exception):
    """Handle any unhandled exceptions"""
    logger.error(f"Unhandled error on {request.method} {request.url}: {str(exc)}")
    logger.error(f"Traceback: {traceback.format_exc()}")
    
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "error_code": "INTERNAL_SERVER_ERROR",
            "message": "An unexpected error occurred",
            "path": str(request.url)
        }
    )

def setup_exception_handlers(app):
    """Setup all exception handlers for the FastAPI app"""
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(CVAlignException, cvalign_exception_handler)
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(StarletteHTTPException, http_exception_handler)
    app.add_exception_handler(SQLAlchemyError, sqlalchemy_exception_handler)
    app.add_exception_handler(Exception, general_exception_handler)