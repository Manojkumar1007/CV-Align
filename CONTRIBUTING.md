# Contributing to CV-Align

Thank you for your interest in contributing to CV-Align! This document provides guidelines and information for contributors.

## Table of Contents
- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Contributing Process](#contributing-process)
- [Coding Standards](#coding-standards)
- [Testing Guidelines](#testing-guidelines)
- [Submitting Changes](#submitting-changes)
- [Review Process](#review-process)

## Code of Conduct

By participating in this project, you agree to abide by our code of conduct:

- Use welcoming and inclusive language
- Be respectful of differing viewpoints and experiences
- Accept constructive criticism gracefully
- Focus on what is best for the community
- Show empathy towards other community members

## Getting Started

### Prerequisites
- Python 3.12+
- Node.js 18+
- Git
- Basic knowledge of FastAPI and React

### Areas for Contribution
- 🐛 **Bug Fixes**: Help identify and fix issues
- ✨ **New Features**: Implement new functionality
- 📖 **Documentation**: Improve docs and examples
- 🧪 **Testing**: Add test coverage
- 🎨 **UI/UX**: Enhance user experience
- ⚡ **Performance**: Optimize code and algorithms
- 🔒 **Security**: Identify and fix security issues

## Development Setup

### 1. Fork and Clone
```bash
git clone https://github.com/your-username/CV-Align.git
cd CV-Align
```

### 2. Backend Setup
```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # Windows: venv\\Scripts\\activate
pip install -r requirements.txt
python -m app.database.init_db
```

### 3. Frontend Setup
```bash
cd frontend
npm install
```

### 4. Environment Configuration
```bash
# Copy example environment files
cp .env.example .env
cp frontend/.env.example frontend/.env
```

### 5. Run Development Servers
```bash
# Terminal 1: Backend
cd backend
source venv/bin/activate
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

# Terminal 2: Frontend
cd frontend
npm start
```

## Contributing Process

### 1. Create an Issue
Before starting work, create an issue to discuss:
- Bug reports with reproduction steps
- Feature requests with use cases
- Questions about implementation

### 2. Branch Naming Convention
Create a descriptive branch name:
- `feature/add-cv-templates`
- `bugfix/fix-auth-redirect`
- `docs/update-api-guide`
- `refactor/improve-rag-pipeline`

### 3. Development Workflow
```bash
# Create and switch to feature branch
git checkout -b feature/your-feature-name

# Make your changes
# ... code, test, commit ...

# Push to your fork
git push origin feature/your-feature-name

# Create Pull Request on GitHub
```

## Coding Standards

### Python (Backend)
- Follow PEP 8 style guide
- Use type hints for function parameters and return values
- Write docstrings for classes and functions
- Maximum line length: 88 characters (Black formatter)
- Use meaningful variable and function names

**Example:**
```python
from typing import List, Optional
from fastapi import HTTPException

async def evaluate_cv(
    cv_text: str, 
    job_requirements: str
) -> Dict[str, float]:
    """
    Evaluate CV against job requirements using RAG pipeline.
    
    Args:
        cv_text: Extracted text from CV document
        job_requirements: Job requirements and description
        
    Returns:
        Dictionary containing evaluation scores
        
    Raises:
        HTTPException: If evaluation fails
    """
    # Implementation here
    pass
```

### JavaScript/React (Frontend)
- Use functional components with hooks
- All React components should use `.jsx` extension
- Use meaningful component and variable names
- Prefer const over let, avoid var
- Use async/await for asynchronous operations

**Example:**
```jsx
import React, { useState, useEffect } from 'react';
import { evaluationsAPI } from '../services/api';

function CandidateCard({ candidate, onViewDetails }) {
    const [loading, setLoading] = useState(false);
    
    const handleViewClick = async () => {
        setLoading(true);
        try {
            await onViewDetails(candidate.id);
        } catch (error) {
            console.error('Failed to load details:', error);
        } finally {
            setLoading(false);
        }
    };
    
    return (
        <div className="candidate-card">
            {/* Component JSX */}
        </div>
    );
}

export default CandidateCard;
```

### General Guidelines
- Write self-documenting code
- Add comments for complex logic
- Use consistent indentation (4 spaces for Python, 2 for JavaScript)
- Remove unused imports and variables
- Handle errors gracefully with appropriate user feedback

## Testing Guidelines

### Backend Testing
- Write unit tests for business logic
- Test API endpoints with different scenarios
- Test error handling and edge cases
- Use pytest for testing framework

**Example:**
```python
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "version": "1.0.0"}

def test_login_with_valid_credentials():
    response = client.post("/api/auth/login", json={
        "email": "admin@demo.com",
        "password": "admin123"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()
```

### Frontend Testing
- Test component rendering and user interactions
- Test API integration and error handling
- Use React Testing Library for component tests

**Example:**
```jsx
import { render, screen, fireEvent } from '@testing-library/react';
import Login from './Login';

test('renders login form', () => {
    render(<Login />);
    expect(screen.getByLabelText(/email/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/password/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /login/i })).toBeInTheDocument();
});

test('shows error message on failed login', async () => {
    render(<Login />);
    fireEvent.click(screen.getByRole('button', { name: /login/i }));
    
    expect(await screen.findByText(/login failed/i)).toBeInTheDocument();
});
```

### Running Tests
```bash
# Backend tests
cd backend
source venv/bin/activate
pytest

# Frontend tests
cd frontend
npm test

# Run tests with coverage
pytest --cov=app
npm test -- --coverage
```

## Submitting Changes

### Before Submitting
- [ ] Code follows project coding standards
- [ ] All tests pass locally
- [ ] New features include appropriate tests
- [ ] Documentation updated if needed
- [ ] No merge conflicts with main branch
- [ ] Commit messages are clear and descriptive

### Commit Message Format
Use conventional commit messages:
```
type(scope): description

body (optional)

footer (optional)
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Examples:**
```
feat(rag): add support for DOCX file processing

Add document processing support for Microsoft Word documents
using python-docx library. Includes text extraction and
section parsing for improved CV analysis.

Closes #123
```

```
fix(auth): resolve JWT token expiration issue

Fix issue where JWT tokens were not being properly validated
after expiration, causing authentication errors.

Fixes #456
```

### Pull Request Guidelines
1. **Create from feature branch**: Never submit from main branch
2. **Fill out PR template**: Provide all requested information
3. **Link related issues**: Reference issue numbers
4. **Add screenshots**: For UI changes
5. **Request specific reviewers**: Tag relevant maintainers
6. **Update documentation**: Include any necessary doc updates

## Review Process

### For Contributors
- Be patient and responsive to feedback
- Make requested changes promptly
- Ask questions if feedback is unclear
- Update your branch if requested
- Be open to suggestions and improvements

### Review Criteria
Reviewers will check for:
- ✅ **Functionality**: Does it work as intended?
- ✅ **Code Quality**: Is it well-written and maintainable?
- ✅ **Testing**: Are there adequate tests?
- ✅ **Documentation**: Is it properly documented?
- ✅ **Performance**: Does it meet performance requirements?
- ✅ **Security**: Are there any security concerns?
- ✅ **UI/UX**: Is the user experience appropriate?

### Review Timeline
- Initial review: Within 48 hours
- Follow-up reviews: Within 24 hours
- Merge timeline: After approval from at least one maintainer

## Getting Help

### Communication Channels
- **GitHub Issues**: For bugs and feature requests
- **GitHub Discussions**: For questions and ideas
- **Pull Request Comments**: For code-specific discussions

### Resources
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [LangChain Documentation](https://langchain.readthedocs.io/)
- [Project README](./README.md)

### Common Issues
1. **Virtual Environment Issues**: Ensure you're in the correct venv
2. **Database Connection**: Check database initialization
3. **CORS Errors**: Verify frontend/backend URL configuration
4. **Import Errors**: Check Python path and installed packages

## Recognition

Contributors will be recognized in:
- GitHub contributor graph
- Release notes for significant contributions
- Special thanks in documentation
- Potential invitation to maintainer team

## Questions?

If you have questions about contributing, please:
1. Check existing issues and documentation
2. Create a new issue with the "question" label
3. Join our discussions for broader topics

Thank you for contributing to CV-Align! 🚀