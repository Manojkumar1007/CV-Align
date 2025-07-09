import logging
import logging.config
import os
from typing import Dict, Any

def setup_logging() -> None:
    """
    Configure logging for the application.
    
    Sets up structured logging with different levels for different components.
    """
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()
    
    logging_config: Dict[str, Any] = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "standard": {
                "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
            },
            "detailed": {
                "format": "%(asctime)s [%(levelname)s] %(name)s:%(lineno)d: %(message)s"
            },
            "json": {
                "format": "%(asctime)s %(name)s %(levelname)s %(message)s",
                "class": "pythonjsonlogger.jsonlogger.JsonFormatter"
            }
        },
        "handlers": {
            "default": {
                "level": log_level,
                "formatter": "standard",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout"
            },
            "file": {
                "level": log_level,
                "formatter": "detailed",
                "class": "logging.FileHandler",
                "filename": "logs/app.log",
                "mode": "a",
            },
            "error_file": {
                "level": "ERROR",
                "formatter": "detailed",
                "class": "logging.FileHandler",
                "filename": "logs/error.log",
                "mode": "a",
            }
        },
        "loggers": {
            "": {  # root logger
                "handlers": ["default", "file", "error_file"],
                "level": log_level,
                "propagate": False
            },
            "uvicorn": {
                "handlers": ["default"],
                "level": "INFO",
                "propagate": False
            },
            "uvicorn.error": {
                "handlers": ["default", "error_file"],
                "level": "INFO",
                "propagate": False
            },
            "uvicorn.access": {
                "handlers": ["default"],
                "level": "INFO",
                "propagate": False
            },
            "sqlalchemy.engine": {
                "handlers": ["default"],
                "level": "WARNING",
                "propagate": False
            },
            "app": {
                "handlers": ["default", "file"],
                "level": log_level,
                "propagate": False
            }
        }
    }
    
    # Create logs directory if it doesn't exist
    os.makedirs("logs", exist_ok=True)
    
    logging.config.dictConfig(logging_config)

def get_logger(name: str) -> logging.Logger:
    """
    Get a logger with the specified name.
    
    Args:
        name: The name of the logger (typically __name__)
        
    Returns:
        Configured logger instance
    """
    return logging.getLogger(name)

# Common logging patterns for the application
class LogPatterns:
    """Common logging patterns for consistent logging across the application"""
    
    @staticmethod
    def api_request(method: str, path: str, user_id: int = None, company_id: int = None) -> str:
        """Log API request pattern"""
        user_info = f"user_id={user_id}" if user_id else "anonymous"
        company_info = f"company_id={company_id}" if company_id else ""
        return f"API Request: {method} {path} [{user_info}] [{company_info}]"
    
    @staticmethod
    def api_response(method: str, path: str, status_code: int, duration_ms: float) -> str:
        """Log API response pattern"""
        return f"API Response: {method} {path} - {status_code} ({duration_ms:.2f}ms)"
    
    @staticmethod
    def database_operation(operation: str, table: str, record_id: int = None) -> str:
        """Log database operation pattern"""
        record_info = f"id={record_id}" if record_id else ""
        return f"Database {operation}: {table} [{record_info}]"
    
    @staticmethod
    def authentication_event(event: str, email: str, success: bool) -> str:
        """Log authentication event pattern"""
        status = "SUCCESS" if success else "FAILURE"
        return f"Auth {event}: {email} - {status}"
    
    @staticmethod
    def file_operation(operation: str, filename: str, size_bytes: int = None) -> str:
        """Log file operation pattern"""
        size_info = f"size={size_bytes} bytes" if size_bytes else ""
        return f"File {operation}: {filename} [{size_info}]"
    
    @staticmethod
    def ai_processing(operation: str, duration_ms: float, input_size: int = None) -> str:
        """Log AI processing pattern"""
        input_info = f"input_size={input_size}" if input_size else ""
        return f"AI {operation}: {duration_ms:.2f}ms [{input_info}]"