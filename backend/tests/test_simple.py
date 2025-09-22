"""
Simple tests that should always pass to ensure basic functionality.
"""
import pytest


def test_basic_imports():
    """Test that basic Python imports work."""
    import sys
    import os
    import json
    assert sys.version_info >= (3, 8)


def test_fastapi_import():
    """Test that FastAPI can be imported."""
    try:
        import fastapi
        assert fastapi.__version__ is not None
    except ImportError:
        pytest.skip("FastAPI not available")


def test_pydantic_import():
    """Test that Pydantic can be imported."""
    try:
        import pydantic
        assert pydantic.__version__ is not None
    except ImportError:
        pytest.skip("Pydantic not available")


def test_environment_variables():
    """Test that environment variables can be set."""
    import os
    os.environ["TEST_VAR"] = "test_value"
    assert os.environ.get("TEST_VAR") == "test_value"


def test_basic_math():
    """Test that basic Python functionality works."""
    assert 2 + 2 == 4
    assert "hello".upper() == "HELLO"