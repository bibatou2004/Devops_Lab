import React, { useEffect, useState } from 'react';
import './App.css';

function App() {
  // On stocke une liste de textes simples, pas d'objets complexes
  const [messages, setMessages] = useState([]);
  const [newMessage, setNewMessage] = useState(""); // Pour le formulaire d'ajout
  const [loading, setLoading] = useState(true);
  
  // URL relative : Nginx (dans Docker/K8s) se chargera de rediriger /api vers le backend
  const API_URL = '/api/messages';

  // Fonction pour charger les messages (READ)
  const fetchMessages = () => {
    setLoading(true);
    fetch(API_URL)
      .then(res => res.json())
      .then(data => {
        setMessages(data);
        setLoading(false);
      })
      .catch(err => {
        console.error("Erreur de connexion:", err);
        setLoading(false);
      });
  };

  // Charger les données au démarrage
  useEffect(() => {
    fetchMessages();
  }, []);

  // Fonction pour ajouter un message (WRITE)
  const handleSubmit = (e) => {
    e.preventDefault();
    if (!newMessage.trim()) return; // On n'envoie pas de vide

    fetch(API_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ content: newMessage }) // Format attendu par le Pydantic Python
    })
    .then(res => res.json())
    .then(() => {
      setNewMessage(""); // Vider le champ
      fetchMessages();   // Recharger la liste pour voir le nouveau message
    })
    .catch(err => console.error("Erreur d'envoi:", err));
  };

  return (
    <div className="app-container">
      <header className="app-header">
        <h1>⚽ Foot Reporting - Espace Supporter</h1>
        <p>Projet DevOps - Architecture Microservices</p>
      </header>

      <main className="news-container">
        
        {/* --- ZONE D'AJOUT (WRITE) --- */}
        <section className="input-section">
          <form onSubmit={handleSubmit} className="message-form">
            <input 
              type="text" 
              value={newMessage}
              onChange={(e) => setNewMessage(e.target.value)}
              placeholder="Écrire un message..."
              className="message-input"
            />
            <button type="submit" className="send-button">Envoyer</button>
          </form>
        </section>

        <hr className="divider"/>

        {/* --- ZONE D'AFFICHAGE (READ) --- */}
        {loading ? (
          <div className="loading">Chargement des messages...</div>
        ) : (
          messages.length > 0 ? (
            <div className="news-grid">
              {messages.map((msg, index) => (
                // On utilise l'index comme clé car c'est une liste simple
                <div key={index} className="news-card">
                  <div className="card-body">
                    <p>{msg}</p>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="no-news">Aucun message. Soyez le premier à poster !</div>
          )
        )}
      </main>
    </div>
  );
}

export default App;