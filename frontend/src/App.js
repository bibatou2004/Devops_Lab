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
      .then(data => { if(Array.isArray(data)) setMessages(data); })
      .catch(console.error);

    fetch(`${API_URL}/matches`)
      .then(res => res.ok ? res.json() : [])
      .then(data => { if(Array.isArray(data)) setMatches(data); })
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

  // --- NOUVELLE FONCTION DE SUPPRESSION ---
  const handleDelete = (id) => {
    fetch(`${API_URL}/messages/${id}`, {
      method: 'DELETE',
    }).then(() => {
      // On retire le message de la liste locale tout de suite (effet instantané)
      setMessages(messages.filter(msg => msg.id !== id));
    });
  };

  const getSentimentEmoji = (score) => {
    if (score >= 0.5) return "🤩";
    if (score > 0) return "🙂";
    if (score <= -0.5) return "🤬";
    if (score < 0) return "🙁";
    return "😐";
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
              placeholder="Ex: Victoire ! ou Quel match nul..."
              className="message-input"
            />
            <button type="submit" className="send-button">Analyser</button>
          </form>
        </section>

        <div className="news-grid">
          {messages.map((msg, index) => (
            // Sécurité : Si pas d'ID, on utilise l'index (évite l'écran blanc)
            <div key={msg.id || index} className="news-card" style={{borderLeft: `5px solid ${msg.sentiment > 0 ? '#2ecc71' : (msg.sentiment < 0 ? '#e74c3c' : '#95a5a6')}`}}>
              <div className="card-body" style={{display:'flex', justifyContent:'space-between', alignItems:'center'}}>
                <div style={{display:'flex', alignItems:'center', gap:'10px'}}>
                   <span style={{fontSize:'1.5rem'}}>{getSentimentEmoji(msg.sentiment)}</span>
                   <p style={{margin:0, fontWeight:'500'}}>{msg.content}</p>
                </div>
                
                {/* CORRECTION : On n'affiche le bouton que si l'ID existe vraiment */}
                {msg.id && (
                  <button 
                    onClick={() => handleDelete(msg.id)}
                    style={{background:'transparent', border:'none', cursor:'pointer', fontSize:'1.2rem'}}
                    title="Supprimer le message"
                  >
                    🗑️
                  </button>
                )}
              </div>
            </div>
          ))}
        </div>
      </main>
    </div>
  );
}

export default App;