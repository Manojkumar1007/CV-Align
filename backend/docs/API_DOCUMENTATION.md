# CV-Align API Documentation

## Overview

CV-Align is an AI-powered CV evaluation system that provides comprehensive analysis and scoring of resumes against job descriptions using advanced RAG (Retrieval-Augmented Generation) technology.

## Base URL

- **Development**: `http://localhost:8000`
- **Production**: `https://api.cv-align.com`

## Interactive Documentation

- **Swagger UI**: `{BASE_URL}/docs`
- **ReDoc**: `{BASE_URL}/redoc`
- **OpenAPI Schema**: `{BASE_URL}/openapi.json`

## Authentication

All protected endpoints require JWT token authentication. Include the token in the `Authorization` header:

```
Authorization: Bearer <your-jwt-token>
```

### Token Expiration
- Access tokens expire after 30 minutes
- Password reset tokens expire after 30 minutes

## Error Handling

The API uses standardized error responses with consistent structure:

```json
{
  "error": "Error Type",
  "error_code": "ERROR_CODE",
  "message": "Detailed error message",
  "path": "/api/endpoint",
  "details": []  // Optional: validation errors
}
```

### Common Error Codes

- `VALIDATION_ERROR` - Input validation failed
- `AUTHENTICATION_ERROR` - Authentication required or failed
- `AUTHORIZATION_ERROR` - Insufficient permissions
- `NOT_FOUND_ERROR` - Resource not found
- `CONFLICT_ERROR` - Resource already exists
- `BUSINESS_LOGIC_ERROR` - Business rule violation
- `FILE_PROCESSING_ERROR` - File processing failed
- `AI_PROCESSING_ERROR` - AI/ML processing failed

## API Endpoints

### Authentication

#### Register User
```http
POST /api/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword123",
  "full_name": "John Doe",
  "role": "recruiter",
  "company_id": 1
}
```

**Response:**
```json
{
  "id": 1,
  "email": "user@example.com",
  "full_name": "John Doe",
  "role": "recruiter",
  "company_id": 1,
  "is_active": true,
  "created_at": "2023-01-01T00:00:00Z"
}
```

#### Login
```http
POST /api/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

**Response:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer"
}
```

#### Get Current User
```http
GET /api/auth/me
Authorization: Bearer <token>
```

**Response:**
```json
{
  "id": 1,
  "email": "user@example.com",
  "full_name": "John Doe",
  "role": "recruiter",
  "company_id": 1,
  "is_active": true,
  "created_at": "2023-01-01T00:00:00Z"
}
```

#### Password Reset Request
```http
POST /api/auth/password-reset-request
Content-Type: application/json

{
  "email": "user@example.com"
}
```

**Response:**
```json
{
  "message": "If this email exists in our system, you will receive a password reset link shortly."
}
```

#### Password Reset Confirmation
```http
POST /api/auth/password-reset-confirm
Content-Type: application/json

{
  "token": "reset-token-here",
  "new_password": "newpassword123"
}
```

**Response:**
```json
{
  "message": "Password has been successfully reset"
}
```

#### Change Password
```http
POST /api/auth/change-password
Authorization: Bearer <token>
Content-Type: application/json

{
  "current_password": "oldpassword123",
  "new_password": "newpassword123"
}
```

**Response:**
```json
{
  "message": "Password has been successfully changed"
}
```

### Job Management

#### Create Job
```http
POST /api/jobs/
Authorization: Bearer <token>
Content-Type: application/json

{
  "title": "Senior Software Engineer",
  "description": "We are looking for a senior software engineer with expertise in Python and FastAPI...",
  "requirements": "Bachelor's degree in Computer Science, 5+ years Python experience, FastAPI knowledge",
  "preferred_skills": "AWS, Docker, Kubernetes, React",
  "experience_level": "Senior"
}
```

**Response:**
```json
{
  "id": 1,
  "title": "Senior Software Engineer",
  "description": "We are looking for a senior software engineer...",
  "requirements": "Bachelor's degree in Computer Science...",
  "preferred_skills": "AWS, Docker, Kubernetes, React",
  "experience_level": "Senior",
  "company_id": 1,
  "created_by": 1,
  "is_active": true,
  "created_at": "2023-01-01T00:00:00Z",
  "updated_at": null
}
```

#### Get All Jobs
```http
GET /api/jobs/
Authorization: Bearer <token>
```

**Response:**
```json
[
  {
    "id": 1,
    "title": "Senior Software Engineer",
    "description": "We are looking for a senior software engineer...",
    "requirements": "Bachelor's degree in Computer Science...",
    "preferred_skills": "AWS, Docker, Kubernetes, React",
    "experience_level": "Senior",
    "company_id": 1,
    "created_by": 1,
    "is_active": true,
    "created_at": "2023-01-01T00:00:00Z",
    "updated_at": null
  }
]
```

#### Get Job by ID
```http
GET /api/jobs/{job_id}
Authorization: Bearer <token>
```

**Response:**
```json
{
  "id": 1,
  "title": "Senior Software Engineer",
  "description": "We are looking for a senior software engineer...",
  "requirements": "Bachelor's degree in Computer Science...",
  "preferred_skills": "AWS, Docker, Kubernetes, React",
  "experience_level": "Senior",
  "company_id": 1,
  "created_by": 1,
  "is_active": true,
  "created_at": "2023-01-01T00:00:00Z",
  "updated_at": null
}
```

#### Update Job
```http
PUT /api/jobs/{job_id}
Authorization: Bearer <token>
Content-Type: application/json

{
  "title": "Senior Software Engineer - Updated",
  "description": "Updated job description...",
  "requirements": "Updated requirements...",
  "preferred_skills": "Updated preferred skills...",
  "experience_level": "Senior"
}
```

**Response:**
```json
{
  "id": 1,
  "title": "Senior Software Engineer - Updated",
  "description": "Updated job description...",
  "requirements": "Updated requirements...",
  "preferred_skills": "Updated preferred skills...",
  "experience_level": "Senior",
  "company_id": 1,
  "created_by": 1,
  "is_active": true,
  "created_at": "2023-01-01T00:00:00Z",
  "updated_at": "2023-01-01T01:00:00Z"
}
```

#### Delete Job
```http
DELETE /api/jobs/{job_id}
Authorization: Bearer <token>
```

**Response:**
```json
{
  "message": "Job deleted successfully"
}
```

### CV Evaluations

#### Upload and Evaluate CV
```http
POST /api/evaluations/upload/{job_id}
Authorization: Bearer <token>
Content-Type: multipart/form-data

file: <cv-file.pdf>
candidate_name: "John Smith"          # Optional
candidate_email: "john@example.com"   # Optional
```

**Response:**
```json
{
  "message": "CV uploaded and evaluated successfully",
  "evaluation_id": 1,
  "overall_score": 85.5
}
```

#### Get All Evaluations for Job
```http
GET /api/evaluations/job/{job_id}
Authorization: Bearer <token>
```

**Response:**
```json
[
  {
    "id": 1,
    "job_id": 1,
    "candidate_name": "John Smith",
    "candidate_email": "john@example.com",
    "overall_score": 85.5,
    "skills_score": 88.0,
    "experience_score": 85.0,
    "education_score": 83.0,
    "feedback": "Strong candidate with excellent Python skills...",
    "strengths": "Excellent Python and FastAPI experience...",
    "weaknesses": "Could benefit from more DevOps experience...",
    "recommendations": "Consider for interview, focus on DevOps questions...",
    "cv_filename": "john_smith_cv.pdf",
    "created_at": "2023-01-01T00:00:00Z"
  }
]
```

#### Get Evaluation by ID
```http
GET /api/evaluations/{evaluation_id}
Authorization: Bearer <token>
```

**Response:**
```json
{
  "id": 1,
  "job_id": 1,
  "candidate_name": "John Smith",
  "candidate_email": "john@example.com",
  "overall_score": 85.5,
  "skills_score": 88.0,
  "experience_score": 85.0,
  "education_score": 83.0,
  "feedback": "Strong candidate with excellent Python skills...",
  "strengths": "Excellent Python and FastAPI experience...",
  "weaknesses": "Could benefit from more DevOps experience...",
  "recommendations": "Consider for interview, focus on DevOps questions...",
  "cv_filename": "john_smith_cv.pdf",
  "created_at": "2023-01-01T00:00:00Z"
}
```

#### Delete Evaluation
```http
DELETE /api/evaluations/{evaluation_id}
Authorization: Bearer <token>
```

**Response:**
```json
{
  "message": "Evaluation deleted successfully"
}
```

### User Management

#### Get Current User Profile
```http
GET /api/users/me
Authorization: Bearer <token>
```

**Response:**
```json
{
  "id": 1,
  "email": "user@example.com",
  "full_name": "John Doe",
  "role": "recruiter",
  "company_id": 1,
  "is_active": true,
  "created_at": "2023-01-01T00:00:00Z"
}
```

#### Get All Companies
```http
GET /api/users/companies
Authorization: Bearer <token>
```

**Response:**
```json
[
  {
    "id": 1,
    "name": "Tech Corp",
    "settings": null,
    "created_at": "2023-01-01T00:00:00Z"
  }
]
```

#### Create Company
```http
POST /api/users/companies
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "New Tech Company",
  "settings": "{\"theme\": \"dark\"}"
}
```

**Response:**
```json
{
  "id": 2,
  "name": "New Tech Company",
  "settings": "{\"theme\": \"dark\"}",
  "created_at": "2023-01-01T00:00:00Z"
}
```

## Role-Based Access Control

### Roles
- **admin**: Full system access
- **recruiter**: Can manage jobs and evaluate CVs
- **hiring_manager**: Can view jobs and evaluations, limited creation rights

### Permissions Matrix

| Endpoint | Admin | Recruiter | Hiring Manager |
|----------|-------|-----------|----------------|
| Create Job | ✓ | ✓ | ✓ |
| View Jobs | ✓ | ✓ | ✓ |
| Update Job | ✓ | ✓ | ✓ |
| Delete Job | ✓ | ✓ | ✗ |
| Upload CV | ✓ | ✓ | ✓ |
| View Evaluations | ✓ | ✓ | ✓ |
| Delete Evaluation | ✓ | ✓ | ✗ |
| Create Company | ✓ | ✗ | ✗ |

## File Upload Specifications

### Supported Formats
- PDF (.pdf)
- Microsoft Word (.docx)
- Plain Text (.txt)

### File Size Limits
- Maximum file size: 10MB
- Recommended size: Under 5MB for optimal processing

### Processing Notes
- Files are processed using AI-powered text extraction
- CV sections are automatically identified and parsed
- Candidate information is extracted when available
- Processing typically takes 2-5 seconds per file

## Rate Limiting

- **Authentication endpoints**: 5 requests per minute
- **File upload endpoints**: 10 requests per minute
- **General API endpoints**: 100 requests per minute

## Monitoring and Logging

### Request Logging
All API requests are logged with:
- Request method and path
- User ID and company ID
- Response status code
- Processing duration
- Error details (if applicable)

### Authentication Logging
Authentication events are tracked:
- Login attempts (success/failure)
- Token creation and verification
- Password reset requests
- Role-based access control events

### File Processing Logging
File operations are monitored:
- File upload events
- Processing duration
- AI evaluation metrics
- Error handling

## Development Setup

1. **Start the backend server:**
   ```bash
   cd backend
   source venv/bin/activate
   python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
   ```

2. **Access interactive documentation:**
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

3. **Test with demo data:**
   ```bash
   python -m app.database.init_db
   ```

   Demo users:
   - Admin: `admin@demo.com` / `admin123`
   - Recruiter: `recruiter@demo.com` / `recruiter123`

## Support

For technical support or questions about the API:
- **Email**: support@cv-align.com
- **Documentation**: https://docs.cv-align.com
- **Issues**: Report bugs via GitHub Issues

## Version History

- **v1.0.0**: Initial release with core CV evaluation functionality
- **v1.1.0**: Added comprehensive error handling and logging
- **v1.2.0**: Enhanced OpenAPI documentation and validation