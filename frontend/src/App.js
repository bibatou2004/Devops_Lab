import React, { useEffect, useState } from 'react';
import './App.css';

function App() {
  const [messages, setMessages] = useState([]);
  const [matches, setMatches] = useState([]); // Nouvel état pour les scores
  const [newMessage, setNewMessage] = useState("");
  const [loading, setLoading] = useState(true);
  
  const API_URL = '/api';

  const fetchData = () => {
    // 1. Charger les messages
    fetch(`${API_URL}/messages`)
      .then(res => res.json())
      .then(data => setMessages(data))
      .catch(err => console.error("Erreur messages:", err));

    // 2. Charger les scores en direct
    fetch(`${API_URL}/matches`)
      .then(res => res.json())
      .then(data => {
        setMatches(data);
        setLoading(false);
      })
      .catch(err => console.error("Erreur matches:", err));
  };

  useEffect(() => {
    fetchData();
    // 3. AUTO-REFRESH : On recharge les données toutes les 3 secondes !
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

      {/* --- NOUVEAU : LE SCOREBOARD --- */}
      <section className="scoreboard">
        <h2>🔴 En Direct des Stades</h2>
        <div className="matches-grid">
          {matches.map(match => (
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
          ))}
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
          {messages.map((msg, index) => (
            <div key={index} className="news-card">
              <p>{msg}</p>
            </div>
          ))}
        </div>
      </main>
    </div>
  );
}

export default App;