import os
import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from app.database.config import get_db
from app.models.models import Evaluation, Job, User
from app.models.schemas import Evaluation as EvaluationSchema, CVUploadResponse
from app.auth.auth import get_current_user, require_role
from app.services.document_processor import DocumentProcessor
from app.services.rag_engine import RAGEngine

router = APIRouter()
document_processor = DocumentProcessor()
rag_engine = RAGEngine()

@router.post("/{job_id}/upload", response_model=CVUploadResponse)
async def upload_and_evaluate_cv(
    job_id: int,
    file: UploadFile = File(...),
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
    
    file_extension = os.path.splitext(file.filename)[1].lower()
    if file_extension not in document_processor.supported_formats:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported file format. Supported formats: {', '.join(document_processor.supported_formats)}"
        )
    
    max_file_size = int(os.getenv("MAX_FILE_SIZE", "10485760"))  # 10MB
    file_content = await file.read()
    if len(file_content) > max_file_size:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="File size too large"
        )
    
    upload_dir = os.getenv("UPLOAD_DIR", "./uploads")
    os.makedirs(upload_dir, exist_ok=True)
    
    file_id = str(uuid.uuid4())
    file_path = os.path.join(upload_dir, f"{file_id}_{file.filename}")
    
    with open(file_path, "wb") as buffer:
        buffer.write(file_content)
    
    try:
        cv_text = await document_processor.extract_text_from_file(file_path)
        cv_sections = document_processor.extract_cv_sections(cv_text)
        candidate_info = document_processor.extract_candidate_info(cv_text)
        
        evaluation_result = rag_engine.evaluate_cv_against_job(
            cv_sections, job.description, job.requirements
        )
        
        # Ensure candidate_name is not None
        candidate_name = candidate_info.get('name')
        if not candidate_name or candidate_name.strip() == '':
            candidate_name = 'Unknown Candidate'
        
        db_evaluation = Evaluation(
            job_id=job_id,
            candidate_name=candidate_name,
            candidate_email=candidate_info.get('email'),
            cv_filename=file.filename,
            cv_text=cv_text,
            overall_score=evaluation_result.overall_score,
            skills_score=evaluation_result.skills_score,
            experience_score=evaluation_result.experience_score,
            education_score=evaluation_result.education_score,
            feedback=evaluation_result.feedback,
            strengths='\n'.join(evaluation_result.strengths),
            weaknesses='\n'.join(evaluation_result.weaknesses),
            recommendations='\n'.join(evaluation_result.recommendations)
        )
        
        db.add(db_evaluation)
        db.commit()
        db.refresh(db_evaluation)
        
        return CVUploadResponse(
            message="CV uploaded and evaluated successfully",
            evaluation_id=db_evaluation.id,
            overall_score=db_evaluation.overall_score
        )
    
    except Exception as e:
        if os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing CV: {str(e)}"
        )
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)

@router.get("/{evaluation_id}", response_model=EvaluationSchema)
async def get_evaluation(
    evaluation_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    evaluation = db.query(Evaluation).join(Job).filter(
        Evaluation.id == evaluation_id,
        Job.company_id == current_user.company_id
    ).first()
    
    if not evaluation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Evaluation not found"
        )
    
    return evaluation

@router.get("/job/{job_id}/candidates", response_model=List[EvaluationSchema])
async def get_job_candidates(
    job_id: int,
    current_user: User = Depends(get_current_user),
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
    
    evaluations = db.query(Evaluation).filter(
        Evaluation.job_id == job_id
    ).order_by(Evaluation.overall_score.desc()).all()
    
    return evaluations

@router.delete("/{evaluation_id}")
async def delete_evaluation(
    evaluation_id: int,
    current_user: User = Depends(require_role(["admin", "recruiter"])),
    db: Session = Depends(get_db)
):
    evaluation = db.query(Evaluation).join(Job).filter(
        Evaluation.id == evaluation_id,
        Job.company_id == current_user.company_id
    ).first()
    
    if not evaluation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Evaluation not found"
        )
    
    db.delete(evaluation)
    db.commit()
    
    return {"message": "Evaluation deleted successfully"}