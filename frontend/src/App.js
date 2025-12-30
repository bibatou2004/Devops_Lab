import React, { useEffect, useState } from 'react';
import './App.css';

function App() {
  const [messages, setMessages] = useState([]);
  const [matches, setMatches] = useState([]);
  const [newMessage, setNewMessage] = useState("");
  const API_URL = '/api';

  const fetchData = () => {
    fetch(`${API_URL}/messages`)
      .then(res => res.ok ? res.json() : [])
      .then(data => {
        if(Array.isArray(data)) setMessages(data);
      })
      .catch(console.error);

    fetch(`${API_URL}/matches`)
      .then(res => res.ok ? res.json() : [])
      .then(data => {
        if(Array.isArray(data)) setMatches(data);
      })
      .catch(console.error);
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

  // Fonction pour transformer le score mathématique en Emoji
  const getSentimentEmoji = (score) => {
    if (score > 0.3) return "🤩"; // Très positif
    if (score > 0) return "🙂";   // Positif
    if (score < -0.3) return "🤬"; // Très négatif
    if (score < 0) return "🙁";   // Négatif
    return "😐"; // Neutre
  };

  return (
    <div className="app-container">
      <header className="app-header">
        <h1>⚽ Foot Data & NLP</h1>
        <p style={{color: '#bdc3c7', fontSize: '0.9rem'}}>Powered by DevOps Pipeline</p>
      </header>

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
        <h3>📢 Analyse de l'ambiance (IA)</h3>
        <section className="input-section">
          <form onSubmit={handleSubmit} className="message-form">
            <input 
              type="text" 
              value={newMessage}
              onChange={(e) => setNewMessage(e.target.value)}
              placeholder="Ex: Quel match incroyable ! ou L'arbitre est nul !"
              className="message-input"
            />
            <button type="submit" className="send-button">Analyser</button>
          </form>
        </section>

        <div className="news-grid">
          {messages.map((msg, index) => (
            <div key={index} className="news-card" style={{borderLeft: `5px solid ${msg.sentiment > 0 ? '#2ecc71' : (msg.sentiment < 0 ? '#e74c3c' : '#95a5a6')}`}}>
              <div className="card-body" style={{display:'flex', justifyContent:'space-between', alignItems:'center'}}>
                <p style={{margin:0}}>{msg.content}</p>
                <span style={{fontSize:'1.5rem'}} title={`Score NLP: ${msg.sentiment}`}>{getSentimentEmoji(msg.sentiment)}</span>
              </div>
            </div>
          ))}
        </div>
      </main>
    </div>
  );
}

export default App;