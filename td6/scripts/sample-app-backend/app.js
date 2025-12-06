const express = require('express');
const app = express();
const PORT = 8080;

app.get('/', (req, res) => {
  res.json({
    text: 'backend microservice',
    timestamp: new Date().toISOString(),
    service: 'backend',
    replicas: 'scaled to 3'
  });
});

app.get('/health', (req, res) => {
  res.json({ status: 'healthy', service: 'backend' });
});

app.listen(PORT, () => {
  console.log(`Backend service running on port ${PORT}`);
});
