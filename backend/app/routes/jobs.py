from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.config import get_db
from app.models.models import Job, User
from app.models.schemas import JobCreate, Job as JobSchema
from app.auth.auth import get_current_user, require_role

router = APIRouter()

@router.post("/", response_model=JobSchema)
async def create_job(
    job_data: JobCreate,
    current_user: User = Depends(require_role(["admin", "recruiter", "hiring_manager"])),
    db: Session = Depends(get_db)
):
    db_job = Job(
        title=job_data.title,
        description=job_data.description,
        requirements=job_data.requirements,
        preferred_skills=job_data.preferred_skills,
        experience_level=job_data.experience_level,
        company_id=current_user.company_id,
        created_by=current_user.id
    )
    
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    
    return db_job

@router.get("/", response_model=List[JobSchema])
async def get_jobs(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    jobs = db.query(Job).filter(
        Job.company_id == current_user.company_id,
        Job.is_active == True
    ).all()
    return jobs

@router.get("/{job_id}", response_model=JobSchema)
async def get_job(
    job_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # First check if job exists at all
    job_exists = db.query(Job).filter(Job.id == job_id).first()
    if not job_exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Job with ID {job_id} does not exist"
        )
    
    # Check if user has access to this job (same company)
    job = db.query(Job).filter(
        Job.id == job_id,
        Job.company_id == current_user.company_id
    ).first()
    
    if not job:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"You do not have permission to access job {job_id}. Job belongs to company {job_exists.company_id}, but you belong to company {current_user.company_id}"
        )
    
    return job

@router.put("/{job_id}", response_model=JobSchema)
async def update_job(
    job_id: int,
    job_data: JobCreate,
    current_user: User = Depends(require_role(["admin", "recruiter", "hiring_manager"])),
    db: Session = Depends(get_db)
):
    job = db.query(Job).filter(
        Job.id == job_id,
        Job.company_id == current_user.company_id
    ).first()
    
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found"
        )
    
    job.title = job_data.title
    job.description = job_data.description
    job.requirements = job_data.requirements
    job.preferred_skills = job_data.preferred_skills
    job.experience_level = job_data.experience_level
    
    db.commit()
    db.refresh(job)
    
    return job

@router.delete("/{job_id}")
async def delete_job(
    job_id: int,
    current_user: User = Depends(require_role(["admin", "recruiter"])),
    db: Session = Depends(get_db)
):
    job = db.query(Job).filter(
        Job.id == job_id,
        Job.company_id == current_user.company_id
    ).first()
    
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found"
        )
    
    job.is_active = False
    db.commit()
    
    return {"message": "Job deleted successfully"}