const express = require('express');
const http = require('http');
const app = express();
const PORT = 8080;

app.set('view engine', 'ejs');
app.set('views', './views');

app.get('/', async (req, res) => {
  try {
    // Call backend service via DNS
    const backendData = await new Promise((resolve, reject) => {
      const options = {
        hostname: 'sample-app-backend-service',
        port: 80,
        path: '/',
        method: 'GET'
      };

      const request = http.request(options, (response) => {
        let data = '';
        response.on('data', (chunk) => { data += chunk; });
        response.on('end', () => {
          try {
            resolve(JSON.parse(data));
          } catch (e) {
            reject(e);
          }
        });
      });

      request.on('error', reject);
      request.end();
    });

    res.render('hello', {
      backendResponse: backendData.text,
      timestamp: new Date().toISOString(),
      service: 'frontend'
    });
  } catch (error) {
    res.render('hello', {
      backendResponse: 'Backend service unavailable',
      error: error.message,
      timestamp: new Date().toISOString(),
      service: 'frontend'
    });
  }
});

app.get('/health', (req, res) => {
  res.json({ status: 'healthy', service: 'frontend' });
});

app.listen(PORT, () => {
  console.log(`Frontend service running on port ${PORT}`);
});
