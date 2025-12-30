import os
import time
import asyncio
import random
import psycopg2
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from typing import List

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- CONFIG DB ---
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "postgres")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASS", "password")

class Message(BaseModel):
    content: str

# Nouveau modèle pour les matchs
class Match(BaseModel):
    id: int
    home_team: str
    away_team: str
    home_score: int
    away_score: int
    is_live: bool

def get_db_connection():
    try:
        conn = psycopg2.connect(
            host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS
        )
        return conn
    except Exception as e:
        print(f"Erreur connexion BDD: {e}")
        return None

# --- TÂCHE DE FOND : SIMULATEUR DE BUTS ---
async def simulate_live_scores():
    """Cette fonction tourne en boucle à l'infini pour simuler des buts."""
    print("⚽ Démarrage du simulateur de scores...")
    while True:
        await asyncio.sleep(10) # Pause de 10 secondes
        conn = get_db_connection()
        if conn:
            try:
                cur = conn.cursor()
                # On choisit un match au hasard qui est en direct
                cur.execute("SELECT id, home_score, away_score FROM matches WHERE is_live = TRUE ORDER BY RANDOM() LIMIT 1")
                match = cur.fetchone()
                
                if match:
                    match_id, h_score, a_score = match
                    # 50% de chance de marquer pour l'équipe domicile ou extérieur
                    if random.choice([True, False]):
                        new_score = h_score + 1
                        cur.execute("UPDATE matches SET home_score = %s WHERE id = %s", (new_score, match_id))
                        print(f"GOAL! Domicile marque pour le match {match_id}")
                    else:
                        new_score = a_score + 1
                        cur.execute("UPDATE matches SET away_score = %s WHERE id = %s", (new_score, match_id))
                        print(f"GOAL! Extérieur marque pour le match {match_id}")
                    conn.commit()
                cur.close()
                conn.close()
            except Exception as e:
                print(f"Erreur simulation: {e}")

@app.on_event("startup")
async def startup_event():
    # 1. Initialisation de la BDD
    conn = get_db_connection()
    if conn:
        cur = conn.cursor()
        # Table Messages
        cur.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id SERIAL PRIMARY KEY,
                content TEXT NOT NULL
            )
        """)
        # Table Matches
        cur.execute("""
            CREATE TABLE IF NOT EXISTS matches (
                id SERIAL PRIMARY KEY,
                home_team VARCHAR(50),
                away_team VARCHAR(50),
                home_score INT DEFAULT 0,
                away_score INT DEFAULT 0,
                is_live BOOLEAN DEFAULT TRUE
            )
        """)
        
        # 2. Création de faux matchs si la table est vide
        cur.execute("SELECT COUNT(*) FROM matches")
        if cur.fetchone()[0] == 0:
            print("Initialisation des matchs de démo...")
            matches_data = [
                ("PSG", "Marseille"),
                ("Real Madrid", "Barcelone"),
                ("Bayern", "Dortmund")
            ]
            for home, away in matches_data:
                cur.execute("INSERT INTO matches (home_team, away_team) VALUES (%s, %s)", (home, away))
        
        conn.commit()
        cur.close()
        conn.close()
        
    # 3. Lancer la simulation en arrière-plan
    asyncio.create_task(simulate_live_scores())

# --- ROUTES API ---

@app.get("/")
def read_root():
    return {"status": "API Foot En Ligne"}

@app.get("/api/messages")
def get_messages():
    conn = get_db_connection()
    if not conn: return []
    cur = conn.cursor()
    cur.execute("SELECT content FROM messages ORDER BY id DESC")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [row[0] for row in rows]

@app.post("/api/messages")
def create_message(msg: Message):
    conn = get_db_connection()
    if not conn: raise HTTPException(500, "DB Error")
    cur = conn.cursor()
    cur.execute("INSERT INTO messages (content) VALUES (%s)", (msg.content,))
    conn.commit()
    cur.close()
    conn.close()
    return {"message": "OK"}

# NOUVELLE ROUTE : Récupérer les scores
@app.get("/api/matches")
def get_matches():
    conn = get_db_connection()
    if not conn: return []
    cur = conn.cursor()
    cur.execute("SELECT id, home_team, away_team, home_score, away_score, is_live FROM matches ORDER BY id")
    rows = cur.fetchall()
    results = []
    for row in rows:
        results.append({
            "id": row[0],
            "home_team": row[1],
            "away_team": row[2],
            "home_score": row[3],
            "away_score": row[4],
            "is_live": row[5]
        })
    cur.close()
    conn.close()
    return results