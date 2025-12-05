const http = require('http');
const os = require('os');

const hostname = os.hostname();
const version = process.env.APP_VERSION || '1.0';

const server = http.createServer((req, res) => {
  res.writeHead(200, { 'Content-Type': 'text/plain' });
  res.end(`Hello, World! (v${version}) - Host: ${hostname}\n`);
});

server.listen(8080, () => {
  console.log('Application listening on port 8080');
});
