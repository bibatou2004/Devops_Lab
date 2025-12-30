import os
import asyncio
import random
import psycopg2
from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from textblob import TextBlob

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"], # Important pour autoriser DELETE
    allow_headers=["*"],
)

# --- CONFIG DB ---
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "postgres")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASS", "password")

class Message(BaseModel):
    content: str

# --- SYSTEME EXPERT (DICTIONNAIRE DE SENTIMENTS) ---
# Pour pallier aux faiblesses de TextBlob en français sur les phrases courtes
FRENCH_SENTIMENTS = {
    "victoire": 0.9, "gagne": 0.8, "bravo": 0.8, "super": 0.8, "goooal": 1.0, "but": 0.7, "bien": 0.6,
    "nul": -0.8, "perdu": -0.9, "honte": -1.0, "triste": -0.7, "mauvais": -0.8, "defaite": -0.9, "ennui": -0.5
}

def analyze_sentiment(text):
    text_lower = text.lower()
    # 1. Approche par règles (Prioritaire)
    for word, score in FRENCH_SENTIMENTS.items():
        if word in text_lower:
            return score
    # 2. Approche IA (Fallback)
    return TextBlob(text).sentiment.polarity

# --- TÂCHE DE FOND (Simulation) ---
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
                    # Reset si score trop haut (pour éviter 150-140)
                    if h_score > 6 or a_score > 6:
                        cur.execute("UPDATE matches SET home_score=0, away_score=0 WHERE id=%s", (match_id,))
                    elif random.choice([True, False]):
                        cur.execute("UPDATE matches SET home_score = %s WHERE id = %s", (h_score + 1, match_id))
                    else:
                        cur.execute("UPDATE matches SET away_score = %s WHERE id = %s", (a_score + 1, match_id))
                    conn.commit()
                cur.close()
                conn.close()
            except: pass

def get_db_connection():
    try:
        return psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS)
    except: return None

@app.on_event("startup")
async def startup_event():
    # ... (Code d'initialisation identique à avant, on garde la structure)
    conn = get_db_connection()
    if conn:
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id SERIAL PRIMARY KEY, content TEXT NOT NULL, sentiment FLOAT DEFAULT 0.0
            )
        """)
        # Patch migration si besoin
        try:
            cur.execute("ALTER TABLE messages ADD COLUMN sentiment FLOAT DEFAULT 0.0")
            conn.commit()
        except: conn.rollback()

        cur.execute("""
            CREATE TABLE IF NOT EXISTS matches (
                id SERIAL PRIMARY KEY, home_team VARCHAR(50), away_team VARCHAR(50),
                home_score INT DEFAULT 0, away_score INT DEFAULT 0, is_live BOOLEAN DEFAULT TRUE
            )
        """)
        cur.execute("SELECT COUNT(*) FROM matches")
        if cur.fetchone()[0] == 0:
            matches_data = [("PSG", "Marseille"), ("Real Madrid", "Barcelone"), ("Bayern", "Dortmund")]
            for home, away in matches_data:
                cur.execute("INSERT INTO matches (home_team, away_team) VALUES (%s, %s)", (home, away))
        conn.commit()
        cur.close()
        conn.close()
    asyncio.create_task(simulate_live_scores())

# --- ROUTES ---

@app.get("/")
def read_root(): return {"status": "API Foot En Ligne"}

@app.get("/api/messages")
def get_messages():
    conn = get_db_connection()
    if not conn: return []
    cur = conn.cursor()
    
    # CORRECTION CRITIQUE : On sélectionne explicitement l'ID
    cur.execute("SELECT id, content, sentiment FROM messages ORDER BY id DESC")
    rows = cur.fetchall()
    
    cur.close()
    conn.close()
    
    # On renvoie un objet complet avec l'ID
    return [{"id": row[0], "content": row[1], "sentiment": row[2]} for row in rows]

@app.post("/api/messages")
def create_message(msg: Message):
    score = analyze_sentiment(msg.content) # Utilisation de notre fonction hybride
    conn = get_db_connection()
    if not conn: raise HTTPException(500, "DB Error")
    cur = conn.cursor()
    cur.execute("INSERT INTO messages (content, sentiment) VALUES (%s, %s)", (msg.content, score))
    conn.commit()
    cur.close()
    conn.close()
    return {"message": "OK"}

# NOUVELLE ROUTE : SUPPRESSION
@app.delete("/api/messages/{message_id}")
def delete_message(message_id: int):
    conn = get_db_connection()
    if not conn: raise HTTPException(500, "DB Error")
    cur = conn.cursor()
    cur.execute("DELETE FROM messages WHERE id = %s", (message_id,))
    conn.commit()
    cur.close()
    conn.close()
    return Response(status_code=204) # 204 = No Content (Succès sans contenu)

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