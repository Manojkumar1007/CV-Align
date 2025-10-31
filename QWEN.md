# QWEN.md

This file provides guidance to Qwen when working with code in this repository.

## Project Overview

CV-Align is a complete AI-powered CV evaluation system using RAG (Retrieval-Augmented Generation) with a FastAPI backend and React frontend. The system automatically evaluates CVs against job descriptions and provides structured feedback.

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



## Key Configuration Files

- `backend/.env` - Backend environment variables
- `frontend/.env` - Frontend environment variables (API URLs)
- `backend/requirements.txt` - Python dependencies
- `frontend/package.json` - Node.js dependencies

## Database

- **Type**: SQLite
- **Initialization**: Run `python -m app.database.init_db` to create the database and demo data.
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