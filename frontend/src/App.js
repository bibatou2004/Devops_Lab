import React, { useEffect, useState } from 'react';

function App() {
  const [news, setNews] = useState([]);

  useEffect(() => {
    // L'URL pointera vers le service Kubernetes plus tard
    fetch('http://localhost:3000/news')
      .then(res => res.json())
      .then(data => setNews(data))
      .catch(err => console.error("Erreur backend:", err));
  }, []);

  return (
    <div style={{ padding: '20px', fontFamily: 'sans-serif' }}>
      <h1>⚽ Foot Reporting News</h1>
      {news.length === 0 ? <p>Aucune news pour le moment.</p> : (
        <ul>
          {news.map(item => (
            <li key={item.id}>
              <strong>{item.title}</strong> - {item.content}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default App;