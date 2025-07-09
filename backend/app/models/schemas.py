from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime

class CompanyBase(BaseModel):
    name: str
    settings: Optional[str] = None

class CompanyCreate(CompanyBase):
    pass

class Company(CompanyBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    role: str
    company_id: int

class UserCreate(UserBase):
    password: str = Field(..., min_length=8, description="User password (minimum 8 characters)")

class User(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr = Field(..., description="User's email address")
    password: str = Field(..., description="User's password")
    
    class Config:
        schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "password123"
            }
        }

class Token(BaseModel):
    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field(..., description="Token type (always 'bearer')")
    
    class Config:
        schema_extra = {
            "example": {
                "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
                "token_type": "bearer"
            }
        }

class PasswordResetRequest(BaseModel):
    email: EmailStr

class PasswordResetConfirm(BaseModel):
    token: str
    new_password: str

class PasswordChangeRequest(BaseModel):
    current_password: str
    new_password: str

class JobBase(BaseModel):
    title: str = Field(..., description="Job title", example="Senior Software Engineer")
    description: str = Field(..., description="Detailed job description", example="We are looking for a senior software engineer...")
    requirements: str = Field(..., description="Required skills and qualifications", example="Bachelor's degree in Computer Science, 5+ years Python experience")
    preferred_skills: Optional[str] = Field(None, description="Optional/preferred skills", example="AWS, Docker, Kubernetes")
    experience_level: str = Field(..., description="Required experience level", example="Senior")

class JobCreate(JobBase):
    pass

class Job(JobBase):
    id: int
    company_id: int
    created_by: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True

class EvaluationBase(BaseModel):
    candidate_name: Optional[str] = None
    candidate_email: Optional[str] = None
    overall_score: float
    skills_score: float
    experience_score: float
    education_score: float
    feedback: str
    strengths: str
    weaknesses: str
    recommendations: str

class EvaluationCreate(EvaluationBase):
    job_id: int
    cv_filename: str
    cv_text: str

class Evaluation(EvaluationBase):
    id: int
    job_id: int
    cv_filename: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class CVUploadResponse(BaseModel):
    message: str
    evaluation_id: int
    overall_score: float