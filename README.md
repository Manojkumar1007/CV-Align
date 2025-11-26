# CV-Align - AI-Powered CV Evaluation System

A comprehensive web application that uses RAG (Retrieval-Augmented Generation) with machine learning to automatically evaluate CVs against job descriptions, providing structured feedback and relevance scoring to streamline the hiring process.

## Features

### Core Functionality
- **Automated CV Evaluation**: AI-powered analysis using dual model RAG pipeline with vector embeddings and LLM-based evaluation
- **Job Management**: Create and manage job postings with detailed requirements
- **Candidate Ranking**: Automatic ranking based on skills, experience, education, and soft skills match
- **Detailed Feedback**: Comprehensive evaluation with strengths, weaknesses, recommendations, and personalized insights
- **Multi-format Support**: Process PDF, DOCX, and TXT files

### User Management
- **Role-based Access Control**: Admin, Recruiter, and Hiring Manager roles
- **Multi-tenant Architecture**: Support for multiple companies
- **JWT Authentication**: Secure login and session management

### Technical Features
- **Dual Model RAG Engine**: Advanced document processing with FAISS vector database and LLM-based evaluation
- **Semantic Chunking**: Intelligent text segmentation using LangChain
- **Gemma Embeddings**: Powered by Google's embeddingGemma model via Ollama
- **LLM-based Scoring**: Enhanced evaluation using Gemma 4b for more nuanced scoring
- **Soft Skills Assessment**: AI-powered evaluation of interpersonal skills
- **Contextual Understanding**: Role-specific evaluation considering job context and industry requirements
- **Real-time Processing**: Fast CV evaluation (typically under 30 seconds)
- **Responsive Design**: Modern React frontend with intuitive UI
- **RESTful API**: Well-documented FastAPI backend

## Technology Stack

### Backend
- **FastAPI**: Modern Python web framework
- **SQLAlchemy**: Database ORM with SQLite
- **LangChain**: RAG pipeline implementation
- **FAISS**: Vector database for semantic search
- **Sentence Transformers**: Text embeddings
- **PyPDF2 & python-docx**: Document processing

### Frontend
- **React**: Modern JavaScript UI library
- **React Router**: Client-side routing
- **Axios**: HTTP client for API communication
- **CSS3**: Custom styling with responsive design

## Quick Start

### Prerequisites
- Python 3.12+
- Node.js 14+
- npm or yarn

**Note**: Use `python3` command on Mac/Linux and `python` command on Windows.

### Backend Setup

1. **Navigate to backend directory**:
   ```bash
   cd backend
   ```

2. **Create and activate virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\\Scripts\\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize database**:
   ```bash
   # Mac/Linux:
   python3 -m app.database.init_db
   
   # Windows:
   python -m app.database.init_db
   ```

5. **Start the server**:
   ```bash
   # Mac/Linux:
   python3 -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
   
   # Windows:
   python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
   ```

The backend will be available at `http://127.0.0.1:8000`

### Frontend Setup

1. **Navigate to frontend directory**:
   ```bash
   cd frontend
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Start the development server**:
   ```bash
   npm start
   ```

The frontend will be available at `http://localhost:3000`

## Demo Credentials

The system comes with pre-configured demo accounts:

- **Admin User**: admin@demo.com / admin123
- **Recruiter User**: recruiter@demo.com / recruiter123

## Project Structure

```
CV-Align/
├── backend/                     # Python/FastAPI backend
│   ├── app/
│   │   ├── auth/               # Authentication logic
│   │   ├── database/           # Database configuration
│   │   ├── models/             # SQLAlchemy models and Pydantic schemas
│   │   ├── routes/             # API route handlers
│   │   ├── services/           # Business logic (RAG, document processing)
│   │   └── main.py             # FastAPI application entry point
│   ├── database/               # SQLite database files
│   ├── uploads/                # Temporary file storage
│   ├── venv/                   # Python virtual environment
│   └── requirements.txt        # Python dependencies
├── frontend/                   # React frontend
│   ├── public/                 # Static files
│   ├── src/
│   │   ├── components/         # React components (.jsx files)
│   │   ├── pages/              # Page components
│   │   ├── services/           # API service calls
│   │   ├── utils/              # Helper functions
│   │   └── App.js              # Main App component
│   └── package.json            # Node.js dependencies
└── README.md                   # This file
```

## API Documentation

### Authentication Endpoints
- `POST /api/auth/login` - User login
- `POST /api/auth/register` - User registration
- `GET /api/auth/me` - Get current user info

### Job Management
- `POST /api/jobs` - Create new job
- `GET /api/jobs` - List all jobs
- `GET /api/jobs/{id}` - Get job details
- `PUT /api/jobs/{id}` - Update job
- `DELETE /api/jobs/{id}` - Delete job

### CV Evaluation
- `POST /api/evaluations/{job_id}/upload` - Upload and evaluate CV
- `GET /api/evaluations/{id}` - Get evaluation details
- `GET /api/evaluations/job/{job_id}/candidates` - Get job candidates
- `DELETE /api/evaluations/{id}` - Delete evaluation

### User Management
- `GET /api/users/me` - Get user profile
- `GET /api/users` - Get company users (admin only)
- `POST /api/users/companies` - Create company
- `GET /api/users/companies` - List companies

## Usage Guide

### 1. Create a Job
1. Login with demo credentials
2. Click "Create New Job" on the dashboard
3. Fill in job title, description, requirements, and preferred skills
4. Set experience level and save

### 2. Upload and Evaluate CVs
1. Navigate to a job's detail page
2. Click "Upload CV" button
3. Drag and drop or select a CV file (PDF, DOCX, or TXT)
4. Click "Upload and Evaluate" to process

### 3. Review Candidates
1. View ranked candidates on the job detail page
2. Click "View Details" for comprehensive evaluation
3. Review scores for skills, experience, and education
4. Read detailed feedback, strengths, and recommendations

## Configuration

### Environment Variables

**Backend** (backend/.env):
```env
DATABASE_URL=sqlite:///./database/cvalign.db
SECRET_KEY=your-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
UPLOAD_DIR=./uploads
MAX_FILE_SIZE=10485760
EMBEDDING_MODEL=embeddinggemma:300m
VECTOR_DB_PATH=./database/vector_store
DEBUG=True
LOG_LEVEL=INFO
```

**Frontend** (frontend/.env):
```env
REACT_APP_API_URL=http://127.0.0.1:8000/api
REACT_APP_UPLOAD_URL=http://127.0.0.1:8000
```

## Development

### Running Tests
```bash
# Backend tests
cd backend

# Mac/Linux:
source venv/bin/activate
python3 -m pytest

# Windows:
venv\Scripts\activate
python -m pytest

# Frontend tests
cd frontend
npm test
```

### Code Quality
The project follows Python PEP 8 and JavaScript ES6+ standards. Key patterns:
- React components use .jsx extension
- FastAPI with dependency injection
- SQLAlchemy models with proper relationships
- JWT-based authentication with role checking
- RAG pipeline with vector embeddings

## Production Deployment

### Environment Setup
1. Use PostgreSQL instead of SQLite for production
2. Configure proper secret keys and JWT settings
3. Set up file storage (AWS S3, Google Cloud Storage)
4. Use environment-specific configuration files

### Security Considerations
- Change default secret keys
- Use HTTPS in production
- Implement rate limiting
- Regular security audits
- Secure file upload validation

## Troubleshooting

### Common Issues

1. **Backend won't start**: Check Python version and virtual environment activation
2. **Database errors**: Ensure database directory exists and run init_db.py
3. **Frontend API calls fail**: Verify backend is running and CORS is configured
4. **File upload errors**: Check file size limits and supported formats
5. **Vector database issues**: Ensure sufficient disk space for embeddings

### Performance Optimization
- Use production-grade ASGI server (Gunicorn + Uvicorn)
- Implement Redis for caching
- Optimize vector database queries
- Use CDN for static assets

## Contributing

1. Fork the repository
2. Create a feature branch
3. Follow coding standards
4. Add tests for new functionality
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review API documentation
3. Create an issue on GitHub
4. Contact the development team

## Acknowledgments

- OpenAI for language model capabilities
- Hugging Face for transformer models
- FastAPI and React communities
- LangChain for RAG implementation