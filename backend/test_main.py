from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_matches():
    """
    Vérifie que la route des matchs (publique) répond bien 200.
    """
    response = client.get("/api/matches")
    assert response.status_code == 200
    # On vérifie qu'on reçoit bien une liste (JSON)
    assert isinstance(response.json(), list)

def test_create_message_unauthorized():
    """
    TEST DE SÉCURITÉ :
    Vérifie qu'on ne peut PAS poster un message sans token.
    On s'attend à recevoir une erreur 401 (Unauthorized).
    """
    response = client.post("/api/messages", json={"content": "Tentative de hack"})
    assert response.status_code == 401