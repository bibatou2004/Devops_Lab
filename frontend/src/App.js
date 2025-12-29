import React, { useEffect, useState } from 'react';
import './App.css'; // On s'assure d'importer le style

function App() {
  const [news, setNews] = useState([]);
  const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:3000';

  useEffect(() => {
    fetch(`${API_URL}/news`)
      .then(res => res.json())
      .then(data => setNews(data))
      .catch(err => console.error("Erreur backend:", err));
  }, [API_URL]);

  return (
    <div className="app-container">
      <header className="app-header">
        <h1>⚽ Foot Reporting News</h1>
        <p>Toute l'actualité du ballon rond en direct</p>
      </header>

      <main className="news-container">
        {news.length === 0 ? (
          <div className="loading">Chargement des news...</div>
        ) : (
          <div className="news-grid">
            {news.map(item => (
              <div key={item.id} className="news-card">
                <div className="card-header">
                  <span className="tag">Flash Info</span>
                </div>
                <div className="card-body">
                  <h3>{item.title}</h3>
                  <p>{item.content}</p>
                </div>
                <div className="card-footer">
                  <small>Publié le {new Date().toLocaleDateString()}</small>
                </div>
              </div>
            ))}
          </div>
        )}
      </main>
    </div>
  );
}

export default App;