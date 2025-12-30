import React, { useEffect, useState } from 'react';
import './App.css';

function App() {
  const [news, setNews] = useState([]);
  // 1. On ajoute un état pour savoir si ça charge vraiment
  const [loading, setLoading] = useState(true); 
  const API_URL = '/api';

  useEffect(() => {
    fetch(`${API_URL}/news`)
      .then(res => res.json())
      .then(data => {
        setNews(data);
        setLoading(false); // 2. Succès : on arrête le chargement
      })
      .catch(err => {
        console.error("Erreur backend:", err);
        setLoading(false); // 3. Erreur : on arrête le chargement aussi (sinon ça bloque)
      });
  }, [API_URL]);

  return (
    <div className="app-container">
      <header className="app-header">
        <h1>⚽ Foot Reporting News</h1>
        <p>Toute l'actualité du ballon rond en direct</p>
      </header>

      <main className="news-container">
        {/* 4. On vérifie d'abord si ça charge */}
        {loading ? (
          <div className="loading">Chargement des news...</div>
        ) : (
          /* 5. Une fois chargé, on vérifie s'il y a des news OU si c'est vide */
          news.length > 0 ? (
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
          ) : (
            <div className="no-news">Aucune news disponible pour le moment.</div>
          )
        )}
      </main>
    </div>
  );
}

export default App;