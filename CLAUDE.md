# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

CV-Align is a complete AI-powered CV evaluation system using RAG (Retrieval-Augmented Generation) with FastAPI backend and React frontend. The system automatically evaluates CVs against job descriptions and provides structured feedback.

## Architecture

### Backend (Python/FastAPI)
- **Location**: `backend/` directory
- **Entry Point**: `backend/app/main.py`
- **Database**: SQLite with SQLAlchemy ORM
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
source venv/bin/activate  # Windows: venv\\Scripts\\activate
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
# Backend
cd backend && source venv/bin/activate && pytest

# Frontend  
cd frontend && npm test
```

## Key Configuration Files

- `backend/.env` - Backend environment variables
- `frontend/.env` - Frontend environment variables (API URLs)
- `backend/requirements.txt` - Python dependencies
- `frontend/package.json` - Node.js dependencies

## Database

- **Type**: SQLite (development), easily upgradeable to PostgreSQL
- **Location**: `backend/database/cvalign.db`
- **Initialization**: Run `python -m app.database.init_db` to create tables and demo data
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
├── models/         # SQLAlchemy models and Pydantic schemas
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
1. Modify models in `backend/app/models/models.py`
2. Update corresponding Pydantic schemas
3. For production, use Alembic migrations
4. For development, can regenerate database with init_db.py

## Troubleshooting

### Backend Issues
- **Import errors**: Ensure virtual environment is activated
- **Database locked**: Stop all running instances, delete .db-journal files
- **Port in use**: Kill existing processes or change port

### Frontend Issues  
- **API calls fail**: Check backend is running on correct port
- **CORS errors**: Verify backend CORS configuration
- **Build errors**: Check all imports use correct file extensions (.jsx)

### RAG/ML Issues
- **Memory errors**: Reduce batch sizes or use smaller models
- **Slow processing**: Vector database may need optimization
- **Model download fails**: Check internet connection and disk space

## Git Workflow

- **Main Branch**: `main`
- **Remote**: https://github.com/Manojkumar1007/CV-Align
- Standard feature branch workflow for development
- Both frontend and backend should be tested before committing

## Environment Variables

Keep sensitive data in .env files (not committed to git):
- Database URLs and credentials  
- JWT secret keys
- API keys (if using external LLM services)
- File upload configurations