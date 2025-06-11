import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture(scope="session")
def client():
    """
    Provides a reusable FastAPI test client for the entire test session.
    """
    return TestClient(app)
