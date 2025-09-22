import time
import logging
from typing import Callable
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from .logging_config import LogPatterns

logger = logging.getLogger("app.middleware")

class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Middleware for logging HTTP requests and responses"""
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        start_time = time.time()
        
        # Extract user info from request if available
        user_id = getattr(request.state, 'user_id', None)
        company_id = getattr(request.state, 'company_id', None)
        
        # Log the incoming request
        logger.info(LogPatterns.api_request(
            method=request.method,
            path=str(request.url.path),
            user_id=user_id,
            company_id=company_id
        ))
        
        # Process the request
        response = await call_next(request)
        
        # Calculate duration
        duration_ms = (time.time() - start_time) * 1000
        
        # Log the response
        logger.info(LogPatterns.api_response(
            method=request.method,
            path=str(request.url.path),
            status_code=response.status_code,
            duration_ms=duration_ms
        ))
        
        # Log slow requests as warnings
        if duration_ms > 1000:  # 1 second threshold
            logger.warning(f"Slow request: {request.method} {request.url.path} took {duration_ms:.2f}ms")
        
        return response

class UserContextMiddleware(BaseHTTPMiddleware):
    """Middleware to add user context to request state for logging"""
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Extract user information from JWT token if present
        authorization = request.headers.get("Authorization")
        if authorization and authorization.startswith("Bearer "):
            try:
                # This would be implemented with your JWT decoding logic
                # For now, we'll just set placeholder values
                request.state.user_id = None
                request.state.company_id = None
            except Exception as e:
                logger.debug(f"Failed to extract user context: {e}")
                request.state.user_id = None
                request.state.company_id = None
        
        return await call_next(request)