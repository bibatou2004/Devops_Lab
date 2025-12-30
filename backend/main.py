import os
import asyncio
import random
import psycopg2
from datetime import datetime, timedelta
from typing import Optional, List

from fastapi import FastAPI, HTTPException, Response, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from textblob import TextBlob
from passlib.context import CryptContext
from jose import JWTError, jwt

app = FastAPI()

# --- SÉCURITÉ & CONFIGURATION ---
SECRET_KEY = "codeultrasecretdemonsite"  
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

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

# --- MODÈLES DE DONNÉES (Pydantic) ---

# Modèle pour l'inscription
class UserCreate(BaseModel):
    username: str
    password: str

# Modèle pour l'affichage utilisateur (sans mot de passe !)
class UserOut(BaseModel):
    id: int
    username: str
    role: str # 'user' ou 'admin'

# Modèle pour créer un message
class MessageCreate(BaseModel):
    content: str

# Modèle pour afficher un message (avec l'auteur)
class MessageOut(BaseModel):
    id: int
    content: str
    sentiment: float
    username: str  # Nom de l'auteur

class Token(BaseModel):
    access_token: str
    token_type: str

# --- FONCTIONS UTILITAIRES DB ---
def get_db_connection():
    try:
        return psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS)
    except: return None

# --- SYSTÈME DE SENTIMENTS (Ton code original) ---
FRENCH_SENTIMENTS = {
    "victoire": 0.9, "gagne": 0.8, "bravo": 0.8, "super": 0.8, "goooal": 1.0, "but": 0.7, "bien": 0.6,
    "nul": -0.8, "perdu": -0.9, "honte": -1.0, "triste": -0.7, "mauvais": -0.8, "defaite": -0.9, "ennui": -0.5
}

def analyze_sentiment(text):
    text_lower = text.lower()
    for word, score in FRENCH_SENTIMENTS.items():
        if word in text_lower: return score
    return TextBlob(text).sentiment.polarity

# --- OUTILS SÉCURITÉ ---
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# --- DÉPENDANCE : RÉCUPÉRER L'UTILISATEUR CONNECTÉ ---
# C'est cette fonction qui protège les routes
async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        role: str = payload.get("role")
        user_id: int = payload.get("id")
        if username is None: raise credentials_exception
        return {"username": username, "role": role, "id": user_id}
    except JWTError:
        raise credentials_exception

# --- STARTUP : MIGRATION DB ---
@app.on_event("startup")
async def startup_event():
    conn = get_db_connection()
    if conn:
        cur = conn.cursor()
        
        # 1. Table Utilisateurs
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                role VARCHAR(20) DEFAULT 'user'
            )
        """)
        
        # 2. Table Messages (modifiée pour inclure user_id)
        # Note: Si la table existe déjà sans user_id, cela pourrait causer une erreur.
        # Pour ce projet, le plus simple est de DROPPÉ la table manuellement ou de gérer la migration.
        # Ici, je recrée si elle n'existe pas, et j'ajoute la colonne si manquante.
        cur.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id SERIAL PRIMARY KEY, 
                content TEXT NOT NULL, 
                sentiment FLOAT DEFAULT 0.0,
                user_id INTEGER REFERENCES users(id) ON DELETE CASCADE
            )
        """)
        
        # 3. Table Matchs (Inchangé)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS matches (
                id SERIAL PRIMARY KEY, home_team VARCHAR(50), away_team VARCHAR(50),
                home_score INT DEFAULT 0, away_score INT DEFAULT 0, is_live BOOLEAN DEFAULT TRUE
            )
        """)

        # Création d'un Admin par défaut si aucun user n'existe
        cur.execute("SELECT COUNT(*) FROM users")
        if cur.fetchone()[0] == 0:
            admin_pass = get_password_hash("admin123")
            cur.execute("INSERT INTO users (username, password_hash, role) VALUES (%s, %s, %s)", 
                        ("admin", admin_pass, "admin"))

        # Création des matchs par défaut
        cur.execute("SELECT COUNT(*) FROM matches")
        if cur.fetchone()[0] == 0:
            matches_data = [("PSG", "Marseille"), ("Real Madrid", "Barcelone")]
            for home, away in matches_data:
                cur.execute("INSERT INTO matches (home_team, away_team) VALUES (%s, %s)", (home, away))

        conn.commit()
        cur.close()
        conn.close()
    asyncio.create_task(simulate_live_scores()) # Ta fonction de simulation (gardée en bas)

# --- ROUTE AUTHENTIFICATION ---

@app.post("/api/register")
def register(user: UserCreate):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        hashed_pw = get_password_hash(user.password)
        # Le premier inscrit devient admin (optionnel, pour faciliter tes tests) ou juste 'user'
        cur.execute("INSERT INTO users (username, password_hash, role) VALUES (%s, %s, 'user')", 
                    (user.username, hashed_pw))
        conn.commit()
    except psycopg2.IntegrityError:
        conn.rollback()
        raise HTTPException(status_code=400, detail="Username already registered")
    finally:
        cur.close()
        conn.close()
    return {"message": "User created successfully"}

@app.post("/token", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, username, password_hash, role FROM users WHERE username = %s", (form_data.username,))
    user = cur.fetchone()
    cur.close()
    conn.close()

    if not user or not verify_password(form_data.password, user[3]): # user[3] est le hash
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    # On met les infos utiles dans le token
    access_token = create_access_token(data={"sub": user[1], "role": user[3], "id": user[0]})
    return {"access_token": access_token, "token_type": "bearer"}

# --- ROUTES MESSAGES SÉCURISÉES ---

@app.get("/api/messages", response_model=List[MessageOut])
def get_messages():
    conn = get_db_connection()
    cur = conn.cursor()
    # Jointure pour récupérer le nom de l'auteur
    query = """
        SELECT m.id, m.content, m.sentiment, u.username 
        FROM messages m 
        JOIN users u ON m.user_id = u.id 
        ORDER BY m.id DESC
    """
    cur.execute(query)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [{"id": r[0], "content": r[1], "sentiment": r[2], "username": r[3]} for r in rows]

@app.post("/api/messages")
def create_message(msg: MessageCreate, current_user: dict = Depends(get_current_user)):
    # Ici, current_user est garanti d'exister grâce à Depends()
    score = analyze_sentiment(msg.content)
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO messages (content, sentiment, user_id) VALUES (%s, %s, %s)", 
                (msg.content, score, current_user['id']))
    conn.commit()
    cur.close()
    conn.close()
    return {"message": "Posted"}

@app.delete("/api/messages/{message_id}")
def delete_message(message_id: int, current_user: dict = Depends(get_current_user)):
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Vérification : Admin OU propriétaire du message
    cur.execute("SELECT user_id FROM messages WHERE id = %s", (message_id,))
    result = cur.fetchone()
    
    if not result:
        cur.close()
        raise HTTPException(404, "Message not found")
        
    author_id = result[0]
    
    if current_user['role'] == 'admin' or current_user['id'] == author_id:
        cur.execute("DELETE FROM messages WHERE id = %s", (message_id,))
        conn.commit()
        cur.close()
        conn.close()
        return Response(status_code=204)
    else:
        cur.close()
        conn.close()
        raise HTTPException(403, "Not authorized to delete this message")

# --- ROUTE PROMOTION ADMIN (Bonus) ---
@app.put("/api/users/{username}/promote")
def promote_user(username: str, current_user: dict = Depends(get_current_user)):
    if current_user['role'] != 'admin':
        raise HTTPException(403, "Only admins can promote users")
    
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("UPDATE users SET role = 'admin' WHERE username = %s", (username,))
    conn.commit()
    cur.close()
    conn.close()
    return {"message": f"{username} is now admin"}

# --- ROUTES MATCHS (Publiques) ---
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

# --- FONCTION SIMULATION (Ton code original) ---
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