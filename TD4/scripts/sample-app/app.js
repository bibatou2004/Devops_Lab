const express = require('express');
const app = express();

// Middleware
app.use(express.json());

// Routes
app.get('/', (req, res) => {
  res.send('Hello, World!');
});

app.get('/name/:name', (req, res) => {
  res.send(`Hello, ${req.params.name}!`);
});

app.get('/api/status', (req, res) => {
  res.json({ status: 'OK', timestamp: new Date() });
});

// EXERCICE 9 : Endpoint /add/:a/:b
app.get('/add/:a/:b', (req, res) => {
  const { a, b } = req.params;
  
  // Vérifier que a et b sont des nombres
  const numA = parseFloat(a);
  const numB = parseFloat(b);
  
  if (isNaN(numA) || isNaN(numB)) {
    return res.status(400).json({
      error: 'Both a and b must be valid numbers',
      received: { a, b }
    });
  }
  
  const sum = numA + numB;
  res.json({
    a: numA,
    b: numB,
    sum: sum
  });
});

module.exports = app;
