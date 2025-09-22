from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.config import get_db
from app.models.models import User, Company
from app.models.schemas import User as UserSchema, CompanyCreate, Company as CompanySchema
from app.auth.auth import get_current_user, require_role

router = APIRouter()

@router.get("/me", response_model=UserSchema)
async def get_current_user_profile(current_user: User = Depends(get_current_user)):
    return current_user

@router.get("/", response_model=List[UserSchema])
async def get_company_users(
    current_user: User = Depends(require_role(["admin"])),
    db: Session = Depends(get_db)
):
    users = db.query(User).filter(User.company_id == current_user.company_id).all()
    return users

@router.post("/companies", response_model=CompanySchema)
async def create_company(
    company_data: CompanyCreate,
    db: Session = Depends(get_db)
):
    existing_company = db.query(Company).filter(Company.name == company_data.name).first()
    if existing_company:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Company name already exists"
        )
    
    db_company = Company(
        name=company_data.name,
        settings=company_data.settings
    )
    
    db.add(db_company)
    db.commit()
    db.refresh(db_company)
    
    return db_company

@router.get("/companies", response_model=List[CompanySchema])
async def get_companies(db: Session = Depends(get_db)):
    companies = db.query(Company).all()
    return companies