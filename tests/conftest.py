import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.database import init_db, seed_db
from pathlib import Path

@pytest.fixture(scope="session", autouse=True)
def setup_db():
    init_db()
    seed_db()

@pytest.fixture
def client():
    return TestClient(app)
