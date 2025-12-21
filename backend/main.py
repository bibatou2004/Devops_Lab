from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Autoriser le frontend à nous parler (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # En prod, on restreint ça, mais ok pour projet étudiant
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/data")
def get_data():
    # Ici, on irait chercher les infos dans la Base de Données
    return {"id": 1, "message": "Bonjour depuis le Backend Python!"}