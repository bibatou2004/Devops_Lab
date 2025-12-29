const express = require('express');
const { Pool } = require('pg');
const cors = require('cors');

const app = express();
app.use(cors());
app.use(express.json());

// Configuration de la connexion PostgreSQL
// Ces variables seront injectées par Kubernetes plus tard
const pool = new Pool({
  connectionString: process.env.DATABASE_URL || 'postgresql://postgres:footsecret@localhost:5432/footnews',
});

// Route de base pour vérifier que l'API tourne
app.get('/', (req, res) => {
  res.send('API Foot News en ligne ⚽');
});

// GET /news : Récupérer toutes les news
app.get('/news', async (req, res) => {
  try {
    // On crée la table si elle n'existe pas (pour simplifier le projet étudiant)
    await pool.query(`
      CREATE TABLE IF NOT EXISTS news (
        id SERIAL PRIMARY KEY,
        title VARCHAR(255) NOT NULL,
        content TEXT,
        date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
      )
    `);
    
    const result = await pool.query('SELECT * FROM news ORDER BY date DESC');
    res.json(result.rows);
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: 'Erreur serveur connexion DB' });
  }
});

// POST /news : Ajouter une news
app.post('/news', async (req, res) => {
  const { title, content } = req.body;
  if (!title || !content) {
    return res.status(400).json({ error: 'Titre et contenu requis' });
  }

  try {
    const result = await pool.query(
      'INSERT INTO news (title, content) VALUES ($1, $2) RETURNING *',
      [title, content]
    );
    res.status(201).json(result.rows[0]);
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: 'Impossible de sauvegarder la news' });
  }
});

// Export de l'app pour les tests (sans lancer le port)
module.exports = app;

// Lancement du serveur uniquement si ce fichier est exécuté directement
if (require.main === module) {
  const PORT = process.env.PORT || 5000;
  app.listen(PORT, () => {
    console.log(`Serveur Backend démarré sur le port ${PORT}`);
  });
}