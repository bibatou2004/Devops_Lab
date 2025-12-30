import os
import psycopg2
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from typing import List

app = FastAPI()

# Configuration CORS (Identique à ta version)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- CONFIGURATION BASE DE DONNÉES ---
# On récupère les infos de connexion depuis les variables d'environnement (K8s)
# Si elles n'existent pas, on met des valeurs par défaut pour tester en local hors conteneur
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "postgres")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASS", "password")

# Modèle de données pour recevoir des infos du frontend (POST)
class Message(BaseModel):
    content: str

def get_db_connection():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASS
        )
        return conn
    except Exception as e:
        print(f"Erreur de connexion BDD : {e}")
        return None

# Initialisation de la BDD au démarrage
@app.on_event("startup")
def startup_event():
    conn = get_db_connection()
    if conn:
        try:
            cur = conn.cursor()
            # Création d'une table simple si elle n'existe pas
            cur.execute("""
                CREATE TABLE IF NOT EXISTS messages (
                    id SERIAL PRIMARY KEY,
                    content TEXT NOT NULL
                )
            """)
            conn.commit()
            cur.close()
            conn.close()
            print("Table 'messages' vérifiée/créée avec succès.")
        except Exception as e:
            print(f"Erreur lors de l'init BDD : {e}")

# --- ROUTES API (CRUD) ---

@app.get("/")
def read_root():
    return {"status": "API en ligne", "db_host": DB_HOST}

# READ : Lire tous les messages
@app.get("/api/messages")
def get_messages():
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Base de données inaccessible")
    
    cur = conn.cursor()
    cur.execute("SELECT content FROM messages;")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    
    # On transforme la liste de tuples [('msg1',), ('msg2',)] en liste simple ['msg1', 'msg2']
    return [row[0] for row in rows]

# WRITE : Ajouter un message
@app.post("/api/messages")
def create_message(msg: Message):
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Base de données inaccessible")
    
    try:
        cur = conn.cursor()
        cur.execute("INSERT INTO messages (content) VALUES (%s)", (msg.content,))
        conn.commit()
        cur.close()
        conn.close()
        return {"message": "Enregistré avec succès !"}
    except Exception as e:
        return {"error": str(e)}