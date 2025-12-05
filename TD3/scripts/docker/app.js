const http = require('http');

const server = http.createServer((req, res) => {
  res.writeHead(200, { 'Content-Type': 'text/plain' });
  res.end('🚀 DevOps Base v2 - Rolling Update Works!\n');
});

server.listen(8080, () => {
  console.log('Application v2 démarrée sur le port 8080');
});
