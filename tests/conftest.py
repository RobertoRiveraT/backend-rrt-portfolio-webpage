import pytest
from fastapi.testclient import TestClient
from app.main import app

from dotenv import load_dotenv
## Load the .env.staging file
# load_dotenv(dotenv_path=".env.staging")
# Now the environment is loaded before any app import

@pytest.fixture(scope="session")
def client():
    """
    Provides a reusable FastAPI test client for the entire test session.
    """
    return TestClient(app)
