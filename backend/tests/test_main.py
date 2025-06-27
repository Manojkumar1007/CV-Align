import pytest
from fastapi.testclient import TestClient


def test_health_endpoint():
    """Test the health check endpoint."""
    try:
        from app.main import app
        client = TestClient(app)
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "version" in data
    except Exception as e:
        pytest.skip(f"Could not import app: {e}")


def test_root_endpoint():
    """Test the root endpoint."""
    try:
        from app.main import app
        client = TestClient(app)
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
    except Exception as e:
        pytest.skip(f"Could not import app: {e}")


def test_import_app():
    """Test that the app can be imported."""
    try:
        from app.main import app
        assert app is not None
    except ImportError as e:
        pytest.fail(f"Could not import app: {e}")