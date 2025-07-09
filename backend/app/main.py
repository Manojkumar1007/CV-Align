from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.database.config import create_tables
from app.routes import auth, jobs, evaluations, users
from app.utils.error_handlers import setup_exception_handlers
from app.utils.logging_config import setup_logging, get_logger
from app.utils.middleware import RequestLoggingMiddleware, UserContextMiddleware
import os
from dotenv import load_dotenv

load_dotenv()

# Setup logging
setup_logging()
logger = get_logger(__name__)

app = FastAPI(
    title="CV-Align API",
    description="""
    ## AI-Powered CV Evaluation System

    This API provides comprehensive CV evaluation capabilities using advanced AI and RAG (Retrieval-Augmented Generation) technology.

    ### Features
    - **Multi-company Support**: Isolated data and users per company
    - **Role-based Access Control**: Admin, Recruiter, and Hiring Manager roles
    - **AI-Powered Evaluation**: Advanced CV analysis using vector embeddings
    - **Document Processing**: Support for PDF and DOCX file formats
    - **Real-time Analysis**: Instant feedback and scoring

    ### Authentication
    All protected endpoints require JWT token authentication. Use the `/api/auth/login` endpoint to obtain a token.

    ### API Structure
    - **Authentication**: `/api/auth/*` - User registration, login, password management
    - **Jobs**: `/api/jobs/*` - Job posting and management
    - **Evaluations**: `/api/evaluations/*` - CV evaluation and candidate management
    - **Users**: `/api/users/*` - User and company management
    """,
    version="1.0.0",
    terms_of_service="https://example.com/terms/",
    contact={
        "name": "CV-Align Support",
        "email": "support@cv-align.com",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
    servers=[
        {
            "url": "http://localhost:8000",
            "description": "Development server"
        },
        {
            "url": "https://api.cv-align.com",
            "description": "Production server"
        }
    ]
)

# Add custom middleware
app.add_middleware(UserContextMiddleware)
app.add_middleware(RequestLoggingMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

upload_dir = os.getenv("UPLOAD_DIR", "./uploads")
os.makedirs(upload_dir, exist_ok=True)

app.mount("/uploads", StaticFiles(directory=upload_dir), name="uploads")

app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(jobs.router, prefix="/api/jobs", tags=["Jobs"])
app.include_router(evaluations.router, prefix="/api/evaluations", tags=["Evaluations"])
app.include_router(users.router, prefix="/api/users", tags=["Users"])

# Setup exception handlers
setup_exception_handlers(app)

@app.on_event("startup")
async def startup_event():
    logger.info("CV-Align API starting up...")
    create_tables()
    logger.info("CV-Align API startup completed")

@app.get("/")
async def root():
    return {"message": "CV-Align API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "1.0.0"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)