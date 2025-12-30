import os
import asyncio
import random
import psycopg2
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from textblob import TextBlob  # <--- L'outil d'analyse de sentiment

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

# --- TÂCHE DE FOND (Simulation Scores) ---
async def simulate_live_scores():
    while True:
        await asyncio.sleep(10)
        conn = get_db_connection()
        if conn:
            try:
                cur = conn.cursor()
                cur.execute("SELECT id, home_score, away_score FROM matches WHERE is_live = TRUE ORDER BY RANDOM() LIMIT 1")
                match = cur.fetchone()
                if match:
                    match_id, h_score, a_score = match
                    if random.choice([True, False]):
                        cur.execute("UPDATE matches SET home_score = %s WHERE id = %s", (h_score + 1, match_id))
                    else:
                        cur.execute("UPDATE matches SET away_score = %s WHERE id = %s", (a_score + 1, match_id))
                    conn.commit()
                cur.close()
                conn.close()
            except Exception:
                pass

def get_db_connection():
    try:
        return psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS)
    except:
        return None

@app.on_event("startup")
async def startup_event():
    conn = get_db_connection()
    if conn:
        cur = conn.cursor()
        # On ajoute une colonne 'sentiment' si elle n'existe pas (Migration simple)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id SERIAL PRIMARY KEY,
                content TEXT NOT NULL,
                sentiment FLOAT DEFAULT 0.0
            )
        """)
        # Si la table existait déjà sans la colonne sentiment, on l'ajoute (Patch)
        try:
            cur.execute("ALTER TABLE messages ADD COLUMN sentiment FLOAT DEFAULT 0.0")
            conn.commit()
        except:
            conn.rollback() # La colonne existe déjà, on ignore

        cur.execute("""
            CREATE TABLE IF NOT EXISTS matches (
                id SERIAL PRIMARY KEY,
                home_team VARCHAR(50), away_team VARCHAR(50),
                home_score INT DEFAULT 0, away_score INT DEFAULT 0,
                is_live BOOLEAN DEFAULT TRUE
            )
        """)
        
        # Init matchs si vide
        cur.execute("SELECT COUNT(*) FROM matches")
        if cur.fetchone()[0] == 0:
            matches_data = [("PSG", "Marseille"), ("Real Madrid", "Barcelone"), ("Bayern", "Dortmund")]
            for home, away in matches_data:
                cur.execute("INSERT INTO matches (home_team, away_team) VALUES (%s, %s)", (home, away))
        
        conn.commit()
        cur.close()
        conn.close()
    asyncio.create_task(simulate_live_scores())

# --- ROUTES INTELLIGENTES ---

@app.get("/")
def read_root():
    return {"status": "API Foot En Ligne"}

@app.get("/api/messages")
def get_messages():
    conn = get_db_connection()
    if not conn: return []
    cur = conn.cursor()
    # On récupère le contenu ET le sentiment
    cur.execute("SELECT content, sentiment FROM messages ORDER BY id DESC")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    # On renvoie une liste d'objets structurés pour le frontend
    return [{"content": row[0], "sentiment": row[1]} for row in rows]

@app.post("/api/messages")
def create_message(msg: Message):
    # 1. ANALYSE NLP ICI 
    blob = TextBlob(msg.content)
    sentiment_score = blob.sentiment.polarity # Entre -1 (Négatif) et 1 (Positif)
    
    conn = get_db_connection()
    if not conn: raise HTTPException(500, "DB Error")
    cur = conn.cursor()
    cur.execute("INSERT INTO messages (content, sentiment) VALUES (%s, %s)", (msg.content, sentiment_score))
    conn.commit()
    cur.close()
    conn.close()
    return {"message": "OK", "sentiment": sentiment_score}

@app.get("/api/matches")
def get_matches():
    conn = get_db_connection()
    if not conn: return []
    cur = conn.cursor()
    cur.execute("SELECT id, home_team, away_team, home_score, away_score, is_live FROM matches ORDER BY id")
    rows = cur.fetchall()
    results = []
    for row in rows:
        results.append({"id": row[0], "home_team": row[1], "away_team": row[2], "home_score": row[3], "away_score": row[4], "is_live": row[5]})
    cur.close()
    conn.close()
    return results