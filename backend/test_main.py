from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_root():
    """
    Vérifie que la route racine répond 200 (OK)
    et retourne le bon status.
    """
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    # CORRECTION ICI : On met le nouveau message attendu
    assert data["status"] == "API Foot En Ligne"