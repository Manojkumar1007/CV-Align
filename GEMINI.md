# GEMINI.md

This file provides guidance to Gemini when working with code in this repository.

## Project Overview

CV-Align is a complete AI-powered CV evaluation system using RAG (Retrieval-Augmented Generation) with FastAPI backend and React frontend. The system automatically evaluates CVs against job descriptions and provides structured feedback.

## MongoDB Migration Plan

The user has requested to migrate the database from SQLite to MongoDB. This is a major undertaking that will require a significant rewrite of the backend. The following is a step-by-step plan for the migration:

1.  **Update Documentation**: Update the `GEMINI.md` file to reflect the new plan.
2.  **Install Dependencies**: Update `backend/requirements.txt` to remove `SQLAlchemy` and add `motor` and `pymongo`.
3.  **Update Configuration**: Update `backend/app/database/config.py` to connect to a MongoDB database using `motor`. Also update `backend/.env.example` with the new environment variables for MongoDB.
4.  **Rewrite Models**: Remove `backend/app/models/models.py` and `backend/app/models/schemas.py` and create new schemas in a new `schemas.py` file.
5.  **Rewrite Database Initialization**: Rewrite `backend/app/database/init_db.py` to create collections and insert the initial data into MongoDB.
6.  **Rewrite Authentication**: Rewrite the authentication logic in `backend/app/auth/auth.py` and `backend/app/routes/auth.py` to work with MongoDB.
7.  **Rewrite Job Management**: Rewrite the job management logic in `backend/app/routes/jobs.py` to work with MongoDB.
8.  **Rewrite User Management**: Rewrite the user management logic in `backend/app/routes/users.py` to work with MongoDB.
9.  **Rewrite Evaluation Management**: Rewrite the evaluation management logic in `backend/app/routes/evaluations.py` to work with MongoDB.
10. **Update `main.py`**: Update `backend/app/main.py` to remove the SQLAlchemy-specific code and add any necessary MongoDB-related setup.
11. **Update Documentation**: Update the `README.md` to reflect the changes.

## Standard Workflow
1. First think through the problem, read the codebase for relevant files, and write a plan to tasks/todo.md.
2. The plan should have a list of todo items that you can check off as you complete them
3. Before you begin working, check in with me and I will verify the plan.
4. Then, begin working on the todo items, marking them as complete as you go.
5. Please every step of the way just give me a high level explanation of what changes you made
6. Make every task and code change you do as simple as possible. We want to avoid making any massive or complex changes. Every change should impact as little code as possible. Everything is about simplicity.
7. Finally, add a review section to the todo.md file with a summary of the changes you made and any other relevant information.

## Architecture

### Backend (Python/FastAPI)
- **Location**: `backend/` directory
- **Entry Point**: `backend/app/main.py`
- **Database**: MongoDB with Motor
- **Authentication**: JWT-based with role-based access control
- **RAG Pipeline**: LangChain + FAISS vector database + Sentence Transformers
- **Document Processing**: PyPDF2, python-docx for CV parsing

### Frontend (React)
- **Location**: `frontend/` directory  
- **Entry Point**: `frontend/src/App.js`
- **Components**: All React components use .jsx extension (JavaScript, not TypeScript)
- **State Management**: Local state with hooks
- **Routing**: React Router for navigation
- **API**: Axios for HTTP requests

## Development Commands

### Backend Setup
```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python -m app.database.init_db
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

### Frontend Setup
```bash
cd frontend
npm install
npm start  # Runs on http://localhost:3000
```

### Testing
```bash
# Backend - Run all tests
cd backend && source venv/bin/activate && pytest

# Backend - Run simple tests only
cd backend && source venv/bin/activate && pytest tests/test_simple.py -v

# Frontend - Run all tests
cd frontend && npm test

# Frontend - Run simple tests only  
cd frontend && npm test -- --testPathPattern=simple.test.js --watchAll=false

# Run CI/CD pipeline locally (backend)
cd backend && python -m pytest tests/test_simple.py -v --tb=short

# Run CI/CD pipeline locally (frontend)
cd frontend && npm test -- --testPathPattern=simple.test.js --watchAll=false --verbose
```

## Key Configuration Files

- `backend/.env` - Backend environment variables
- `frontend/.env` - Frontend environment variables (API URLs)
- `backend/requirements.txt` - Python dependencies
- `frontend/package.json` - Node.js dependencies

## Database

- **Type**: MongoDB
- **Initialization**: Run `python -m app.database.init_db` to create collections and demo data
- **Demo Users**: 
  - Admin: admin@demo.com / admin123
  - Recruiter: recruiter@demo.com / recruiter123

## API Structure

All API endpoints are prefixed with `/api/`:
- `/api/auth/*` - Authentication (login, register, user info)
- `/api/jobs/*` - Job management (CRUD operations)
- `/api/evaluations/*` - CV evaluation and candidate management
- `/api/users/*` - User and company management

## File Organization

### Backend Structure
```
backend/app/
├── auth/           # JWT authentication logic
├── database/       # Database config and initialization
├── models/         # Pydantic schemas
├── routes/         # API endpoint handlers
├── services/       # Business logic (RAG engine, document processing)
└── main.py         # FastAPI application
```

### Frontend Structure
```
frontend/src/
├── components/     # Reusable React components (.jsx files)
├── pages/          # Page-level components (.jsx files)
├── services/       # API service functions
├── utils/          # Helper functions (auth, etc.)
└── App.js          # Main application component
```

## Important Development Notes

### Code Standards
- **React Components**: Always use .jsx extension, not .tsx (JavaScript, not TypeScript)
- **Python**: Follow PEP 8 standards
- **Authentication**: All protected routes require JWT token
- **Error Handling**: Comprehensive error handling in both frontend and backend

### RAG Pipeline
- **Embeddings**: Uses sentence-transformers/all-MiniLM-L6-v2 model
- **Vector Store**: FAISS for similarity search
- **Document Processing**: Extracts text from PDF/DOCX, structures into sections
- **Evaluation**: Scores based on skills (40%), experience (40%), education (20%)

### Security
- JWT tokens for authentication
- Role-based access control (admin, recruiter, hiring_manager)
- File upload validation and size limits
- CORS configured for local development

## Common Development Tasks

### Adding New API Endpoint
1. Create route handler in appropriate `backend/app/routes/` file
2. Add Pydantic schemas in `backend/app/models/schemas.py` if needed
3. Update main.py to include router if new file
4. Add corresponding frontend service function in `frontend/src/services/api.js`

### Adding New React Component
1. Create .jsx file in `frontend/src/components/` or `frontend/src/pages/`
2. Use functional components with hooks
3. Import and use in parent component
4. Add CSS file for styling if needed

### Database Schema Changes
1. Modify schemas in `backend/app/models/schemas.py`
2. For development, can regenerate database with init_db.py

## Troubleshooting

### Backend Issues
- **Import errors**: Ensure virtual environment is activated
- **Port in use**: Kill existing processes or change port with `pkill -f uvicorn`
- **Test failures**: Run simple tests first with `pytest tests/test_simple.py -v`

### Frontend Issues  
- **API calls fail**: Check backend is running on correct port
- **CORS errors**: Verify backend CORS configuration
- **Build errors**: Check all imports use correct file extensions (.jsx)
- **Test failures**: Run simple tests first with `npm test -- --testPathPattern=simple.test.js`

### RAG/ML Issues
- **Memory errors**: Reduce batch sizes or use smaller models
- **Slow processing**: Vector database may need optimization
- **Model download fails**: Check internet connection and disk space

### CI/CD Issues
- **GitHub Actions failing**: Check the Actions tab in GitHub repository
- **Test timeouts**: Simple tests should complete quickly; complex tests may timeout
- **Security scan failures**: Security scan is non-blocking and won't fail the build
- **Deployment failures**: Check artifact upload and ensure all files are committed

## Git Workflow

- **Main Branch**: `main`
- **Remote**: https://github.com/Manojkumar1007/CV-Align
- Standard feature branch workflow for development
- Both frontend and backend should be tested before committing

## CI/CD Pipeline

The project uses GitHub Actions for continuous integration:

### Workflows
- **CI Pipeline** (`.github/workflows/ci.yml`): Runs tests, linting, security scans
- **Deploy Pipeline** (`.github/workflows/deploy.yml`): Creates deployment artifacts

### Test Strategy
- **Simple Tests**: Basic functionality tests that should always pass
  - `backend/tests/test_simple.py` - Python imports and basic functionality
  - `frontend/src/__tests__/simple.test.js` - React imports and basic functionality
- **Integration Tests**: Full application tests with API endpoints
- **Security Scanning**: Trivy vulnerability scanner (non-blocking)

### Pipeline Jobs
1. **backend-tests**: Python testing with pytest
2. **frontend-tests**: React testing with Jest
3. **security-scan**: Vulnerability scanning (continue-on-error)
4. **lint-and-format**: Code quality checks (tolerant of warnings)
5. **integration-tests**: End-to-end API testing
6. **deploy**: Deployment artifact creation

### Environment Variables in CI
```bash
DATABASE_URL=mongodb://localhost:27017/
SECRET_KEY=test-secret-key-for-ci-that-is-long-enough-for-jwt
DEBUG=True
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
UPLOAD_DIR=./uploads
MAX_FILE_SIZE=10485760
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
VECTOR_DB_PATH=./vector_store
LOG_LEVEL=INFO
```

## Environment Variables

Keep sensitive data in .env files (not committed to git):
- Database URLs and credentials  
- JWT secret keys
- API keys (if using external LLM services)
- File upload configurations
