import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./test.db"

@pytest.fixture
def client():
    from app.main import app
    return TestClient(app)

def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_create_task(client):
    response = client.post(
        "/tasks",
        json={"title": "Test Task", "description": "Test description"}
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Test Task"

def test_list_tasks(client):
    response = client.get("/tasks")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_statistics(client):
    response = client.get("/stats")
    assert response.status_code == 200
    assert "total_tasks" in response.json()
