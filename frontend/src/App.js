import React, { useEffect, useState } from 'react';
import './App.css';

function App() {
  // On initialise avec des tableaux vides pour éviter le crash "undefined"
  const [messages, setMessages] = useState([]);
  const [matches, setMatches] = useState([]);
  const [newMessage, setNewMessage] = useState("");
  const [loading, setLoading] = useState(true);
  
  const API_URL = '/api';

  const fetchData = () => {
    // 1. Charger les messages (Sécurisé)
    fetch(`${API_URL}/messages`)
      .then(res => {
        if (!res.ok) throw new Error("Erreur réseau messages");
        return res.json();
      })
      .then(data => {
        // PROTECTION : Si ce n'est pas un tableau, on met un tableau vide
        if (Array.isArray(data)) {
          setMessages(data);
        } else {
          console.error("Format messages invalide:", data);
          setMessages([]);
        }
      })
      .catch(err => console.error("Erreur messages:", err));

    // 2. Charger les scores (Sécurisé)
    fetch(`${API_URL}/matches`)
      .then(res => {
        if (!res.ok) throw new Error("Erreur réseau matches");
        return res.json();
      })
      .then(data => {
        // PROTECTION CRITIQUE ICI : C'est souvent là que ça plante
        if (Array.isArray(data)) {
          setMatches(data);
        } else {
          console.error("Format matches invalide (Probablement une erreur 500):", data);
          setMatches([]); 
        }
        setLoading(false);
      })
      .catch(err => {
        console.error("Erreur matches:", err);
        setLoading(false);
      });
  };

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 3000);
    return () => clearInterval(interval);
  }, []);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!newMessage.trim()) return;
    fetch(`${API_URL}/messages`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ content: newMessage })
    }).then(() => {
      setNewMessage("");
      fetchData();
    });
  };

  return (
    <div className="app-container">
      <header className="app-header">
        <h1>⚽ Foot Reporting Live</h1>
      </header>

      {/* --- SCOREBOARD --- */}
      <section className="scoreboard">
        <h2>🔴 En Direct des Stades</h2>
        <div className="matches-grid">
          {/* PROTECTION : On vérifie match && match.id pour éviter les objets vides */}
          {matches.length > 0 ? (
            matches.map(match => (
              <div key={match.id} className="match-card">
                <div className="team home">{match.home_team}</div>
                <div className="score">
                  <span className="score-number">{match.home_score}</span>
                  <span className="separator">-</span>
                  <span className="score-number">{match.away_score}</span>
                </div>
                <div className="team away">{match.away_team}</div>
                {match.is_live && <div className="live-indicator">LIVE</div>}
              </div>
            ))
          ) : (
            <div className="no-matches">Chargement des scores ou aucun match en cours...</div>
          )}
        </div>
      </section>

      <main className="news-container">
        <h3>💬 Chat des Supporters</h3>
        <section className="input-section">
          <form onSubmit={handleSubmit} className="message-form">
            <input 
              type="text" 
              value={newMessage}
              onChange={(e) => setNewMessage(e.target.value)}
              placeholder="Commentez le match..."
              className="message-input"
            />
            <button type="submit" className="send-button">Envoyer</button>
          </form>
        </section>

        <div className="news-grid">
          {messages.length > 0 ? (
            messages.map((msg, index) => (
              <div key={index} className="news-card">
                <p>{msg}</p>
              </div>
            ))
          ) : (
            <div className="no-news">Aucun message.</div>
          )}
        </div>
      </main>
    </div>
  );
}

export default App;