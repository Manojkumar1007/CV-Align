import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def get_auth_token():
    """Helper function to get authentication token."""
    response = client.post("/api/auth/login", json={
        "email": "admin@demo.com",
        "password": "admin123"
    })
    if response.status_code == 200:
        return response.json()["access_token"]
    return None


def test_get_jobs_without_auth():
    """Test getting jobs without authentication."""
    response = client.get("/api/jobs")
    assert response.status_code == 401


def test_get_jobs_with_auth():
    """Test getting jobs with authentication."""
    token = get_auth_token()
    if token:
        headers = {"Authorization": f"Bearer {token}"}
        response = client.get("/api/jobs/", headers=headers)
        assert response.status_code == 200
        assert isinstance(response.json(), list)


def test_create_job_without_auth():
    """Test creating job without authentication."""
    job_data = {
        "title": "Test Job",
        "description": "Test Description",
        "requirements": "Test Requirements",
        "experience_level": "entry"
    }
    response = client.post("/api/jobs", json=job_data)
    assert response.status_code == 401


def test_create_job_with_auth():
    """Test creating job with authentication."""
    token = get_auth_token()
    if token:
        headers = {"Authorization": f"Bearer {token}"}
        job_data = {
            "title": "Test Job",
            "description": "Test Description",
            "requirements": "Test Requirements",
            "experience_level": "entry"
        }
        response = client.post("/api/jobs/", json=job_data, headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Test Job"