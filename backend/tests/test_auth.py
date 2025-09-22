import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_login_with_valid_credentials():
    """Test login with valid demo credentials."""
    response = client.post("/api/auth/login", json={
        "email": "admin@demo.com",
        "password": "admin123"
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_with_invalid_credentials():
    """Test login with invalid credentials."""
    response = client.post("/api/auth/login", json={
        "email": "invalid@email.com",
        "password": "wrongpassword"
    })
    assert response.status_code == 401


def test_login_missing_fields():
    """Test login with missing required fields."""
    response = client.post("/api/auth/login", json={
        "email": "admin@demo.com"
    })
    assert response.status_code == 422  # Unprocessable Entity


def test_protected_endpoint_without_token():
    """Test accessing protected endpoint without token."""
    response = client.get("/api/auth/me")
    assert response.status_code == 401


def test_protected_endpoint_with_token():
    """Test accessing protected endpoint with valid token."""
    # First, get a token
    login_response = client.post("/api/auth/login", json={
        "email": "admin@demo.com",
        "password": "admin123"
    })
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]
    
    # Use token to access protected endpoint
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/api/auth/me", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "admin@demo.com"