from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.config import get_db
from app.models.models import User, Company
from app.models.schemas import UserCreate, UserLogin, Token, User as UserSchema, PasswordResetRequest, PasswordResetConfirm, PasswordChangeRequest
from app.auth.auth import authenticate_user, create_access_token, get_password_hash, get_current_user, create_reset_token, verify_reset_token, send_reset_email, send_password_changed_notification

router = APIRouter()

@router.post("/register", response_model=UserSchema)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    company = db.query(Company).filter(Company.id == user_data.company_id).first()
    if not company:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid company ID"
        )
    
    hashed_password = get_password_hash(user_data.password)
    db_user = User(
        email=user_data.email,
        hashed_password=hashed_password,
        full_name=user_data.full_name,
        role=user_data.role,
        company_id=user_data.company_id
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user

@router.post("/login", response_model=Token)
async def login(user_credentials: UserLogin, db: Session = Depends(get_db)):
    user = authenticate_user(db, user_credentials.email, user_credentials.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User account is disabled"
        )
    
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserSchema)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    return current_user

@router.post("/logout")
async def logout():
    return {"message": "Successfully logged out"}

@router.post("/password-reset-request")
async def request_password_reset(
    password_reset: PasswordResetRequest,
    db: Session = Depends(get_db)
):
    """Request password reset - sends reset email if user exists"""
    user = db.query(User).filter(User.email == password_reset.email).first()
    
    # Always return success to prevent email enumeration attacks
    if user:
        reset_token = create_reset_token(user.email)
        send_reset_email(user.email, reset_token)
    
    return {"message": "If this email exists in our system, you will receive a password reset link shortly."}

@router.post("/password-reset-confirm")
async def confirm_password_reset(
    reset_data: PasswordResetConfirm,
    db: Session = Depends(get_db)
):
    """Confirm password reset with token and new password"""
    email = verify_reset_token(reset_data.token)
    
    if not email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired reset token"
        )
    
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Validate password strength
    if len(reset_data.new_password) < 8:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must be at least 8 characters long"
        )
    
    # Update password
    user.hashed_password = get_password_hash(reset_data.new_password)
    db.commit()
    
    # Send confirmation notification
    send_password_changed_notification(user.email)
    
    return {"message": "Password has been successfully reset"}

@router.post("/change-password")
async def change_password(
    password_change: PasswordChangeRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Change password for authenticated user"""
    # Verify current password
    if not authenticate_user(db, current_user.email, password_change.current_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current password is incorrect"
        )
    
    # Validate new password strength
    if len(password_change.new_password) < 8:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="New password must be at least 8 characters long"
        )
    
    # Check if new password is different from current
    if password_change.current_password == password_change.new_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="New password must be different from current password"
        )
    
    # Update password
    current_user.hashed_password = get_password_hash(password_change.new_password)
    db.commit()
    
    # Send confirmation notification
    send_password_changed_notification(current_user.email)
    
    return {"message": "Password has been successfully changed"}