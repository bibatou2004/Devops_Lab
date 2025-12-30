import React, { useEffect, useState } from 'react';
import './App.css';

function App() {
  // --- ÉTATS GLOBAUX ---
  const [token, setToken] = useState(null);       // Token JWT de sécurité
  const [currentUser, setCurrentUser] = useState(null); // Infos de l'utilisateur (nom, role, id)
  
  // --- ÉTATS DE L'APP ---
  const [messages, setMessages] = useState([]);
  const [matches, setMatches] = useState([]);
  const [newMessage, setNewMessage] = useState("");
  
  // --- ÉTATS DU LOGIN ---
  const [isLoginView, setIsLoginView] = useState(true); // Basculer entre Login et Inscription
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [authError, setAuthError] = useState("");

  const API_URL = '/api';

  // --- 1. GESTION DE L'AUTHENTIFICATION ---

  const handleAuth = (e) => {
    e.preventDefault();
    setAuthError("");

    if (isLoginView) {
      // LOGIN (Récupération du Token)
      const formData = new FormData();
      formData.append('username', username);
      formData.append('password', password);

      fetch(`${API_URL}/token`, {
        method: 'POST',
        body: formData
      })
      .then(res => {
        if (!res.ok) throw new Error("Identifiants incorrects");
        return res.json();
      })
      .then(data => {
        setToken(data.access_token);
        // On décode le payload du token (méthode simple pour éviter une lib externe)
        const payload = JSON.parse(atob(data.access_token.split('.')[1]));
        setCurrentUser({ username: payload.sub, role: payload.role, id: payload.id });
      })
      .catch(err => setAuthError(err.message));

    } else {
      // INSCRIPTION (Register)
      fetch(`${API_URL}/api/register`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
      })
      .then(res => {
        if (!res.ok) throw new Error("Nom d'utilisateur déjà pris");
        return res.json();
      })
      .then(() => {
        setIsLoginView(true); // On bascule sur le login après succès
        setAuthError("Compte créé ! Connectez-vous.");
      })
      .catch(err => setAuthError(err.message));
    }
  };

  const logout = () => {
    setToken(null);
    setCurrentUser(null);
    setMessages([]); // On vide pour la sécurité
  };

  // --- 2. LOGIQUE DE DONNÉES (Se lance seulement si connecté) ---

  const fetchData = () => {
    // Note: /matches est public, /messages est public en lecture mais on a besoin du token pour POST/DELETE
    fetch(`${API_URL}/messages`)
      .then(res => res.json())
      .then(data => { if(Array.isArray(data)) setMessages(data); })
      .catch(console.error);

    fetch(`${API_URL}/matches`)
      .then(res => res.json())
      .then(data => { if(Array.isArray(data)) setMatches(data); })
      .catch(console.error);
  };

  useEffect(() => {
    if (token) {
      fetchData();
      const interval = setInterval(fetchData, 3000);
      return () => clearInterval(interval);
    }
  }, [token]);

  // --- 3. ACTIONS UTILISATEUR ---

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!newMessage.trim()) return;

    fetch(`${API_URL}/messages`, {
      method: 'POST',
      headers: { 
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}` // IMPORTANT: On envoie le token
      },
      body: JSON.stringify({ content: newMessage })
    }).then(() => {
      setNewMessage("");
      fetchData();
    });
  };

  const handleDelete = (id) => {
    fetch(`${API_URL}/messages/${id}`, {
      method: 'DELETE',
      headers: { 
        'Authorization': `Bearer ${token}` // Sécurité Backend
      },
    }).then(res => {
      if (res.ok) {
        setMessages(messages.filter(msg => msg.id !== id));
      } else {
        alert("Action non autorisée");
      }
    });
  };

  const getSentimentEmoji = (score) => {
    if (score >= 0.5) return "🤩";
    if (score > 0) return "🙂";
    if (score <= -0.5) return "🤬";
    if (score < 0) return "🙁";
    return "😐";
  };

  // --- 4. RENDU CONDITIONNEL (LOGIN vs APP) ---

  if (!token) {
    return (
      <div className="login-container">
        <div className="login-box">
          <h2>⚽ Foot Data</h2>
          <h3>{isLoginView ? "Connexion" : "Créer un compte"}</h3>
          {authError && <p style={{color:'red'}}>{authError}</p>}
          
          <form onSubmit={handleAuth}>
            <input 
              className="login-input" 
              type="text" placeholder="Nom d'utilisateur" 
              value={username} onChange={e => setUsername(e.target.value)} 
              required
            />
            <input 
              className="login-input" 
              type="password" placeholder="Mot de passe" 
              value={password} onChange={e => setPassword(e.target.value)} 
              required
            />
            <button type="submit" className="login-btn">
              {isLoginView ? "Se connecter" : "S'inscrire"}
            </button>
          </form>
          
          <span className="toggle-link" onClick={() => setIsLoginView(!isLoginView)}>
            {isLoginView ? "Pas encore de compte ? S'inscrire" : "J'ai déjà un compte"}
          </span>
        </div>
      </div>
    );
  }

  // Si Token existe -> On affiche l'App
  return (
    <div className="app-container">
      <header className="app-header">
        <h1>⚽ Foot Data & NLP</h1>
      </header>
      
      {/* Barre d'info utilisateur */}
      <div className="user-info-bar">
        <span>👤 {currentUser?.username} {currentUser?.role === 'admin' && <span className="role-badge">ADMIN</span>}</span>
        <button onClick={logout} className="logout-btn">Déconnexion</button>
      </div>

      <section className="scoreboard">
        <div className="matches-grid">
          {matches.map(match => (
            <div key={match.id} className="match-card">
              <div className="team home">{match.home_team}</div>
              <div className="score">{match.home_score} - {match.away_score}</div>
              <div className="team away">{match.away_team}</div>
              {match.is_live && <div className="live-indicator">LIVE</div>}
            </div>
          ))}
        </div>
      </section>

      <main className="news-container">
        <h3>📢 Chat en direct</h3>
        <section className="input-section">
          <form onSubmit={handleSubmit} className="message-form">
            <input 
              type="text" 
              value={newMessage}
              onChange={(e) => setNewMessage(e.target.value)}
              placeholder="Ex: Quel but magnifique !"
              className="message-input"
            />
            <button type="submit" className="send-button">Envoyer</button>
          </form>
        </section>

        <div className="news-grid">
          {messages.map((msg, index) => (
            <div key={msg.id || index} className="news-card" style={{borderLeft: `5px solid ${msg.sentiment > 0 ? '#2ecc71' : (msg.sentiment < 0 ? '#e74c3c' : '#95a5a6')}`}}>
              
              {/* En-tête du message avec Nom + Bouton Supprimer conditionnel */}
              <div className="msg-header">
                <span>@{msg.username || 'Anonyme'}</span>
                
                {/* LOGIQUE D'AFFICHAGE DU BOUTON POUBELLE */}
                {/* Visible seulement si je suis Admin OU si c'est mon message */}
                {(currentUser.role === 'admin' || currentUser.username === msg.username) && (
                   <span 
                     style={{cursor:'pointer', color:'#e74c3c'}} 
                     onClick={() => handleDelete(msg.id)}
                     title="Supprimer"
                   >
                     🗑️
                   </span>
                )}
              </div>

              <div className="card-body" style={{display:'flex', alignItems:'center', gap:'10px'}}>
                 <span style={{fontSize:'1.5rem'}}>{getSentimentEmoji(msg.sentiment)}</span>
                 <p style={{margin:0, fontWeight:'500'}}>{msg.content}</p>
              </div>
            </div>
          ))}
        </div>
      </main>
    </div>
  );
}

export default App;