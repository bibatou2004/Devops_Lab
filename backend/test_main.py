from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_main():
    # Ce test vérifie que l'API répond bien 200 (OK)
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Status": "Active", "Version": "1.0.0"}