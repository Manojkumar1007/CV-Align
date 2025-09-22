from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.config import get_db
from app.models.models import Job, User
from app.models.schemas import JobCreate, Job as JobSchema
from app.auth.auth import get_current_user, require_role
from app.utils.exceptions import NotFoundException, AuthorizationException

router = APIRouter()

@router.post("/", response_model=JobSchema, summary="Create a new job posting")
async def create_job(
    job_data: JobCreate,
    current_user: User = Depends(require_role(["admin", "recruiter", "hiring_manager"])),
    db: Session = Depends(get_db)
):
    """
    Create a new job posting.
    
    - **title**: Job title
    - **description**: Detailed job description
    - **requirements**: Required skills and qualifications
    - **preferred_skills**: Optional/preferred skills
    - **experience_level**: Required experience level (e.g., "Junior", "Senior")
    
    Only admin, recruiter, and hiring_manager roles can create jobs.
    Job will be associated with the current user's company.
    """
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

@router.get("/", response_model=List[JobSchema], summary="Get all jobs for current user's company")
async def get_jobs(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Retrieve all active job postings for the current user's company.
    
    Returns only jobs that belong to the same company as the authenticated user.
    """
    jobs = db.query(Job).filter(
        Job.company_id == current_user.company_id,
        Job.is_active == True
    ).all()
    return jobs

@router.get("/{job_id}", response_model=JobSchema, summary="Get a specific job by ID")
async def get_job(
    job_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Retrieve a specific job posting by ID.
    
    - **job_id**: The ID of the job to retrieve
    
    User can only access jobs that belong to their company.
    """
    # First check if job exists at all
    job_exists = db.query(Job).filter(Job.id == job_id).first()
    if not job_exists:
        raise NotFoundException(f"Job with ID {job_id} does not exist", "job")
    
    # Check if user has access to this job (same company)
    job = db.query(Job).filter(
        Job.id == job_id,
        Job.company_id == current_user.company_id
    ).first()
    
    if not job:
        raise AuthorizationException(f"You do not have permission to access job {job_id}. Job belongs to company {job_exists.company_id}, but you belong to company {current_user.company_id}")
    
    return job

@router.put("/{job_id}", response_model=JobSchema, summary="Update a job posting")
async def update_job(
    job_id: int,
    job_data: JobCreate,
    current_user: User = Depends(require_role(["admin", "recruiter", "hiring_manager"])),
    db: Session = Depends(get_db)
):
    """
    Update an existing job posting.
    
    - **job_id**: The ID of the job to update
    - **job_data**: Updated job information
    
    Only admin, recruiter, and hiring_manager roles can update jobs.
    User can only update jobs that belong to their company.
    """
    job = db.query(Job).filter(
        Job.id == job_id,
        Job.company_id == current_user.company_id
    ).first()
    
    if not job:
        raise NotFoundException("Job not found", "job")
    
    job.title = job_data.title
    job.description = job_data.description
    job.requirements = job_data.requirements
    job.preferred_skills = job_data.preferred_skills
    job.experience_level = job_data.experience_level
    
    db.commit()
    db.refresh(job)
    
    return job

@router.delete("/{job_id}", summary="Delete a job posting")
async def delete_job(
    job_id: int,
    current_user: User = Depends(require_role(["admin", "recruiter"])),
    db: Session = Depends(get_db)
):
    """
    Delete a job posting (soft delete - marks as inactive).
    
    - **job_id**: The ID of the job to delete
    
    Only admin and recruiter roles can delete jobs.
    User can only delete jobs that belong to their company.
    
    Note: This is a soft delete - the job is marked as inactive
    but not permanently removed from the database.
    """
    job = db.query(Job).filter(
        Job.id == job_id,
        Job.company_id == current_user.company_id
    ).first()
    
    if not job:
        raise NotFoundException("Job not found", "job")
    
    job.is_active = False
    db.commit()
    
    return {"message": "Job deleted successfully"}