from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.database.config import get_db
from app.models.models import User
from app.utils.logging_config import get_logger, LogPatterns
import os
import secrets
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

logger = get_logger(__name__)

SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
RESET_TOKEN_EXPIRE_MINUTES = int(os.getenv("RESET_TOKEN_EXPIRE_MINUTES", "30"))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    
    try:
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        logger.debug(f"Access token created for user: {data.get('sub')}")
        return encoded_jwt
    except Exception as e:
        logger.error(f"Failed to create access token: {e}")
        raise

def verify_token(token: str) -> Optional[dict]:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        logger.debug(f"Token verified for user: {payload.get('sub')}")
        return payload
    except JWTError as e:
        logger.warning(f"Token verification failed: {e}")
        return None

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    token = credentials.credentials
    payload = verify_token(token)
    
    if payload is None:
        logger.warning("Token verification failed in get_current_user")
        raise credentials_exception
    
    email: str = payload.get("sub")
    if email is None:
        logger.warning("No email found in token payload")
        raise credentials_exception
    
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        logger.warning(f"User not found for email: {email}")
        raise credentials_exception
    
    logger.debug(f"User authenticated: {email}")
    return user

def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    user = db.query(User).filter(User.email == email).first()
    if not user:
        logger.info(LogPatterns.authentication_event("login", email, False))
        return None
    if not verify_password(password, user.hashed_password):
        logger.info(LogPatterns.authentication_event("login", email, False))
        return None
    
    logger.info(LogPatterns.authentication_event("login", email, True))
    return user

def require_role(allowed_roles: list):
    def role_checker(current_user: User = Depends(get_current_user)):
        if current_user.role not in allowed_roles:
            logger.warning(f"Access denied: user {current_user.email} (role: {current_user.role}) attempted to access resource requiring roles: {allowed_roles}")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions"
            )
        logger.debug(f"Access granted: user {current_user.email} (role: {current_user.role}) accessing resource")
        return current_user
    return role_checker

def create_reset_token(email: str) -> str:
    """Create a password reset token that expires in 30 minutes"""
    data = {
        "sub": email,
        "type": "password_reset",
        "exp": datetime.utcnow() + timedelta(minutes=RESET_TOKEN_EXPIRE_MINUTES)
    }
    try:
        token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
        logger.info(LogPatterns.authentication_event("password_reset_token_created", email, True))
        return token
    except Exception as e:
        logger.error(f"Failed to create reset token for {email}: {e}")
        raise

def verify_reset_token(token: str) -> Optional[str]:
    """Verify password reset token and return email if valid"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        token_type = payload.get("type")
        
        if email is None or token_type != "password_reset":
            logger.warning(f"Invalid reset token: email={email}, type={token_type}")
            return None
            
        logger.info(LogPatterns.authentication_event("password_reset_token_verified", email, True))
        return email
    except JWTError as e:
        logger.warning(f"Password reset token verification failed: {e}")
        return None

def send_reset_email(email: str, token: str) -> bool:
    """Send password reset email (mock implementation for development)"""
    try:
        # Mock email sending for development
        # In production, replace with actual email service (SendGrid, AWS SES, etc.)
        
        reset_url = f"http://localhost:3000/reset-password?token={token}"
        
        print(f"""
        ===== PASSWORD RESET EMAIL =====
        To: {email}
        Subject: Reset Your CV-Align Password
        
        Click the link below to reset your password:
        {reset_url}
        
        This link will expire in {RESET_TOKEN_EXPIRE_MINUTES} minutes.
        
        If you didn't request this reset, please ignore this email.
        =================================
        """)
        
        logger.info(f"Password reset email sent to {email}")
        return True
    except Exception as e:
        logger.error(f"Failed to send reset email to {email}: {e}")
        return False

def send_password_changed_notification(email: str) -> bool:
    """Send notification that password was successfully changed"""
    try:
        print(f"""
        ===== PASSWORD CHANGED NOTIFICATION =====
        To: {email}
        Subject: CV-Align Password Changed Successfully
        
        Your password has been successfully changed.
        
        If you didn't make this change, please contact support immediately.
        ==========================================
        """)
        
        logger.info(LogPatterns.authentication_event("password_changed", email, True))
        return True
    except Exception as e:
        logger.error(f"Failed to send password changed notification to {email}: {e}")
        return False